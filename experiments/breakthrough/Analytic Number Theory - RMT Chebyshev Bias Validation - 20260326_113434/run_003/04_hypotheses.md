

**H1 – Exact‑zero variance is at least 60 % larger than the logarithmic‑approximation variance for modulus 210**  

**Statement**  
When the exact (machine‑verified) non‑trivial zeros of the nine primitive Dirichlet L‑functions modulo 210 are inserted into the Rubinstein–Sarnak logarithmic variance formula, the resulting theoretical variance exceeds the variance obtained with the simple log‑approximation by **≥ 60 %** (i.e. the increase observed in the pilot “simulated exact‑zero” experiment is reproduced and possibly surpassed).

**Why it is testable**  
Both quantities (variance with log‑approximation and variance with exact zeros) are computable deterministic functions of the zero set.  By evaluating the same variance expression for the same set of moduli (210) and the same range of \(x\) we obtain two numbers that can be compared directly; the hypothesis is false if the increase is < 60 %.

**Experiment**  

1. **Zero computation** – Use the **Arb** library (Euler‑Maclaurin + interval arithmetic) to produce a verified list of the low‑lying zeros \(\gamma\) for each primitive character modulo 210 up to height \(T=10^{4}\).  Store the zeros with error bounds ≤ 10⁻³⁰.  
2. **Variance evaluation** – Plug the exact zeros into the Rubinstein–Sarnak formula  

   \[
   \mathcal{V}_{\text{exact}}(X)=\sum_{q\mid210}\frac{1}{\varphi(q)}\sum_{\chi\neq\chi_{0}}
      \Bigl|\sum_{n\le X}\chi(n)\,\Lambda(n)-\frac{X}{\phi(q)}\Bigr|^{2},
   \]

   where \(\Lambda\) is the von Mangoldt function and the inner sum is expressed via the explicit formula with the exact \(\gamma\).  Compute the same quantity with the usual log‑approximation for the zeros (i.e. \(\gamma\approx\log\frac{n}{2\pi}\) ).  
3. **Comparison** – For several values of \(X\) (e.g. \(X=10^{6},2\times10^{6},5\times10^{6},10^{7}\)) compute the ratio  

   \[
   R(X)=\frac{\mathcal{V}_{\text{exact}}(X)}{\mathcal{V}_{\text{log}}(X)}.
   \]

   If \(R(X)\ge1.60\) for **all** tested \(X\), the hypothesis is supported; if any \(R<1.60\) it is falsified.  

---

**H2 – The correction factor \(C(X)=\mathcal{V}_{\text{exact}}(X)/\mathcal{V}_{\text{log}}(X)\) follows a power‑law in \(X\) for \(X\ge2\times10^{6}\)**  

**Statement**  
There exist constants \(A>0\) and \(\alpha\) such that  

\[
C(X)=A\,X^{\alpha}\qquad\text{for }X\ge2\times10^{6},
\]

i.e. the relative gain of using exact zeros grows (or shrinks) algebraically with the sample size, rather than fluctuating randomly.

**Why it is testable**  
If the ratio \(C(X)\) behaves as a power law, a log‑log plot of \(C\) versus \(X\) will be linear.  Departures from linearity (e.g. systematic curvature) can be detected with standard regression diagnostics, providing a clear falsifiable criterion.

**Experiment**  

1. Compute \(C(X)\) at a dense grid of \(X\) values (e.g. every \(5\times10^{5}\) from \(2\times10^{6}\) up to \(10^{8}\)).  
2. Fit the model \(\log C = \log A + \alpha \log X\) by ordinary least‑squares.  
3. Test the goodness‑of‑fit via the coefficient of determination \(R^{2}\) and a runs test on the residuals.  If \(R^{2}>0.95\) and the residuals show no systematic pattern, accept the power‑law hypothesis; otherwise reject it.  

---

**H3 – After inserting the exact zeros, the empirical‑to‑theoretical variance ratio drops below 10 % of its original value of ≈ 430 for \(X\ge10^{7}\)**  

**Statement**  
Define  

\[
\rho(X)=\frac{\operatorname{Var}_{\text{emp}}(X)}{\mathcal{V}_{\text{exact}}(X)},
\]

where \(\operatorname{Var}_{\text{emp}}(X)\) is the observed variance of the Chebyshev bias computed from exhaustive enumeration of integers up to \(X\).  The hypothesis asserts that  

\[
\rho(X)<0.10\;\;\text{for all }X\ge10^{7},
\]

i.e. the exact‑zero correction resolves at least **90 %** of the discrepancy that originally exceeded the theoretical prediction by a factor of 430.

**Why it is testable**  
Both \(\operatorname{Var}_{\text{emp}}(X)\) and \(\mathcal{V}_{\text{exact}}(X)\) are directly computable quantities.  For each \(X\) we can evaluate \(\rho(X)\) and compare it to the threshold 0.10.  The hypothesis is falsified as soon as a single value of \(X\) yields \(\rho\ge0.10\).

