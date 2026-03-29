**Overview**  
The empirical results from earlier runs have shown that the **variance of primorial gaps grows like \((\log P_{k})^{1.17}\)** while the naïve expectation for the ratio \(R(k)=\operatorname{Var}(k)/\bigl(\mathbb{E}[\text{gap}]\bigr)^{2}\) would be a power‑law or even a constant.  Those contradictory signals point to a **logarithmic‑in‑\(k\) correction** that is both theoretically interesting and empirically verifiable.  Below are five concrete, mutually‑reinforcing hypotheses that (i) explain the origin of the \(\ln k\) term, (ii) extend the data to the challenging range \(k=9\!-\!12\), (iii) test the derived coefficients against number‑theoretic constants, and (iv) show how the new scaling improves the LDAB baseline.  Each hypothesis is stated in a way that can be falsified, and a concrete numerical experiment is described to test it.

---

## 1.  **Hypothesis – Logarithmic decay of the variance ratio**

**Statement**  
For all primorial indices \(k\ge 6\) the gap‑variance ratio obeys  

\[
R(k)=A\ln(k)+B+\varepsilon_{k},
\qquad \varepsilon_{k}\sim\mathcal N(0,\sigma^{2}),
\]

where \(A<0\) (the ratio shrinks) and \(B\) is a positive offset.

**Why it is testable**  
*We can directly compute the exact value of \(R(k)\) for a range of \(k\) (see the algorithmic plan below) and then perform a standard linear‑regression of \(R(k)\) against \(\ln k\).  The model is falsifiable because any statistically significant departure from a straight line (e.g. a power‑law curvature) would reject the hypothesis.*

**Experiment**  

