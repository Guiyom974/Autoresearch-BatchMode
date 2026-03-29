
Below are **five concrete, testable hypotheses** that extend the work that has already cleared the methodological artefacts for the small‑\(k\) regime.  Each hypothesis is written as a **statement**, followed by a short justification of why it can be examined with the planned arbitrary‑precision, distributed‑computing pipeline, and by a concise **experimental design** that would produce a definitive pass/fail verdict.

---

## 1.  **H‑1 – Stability of the VMR scaling exponent**

**Statement**  
For primorial bases \(k\ge 9\) the variance‑to‑mean ratio (VMR) of the gaps continues to obey a power‑law in the index \(k\)

\[
\operatorname{VMR}(k)=A\;k^{\gamma}+o(k^{\gamma})\qquad\text{with }\gamma\approx0.63,
\]

i.e. the exponent that was fitted for \(k\le 8\) remains the same for the much larger bases \(P_{9}\) and \(P_{10}\).

**Why it is testable**  
The pipeline that will be built for \(P_{9}\) (≈ 2.23 × 10⁸) and \(P_{10}\) (≈ 6.47 × 10⁹) can compute *exact* gap counts and all required moments using arbitrary‑precision integers.  Because the artefact that previously suppressed variance has been identified and corrected, any systematic change in the exponent will be visible in the new data.

**Experiment that tests it**  

1. **Compute VMR for \(k=9\) and \(k=10\).**  
   - Run the chunked, MPI‑parallel sieve, accumulating in Python’s `int` (or GMP) the three quantities  
     \[
     N_k=\#\{\text{gaps}\},\qquad
     S_k=\sum g_i,\qquad
     Q_k=\sum g_i^{2},
     \]  
     where \(g_i\) is the length of the \(i\)-th gap.  
   - Form the mean \(\mu_k=S_k/N_k\) and the variance \(\sigma^2_k=(Q_k/N_k)-\mu_k^{2}\).  
   - Compute \(\operatorname{VMR}(k)=\sigma^2_k/\mu_k\).

2. **Fit a log‑log linear model**  
   \[
   \ln\operatorname{VMR}(k)=\ln A+\gamma\ln k+\varepsilon_k .
   \]  
   Use ordinary least squares on the points \((k,\operatorname{VMR}(k))\) for \(k=1,\dots,10\) (including the already‑available values for \(k\le8\)).  

3. **Statistical test**  
   - Compute the 95 % confidence interval for \(\hat\gamma\).  
   - If the interval contains 0.63, accept the hypothesis; if it lies entirely outside (e.g. entirely below 0.55 or above 0.70), reject it.  

A *positive* outcome (γ≈0.63) would confirm that the sub‑linear scaling discovered for small \(k\) is a genuine asymptotic property of primorial gaps.

---

## 2.  **H‑2 – Change‑point in the VMR scaling at the \(k\ge 9\) threshold**

**Statement**  
The VMR for \(k\ge 9\) follows a **different** power‑law exponent, either flattening (\(\gamma<\!0.63\)) or accelerating (\(\gamma>\!0.63\)).  This would indicate that the regime observed for \(k\le 8\) is only a transient phenomenon.

**Why it is testable**  
The same exact VMR values obtained for \(k=9\) and \(k=10\) can be compared with the extrapolation based on the fitted \(\gamma\) from the lower‑\(k\) data.  A statistically significant deviation will be detectable because the new points will have very small relative numerical error (thanks to arbitrary‑precision accumulators).

**Experiment that tests it**  

1. **Predict VMR for \(k=9,10\)** using the model fitted on \(k\le 8\):
   \[
   \widehat{\operatorname{VMR}}(9)=A\;9^{0.63},\qquad 
   \widehat{\operatorname{VMR}}(10)=A\;10^{0.63}.
   \]

2. **Compute the observed/expected ratio**  
   \[
   R_k=\frac{\operatorname{VMR}_{\text{obs}}(k)}{\widehat{\operatorname{VMR}}(k)}.
   \]  

3. **Hypothesis test**  
   - Under the null hypothesis \(R_k\approx1\) with sampling variability estimated from the bootstrap of the original eight‑point fit.  
   - If \(|R_9-1|\) or \(|R_{10}-1|\) exceeds the 95 % bootstrap quantile, reject the “no‑change” null and accept that a genuine change‑point has occurred.

A *negative* outcome (i.e. no significant deviation) would reinforce H‑1, while a *positive* outcome would require a reformulation of the scaling law.

---

## 3.  **H‑3 – Analytically‑derived upper bound on the variance of primorial gaps**

**Statement**  
Using standard combinatorial‑sieve techniques (e.g., the Selberg upper‑sieve applied to the set \(\{n\le x:\gcd(n,P_k)=1\}\)) one can prove

\[
\operatorname{Var}(G_k)\;<\;C\;\bigl(\log P_k\bigr)^{\delta}\qquad\text{with }\delta\approx2\gamma\approx1.27,
\]

where \(G_k\) denotes a random primorial gap for base \(P_k\) and \(C\) is an absolute, explicit constant.

**Why it is testable**  
The bound is a *deterministic* inequality that can be evaluated for each \(k\) once \(\operatorname{Var}(G_k)\) is known from the exact computation.  The bound is tight enough to be violated only if the true variance grows faster than the predicted order.

**Experiment that tests it**  

1. **Derive the constant \(C\)** from the sieve calculation (the derivation will be part of the theoretical deliverable).  

2. **Compute the empirical variance** \(\widehat{\operatorname{Var}}(G_k)\) for \(k=9,10\) (as described in H‑1).  

