# QST 重子包覆因子理論（更新版）

## 1. 理論定位

本章把重子質量拆成兩層：

\[
M_B = M_B^{(0)}\,\Gamma_B.
\]

其中，零階項來自 constituent quark-vortex 的 lock-level 質量殼；包覆因子 \(\Gamma_B\) 則描述三體在 post-lock 幾何束縛態中的 unified-force dressing。

對齊 QSTv7.1 Combine 與 FSCA / QST-Matrix，可寫成

\[
M_B
=
\kappa g_s \sigma_{\rm lock}^2
\Bigl(\phi^{-2n_1}+\phi^{-2n_2}+\phi^{-2n_3}\Bigr)\Gamma_B.
\]

## 2. 零階 constituent lock-level 質量律

定義 constituent 質量殼

\[
\mu_i \equiv \kappa g_s \sigma_{\rm lock}^2\phi^{-2n_i},
\]

則主公式改寫成

\[
M_B=(\mu_{q_1}+\mu_{q_2}+\mu_{q_3})\Gamma_B.
\]

若忽略 post-lock 幾何包覆，即取 \(\Gamma_B=1\)，得到零階質量律

\[
M_B^{(0)}=(\mu_{q_1}+\mu_{q_2}+\mu_{q_3}).
\]

這一步的物理意思是：每個 constituent quark 不是自由小球，而是被 FVF/DSI 鎖在某一階梯 \(n_i\) 的 vortex knot；每個 locked constituent 先提供一個基本質量殼 \(\mu_i\)。

## 3. 為何必須有 \(\Gamma_B\)

零階和式可抓住 baryon 的主體質量，但一旦三個 constituent 進入 post-lock 束縛態，內部幾何會重排：

- \(D(x)\) 不再只是三個局域坑的簡單疊加；
- \(\mathbf J_{\rm SC}\) 不再是三股彼此獨立的流；
- 三體鎖定會出現 screening、回流、對齊與 topology 分支。

因此引入

\[
\Gamma_B \equiv \frac{M_B}{M_B^{(0)}}.
\]

其物理意義不是殘差補差，而是三體幾何束縛的 unified-force dressing。

## 4. 第一原理宿主：統一力密度積分

QST 統一力骨架為

\[
\mathbf F_{\rm QST}=\kappa \sigma^2(\nabla D\times \mathbf J_{\rm SC}).
\]

因此，\(\Gamma_B\) 的第一原理候選定義可寫成

\[
\Gamma_B = \frac{\mathcal I_B}{\mathcal I_{\rm ref}},
\qquad
\mathcal I_B = \int_{\Omega_B}\left|\nabla D_B(\mathbf x)\times \mathbf J_{{\rm SC},B}(\mathbf x)\right|d^3x.
\]

其中 \(\Omega_B\) 是 baryon 束縛域；\(\mathcal I_{\rm ref}\) 是固定參考流型的同類積分。更新版取 mixed non-strange 分支作 reference：

\[
\mathcal I_{\rm ref}\equiv \mathcal I_{\rm mix}.
\]

於是

\[
\Gamma_{\rm mix}=1,\qquad
\Gamma_{\rm str}=\frac{\mathcal I_{\rm str}}{\mathcal I_{\rm mix}},\qquad
\Gamma_{\rm pure}=\frac{\mathcal I_{\rm pure}}{\mathcal I_{\rm mix}}.
\]

## 5. 三種最小拓撲流型

### 5.1 Mixed non-strange

代表：\(\Lambda_c(udc),\ \Xi_{cc}(qcc)\)

\[
D_{\rm mix}(\mathbf x)=D_0-\sum_{i=1}^3 A_i\exp\!\left[-\frac{|\mathbf x-\mathbf r_i|^2}{\ell_i^2}\right]
\]

\[
\mathbf J_{\rm mix}(\mathbf x)=
\sum_{\langle ij\rangle}
J_{ij}
\exp\!\left[-\frac{d_{ij}(\mathbf x)^2}{w_{ij}^2}\right]\hat{\mathbf t}_{ij}.
\]

物理圖像：開放橋接、有效重疊體積大、\(\nabla D\) 與 \(\mathbf J_{\rm SC}\) 的平均夾角較大、screening 較弱。

### 5.2 Strange-rich

代表：\(\Omega_c(ssc),\ \Omega_{cc}(scc)\)

\[
D_{\rm str}(\mathbf x)=D_0-\sum_{i=1}^3 A_i^{(s)}\exp\!\left[-\frac{|\mathbf x-\mathbf r_i|^2}{\ell_{i,s}^2}\right],
\qquad \ell_{i,s}<\ell_{i,q}
\]

