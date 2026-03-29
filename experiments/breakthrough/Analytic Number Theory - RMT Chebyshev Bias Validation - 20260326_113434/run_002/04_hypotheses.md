

Below are **five concrete, quantitative hypotheses** that can be tested with the GPU‑accelerated pipeline that is already in place.  
Each hypothesis makes a clear numerical prediction, so we can decide after the experiments whether the data support or refute it.

---

## Hypothesis 1 – *Exact‑zero effect*  

**Statement**  
Replacing the logarithmic approximations of the non‑trivial zeros of the Dirichlet L‑functions modulo 210 with **high‑precision exact zeros** will **raise the theoretical Rubinstein–Sarnak variance** by at least **30 %** (i.e. the ratio  \(V_{\text{exact}}/V_{\text{approx}}\) ≥ 1.30) and will therefore account for a sizable fraction of the observed 430‑fold gap.

**Why it is testable**  
* We can compute the theoretical variance using the same RMT formula **once with the usual log‑approximation zeros** and **once with the exact zeros** (Hardy‑Z/Riemann‑Siegel methods, FP64).  
* The two numbers are directly comparable; any systematic increase is a measurable quantity.

**Experiment that tests it**  

1. **Exact‑zero generation** – For each Dirichlet character modulo 210, generate the first \(N\) non‑trivial zeros with imaginary part ≤ \(T\) (e.g. \(T=10^6\)) to at least **16‑digit FP64 accuracy** using the Hardy‑Z implementation already in the code base.  
2. **Variance recomputation** – Plug the exact zero list into the Rubinstein–Sarnak variance integral (the sum over zeros) and obtain \(V_{\text{exact}}\).  
3. **Baseline** – Keep the original log‑approximation zero set and compute \(V_{\text{approx}}\) under identical truncation (same \(N\) and \(T\)).  
4. **Comparison** – Compute the ratio \(V_{\text{exact}}/V_{\text{approx}}\) and the absolute percentage reduction in the 430‑fold gap:
   \[
   \Delta_{\text{gap}}=\frac{V_{\text{empirical}}-V_{\text{approx}}}{V_{\text{empirical}}-V_{\text{exact}}}\times100\%.
   \]
   If \(\Delta_{\text{gap}}\) exceeds (say) 30 % the hypothesis is supported.

---

## Hypothesis 2 – *Finite‑scale correction*  

**Statement**  
A **finite‑scale correction term** of order \(\displaystyle \frac{C}{\log x}\) (with a positive constant \(C\) that can be extracted from the data) must be added to the asymptotic RMT variance formula. After this correction the **theoretical variance at \(x=10^{8}\)** will be within **15 %** of the empirical variance.

**Why it is testable**  
* The correction term makes a **quantitative prediction**: the corrected variance,
  \[
  V_{\text{corr}}(x)=V_{\text{RMT}}\!\Bigl(1+\frac{C}{\log x}\Bigr),
  \]
  must be a monotonic function that approaches \(V_{\text{RMT}}\) as \(x\) grows.  
* By fitting the observed scaling of the empirical variance we can estimate \(C\) and check whether the corrected formula meets the 15 % target.

**Experiment that tests it**  

1. **Empirical scaling runs** – Using the Multi‑GPU pipeline, compute the empirical Chebyshev‑bias variance for the set of bounds  
   \[
   x\in\{2\times10^{6},\,5\times10^{6},\,10^{7},\,5\times10^{7},\,10^{8}\}.
   \]  
2. **Fit the correction** – Model the data as  
   \[
   V_{\text{emp}}(x)=V_{\text{RMT}}\!\Bigl(1+\frac{C}{\log x}\Bigr)+\varepsilon(x),
   \]  
   where \(\varepsilon(x)\) is a small stochastic error. Perform a non‑linear least‑squares fit to obtain \(\hat C\) and its uncertainty.  
3. **Validate at the largest bound** – Plug \(\hat C\) into the formula and evaluate \(V_{\text{corr}}(10^{8})\). Compute the percentage error  
   \[
   \text{err}\% = \frac{|V_{\text{emp}}(10^{8})-V_{\text{corr}}(10^{8})|}{V_{\text{emp}}(10^{8})}\times100\%.
   \]  
   If \(\text{err}\% < 15\%\) the hypothesis is confirmed.

---

## Hypothesis 3 – *Zero‑sum truncation dominates the discrepancy*  

**Statement**  
The **truncation of the L‑function zero sum at a finite height** (i.e. using only zeros up to imaginary part \(T\)) is the **primary driver** of the 430‑fold gap, and **including zeros up to a larger height** reduces the gap by at least **70 %**.

**Why it is testable**  
* The variance formula is a sum over zeros; truncating the sum at a finite \(T\) inevitably leaves out contributions that are negligible only as \(T\to\infty\).  
* By **systematically increasing \(T\)** we can monitor how quickly the theoretical variance climbs toward the empirical value. The experiment yields a measurable curve of \(V(T)\).

**Experiment that tests it**  

1. **Baseline** – Compute \(V(T_{0})\) with the current truncation used in the original model (e.g. \(T_{0}=10^{5}\)). This should reproduce the low theoretical value of 168.08.  
2. **Increase \(T\)** – For the same set of exact zeros generated in Hypothesis 1, recompute the variance using a **doubling sequence** of heights  
   \[
   T\in\{10^{5},\,2\times10^{5},\,5\times10^{5},\,10^{6},\,2\times10^{6},\dots\}.
   \]  
   Keep the number of zeros proportional to each \(T\).  