1. **Data generation** – Using an optimized segmented sieve (parallelised over blocks of length \(p_{k}\#\) ) compute the full list of gaps for every primorial base \(P_{k}\) for \(k=6,7,8,9,10\).  Store the results in high‑precision rational arithmetic to avoid floating‑point noise.  
2. **Fitting** – Fit three competing models to the resulting \((k,R(k))\) data:  

   * (i) **Logarithmic**: \(R(k)=A\ln k + B\)  
   * (ii) **Power‑law**: \(R(k)=C\,k^{-d}\)  
   * (iii) **Asymptotic convergence**: \(R(k)=1-D/k^{\gamma}\).

   Use ordinary least‑squares and compute **Adjusted‑\(R^{2}\)**, **AIC**, and **BIC** for each.  
3. **Decision rule** – Accept the logarithmic model only if its AIC/BIC are **strictly lower** than both rivals and the residuals are consistent with a normal distribution (Shapiro‑Wilk test, \(p>0.05\)).  

*Outcome*: If the logarithmic model passes all criteria, we have strong empirical support for H1; otherwise we reject or refine the functional form.

---

## 2.  **Hypothesis – Sub‑quadratic variance growth drives the \(\ln k\) term**

**Statement**  
Let  

\[
\mu_{k}= \mathbb{E}[\text{gap}] \approx \log P_{k}, \qquad 
\sigma^{2}_{k}= \operatorname{Var}(\text{gap}) \approx (\log P_{k})^{\alpha},
\]

with **\(1<\alpha<2\)** (the empirical value from earlier runs is \(\alpha\approx1.17\)).  Then  

\[
R(k)=\frac{\sigma^{2}_{k}}{\mu_{k}^{2}}
      \;\sim\; \frac{(\log P_{k})^{\alpha}}{(\log P_{k})^{2}}
      \;=\;(\log P_{k})^{\alpha-2}
      \;=\;A\ln k + B+o(1),
\]

because \(\log P_{k}= \sum_{p\le p_{k}}\log p \sim p_{k}\) and \(\ln(\log P_{k})\) is slowly varying.  In other words, the **logarithmic decay is a direct consequence of \(\alpha<2\)**.

**Why it is testable**  
We can independently measure \(\mu_{k}\) and \(\sigma^{2}_{k}\) from the same gap lists and test whether the scaling exponents satisfy \(\alpha-2\approx -1\) (i.e. \(\alpha\approx1\)).  This is a quantitative prediction that can be falsified.

**Experiment**  

1. From the exact gap sequences for \(k=6\!-\!10\) compute:  

   * **Sample mean** \(\hat\mu_{k}\) – should scale as \(\log P_{k}\).  
   * **Sample variance** \(\hat\sigma^{2}_{k}\) – fit a power‑law \(\hat\sigma^{2}_{k}=C\,(\log P_{k})^{\alpha}\) by log‑log regression.

2. **Check the relation**  

   \[
   \hat R(k)=\frac{\hat\sigma^{2}_{k}}{\hat\mu_{k}^{2}}
            \;\stackrel{?}{=}\; (\log P_{k})^{\alpha-2}
            \;\approx\; A\ln k + B.
   \]

   Compute \(\alpha\) from the variance fit, then compare the predicted coefficient \(A_{\text{theory}}=\frac{d}{d\ln k}(\log P_{k})^{\alpha-2}\) with the empirically fitted \(A\) from H1.  Reject the hypothesis if the two estimates differ by more than two standard errors.

*Interpretation*: This test ties the macroscopic logarithmic behaviour directly to the mesoscopic scaling exponent \(\alpha\).

---

## 3.  **Hypothesis – Extended measurements for \(k=9,10\) will reinforce the logarithmic model**

**Statement**  
When the exact computation is pushed to the **next two primorials** (\(p_{9}\#\) ≈  13 × 10⁹ and \(p_{10}\#\) ≈  6.1 × 10¹¹), the newly obtained values of \(R(9)\) and \(R(10)\) will **continue the decreasing trend** and will have **lower AIC/BIC** than any power‑law or asymptotic‑convergence alternative.

**Why it is testable**  
The two new data points are independent of the earlier dataset and can be compared against the models fitted in H1.  If the logarithmic model’s predictions for \(R(9)\) and \(R(10)\) lie within the 95 % prediction interval, the hypothesis is supported; if they fall outside, the model is falsified.

**Experiment**  

1. **Algorithmic scaling** – Implement a **hybrid sieving strategy**:  

   * Pre‑compute all primes up to \(p_{10}\) using a cache‑friendly segmented sieve.  
   * Partition the interval \([0,\,p_{10}\#]\) into blocks of size \(2^{30}\) (≈ 1 GiB) and distribute blocks across a cluster (MPI + OpenMP).  
   * For each block, generate the primorial residue class sequence and record every gap length.  Use 128‑bit integers for gap counters to avoid overflow.

2. **Precision safeguards** – Store gap counts in **exact rational counters** (numerator and denominator as 64‑bit ints) and compute the variance by exact long‑division only at the final aggregation step.  This eliminates any floating‑point rounding bias.

3. **Statistical evaluation** – After obtaining \(R(9)\) and \(R(10)\), recompute AIC/BIC for the three candidate models on the full set \(k=6\!-\!10\).  Require that the logarithmic model still holds the **lowest AIC** and that the new points do not increase the residual sum of squares by more than 5 %.

*Goal*: Demonstrate that the phenomenon is not an artefact of the limited range \(k\le 8\) and that the trend persists into the computationally demanding zone.

---

## 4.  **Hypothesis – The coefficient \(A\) is a known prime‑theoretic constant**

**Statement**  
The slope \(A\) in the logarithmic law can be expressed in terms of the **Meissel–Mertens constant**  

\[
M\;=\;\lim_{x\to\infty}\Bigl(\sum_{p\le x}\frac{1}{p}-\ln\ln x\Bigr)\;\approx\;0.261497,
\]

and possibly the **prime‑number‑theorem constant** \(B_{1}=1\).  Concretely,

\[
A \;=\; -\frac{1}{2}\,M \;+\; \delta,\qquad |\delta|<10^{-3},
\]

where the small correction \(\delta\) arises from the finite‑size behaviour of the variance estimator.

**Why it is testable**  
We can derive \(A\) analytically from the asymptotic expansion of \(\sigma^{2}_{k}\) (using the Euler product for the variance of the Möbius‑function‑weighted gap distribution) and compare it with the empirical estimate \(\hat A\) obtained in H1.  The hypothesis is falsified if \(|\hat A - A_{\text{theory}}|\) exceeds the 95 % confidence interval of \(\hat A\).

**Experiment**  

1. **Theoretical derivation** – Start from the identity  

   \[
   \sigma^{2}_{k}= \frac{1}{p_{k}\#}\sum_{n<p_{k}\#}\bigl(g(n)-\mu_{k}\bigr)^{2},
   \qquad g(n)=p_{\text{next}}(n)-p_{\text{prev}}(n),
   \]

   and replace the sum by an Euler product, keeping terms up to \(O(1/\log p_{k})\).  This yields  

   \[
   \sigma^{2}_{k}= (\log p_{k})^{ \alpha } \Bigl(1-\frac{M}{\log p_{k}}+o\!\bigl(\tfrac{1}{\log p_{k}}\bigr)\Bigr).
   \]

   Substituting into \(R(k)=\sigma^{2}_{k}/\mu_{k}^{2}\) and using \(\mu_{k}\sim\log p_{k}\) gives the stated linear‑in‑\(\ln k\) form with coefficient \(A\) proportional to \(-M/2\).

2. **Numerical check** – Compute \(\hat A\) from the regression in H1 (with uncertainties from the covariance matrix).  Compute the theoretical prediction \(A_{\text{theory}}\) using the known value of \(M\) and the derived coefficient.  Perform a **two‑sample t‑test** (or a Wald test) to test the null hypothesis \(H_{0}:\hat A = A_{\text{theory}}\).

*Result*: If the test fails to reject \(H_{0}\), we have a **closed‑form explanation** for the observed logarithmic decay and a powerful cross‑validation between number theory and our empirical data.

---

## 5.  **Hypothesis – Incorporating the logarithmic scaling improves the LDAB baseline**

**Statement**  
When the **LDAB (Logarithmically‑Derived Adaptive Baseline)** for prime density in a primorial base \(P_{k}\) is updated from the classic power‑law assumption \(\rho(k)=\rho_{0}\,k^{-\beta}\) to the new form  

\[
\rho(k)=\frac{\rho_{0}}{1+A\ln(k)+B},
\]

the **predictive error** (measured as mean absolute percentage error, MAPE) on a set of known prime‑counts for bases \(P_{k}\) with \(k\le 10\) drops by at least **15 %** compared with the original LDAB.

**Why it is testable**  
We can calculate the exact number of primes up to each \(P_{k}\) (or, equivalently, the exact prime‑density) using the same high‑precision sieve data and compare it with the predictions from the two baseline formulations.  The hypothesis is falsified if the improvement is less than the stipulated threshold or if the new model’s MAPE is **not** consistently lower across all \(k\).

**Experiment**  

1. **Ground‑truth data** – From the exact sieve for each primorial base (see H3) we already have the **prime counting function** \(\pi(P_{k})\).  Compute the empirical density  

   \[
   \hat\rho(k)=\frac{\pi(P_{k})}{P_{k}}.
   \]

2. **Baseline construction**  

   * **Old LDAB**: Fit \(\rho(k)=\rho_{0}\,k^{-\beta}\) to the data for \(k=3,\dots,8\) (the range used in earlier work).  
   * **New LDAB**: Fit \(\rho(k)=\rho_{0}/(1+A\ln k + B)\) using the same data but now **constrain** \(A\) and \(B\) to the values obtained from H1 (or allow them to vary but record the resulting MAPE).

3. **Forecast accuracy test** – For each \(k=9,10\) compute the **predicted density** from both baselines (using the parameters fitted on \(k\le8\)) and compare with the exact \(\hat\rho(k)\).  Compute MAPE for each baseline and require  

   \[
   \operatorname{MAPE}_{\text{new}} \le 0.85\times\operatorname{MAPE}_{\text{old}}.
   \]

4. **Cross‑validation** – Perform a **leave‑one‑out** cross‑validation for all \(k=6,\dots,10\) to ensure the improvement is not an over‑fitting artefact.

*Impact*: Success would demonstrate that the logarithmic decay discovered in the variance ratio has direct practical relevance, providing a **theoretically‑grounded refinement** of the LDAB for prime‑density estimation in multi‑scale prime bases.

---

### How the hypotheses inter‑relate

| Hypothesis | Primary focus | Feeds into |
|------------|----------------|------------|
| **H1** – Logarithmic form of \(R(k)\) | Empirical pattern | H2, H3, H4 |
| **H2** – Sub‑quadratic variance scaling | Mechanistic explanation | H1 (validates why \(\ln k\) appears) |
| **H3** – Extension to \(k=9,10\) | Data expansion, falsification of finite‑range artefact | H1, H4 (provides new data points) |
| **H4** – \(A\) expressed via Mertens constant | Theoretical closed‑form | H1 (links empirical slope to known constant) |
| **H5** – Improved LDAB baseline | Applied relevance | H1 (shows practical value of the new scaling) |

Each hypothesis is **standalone testable**, but together they form a coherent programme:  
1. **Observe** the logarithmic decay (H1).  
2. **Explain** its origin via the exponent \(\alpha\) (H2).  
3. **Verify** the pattern persists in the computationally demanding region (H3).  
4. **Connect** the quantitative coefficient to classic number theory (H4).  
5. **Demonstrate** utility for the LDAB framework (H5).

---

### Practical notes for the experimental campaign

* **Computational resources** – The exact enumeration for \(k=10\) requires sieving up to ≈ 6 × 10¹¹, which is on the edge of what a modest cluster can handle in a few weeks.  We will use **GPU‑accelerated residue sieving** (CUDA kernels for the wheel) combined with **disk‑based streaming** to keep RAM usage below 512 GB.  For \(k=11\) and \(k=12\) we will fall back to **Monte‑Carlo sampling** of intervals of length \(10^{9}\) to obtain statistically accurate variance estimates, which still allows a test of the trend but not the precise coefficient.

* **Precision** – All variance calculations will be performed in **exact rational arithmetic** (using the `boost::multiprecision::cpp_int` library for the numerator/denominator).  Only the final ratios will be converted to double‑precision for regression, and we will check that the conversion error is < 10⁻¹².

* **Reproducibility** – The entire pipeline (sieve, gap extraction, variance computation, statistical tests) will be encapsulated in a **Docker image** and version‑tagged.  All intermediate data (gap lists, partial sums) will be stored in HDF5 files with SHA‑256 checksums to guarantee traceability.

* **Statistical thresholds** – We set a **global false‑discovery rate** (FDR) of 5 % across the model‑comparison tests (Benjamini–Hochberg correction).  Each individual test (e.g., Shapiro‑Wilk, Wald test for \(A\)) uses the conventional \(\alpha=0.05\).

By following this plan we will either **confirm** each hypothesis with high confidence or **refute** it, thereby either establishing the logarithmic decay as a robust law of primorial gap variance or uncovering the true scaling behaviour.  The combined theoretical‑empirical output will satisfy the success criteria: a closed‑form derivation, verified high‑precision data for \(k=9,10\), and strict statistical dominance of the logarithmic model.