\[
\mathbf J_{\rm str}(\mathbf x)=
\sum_{\langle ij\rangle}
J_{ij}^{(s)}
\exp\!\left[-\frac{d_{ij}(\mathbf x)^2}{w_{ij,s}^2}\right]\hat{\mathbf a}_{ij},
\qquad
\hat{\mathbf a}_{ij}\text{較多平行於局部 }\nabla D.
\]

物理圖像：strange core 更緊、更局域；\(|\nabla D|\) 可更強，但對齊增加令 \(\sin\theta\) 降低，且有效重疊體積縮小。

### 5.3 Pure-heavy

代表：\(\Omega_{ccc}(ccc)\)

\[
D_{\rm pure}(\mathbf x)=D_0-A_c\sum_{i=1}^3\exp\!\left[-\frac{|\mathbf x-\mathbf r_i|^2}{\ell_c^2}\right]
\]

\[
\mathbf J_{\rm pure}(\mathbf x)=
J_c\sum_{i=1}^3\exp\!\left[-\frac{d_i(\mathbf x)^2}{w_c^2}\right]\hat{\mathbf u}_i
\]

物理圖像：三重對稱、回流與 screening 最強、有效束縛體積最小。

## 6. Branch 排序的第一原理預言

由三種最小流型，不需要任何觀測質量，即可先推出

\[
\mathcal I_{\rm mix}>\mathcal I_{\rm str}>\mathcal I_{\rm pure}
\]

因此

\[
\Gamma_{\rm mix}>\Gamma_{\rm str}>\Gamma_{\rm pure}.
\]

在 reference 規範下：

\[
\Gamma_{\rm mix}=1,\qquad 0<\Gamma_{\rm pure}<\Gamma_{\rm str}<1.
\]

這一步只推出排序，不注入經驗 branch 常數，因而是審計安全的。

## 7. 如何唯一決定 branch 比值

要令 branch 比值不再依賴手選 ansatz，而是由同一個三體場解唯一決定，必須把三支 branch 升級成同一個統一泛函的三個極小解。

最小統一泛函可寫成

\[
\mathcal S_B
=
\int
\Big[
\alpha_D |\nabla D|^2
+
\alpha_J |\mathbf J|^2
+
\sum_i \lambda_i\chi_i(D-D_{n_i})^2
+
\mu\sum_{a,b}(1-C_{ab})|\psi_a||\psi_b|
-
\alpha_\times\sigma^2|\nabla D\times\mathbf J|
\Big]d^3x
\]

並配以自洽 closure：

\[
\sigma=\tanh\!\big(\phi\,C_{\rm lock}[\psi]\big).
\]

對不同 topology constraint \(\mathcal C_T\) 求極小解

\[
(D_T^\*,\mathbf J_T^\*,\psi_T^\*,\sigma_T^\*)=
\arg\min_{\mathcal C_T}\mathcal S_B,
\]

再定義

\[
\mathcal I_T=\int|\nabla D_T^\*\times \mathbf J_T^\*|\,d^3x,
\qquad
\Gamma_T=\frac{\mathcal I_T}{\mathcal I_{\rm mix}}.
\]

如此，branch 不再先假設，而是同一個三體幾何方程的多重穩定解。

## 8. 最小離散求解器

更新版附上一個 2D + PyTorch 的最小求解器骨架，直接最小化離散泛函並輸出

\[
\Gamma_{\rm str}=\frac{\mathcal I_{\rm str}}{\mathcal I_{\rm mix}},
\qquad
\Gamma_{\rm pure}=\frac{\mathcal I_{\rm pure}}{\mathcal I_{\rm mix}}.
\]

完整程式見 `qst_baryon_branch_solver.py`。

## 9. 本章結論

1. 重子零階質量律來自三個 locked constituent quark-vortex 的質量殼和：

\[
M_B^{(0)}=
\kappa g_s \sigma_{\rm lock}^2
\Bigl(\phi^{-2n_1}+\phi^{-2n_2}+\phi^{-2n_3}\Bigr)
\]

2. \(\Gamma_B\) 不是經驗補差，而是 post-lock 三體幾何束縛的 unified-force dressing：

\[
\Gamma_B=\frac{\mathcal I_B}{\mathcal I_{\rm mix}}
\]

3. 三種最小拓撲流型自然導出：

\[
\Gamma_{\rm mix}>\Gamma_{\rm str}>\Gamma_{\rm pure}
\]

4. 真正的下一步，不是再擬合 branch 常數，而是用同一個三體統一泛函在不同 topology 約束下求極小解，令 branch 比值唯一化。
