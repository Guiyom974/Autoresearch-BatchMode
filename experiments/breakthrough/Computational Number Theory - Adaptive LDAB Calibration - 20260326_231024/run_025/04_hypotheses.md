Based on the research problem and the prior findings (floating‑point underflow artifacts, a corrected variance‑extraction method, and the first empirical indication of a sub‑quadratic scaling of the variance‑to‑mean ratio), we propose the following five testable hypotheses.  Each hypothesis is stated together with why it can be tested and the specific numerical experiment that would supply evidence for or against it.

---

### 1.  Hypothesis – The 0.56 exponent originates from the inclusion‑exclusion structure of the primorial sieve  

**Statement**  
The dampening of the variance‑to‑mean scaling exponent to β ≈ 0.56 is a direct consequence of the correlation of gaps induced by the modular constraints of the first *k* primes (the primorial sieve).  An analytic treatment of the Möbius inversion that underlies the sieve predicts a unique exponent βₜₕₑₒ ≈ 0.56 that is independent of the size of *k* (once *k* is large enough).

**Why it is testable**  
If the exponent truly follows from the inclusion‑exclusion structure, then a *theoretically derived* value βₜₕₑₒ can be computed from known number‑theoretic quantities (e.g., the Euler product over the first *k* primes) and must agree with the *empirically measured* β for all sufficiently large *k*.  The prediction can therefore be falsified by a precise measurement of β.

**Experiment**  

1. **High‑precision data generation** – Using arbitrary‑precision integer arithmetic (to eliminate the underflow problem identified in run 006) and the corrected gap‑variance extraction (run 010), compute the exact variance‑to‑mean ratio *R*(*k*) for *k* = 13, 14, 15 (and, if computationally feasible, up to *k* = 16).  Store only streaming summaries (e.g., running sums of gaps, sum of squares) to avoid memory bottlenecks.  
2. **Analytic derivation** – Starting from the inclusion‑exclusion expression for the density of numbers coprime to *Pₖ*, derive the asymptotic form of the gap‑variance and obtain βₜₕₑₒ as a function of *k* (e.g., βₜₕₑₒ ≈ 0.56 + O(1/log *Pₖ*)).  
3. **Comparison** – For each *k*, compute βₑₘₚ from the slope of log *R*(*k*) versus log log *Pₖ* using weighted least squares, and compare βₑₘₚ with βₜₕₑₒ.  A residual RMS < 0.01 and *R*² > 0.99 would support the hypothesis; systematic deviation would refute it.

---

### 2.  Hypothesis – The scaling exponent is asymptotically stable (no drift) for *k* ≥ 12  

**Statement**  
The measured exponent β ≈ 0.5633 is not a transient finite‑size effect but converges to a constant value that remains essentially unchanged as *k* grows beyond 12 (up to at least *k* = 15).

**Why it is testable**  
If the exponent were drifting, successive estimates of β for larger *k* would show a monotonic shift outside their confidence intervals.  Conversely, if the exponent is stable, the confidence intervals for β at *k* = 13, 14, 15 should overlap with the interval obtained from the earlier data (*k* ≤ 12).  Statistical tests for parameter constancy can therefore decide.

**Experiment**  

1. **Extended regression** – Perform a joint weighted linear regression of log *R*(*k*) on log log *Pₖ* using all data from *k* = 2,…,15.  Obtain the overall β̂ and its 95 % confidence interval (CI).  
2. **Individual fits** – For each *k* = 13, 14, 15, compute β̂ₖ from a local regression on a sliding window of the three largest *k* values (or on the full dataset with a dummy variable for “large *k*”).  
3. **Stability tests** –  
   * **Overlap of CIs** – Check whether β̂₁₃, β̂₁₄, β̂₁₅ lie within the overall 95 % CI.  
   * **Chow‑type breakpoint test** – Test the null hypothesis that the slope (β) is the same for *k* ≤ 12 and *k* > 12.  A *p*‑value > 0.10 would indicate stability.  

If the exponent remains within ±0.01 of the pooled estimate, we accept the hypothesis; otherwise we reject it as a drifting effect.

---

### 3.  Hypothesis – A modified random‑subset model analytically predicts the observed exponent  

**Statement**  
If one treats the set of integers coprime to *Pₖ* as a random subset with the correct density (i.e., each integer is included independently with probability 1/ζ(*k*+1)), then the variance‑to‑mean ratio of the resulting gaps scales as  

\[
R(k)=\frac{\operatorname{Var}(G)}{\mathbb{E}[G]}\;\propto\;(\log P_k)^{\beta}
\]

with β ≈ 0.56.  The exponent emerges from the competition between the Poisson‑like randomness of the subset and the deterministic constraints imposed by the primorial’s prime factors.

**Why it is testable**  
We can (a) simulate the random‑subset model for a range of *k* and directly measure the scaling exponent, and (b) attempt an analytic calculation of the variance of gaps in this model, which should yield the same β.  The simulated exponent can be compared with the empirical β, providing a clear test.

**Experiment**  

1. **Monte‑Carlo simulation** – For each *k* = 6,…,15, generate 10 000 independent random subsets of the integers 1,…,*Pₖ* where each integer is kept with probability 1/ζ(*k*+1).  For each subset, compute the list of “gaps” (differences between successive retained integers) and record the sample variance and mean of the gaps.  Aggregate across trials to obtain an unbiased estimator of *R*(*k*).  
2. **Scaling analysis** – Plot log ⟨*R*(*k*)⟩ versus log log *Pₖ* and fit a line; extract β̂ₛₜₒ.  Compare β̂ₛₜₒ with the empirical β̂ (≈ 0.5633) using a two‑sample *t*‑test (or a Wald test for regression slopes).  
3. **Analytic derivation** – Derive the asymptotic variance of gaps for the random‑subset model using generating‑function techniques; show that the leading‑order term gives β = 0.56 up to corrections of order 1/log *Pₖ*.  

