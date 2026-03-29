**Premise (building on prior work)**  
Prior experiments showed that the “collapse to 0” of the variance differential Δ(Pₖ) in high‑order primorial bases is an artifact of IEEE‑754 under‑flow (float32/64 cancellation).  The next step is to prove that the differential is in fact **non‑zero**, to uncover its true asymptotic shape, and to see how that shape feeds back into the LDAB weighting parameter α.  The hypotheses below are designed to be tested with arbitrary‑precision arithmetic (≥ 256 bits) and will **not** reuse the float‑only experiments that already gave a clear “zero‑due‑to‑under‑flow” result.

---

## 1.  Asymptotic scaling law for Δ(Pₖ)

**Statement**  
The true variance differential decays as a power of the logarithm of the primorial size:

\[
\Delta(P_k)\;=\;A\;\bigl(\log P_k\bigr)^{-\gamma}\;\bigl(1+o(1)\bigr),
\qquad k\to\infty,
\]

where \(A>0\) and \(\gamma>0\) are constants that depend only on the underlying residue‑class model.

**Why it is testable**  
We can compute exact (up to the chosen precision) values of Δ(Pₖ) for a sequence of primorial bases and fit the candidate function by nonlinear regression.  The fitted parameters can be compared across different base ranges to see if they converge.

**Experiment**  
1. **Implementation** – Use an arbitrary‑precision library (e.g., Python `mpmath` with 256‑bit working precision) to evaluate  

   \[
   \Delta(P_k)=\operatorname{Var}(P_k)-\operatorname{Var}(P_{k-1})
   \]

   for the first 12 primorials ( \(P_1=2\) up to \(P_{12}=2\!\cdot\!3\!\cdot\!5\!\cdot\!7\!\cdot\!11\!\cdot\!13\!\cdot\!17\!\cdot\!19\!\cdot\!23\!\cdot\!29\!\cdot\!31\!\cdot\!37\) ).  
2. **Model fitting** – Perform a nonlinear least‑squares fit of  

   \[
   \log\Delta(P_k)=\log A-\gamma\log\!\bigl(\log P_k\bigr)
   \]

   to the 12 data points.  Compute the coefficient of determination \(R^2\) and the standard errors of \(A\) and \(\gamma\).  
3. **Model selection** – Compare the power‑law fit with alternative candidates (e.g., exponential decay \(e^{-bP_k}\) or rational‑function forms) using AIC/BIC.  The hypothesis is supported if the power‑law yields \(R^2\ge0.99\) and the lowest AIC.

---

## 2.  Positivity of Δ(Pₖ) under sufficient precision

**Statement**  
When Δ(Pₖ) is computed with an arbitrary‑precision backend offering at least 256 bits of mantissa, the differential is **strictly positive** for every primorial base \(P_k\ge 30030\) (i.e., the “zero” observed with float64 is an artifact).

**Why it is testable**  
A direct numerical evaluation with high precision can reveal a non‑zero value, and a statistical test can quantify the evidence against the null hypothesis Δ(Pₖ) ≤ 0.

**Experiment**  
1. **High‑precision evaluation** – Using `mpmath` set to 256‑bit precision, compute Δ(Pₖ) for the six bases from \(P_6=30030\) up to \(P_{12}\).  Record the sign and the magnitude (in scientific notation).  
2. **Comparison with float64** – Also compute the same differentials with IEEE‑754 `float64` (or `float128` when available) and note that they return exactly 0.0.  
3. **Hypothesis test** – Treat the high‑precision values as a sample and perform a one‑sample, one‑sided t‑test (or a sign test) against the null hypothesis Δ(Pₖ) ≤ 0.  A p‑value < 0.01 will be taken as strong evidence that the true differential is positive.

---

## 3.  LDAB interpolation parameter α is a monotonic function of Δ(Pₖ)

**Statement**  
In the hybrid LDAB weighting scheme, the interpolation parameter α decreases monotonically as the variance differential shrinks, following a simple parametric relationship such as  

\[
\alpha \;=\;\alpha_0 \;-\;\lambda\,\Delta(P_k)
\quad\text{or}\quad
\alpha \;=\;\frac{\alpha_0}{1+\lambda\,\Delta(P_k)},
\]

with fitted constants \(\alpha_0\in(0,1)\) and \(\lambda>0\) that are independent of the primorial index.

**Why it is testable**  
We can measure the optimal α for each base (by minimizing the weighted variance or maximizing a target score) and then test whether the observed (α, Δ) pairs conform to the hypothesized functional form.

**Experiment**  
1. **Compute Δ(Pₖ)** – Using the 256‑bit pipeline from Hypothesis 2.  
2. **Optimize α** – For each primorial base, run the LDAB hybrid weighting algorithm over a fine grid of α values (e.g., 0.01–0.99) and select the α that minimizes the empirical variance of the resulting distribution (or maximizes the cross‑validated likelihood).  
3. **Fit the relationship** – Collect the pairs \((\Delta(P_k),\alpha_{\text{opt}})\).  Fit both the linear and the rational models by ordinary least squares (after appropriate transformation).  Use \(R^2\) and residual diagnostics to decide which description best captures the trend.  Validate by predicting α for a held‑out primorial (e.g., \(P_{13}\)) and comparing the predicted versus observed value.

