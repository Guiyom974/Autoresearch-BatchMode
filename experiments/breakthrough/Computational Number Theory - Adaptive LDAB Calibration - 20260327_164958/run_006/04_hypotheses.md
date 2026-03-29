**Background – what the prior experiments have already shown**

| Prior run | Key observation | Implication for the next step |
|-----------|------------------|--------------------------------|
| 036 | `log P` overflows double‑precision at primorial order **k = 132**. | Any evaluation that must go beyond the first ∼130 primorials needs **arbitrary‑precision** arithmetic. |
| 037 | Un‑guarded γ‑evaluations cause premature overflow at factorial index **k = 5**. | A **guarded log‑γ** (or log‑Gamma) scheme is required to keep the binomial terms finite. |
| 038 | A guarded log‑γ approximation yields finite log‑binomial terms for large primorials. | This trick can be incorporated into the new high‑precision estimator. |
| 040 | High‑order LDAB expansions reach machine‑ε accuracy at **x = 2310** after only a few terms. | The asymptotic series can be used as a **reference** for error estimation, but the decay rate **λ** seemed to vary unpredictably (run 043). |
| 043 | The exponential decay constant **λ** of the truncation error “jumps” between primorial indices, suggesting **numerical artefacts** rather than a genuine trend. | With enough precision we should be able to **stabilise** the λ‑estimates. |

The next phase therefore aims at (i) building a **self‑contained, arbitrary‑precision logarithmic‑integral/LDAB routine**, (ii) extracting the empirical correction factor \(c_{\text{emp}}(t)\) for the three target bases, and (iii) characterising its variance and base‑dependence.  
Below are **five testable hypotheses** that follow directly from the open gaps identified above.  Each hypothesis is stated, explained why it can be tested, and a concrete numerical experiment is outlined.

---

## Hypothesis 1 – High‑precision estimator dramatically reduces the variance of \(c_{\text{emp}}(t)\)

**Statement**  
When the LDAB density is evaluated with a **custom, arbitrary‑precision logarithmic‑integral routine** (≥ 200‑bit mantissa), the empirical correction factor \(c_{\text{emp}}(t)\) for bases 210, 2310 and 30030 will have a **sample variance at least 10 × smaller** than the ≈ 938 (σ) reported earlier for double‑precision asymptotics.

**Why it is testable**  
Variance is a directly measurable statistic from a time‑series.  By generating the same prime‑stream data and the same set of theoretical LDAB densities, we can compare the spread of \(c_{\text{emp}}(t)\) obtained under two arithmetic regimes (double vs. arbitrary precision).  The reduction can be quantified with a simple ratio of variances and tested for statistical significance (e.g., an F‑test).

**Proposed experiment**  

1. **Prime‑stream generation** – sieve deterministically up to \(t = 10^{6}\) and record the exact count of primes at every 10 000‑th integer.  
2. **Reference LDAB density** – compute the theoretical LDAB density \(\rho_{\text{LDAB}}(t)\) using the new **high‑precision li** implementation (series expansion of \(\text{li}(x)\) with ≥ 200‑bit MPFR or Python’s `decimal` set to 50‑digit precision).  
3. **Empirical density** – \(\rho_{\text{emp}}(i) = \pi(i)/i\) for each recorded \(i\).  
4. **Correction factor** – \(c_{\text{emp}}(i) = \rho_{\text{emp}}(i) - \rho_{\text{LDAB}}(i)\).  
5. **Control run** – repeat steps 2‑4 with the standard double‑precision asymptotic li (`scipy.special.expi`).  
6. **Statistical comparison** – compute the sample variance \(\widehat{\sigma}^{2}\) for each base in both precision regimes and apply an F‑test (or a Levene test if the distributions are non‑normal).  

*Expected outcome*: The high‑precision series should push \(\widehat{\sigma}^{2}\) well below 100 (i.e. σ ≪ 10), confirming that the earlier “≈ 938” was an artefact of round‑off error propagation.

---

## Hypothesis 2 – The base‑dependent shift of \(c_{\text{emp}}(t)\) (≈ 0.307 – 0.366) is genuine and persists under high‑precision evaluation

**Statement**  
The **mean value** of \(c_{\text{emp}}(t)\) for base 210 will be statistically distinguishable from the mean for base 2310, and both will differ from the mean for base 30030, even after eliminating numerical noise.

**Why it is testable**  
If the three means (and their 95 % confidence intervals) do not overlap, a simple hypothesis test (e.g., one‑way ANOVA or pairwise t‑tests) can reject the null that the shifts are identical.  The test requires only the series of \(c_{\text{emp}}(t)\) already generated in Hypothesis 1.

**Proposed experiment**  

1. Using the high‑precision data from Hypothesis 1, compute the **sample mean** \(\bar{c}_{b}\) and the **standard error** for each base \(b \in \{210,2310,30030\}\).  
2. Construct 95 % confidence intervals (e.g., \(\bar{c}_{b} \pm t_{0.975,\,n-1}\, \text{SE}\)).  
3. Perform a **one‑way ANOVA** (or Kruskal–Wallis if normality fails) on the three groups; if the p‑value < 0.05, conclude that at least one mean differs.  
4. Follow up with **pairwise t‑tests** (Bonferroni‑adjusted) to identify which bases are distinct.

*Expected outcome*: The intervals for the three bases will be **non‑overlapping**, confirming a systematic base‑dependent offset.

---

## Hypothesis 3 – \(c_{\text{emp}}(t)\) is a **stationary** time series when evaluated with the high‑precision framework

**Statement**  
The high‑precision correction‑factor series for each base will **not contain a unit root**; i.e., it will be stationary (mean‑reverting) rather than exhibiting ever‑increasing variance with \(t\).

