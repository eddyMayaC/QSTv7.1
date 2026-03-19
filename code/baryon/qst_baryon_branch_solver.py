import math
from dataclasses import dataclass
from typing import List, Tuple

import torch

PHI = (1.0 + math.sqrt(5.0)) / 2.0


@dataclass
class SolverConfig:
    nx: int = 96
    ny: int = 96
    lx: float = 8.0
    ly: float = 8.0
    n_channels: int = 3
    lr: float = 2e-2
    steps: int = 2000
    print_every: int = 100
    device: str = "cpu"

    # Functional weights
    alpha_D: float = 1.0
    alpha_J: float = 1.0
    alpha_x: float = 1.0
    mu_e8: float = 1.0
    alpha_psi_grad: float = 0.05
    lock_sigma: float = 0.50
    eps: float = 1e-8


def make_grid(cfg: SolverConfig):
    x = torch.linspace(-cfg.lx / 2, cfg.lx / 2, cfg.nx, device=cfg.device)
    y = torch.linspace(-cfg.ly / 2, cfg.ly / 2, cfg.ny, device=cfg.device)
    X, Y = torch.meshgrid(x, y, indexing="ij")
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    dA = dx * dy
    return X, Y, dx, dy, dA


def grad2d_scalar(u: torch.Tensor, dx: float, dy: float):
    ux = (torch.roll(u, shifts=-1, dims=0) - torch.roll(u, shifts=1, dims=0)) / (2 * dx)
    uy = (torch.roll(u, shifts=-1, dims=1) - torch.roll(u, shifts=1, dims=1)) / (2 * dy)
    return ux, uy


def grad_norm_sq(u: torch.Tensor, dx: float, dy: float):
    ux, uy = grad2d_scalar(u, dx, dy)
    return ux**2 + uy**2


def make_core_mask(X, Y, center: Tuple[float, float], sigma: float):
    cx, cy = center
    r2 = (X - cx) ** 2 + (Y - cy) ** 2
    return torch.exp(-r2 / (2 * sigma**2))


def point_to_segment_distance_2d(X, Y, a: Tuple[float, float], b: Tuple[float, float]):
    ax, ay = a
    bx, by = b
    px = X - ax
    py = Y - ay
    abx = bx - ax
    aby = by - ay
    ab2 = abx * abx + aby * aby + 1e-12
    t = (px * abx + py * aby) / ab2
    t = torch.clamp(t, 0.0, 1.0)
    projx = ax + t * abx
    projy = ay + t * aby
    return torch.sqrt((X - projx) ** 2 + (Y - projy) ** 2 + 1e-12)


def make_bridge_mask(X, Y, a: Tuple[float, float], b: Tuple[float, float], width: float):
    d = point_to_segment_distance_2d(X, Y, a, b)
    return torch.exp(-(d**2) / (2 * width**2))


def D_n_from_lock_level(n_i: float, D0: float = 4.236, beta: float = 1.0):
    """
    Placeholder mapping.
    IMPORTANT:
    This is still an unclosed interface and should not be treated
    as a final QST theorem.
    """
    return D0 + beta * math.log(PHI ** (-2 * n_i))


def effective_lock_level(n_i: float, flavor_i: str, sigma: torch.Tensor):
    """
    Bare-to-effective lock backreaction.
    Current minimal v1:
      - only light quark q gets backreaction
      - s and c remain unchanged
      - no new free constants
      - delta_q = phi^{-2} * (1 - sigma)
    """
    if flavor_i == "q":
        delta_q = (PHI ** -2) * (1.0 - sigma)
        return torch.tensor(float(n_i), device=sigma.device) - delta_q
    elif flavor_i == "s":
        return torch.tensor(float(n_i), device=sigma.device)
    elif flavor_i == "c":
        return torch.tensor(float(n_i), device=sigma.device)
    else:
        raise ValueError(f"Unknown flavor_i={flavor_i}")