Agreement within ±0.02 would support the hypothesis; larger discrepancies would suggest that the primorial’s exact modular structure (beyond pure density) is essential.

---

### 4.  Hypothesis – The exponent is a deterministic function of the partial Euler product (or ζ(*k*+1))  

**Statement**  
β can be expressed explicitly in terms of the first *k* primes, for example  

\[
\beta(k)=1-\frac{1}{\log\!\bigl(\zeta(k+1)\bigr)}\qquad\text{or}\qquad
\beta(k)=a+\frac{b}{\log\!\bigl(\prod_{i=1}^{k}p_i\bigr)},
\]

so that once the primorial is fixed, β is completely determined by a known number‑theoretic quantity.

**Why it is testable**  
If such a functional form holds, then the sequence {β(k)}ₖ must match the sequence obtained from the formula when evaluated at the same *k*.  The match can be quantified with correlation, root‑mean‑square error, or a goodness‑of‑fit test.  Systematic deviations would invalidate the specific formula, prompting a search for alternative expressions.

**Experiment**  

1. **Compute β(k) from data** – Using the high‑precision *R*(*k*) values for *k* = 2,…,15, compute βₑₘₚ(k) by log‑log regression as before.  
2. **Evaluate candidate functions** – For each *k*, compute βₜₕₑₒ(k) using the proposed formulas (e.g., β = 1 − 1/log ζ(*k*+1)).  Also try a flexible parametrisation β(k) = a + b / log ζ(*k*+1) and fit *a*, *b* by nonlinear least squares to the empirical βₑₘₚ(k).  
3. **Model comparison** – Assess fit quality with *R*², AIC, and residual plots.  If a fitted formula yields *R*² > 0.95 and residuals are randomly scattered, the hypothesis is supported; if residuals show structure (e.g., curvature), reject in favor of a more complex dependence.  

This test directly links the observed scaling to classic objects in analytic number theory.

---

### 5.  Hypothesis – The 0.56 exponent is robust to numeric precision, variance definition, and sampling method  

**Statement**  
The exponent β ≈ 0.5633 is not an artifact of floating‑point underflow, of the particular variance estimator used, or of any sampling scheme.  It persists when the analysis is repeated with (i) arbitrary‑precision integer arithmetic, (ii) both the population variance and the unbiased sample‑variance formulas, and (iii) either full‑period enumeration or unbiased random sampling of gaps.

**Why it is testable**  
If the exponent changes appreciably under any of these variations, it would indicate sensitivity to methodological choices and would undermine confidence in the result.  Conversely, if the exponent remains within statistical error across all variations, we can be confident that the observed scaling reflects the underlying mathematical structure.

**Experiment**  

1. **Arbitrary‑precision recomputation** – Re‑calculate *R*(*k*) for *k* = 13, 14, 15 using a bignum library (e.g., GMP) with at least 200‑bit precision, guaranteeing that no underflow occurs in intermediate sums of squares.  
2. **Variance‑estimator comparison** – For the same dataset, compute the variance using (a) the population variance (∑(x‑μ)²/N) and (b) the unbiased sample variance (∑(x‑μ)²/(N‑1)).  Fit β for each estimator and compare the resulting slopes; they should agree within Monte‑Carlo error.  
3. **Sampling vs. full‑period** – For *k* = 13, 14, 15, draw independent unbiased samples of gaps (e.g., 10⁶ randomly chosen start points and record the next gap) and compute the variance‑to‑mean ratio from the sample.  Perform the same scaling analysis and see whether the estimated β matches the full‑period β.  

A combined analysis (e.g., a meta‑analysis across the three orthogonal variations) can be performed: if the pooled estimate of β remains 0.563 ± 0.005, the hypothesis is upheld; any systematic shift > 0.02 would be taken as evidence against.

---

#### Summary of Experimental Requirements

| Hypothesis | Data needed | Primary statistical tool | Success criteria |
|------------|-------------|---------------------------|------------------|
| 1 – Inclusion‑exclusion origin | Exact *R*(*k*) for *k* = 13–15 (arbitrary‑precision) | Weighted least‑squares on log‑log scale, residual analysis | βₑₘₚ − βₜₕₑₒ < 0.01, *R*² > 0.99 |
| 2 – Asymptotic stability | Same extended dataset | Overlap of 95 % CIs, Chow breakpoint test | *p* > 0.10 for a change in β after *k* = 12 |
| 3 – Random‑subset model | Monte‑Carlo simulations for *k* = 6–15 | Linear regression on simulated *R*(*k*) | β̂ₛₜₒ − β̂ₑₘₚ < 0.02 |
| 4 – Functional dependence on ζ(*k*+1) | Empirical βₑₘₚ(k) for *k* = 2–15 | Nonlinear least‑squares fit of candidate formula | *R*² > 0.95, randomly distributed residuals |
| 5 – Robustness to methodology | Three independent analyses (precision, estimator, sampling) | Meta‑analysis across variations | Pooled β = 0.563 ± 0.005, no systematic drift |

Each hypothesis is designed to be falsifiable, builds directly on the earlier findings (artifact correction, underflow warning, and the observed sub‑quadratic scaling), and uses the extended empirical data that the methodology will generate.  Together they cover the theoretical origin, the asymptotic behaviour, the predictive model, a possible explicit formula, and the critical check that the result is not a numerical artifact.