3. **Check the inequality**  
   \[
   \frac{\widehat{\operatorname{Var}}(G_k)}{(\log P_k)^{\delta}} \;<\; C\;?
   \]  

   - If the inequality holds for both \(k=9\) and \(k=10\), the bound is validated across the new regime.  
   - If it is violated, the bound must be strengthened (increase \(C\) or \(\delta\)).

Because the bound is *asymptotic*, a single violation for \(k=10\) would be strong evidence that the conjectured exponent \(\delta\) is too low.

---

## 4.  **H‑4 – Alignment of the large‑gap tail with an extreme‑value law**

**Statement**  
For the large‑gap tail (e.g., gaps exceeding the 95th percentile) the exceedance probabilities for \(P_{9}\) and \(P_{10}\) follow a Gumbel distribution (or, more generally, a Generalized Extreme Value distribution with shape parameter \(\xi=0\)).  This would corroborate the heuristic that the tail is governed by the same logarithmic fluctuations that underlie the sieve‑theoretic bounds.

**Why it is testable**  
The exact gap list for each primorial yields a full empirical distribution, allowing a tail‑fit without resorting to approximations.  The Gumbel hypothesis can be assessed with standard goodness‑of‑fit tests.

**Experiment that tests it**  

1. **Extract the upper tail** – for each primorial, collect all gaps \(g_i\) that exceed the 95 % quantile \(q_{0.95}\).  

2. **Standardize** the exceedances:  
   \[
   u_i = \frac{g_i - \mu_{k}^{\text{tail}}}{\sigma_{k}^{\text{tail}}},
   \]  
   where \(\mu_{k}^{\text{tail}}\) and \(\sigma_{k}^{\text{tail}}\) are the mean and standard deviation of the tail sample.  

3. **Fit a Gumbel distribution** (or a GEV with \(\xi\) estimated) to the set \(\{u_i\}\).  

4. **Goodness‑of‑fit** – perform a Kolmogorov‑Smirnov test (or an Anderson‑Darling test) at the 5 % level.  

   - *Pass*: the p‑value > 0.05 → the tail is consistent with the extreme‑value law.  
   - *Fail*: p‑value ≤ 0.05 → reject the Gumbel hypothesis, indicating that the tail evolves differently than predicted.

Repeating the test for both \(k=9\) and \(k=10\) will show whether the law is stable across the new scale.

---

## 5.  **H‑5 – Convergence of the successive‑VMR growth factor to unity**

**Statement**  
Define the growth factor  

\[
\phi_k \;=\; \frac{\operatorname{VMR}(k)}{\operatorname{VMR}(k-1)}\qquad(k\ge2).
\]

As \(k\) becomes large, \(\phi_k\) approaches 1, reflecting a *steady* sub‑linear increase rather than a runaway or damped one.  In other words, the VMR is asymptotically “log‑linear’’ in \(k\).

**Why it is testable**  
Because we will have exact VMR values for a range of \(k\) (up to 10), we can compute the sequence \(\{\phi_k\}\) and examine its trend.  The hypothesis is a simple statement about the limit of a bounded monotone sequence, which can be examined statistically.

**Experiment that tests it**  

1. **Compute \(\phi_k\) for \(k=2,\dots,10\)** using the VMRs obtained in H‑1.  

2. **Fit a decay model**  
   \[
   \phi_k = 1 + a\,k^{-b} + \eta_k,
   \]  
   where \(a,b>0\) and \(\eta_k\) is zero‑mean noise.  

3. **Test for convergence**  

   - Estimate \(b\) via nonlinear least squares.  If the 95 % confidence interval for \(b\) excludes 0 (i.e. \(b>0\)), the model supports the claim that \(\phi_k\to1\).  
   - Additionally, perform a runs‑test on the residuals \(\{\phi_k-1\}\) to verify that there is no systematic drift.

A *positive* result would give a complementary view of the asymptotic behaviour that is independent of the exact exponent \(\gamma\).

---

### How these hypotheses together answer the research problem

| Hypothesis | What it probes | What a positive result would imply |
|------------|----------------|-----------------------------------|
| **H‑1** | Stability of the γ≈0.63 exponent | The scaling law discovered for \(k\le8\) holds for the much larger bases → the exponent is a genuine asymptotic property. |
| **H‑2** | Possible change of exponent at higher \(k\) | If H‑2 is preferred, the earlier exponent is a transient; a new (higher or lower) exponent must be incorporated into the final model. |
| **H‑3** | Theoretical upper bound on variance | Demonstrates that sieve‑theoretic reasoning can reproduce the observed sub‑linear growth, providing a rigorous analytical foundation. |
| **H‑4** | Tail‑distribution behaviour | Confirms (or refutes) that the extreme‑value intuition behind the analytical bounds is correct for the new scales. |
| **H‑5** | Convergence of successive VMR ratios | Gives a second, complementary perspective on the asymptotic stability of the scaling. |

All five hypotheses can be evaluated **simultaneously** with the same high‑precision dataset that the pipeline for \(P_{9}\) and \(P_{10}\) will produce, thereby delivering the three‑fold success criteria (computational exactness, analytical bounds, and a conclusive determination of the scaling exponent).  

---  

**Bottom line:** The next round of exact computations will either **reinforce** the γ≈0.63 law (H‑1, H‑3, H‑4, H‑5) or **reveal a departure** from it (H‑2).  Either outcome advances the research from “incremental observation’’ to a rigorous, data‑validated theory of primorial‑gap variance.