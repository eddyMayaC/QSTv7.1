# QST 重子包覆因子理論：2026-03 狀態補充（最終清理版）

## 1. 目前最重要的結論

重子包覆因子理論目前可以誠實聲稱的，不是 constituent lock-level 的第一原理 closure，而是三體泛函所導出的幾何排序結構。

目前最小 bare 草圖為：

\[
\boxed{(n_q,n_s,n_c)=(2,1,0)}
\]

這組數值只應被視為 **bare integer anchor**，而不是已封閉的精確觀測 lock level。

## 2. 現階段狀態表

| 項目 | 狀態 | 可入文件？ |
|---|---|---|
| Branch ordering \(\Gamma_{\rm mix} > \Gamma_{\rm str} > \Gamma_{\rm pure}\) | ✅ 穩定通過 | ✅ |
| Topology assignment rule | ✅ 清晰且有物理來源 | ✅ |
| \(n_q/n_s \approx \varphi^2\) | 🟡 數值信號，未證為定理 | 🟡 可寫，但要標明是觀察 |
| bare \((2,1,0)\) 在 charm sector 的精度 | 🟡 約 3%–8%（部分重子） | ✅ 可誠實標注精度上限 |
| constituent \(n_f\) 的第一原理來源 | ❌ 未解決 | ❌ |
| FVF lock spectrum 的可執行 closure | ❌ 目前會落入循環論證 | ❌ |
| \(\Xi_{cc}\) 達到 5% 以內精度 | ❌ 目前仍約 13% | ❌ |

## 3. 哪些結果已成立

### 3.1 Branch ordering 已成立

目前最穩定、最乾淨的成果是：

\[
\boxed{\Gamma_{\rm mix} > \Gamma_{\rm str} > \Gamma_{\rm pure}}
\]

這表示三體幾何排序結構已經建立。換句話講，QST 在 baryon 問題上，已經成功分離出 topology dressing 的主體方向。

### 3.2 Topology assignment rule 可入文件

以下分支指派目前結構清楚：

- mixed：含 light quark 參與，例如 \(\Lambda_c(udc)\)、\(\Xi_{cc}(qcc)\)
- strange-rich：含 strange/heavy 組合，例如 \(\Omega_c(ssc)\)、\(\Omega_{cc}(scc)\)
- pure-heavy：純 heavy，例如 \(\Omega_{ccc}(ccc)\)

這一層的幾何分類可以獨立成立，不必等 constituent lock-level fully closed 才能說明。

### 3.3 bare \((2,1,0)\) 是有用的最小草圖

以 \(\Omega_{ccc}\) 作錨點時，目前 charm-sector 的半定量精度大致為：

- \(\Xi_{cc}\)：約 \(-3.2\%\)
- \(\Omega_{cc}\)：約 \(+3.0\%\)
- \(\Lambda_c\)：約 \(-7.7\%\)
- \(\Omega_c\)：約 \(+6.9\%\)
- \(\Omega_{ccc}\)：錨點

因此：

\[
\boxed{\text{bare }(2,1,0)\text{ 目前是有理論動機、且可達約 }3\%\text{–}8\%\text{ 的最小整數候選。}}
\]

它不是最終 closure，但亦不是無意義的假設。

## 4. 哪些結果目前只是觀察，不是定理

### 4.1 \(n_q/n_s \approx \varphi^2\)

最新反推顯示：

\[
\boxed{\frac{n_q}{n_s} \approx \varphi^2}
\]

數值上，最佳比值約為 \(2.66\)，而

\[
\boxed{\varphi^2 \approx 2.618}
\]

兩者只差約 1.5%。而且當強制該比值時，整體誤差幾乎不變。這是一個值得保留的結構信號。

但目前最誠實的表述必須是：

\[
\boxed{\text{這是數值支持的結構觀察，不是已從第一原理完成證明的定理。}}
\]

## 5. 哪些路線已知失敗或暫停

為保持文件乾淨，以下探索性路線不再作為主線總結：

### 5.1 單一 flavor-universal 的 \(n_q^{\rm eff}\) 修正式

原因是：

- \(\Lambda_c\) 需要 \(n_q^{\rm eff}\) 向下拉低；
- \(\Xi_{cc}\) 反而需要 \(n_q^{\rm eff}\) 向上修正。

因此，單一普適修正式不能同時改好兩者。

### 5.2 二階 \(\varphi\)-backreaction 方案

目前數值顯示，它不足以形成主線 closure，因此暫停。

### 5.3 以 \(\eta_m\sigma_M^2\) 作主 closure 機制

對 \(\Xi_{cc}\) 反推會得到不合法的負值，因此在現階段不能成立。

### 5.4 FVF lock selection functional 的直接執行版

若把

\[
D_f^{\rm proto}=D_0-q_K\varphi^{-2}
\]

直接作為 proto input，則 spectrum 選擇會自動回到原本的 ordering label，形成循環論證。要打破此循環，需要一個獨立的 \(D_f^{\rm proto}\) 來源；而目前這一步尚未在框架內解決。因此，FVF lock spectrum 的「執行版 closure」暫時失敗。

## 6. 真正的開口在哪裡

而家最關鍵的判斷是：

\[
\boxed{\Gamma_B\text{ 已基本解決 topology 排序；真正未封閉的是 }n_f\text{ 的定量來源。}}
\]

換句話講：

- E8 / Golden-K 目前穩定提供的是 **flavor hierarchy ordering**；
- bare integer levels \((2,1,0)\) 提供的是 **最小 anchor**；
- 若要進一步超越 3%–8% 的半定量精度，必須由一個非循環的 FVF lock 動力學正式給出 constituent 的 effective locking。

## 7. 通俗解釋

最白話可以咁理解：

- E8 而家主要做到的，是幫你排好隊，知道 light、strange、charm 大致上誰高誰低；
- bare \((2,1,0)\) 就像一張最簡單的樓層草圖：light 在二樓、strange 在一樓、charm 在零樓；
- 這張草圖唔差，因為用 \(\Omega_{ccc}\) 做錨點後，多數 charm baryon 已經進入 3%–8% 區間；
- 但真正 baryon 裡，三粒 quark 不是靜止站在自己樓層，而是綁在一起、互相拉扯；所以同一粒 light quark，放在 \(\Lambda_c\) 同放在 \(\Xi_{cc}\) 內部，實際表現出的有效樓層可以不同；
- 如果你想真正算這個有效樓層，就要有一個不循環的 FVF lock 譜；而目前這一步仍未打通。

所以，問題已經唔再係「排序錯」，而係：

\[
\boxed{\text{真實的有效樓層，仍要由非循環的 FVF lock 動力學自己算出，唔能只靠 bare integer 表硬定。}}
\]

## 8. 一句總結

\[
\boxed{\text{QST baryon programme 目前已完成排序層與最小整數 anchor；}\ \text{它可以誠實聲稱幾何排序結構，但仍不能誠實聲稱 constituent lock-level 的第一原理 closure。}}
\]