**Why it is testable**  
Standard econometric tests (Augmented Dickey–Fuller, ADF; or Phillips–Perron, PP) can be applied to the three series.  A p‑value < 0.05 in the ADF test rejects the unit‑root null, implying stationarity.  The test only needs the series of \(c_{\text{emp}}(t)\).

**Proposed experiment**  

1. Take the high‑precision \(c_{\text{emp}}(t)\) series (≈ 100 points, one per 10 000‑primes interval).  
2. Run an **ADF test** (including an optimal lag selection via AIC) for each base.  
3. Optionally, apply the **KPSS test** (where the null is stationarity) as a complementary check.  
4. Visualise the series with an **autocorrelation function (ACF)** – a rapidly decaying ACF further supports stationarity.

*Expected outcome*: ADF p‑values < 0.05 for all three bases, indicating that the previously observed “runaway” standard deviation was a transient numerical artefact, not an intrinsic property of the LDAB model.

---

## Hypothesis 4 – Guarded log‑γ with arbitrary precision eliminates overflow for primorial indices up to **k = 132** (and beyond) while preserving ≥ 12‑digit accuracy

**Statement**  
Implementing a **guarded log‑Gamma** routine inside an arbitrary‑precision environment (MPFR with ≥ 500‑bit precision) will allow stable evaluation of the LDAB density for **all primorial orders up to k = 132**, with a **relative error < 10⁻¹²** compared with a reference value computed at 1000‑bit precision.

**Why it is testable**  
We can directly compare the computed log‑primorial values and the resulting binomial‑coefficient terms to a “gold‑standard” high‑precision reference.  The presence of overflow (NaN, Inf) or excessive rounding error (> 10⁻¹²) would falsify the hypothesis.

**Proposed experiment**  

1. **Reference library** – using Python’s `mpmath` with 1000‑bit precision, compute the exact log‑primorial \(\log P_{k}\) for each \(k = 1,\dots,132\) (where \(P_{k}\) is the product of the first \(k\) primes).  
2. **Test implementation** – code the guarded log‑γ in C++ with MPFR (or in Python with `mpmath` set to 500‑bit) and evaluate \(\log P_{k}\) for the same range.  
3. **Error measurement** – for each \(k\), compute the absolute difference \(|\log P_{k}^{\text{test}} - \log P_{k}^{\text{ref}}|\) and the relative error \(\frac{|\log P_{k}^{\text{test}} - \log P_{k}^{\text{ref}}|}{\log P_{k}^{\text{ref}}}\).  
4. **Overflow check** – verify that no `Inf` or `NaN` appears for any \(k\).  

*Expected outcome*: All 132 values have relative error < 10⁻¹² and no overflow, confirming that the guarded log‑γ approach scales far beyond double‑precision limits.

---

## Hypothesis 5 – The truncation error of the high‑order LDAB asymptotic expansion decays **exponentially** with a **stable, base‑specific decay constant λ** across expansion orders 5 – 20

**Statement**  
When the LDAB expansion is evaluated with the arbitrary‑precision framework, the residual error (difference between the truncated series and the high‑precision reference) will fit the model  

\[
\log\bigl|e_{m}(x)\bigr| = \log A - \lambda m + \varepsilon,
\]

where \(m\) is the number of terms retained, and the fitted **λ** will be **consistent (within ± 0.05) across the three bases**, contradicting the earlier report of “unpredictable” λ.

**Why it is testable**  
Regression of \(\log|e_{m}|\) versus \(m\) yields an estimate of λ with a standard error.  Consistency across bases can be assessed by comparing the 95 % confidence intervals for λ.

**Proposed experiment**  

1. **Reference values** – for each base \(b\) (210, 2310, 30030) compute a “true” LDAB density \(\rho_{\text{ref}}(b)\) using the high‑precision li at 500‑bit precision.  
2. **Series computation** – evaluate the LDAB asymptotic series with **\(m = 1,\dots,30\)** terms (using the same high‑precision arithmetic).  
3. **Error calculation** – \(e_{m}(b) = \rho_{m}(b) - \rho_{\text{ref}}(b)\).  
4. **Fitting** – perform ordinary least‑squares on \(\log|e_{m}(b)|\) vs. \(m\) for each base; extract λ̂ and its 95 % CI.  
5. **Cross‑base comparison** – test whether the CI for λ̂ overlap (if they do, the decay constants are statistically indistinguishable, supporting a universal λ for the LDAB model).

*Expected outcome*: λ̂ ≈ 0.7 – 0.9 (consistent with the “≈ 0.8” hinted at in run 041) with narrow CIs (± 0.02) and overlapping intervals across the three bases, indicating that the earlier erratic behaviour was due to insufficient precision.

---

### How these hypotheses together satisfy the **success criteria**

| Success criterion | How the hypotheses address it |
|--------------------|--------------------------------|
| **Framework validation** – convergence & stability up to \(10^{6}\) | H1 & H4 demonstrate that the custom li and guarded log‑γ produce **error < 10⁻¹²** and **no overflow** for the full range. |
| **Reliable extraction of \(c_{\text{emp}}(t)\)** | H1 guarantees low‑variance, high‑precision correction factors; H2 confirms a **systematic base‑dependent shift**; H3 shows the series is **stationary**, not polluted by transient noise. |
| **Statistical profile of \(c_{\text{emp}}(t)\)** | H2 provides means & confidence intervals; H3 supplies unit‑root test results; H5 characterises the **error‑decay behaviour** of the underlying asymptotic model. |

All experiments are **self‑contained**, rely only on the LDAB model and the three primorial bases, and employ **reproducible, arbitrary‑precision arithmetic**—exactly the requirements stipulated in the problem statement.  The hypotheses therefore form a coherent, testable roadmap for the next research phase.