def c_lock_from_psi(psi: torch.Tensor, C: torch.Tensor, eps: float = 1e-8):
    """
    Average normalized overlap over allowed channel pairs.
    """
    A = psi.shape[0]
    overlaps = []
    for a in range(A):
        pa = psi[a]
        na = torch.sqrt(torch.sum(pa * pa) + eps)
        for b in range(A):
            if C[a, b] > 0.5:
                pb = psi[b]
                nb = torch.sqrt(torch.sum(pb * pb) + eps)
                ov = torch.sum(pa * pb) / (na * nb + eps)
                overlaps.append(ov)
    if len(overlaps) == 0:
        return torch.tensor(0.0, device=psi.device)
    return torch.stack(overlaps).mean()


def sigma_from_psi(psi: torch.Tensor, C: torch.Tensor):
    c_lock = c_lock_from_psi(psi, C)
    sigma = torch.tanh(torch.tensor(PHI, device=psi.device) * c_lock)
    return sigma, c_lock


def e8_penalty(psi: torch.Tensor, C: torch.Tensor):
    """
    Penalize simultaneous occupancy of forbidden channel pairs.
    """
    A = psi.shape[0]
    occ = torch.sqrt(torch.sum(psi * psi, dim=(1, 2)) + 1e-12)
    penalty = 0.0
    for a in range(A):
        for b in range(A):
            penalty = penalty + (1.0 - C[a, b]) * occ[a] * occ[b]
    return penalty


def psi_smoothness(psi: torch.Tensor, dx: float, dy: float):
    total = 0.0
    for a in range(psi.shape[0]):
        total = total + torch.sum(grad_norm_sq(psi[a], dx, dy))
    return total


def topology_constraints(topology: str, X: torch.Tensor, Y: torch.Tensor, cfg: SolverConfig):
    """
    Returns:
      core_masks: list of chi_i masks
      bridge_masks: soft support masks for J
      core_positions
    """
    if topology == "mixed":
        core_positions = [(-1.2, 0.0), (1.2, 0.0), (0.0, 1.2)]
        widths = [0.85, 0.85, 1.00]
        bridges = [
            ((-1.2, 0.0), (0.0, 1.2), 0.65),
            ((1.2, 0.0), (0.0, 1.2), 0.65),
        ]

    elif topology == "strange":
        core_positions = [(-0.95, 0.0), (0.95, 0.0), (0.0, 0.95)]
        widths = [0.65, 0.65, 0.72]
        bridges = [
            ((-0.95, 0.0), (0.0, 0.95), 0.48),
            ((0.95, 0.0), (0.0, 0.95), 0.48),
        ]

    elif topology == "pure":
        core_positions = [(-1.00, -0.58), (1.00, -0.58), (0.00, 1.15)]
        widths = [0.58, 0.58, 0.58]
        bridges = [
            ((-1.00, -0.58), (1.00, -0.58), 0.42),
            ((1.00, -0.58), (0.00, 1.15), 0.42),
            ((0.00, 1.15), (-1.00, -0.58), 0.42),
        ]

    else:
        raise ValueError("topology must be one of: mixed, strange, pure")

    core_masks = [
        make_core_mask(X, Y, pos, sigma=cfg.lock_sigma * w)
        for pos, w in zip(core_positions, widths)
    ]
    bridge_masks = [
        make_bridge_mask(X, Y, a, b, width=w)
        for (a, b, w) in bridges
    ]
    return core_masks, bridge_masks, core_positions


def init_fields(cfg: SolverConfig):
    D = torch.zeros((cfg.nx, cfg.ny), device=cfg.device, requires_grad=True)
    Jx = torch.zeros((cfg.nx, cfg.ny), device=cfg.device, requires_grad=True)
    Jy = torch.zeros((cfg.nx, cfg.ny), device=cfg.device, requires_grad=True)
    psi = 0.01 * torch.randn((cfg.n_channels, cfg.nx, cfg.ny), device=cfg.device, requires_grad=True)
    return D, Jx, Jy, psi