---

## 4.  Precision threshold needed to capture the true Δ(Pₖ)

**Statement**  
There exists a minimum number of precision bits, \(N_c(P_k)\), beyond which the relative error of Δ(Pₖ) falls below a prescribed tolerance (e.g., \(10^{-6}\)).  This threshold grows roughly logarithmically with the primorial size, and for all bases up to \(P_{12}=223\,092\,870\) a ceiling of **512 bits** is sufficient.

**Why it is testable**  
We can compute Δ(Pₖ) at several increasing precision levels, compare each to a high‑precision reference, and locate the point where the error drops below the tolerance.

**Experiment**  
1. **Reference computation** – Choose a “exact” value by evaluating Δ(Pₖ) with 1024‑bit (or higher) precision; treat this as the ground truth.  
2. **Precision sweep** – For each primorial base, recompute Δ(Pₖ) using mantissa lengths of 64, 128, 256, 512, and 1024 bits.  Compute the relative error  

   \[
   \varepsilon_n \;=\; \frac{\bigl|\Delta_{n}(P_k)-\Delta_{\text{ref}}(P_k)\bigr|}
                              {\bigl|\Delta_{\text{ref}}(P_k)\bigr|}
   \]

   for each precision \(n\).  
3. **Determine \(N_c\)** – Find the smallest \(n\) such that \(\varepsilon_n<10^{-6}\) for all bases.  Plot \(N_c\) versus \(\log_2 P_k\) and perform a linear regression to verify the logarithmic scaling.  Confirm that the required precision never exceeds 512 bits in the studied range.

---

## 5.  Connection between the scaling amplitude and Mertens‑type constants

**Statement**  
The amplitude \(A\) in the power‑law scaling (Hypothesis 1) is proportional to the Mertens‑type product  

\[
M_k \;=\; \prod_{p\le p_k}\bigl(1-\tfrac1p\bigr)^2,
\]

or equivalently to Mertens’ constant \(B\).  In formulas:

\[
A \;=\; c\;M_k\;(1+o(1)),
\]

where \(c\) is a dimensionless constant that can be predicted from the variance‑gap model.

**Why it is testable**  
We can compute the theoretical product \(M_k\) for each primorial base, estimate the empirical amplitude \(\hat A\) from the regression in Hypothesis 1, and test whether \(\hat A / M_k\) is consistent across bases.

**Experiment**  
1. **Compute Mₖ** – Using arbitrary‑precision arithmetic, evaluate  

   \[
   M_k \;=\; \prod_{p\le p_k}\bigl(1-\tfrac1p\bigr)^2
   \]

   for the primes up to the 12‑th primorial (i.e., up to 37).  
2. **Extract \(\hat A\)** – From the fit in Hypothesis 1, obtain the estimated amplitude \(\hat A\) and its confidence interval.  
3. **Test proportionality** – Compute the ratio \(\hat A / M_k\) for each base and perform a one‑sample t‑test (or a runs test) to see if the ratios are constant (i.e., the null hypothesis that the mean ratio equals a universal constant \(c\)).  A non‑significant result (p > 0.05) would support the hypothesis.  Additionally, plug the theoretical constant \(c\) into the model  

   \[
   \Delta(P_k) \approx c\,M_k\,\bigl(\log P_k\bigr)^{-\gamma}
   \]

   and compare its goodness‑of‑fit with the empirical model from Hypothesis 1 (e.g., via an extra‑sum‑of‑squares F‑test).

---

### Summary of the Testable Hypotheses

| # | Hypothesis (statement) | Key experiment(s) |
|---|------------------------|-------------------|
| 1 | **Power‑law decay**: \(\Delta(P_k)=A(\log P_k)^{-\gamma}\) | Arbitrary‑precision computation + nonlinear regression (R², AIC) |
| 2 | **Strict positivity** of the true differential at ≥ 256‑bit precision | One‑sided t‑test against Δ ≤ 0, comparing high‑precision vs. float64 |
| 3 | **α‑Δ relationship**: α decreases monotonically with Δ, linear or rational form | Grid‑search optimal α per base → fit α(Δ) models |
| 4 | **Precision threshold** \(N_c(P_k)\) for ε < 10⁻⁶ scales logarithmically | Precision sweep (64‑1024 bits) → error analysis & regression |
| 5 | **Mertens link**: scaling amplitude \(A\) ∝ Mertens‑type product \(M_k\) | Compute \(M_k\) → compare \(\hat A/M_k\) across bases (t‑test) |

These hypotheses directly extend the prior finding that the “zero” variance differential is an artifact, provide concrete mathematical forms to validate, and link the observed behavior to both computational precision requirements and underlying number‑theoretic structure.  All experiments are designed to be performed **exclusively** with arbitrary‑precision arithmetic, satisfying the constraint that float32/64 may not be used for Δ(Pₖ) at \(P_k\ge30030\).