3. **Convergence plot** – Plot \(V(T)\) versus \(1/T\) (or versus \(\log T\)). Observe whether \(V(T)\) **monotonically increases** and approaches the empirical variance of 72 593.  
4. **Quantify reduction** – For each step compute the percentage of the original gap that is “closed”. If after the largest feasible \(T\) (e.g. \(T=5\times10^{6}\)) the gap is reduced by **≥ 70 %**, the hypothesis is upheld.

---

## Hypothesis 4 – *Negligibility of inter‑character correlations*  

**Statement**  
The **cross‑terms between distinct Dirichlet characters modulo 210** contribute **less than 5 %** of the total theoretical variance, so the bulk of the discrepancy is **not** due to inter‑character interference.

**Why it is testable**  
* The Rubinstein–Sarnak framework splits the variance into a **sum of autocorrelations** (same character) and **cross‑correlations** (different characters). Each component can be computed independently.  
* By evaluating the cross‑term sum separately we obtain a concrete numerical bound.

**Experiment that tests it**  

1. **Separate the sums** – Using the exact zero list from Hypothesis 1, compute the variance contributed by each **individual character** (autocorrelation term) and sum them to get \(V_{\text{auto}}\).  
2. **Compute cross‑terms** – Evaluate the mixed term  
   \[
   V_{\text{cross}}=\sum_{\chi\neq\chi'} \Bigl(\sum_{\rho_{\chi}} \sum_{\rho_{\chi'}} \dots\Bigr),
   \]  
   using the same high‑precision zero set.  
3. **Relative size** – Form the ratio  
   \[
   R = \frac{V_{\text{cross}}}{V_{\text{auto}}+V_{\text{cross}}}.
   \]  
   If \(R<0.05\) the hypothesis holds; if it is larger, cross‑terms are non‑negligible and must be incorporated more carefully.

---

## Hypothesis 5 – *Saturation of the discrepancy at very large \(x\)*  

**Statement**  
Beyond a certain **critical bound** (approximately \(x_{\text{c}} \sim 10^{7}\)), the empirical variance **stops growing** and begins to settle toward the corrected RMT value, indicating **asymptotic convergence**. Consequently, the ratio  
\[
\frac{V_{\text{emp}}(x)}{V_{\text{corr}}(x)}\rightarrow 1
\]  
as \(x\) exceeds \(x_{\text{c}}\).

**Why it is testable**  
* The hypothesis predicts a **qualitative change** in the scaling law: a transition from a regime where finite‑size effects dominate to one where the RMT prediction dominates. This transition can be detected by measuring the empirical variance at several large \(x\) values.

**Experiment that tests it**  

1. **Extended simulations** – Run the GPU‑accelerated Chebyshev‑bias generator for the next set of bounds  
   \[
   x\in\{2\times10^{7},\,5\times10^{7},\,10^{8},\,2\times10^{8}\},
   \]  
   keeping the same modulus 210.  
2. **Compute the ratio** – For each \(x\) compute  
   \[
   r(x)=\frac{V_{\text{emp}}(x)}{V_{\text{corr}}(x)},
   \]  
   using the corrected variance from Hypothesis 2.  
3. **Detect saturation** – Plot \(r(x)\) versus \(\log x\). If the curve **flattens** toward \(r=1\) for the two largest \(x\) values (i.e. the difference \(|r(x)-1|\) drops below the 15 % threshold), the hypothesis is supported.  
4. **Identify \(x_{\text{c}}\)** – Fit a simple logistic or asymptotic model to estimate the crossing point where the derivative \(|dr/d\log x|\) becomes < 0.01.

---

### How these hypotheses together address the core problem  

| Hypothesis | What it isolates | Expected impact on the 430‑fold gap |
|------------|-------------------|--------------------------------------|
| **H1** (exact zeros) | Numerical error from log approximations | ↑ theoretical variance → gap shrinks (target ≥30 % reduction) |
| **H2** (finite‑scale correction) | Missing \(\mathcal{O}(1/\log x)\) terms in the formula | Brings the corrected variance within 15 % of the empirical at \(x=10^{8}\) |
| **H3** (zero‑sum truncation) | Effect of finite‑height cut‑off on the zero sum | Demonstrates >70 % gap reduction when higher zeros are included |
| **H4** (inter‑character cross‑terms) | Possible missed correlations | If negligible, we can safely ignore them, simplifying the model |
| **H5** (asymptotic saturation) | Behaviour of the empirical variance at very large \(x\) | Confirms that the model converges to the true RMT prediction, satisfying the “success criteria” of the project |

If **H1–H3** collectively reduce the discrepancy below the 15 % threshold and **H5** shows clear convergence, the research objective—“resolve the RMT‑empirical variance discrepancy via exact zeros and finite‑scale corrections”—will be deemed achieved.  

---  

**In short:** the five hypotheses turn the abstract problem into a sequence of **quantifiable computational tests**, each producing a concrete number that can be compared against the target criteria. The Multi‑GPU pipeline supplies the necessary throughput, while the high‑precision zero‑generation routines (Hardy‑Z/Riemann‑Siegel, FP64) guarantee that the only remaining source of error is the theoretical modeling itself.