def build_loss(
    D: torch.Tensor,
    Jx: torch.Tensor,
    Jy: torch.Tensor,
    psi: torch.Tensor,
    core_masks: List[torch.Tensor],
    bridge_masks: List[torch.Tensor],
    n_levels: List[int],
    flavors: List[str],
    C: torch.Tensor,
    cfg: SolverConfig,
    dx: float,
    dy: float,
    dA: float,
):
    sigma, c_lock = sigma_from_psi(psi, C)

    Dx, Dy = grad2d_scalar(D, dx, dy)
    gradD_sq = Dx**2 + Dy**2
    J_sq = Jx**2 + Jy**2
    cross_mag = torch.abs(Dx * Jy - Dy * Jx)

    # lock potential with effective backreaction
    V_lock = 0.0
    n_eff_list = []

    for chi_i, n_i, f_i in zip(core_masks, n_levels, flavors):
        n_eff_i = effective_lock_level(n_i, f_i, sigma)
        n_eff_list.append(n_eff_i.detach())
        D_target = D_n_from_lock_level(float(n_eff_i.item()))
        V_lock = V_lock + torch.sum(chi_i * (D - D_target) ** 2)

    V_e8 = e8_penalty(torch.abs(psi), C)
    V_psi = psi_smoothness(psi, dx, dy)

    # soft topology support mask for current
    if len(bridge_masks) > 0:
        M = torch.clamp(sum(bridge_masks), 0.0, 1.0)
        Jmag = torch.sqrt(J_sq + cfg.eps)
        V_topo = torch.sum((1.0 - M) * Jmag**2)
    else:
        V_topo = torch.tensor(0.0, device=D.device)

    loss_density = (
        cfg.alpha_D * gradD_sq
        + cfg.alpha_J * J_sq
        - cfg.alpha_x * (sigma**2) * cross_mag
    )

    S = torch.sum(loss_density) * dA
    S = S + V_lock * dA
    S = S + cfg.mu_e8 * V_e8
    S = S + cfg.alpha_psi_grad * V_psi * dA
    S = S + 0.5 * V_topo * dA

    diagnostics = {
        "sigma": sigma.detach(),
        "c_lock": c_lock.detach(),
        "I_cross": (torch.sum(cross_mag) * dA).detach(),
        "E_gradD": (torch.sum(cfg.alpha_D * gradD_sq) * dA).detach(),
        "E_J": (torch.sum(cfg.alpha_J * J_sq) * dA).detach(),
        "V_lock": (V_lock * dA).detach(),
        "V_e8": V_e8.detach(),
        "V_topo": (V_topo * dA).detach(),
        "n_eff": [float(x.item()) for x in n_eff_list],
    }
    return S, diagnostics


def solve_branch(
    topology: str,
    n_levels: List[int],
    flavors: List[str],
    C: torch.Tensor,
    cfg: SolverConfig,
    label: str = "",
):
    X, Y, dx, dy, dA = make_grid(cfg)
    core_masks, bridge_masks, _ = topology_constraints(topology, X, Y, cfg)

    D, Jx, Jy, psi = init_fields(cfg)
    opt = torch.optim.Adam([D, Jx, Jy, psi], lr=cfg.lr)

    best = None

    for step in range(cfg.steps):
        opt.zero_grad()

        S, diag = build_loss(
            D, Jx, Jy, psi,
            core_masks, bridge_masks,
            n_levels, flavors,
            C, cfg, dx, dy, dA
        )
        S.backward()
        opt.step()

        if best is None or S.item() < best["loss"]:
            best = {
                "loss": S.item(),
                "label": label,
                "topology": topology,
                "n_levels": list(n_levels),
                "flavors": list(flavors),
                "D": D.detach().clone(),
                "Jx": Jx.detach().clone(),
                "Jy": Jy.detach().clone(),
                "psi": psi.detach().clone(),
                "diag": {k: v.clone() if torch.is_tensor(v) else v for k, v in diag.items()}
            }

        if step % cfg.print_every == 0 or step == cfg.steps - 1:
            tag = f"{topology}:{label}" if label else topology
            print(
                f"[{tag:18s}] step={step:4d} "
                f"S={S.item():.6e} "
                f"sigma={diag['sigma'].item():.4f} "
                f"I={diag['I_cross'].item():.6e}"
            )

    return best


def branch_average_I(solutions: List[dict]) -> float:
    return sum(sol["diag"]["I_cross"].item() for sol in solutions) / len(solutions)