**Experiment**  

1. **Empirical variance** – Using a multi‑CPU implementation, count the sign of \(\Delta(x)=\sum_{n\le x}\Lambda(n)-\frac{x}{\phi(q)}\) for all primitive characters modulo 210 and accumulate the squared deviations up to \(X_{\max}=10^{8}\).  Compute the variance at each \(X\) step (e.g., every \(10^{6}\)).  
2. **Exact‑zero variance** – As in H1, compute \(\mathcal{V}_{\text{exact}}(X)\) for the same grid of \(X\).  
3. **Ratio** – Plot \(\rho(X)\) and verify that for all \(X\ge10^{7}\) the curve lies under the line \(\rho=0.10\).  Perform a one‑sided t‑test on the set \(\{\rho(X_i)\}\) to confirm statistical significance.  

---

**H4 – The contribution of zeros with \(|\gamma|>10^{4}\) to the variance correction is < 5 %**  

**Statement**  
When the variance formula is truncated at height \(T=10^{4}\), the resulting correction factor differs from the full (untruncated) factor by less than **5 %**.  In other words, the low‑lying zeros already capture the dominant part of the exact‑zero effect.

**Why it is testable**  
We can compute the variance with two zero sets: (i) only zeros up to \(T=10^{4}\) and (ii) zeros up to a larger height \(T'=5\times10^{4}\) (or up to the first 100 000 zeros).  The percentage difference in the correction factor can be quantified and compared to the 5 % threshold.

**Experiment**  

1. Using the LMO/Riemann‑Siegel FFT algorithm (or an extension of the Arb pipeline), generate a second verified zero list for each Dirichlet character up to \(T'=5\times10^{4}\).  
2. Evaluate the variance correction factor \(C_T(X)\) for both zero truncations (T and T′) at several \(X\) values (e.g., \(X=2\times10^{6},10^{7},10^{8}\)).  
3. Compute the relative error  

   \[
   \epsilon_T(X)=\Bigl|\frac{C_{T'}(X)-C_T(X)}{C_{T'}(X)}\Bigr|.
   \]

   If \(\epsilon_T(X)<0.05\) for all tested \(X\), the hypothesis holds; otherwise it is refuted.  

---

**H5 – The Arb‑based rigorous zero list and the LMO‑based fast zero list agree on the variance correction to within 0.1 %**  

**Statement**  
Two independent computational pipelines (one using **Arb** with interval arithmetic, the other using the **LMO/Odlyzko** FFT‑accelerated algorithm) produce zero sets that, when plugged into the Rubinstein–Sarnak formula, yield variance values differing by less than **0.1 %**.  This confirms that numerical implementation choices do not bias the final variance estimate.

**Why it is testable**  
Both pipelines are deterministic (given the same precision settings) and produce comparable outputs.  The 0.1 % tolerance is a concrete numerical bound that can be checked directly; exceeding it falsifies the hypothesis.

**Experiment**  

1. **Arb pipeline** – As in H1, produce a verified zero list up to \(T=10^{4}\) with error ≤ 10⁻³⁰.  
2. **LMO pipeline** – Implement (or call) a parallel LMO routine (e.g., the `lcalc` library) using double‑precision but with a “high‑accuracy” flag (or 80‑bit extended precision) to compute the same zeros.  Ensure that the imaginary parts are sorted and paired with the same characters.  
3. **Cross‑validation** – Compute the variance correction factor \(C_{\text{Arb}}(X)\) and \(C_{\text{LMO}}(X)\) for the same set of \(X\).  Compute the relative difference  

   \[
   \delta(X)=\Bigl|\frac{C_{\text{Arb}}(X)-C_{\text{LMO}}(X)}{C_{\text{LMO}}(X)}\Bigr|.
   \]

   If \(\delta(X)<10^{-3}\) for all \(X\), the hypothesis is supported.  

---

### How to Use These Hypotheses

| # | Primary quantity examined | Falsification condition |
|---|---------------------------|--------------------------|
| H1 | Increase of variance when exact zeros replace log‑approx. | Ratio < 1.60 for any test \(X\) |
| H2 | Scaling law of the variance correction factor | No power‑law fit with \(R^{2}>0.95\) or significant curvature |
| H3 | Residual empirical‑theoretical gap after exact‑zero correction | Empirical‑to‑exact ratio ≥ 0.10 for any \(X\ge10^{7}\) |
| H4 | Importance of high‑lying zeros beyond \(T=10^{4}\) | Relative error > 5 % when truncating at \(T=10^{4}\) |
| H5 | Consistency between rigorous (Arb) and fast (LMO) zero computations | Relative discrepancy > 0.1 % between the two pipelines |

Each hypothesis can be **tested in a fully automated, reproducible computational workflow** on a multi‑GPU/CPU cluster, and all required software (Arb, lcalc, custom variance scripts) is publicly available.  The experiments generate objective numerical thresholds, making the hypotheses rigorously falsifiable and providing clear guidance for the next research iteration.