def print_solution_summary(sol: dict):
    print(
        f"{sol['label']:12s} "
        f"topology={sol['topology']:7s} "
        f"flavors={sol['flavors']} "
        f"n_bare={sol['n_levels']} "
        f"n_eff={sol['diag']['n_eff']} "
        f"sigma={sol['diag']['sigma'].item():.6f} "
        f"I={sol['diag']['I_cross'].item():.6e} "
        f"S={sol['loss']:.6e}"
    )


if __name__ == "__main__":
    cfg = SolverConfig(device="cpu")

    # Placeholder E8-induced adjacency matrix
    # Replace later with a true selection-generated C^{E8}
    C = torch.tensor([
        [1.0, 1.0, 0.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0],
    ], device=cfg.device)

    # ============================================================
    # Updated triplets from E8-FVF bridge hypothesis v1
    # n_q = 2, n_s = 1, n_c = 0
    # ============================================================

    # mixed non-strange charm branch
    # Lambda_c(udc) -> q q c
    sol_lambda_c = solve_branch(
        "mixed",
        [2, 2, 0],
        ["q", "q", "c"],
        C, cfg,
        label="Lambda_c"
    )

    # Xi_cc(qcc) -> q c c
    sol_xi_cc = solve_branch(
        "mixed",
        [2, 0, 0],
        ["q", "c", "c"],
        C, cfg,
        label="Xi_cc"
    )

    # strange-rich charm branch
    # Omega_c(ssc) -> s s c
    sol_omega_c = solve_branch(
        "strange",
        [1, 1, 0],
        ["s", "s", "c"],
        C, cfg,
        label="Omega_c"
    )

    # Omega_cc(scc) -> s c c
    sol_omega_cc = solve_branch(
        "strange",
        [1, 0, 0],
        ["s", "c", "c"],
        C, cfg,
        label="Omega_cc"
    )

    # pure-heavy branch
    # Omega_ccc(ccc) -> c c c
    sol_omega_ccc = solve_branch(
        "pure",
        [0, 0, 0],
        ["c", "c", "c"],
        C, cfg,
        label="Omega_ccc"
    )

    print("\n=== Representative solutions ===")
    for sol in [sol_lambda_c, sol_xi_cc, sol_omega_c, sol_omega_cc, sol_omega_ccc]:
        print_solution_summary(sol)

    # ------------------------------------------------------------
    # Branch-level averages
    # ------------------------------------------------------------
    I_mix = branch_average_I([sol_lambda_c, sol_xi_cc])
    I_str = branch_average_I([sol_omega_c, sol_omega_cc])
    I_pure = sol_omega_ccc["diag"]["I_cross"].item()

    Gamma_mix = 1.0
    Gamma_str = I_str / (I_mix + 1e-12)
    Gamma_pure = I_pure / (I_mix + 1e-12)

    print("\n=== Branch averages ===")
    print(f"I_mix   = {I_mix:.6e}")
    print(f"I_str   = {I_str:.6e}")
    print(f"I_pure  = {I_pure:.6e}")

    print("\n=== Branch ratios ===")
    print(f"Gamma_mix  = {Gamma_mix:.6f}")
    print(f"Gamma_str  = {Gamma_str:.6f}")
    print(f"Gamma_pure = {Gamma_pure:.6f}")
    print(f"Ordering   = {Gamma_mix > Gamma_str > Gamma_pure}")

    # ------------------------------------------------------------
    # Intra-branch consistency checks
    # ------------------------------------------------------------
    print("\n=== Intra-branch consistency ===")
    print(
        "mixed branch delta_I =",
        abs(sol_lambda_c["diag"]["I_cross"].item() - sol_xi_cc["diag"]["I_cross"].item())
    )
    print(
        "strange branch delta_I =",
        abs(sol_omega_c["diag"]["I_cross"].item() - sol_omega_cc["diag"]["I_cross"].item())
    )
    print(
        "mixed branch delta_sigma =",
        abs(sol_lambda_c["diag"]["sigma"].item() - sol_xi_cc["diag"]["sigma"].item())
    )
    print(
        "strange branch delta_sigma =",
        abs(sol_omega_c["diag"]["sigma"].item() - sol_omega_cc["diag"]["sigma"].item())
    )
