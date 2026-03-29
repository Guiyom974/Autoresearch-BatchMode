**Hypotheses – High‑Precision Primorial‑Gap Validation at \(k\ge 8\)**  

Below are five concrete, testable propositions that (i) extend the insight gained from the earlier \(k=3\!-\!7\) runs, (ii) address the three core research questions (implementation, theoretical alignment, statistical baselines), and (iii) can be examined with the planned arbitrary‑precision pipeline.  Each hypothesis is stated, the reason it is testable is given, and a specific computational experiment that would evaluate it is described.

---

### H 1 – **The arbitrary‑precision engine will produce *exact* primorial‑gap sequences for \(k=8\) without integer overflow and the resulting mean and variance will match the theoretical expectations for primorial gaps.**

**Why it is testable**  
*What we can measure*: After the pipeline finishes we can read off the exact integer gaps, compute the sample mean \(\bar g\) and sample variance \(s_g^2\) (using arbitrary‑precision rational arithmetic), and compare them with the known theoretical values for a primorial of index 8 (e.g. \(\mathbb{E}[g]=\log p_k\#\) and the variance predicted by the higher‑order log‑correction model). Because the arithmetic is exact, any deviation must be a genuine discrepancy, not a rounding artefact.

**Experiment**  
1. Implement the pipeline in Python with `gmpy2` (or wrap GMP) and generate the full set of primes ≤ \(p_8\# = 9 699 690\).  
2. Form the ordered list of gaps \(\{g_i\}\) between consecutive primes that are coprime to the primorial base.  
3. Using arbitrary‑precision integers, compute  
   \[
   \bar g = \frac{1}{N}\sum_i g_i,\qquad 
   s_g^2 = \frac{1}{N-1}\sum_i (g_i-\bar g)^2 .
   \]  
4. Evaluate the theoretical predictions (e.g. \(\log p_8\#\) for the mean and the higher‑order log‑correction formula for the variance) with the same precision.  
5. Test equality with a high‑precision two‑tailed t‑test (or a difference test in exact rational arithmetic).  Success is declared when the observed values lie within one ulp of the theory.

---

### H 2 – **The variance of primorial gaps continues to scale *sub‑quadratically* with the mean for \(k\ge 8\); i.e. \(\operatorname{Var}(g) \propto \mu(g)^{\alpha}\) with \(\alpha<2\).**

**Why it is testable**  
We can estimate the scaling exponent \(\alpha\) from the empirical mean‑variance pairs for \(k=6,7,8\) and test whether the confidence interval for \(\alpha\) lies below 2.  The earlier runs (k = 3‑7) already suggested \(\alpha\approx1.7\); we now ask whether the same pattern persists at the next primorial level.

**Experiment**  
1. For each of \(k=6,7,8\) compute the sample mean \(\mu_k\) and variance \(\sigma^2_k\) of the gap sequence (as in H 1).  
2. Fit the model \(\log\sigma^2_k = \log C + \alpha\log\mu_k\) by ordinary least‑squares (or by non‑linear regression) and obtain the 95 % confidence interval for \(\alpha\).  
3. Perform a one‑sided hypothesis test: \(H_0:\alpha\ge 2\) versus \(H_a:\alpha<2\).  Reject \(H_0\) (and accept H 2) if the upper bound of the CI is < 2.

---

### H 3 – **The variance‑to‑mean ratio (VMR) at \(k=8\) is better described by a *second‑order log‑correction* model (e.g. \(\mathrm{VMR}= \tfrac13 - \tfrac{C}{\log p_k\#} + \tfrac{D}{(\log p_k\#)^2}\)) than by the simple first‑order model \(\mathrm{VMR}= \tfrac13 - \tfrac{C}{\log p_k\#}\).**

**Why it is testable**  
Both models can be fitted to the observed VMRs for \(k=6,7,8\); the relative goodness‑of‑fit can be quantified with information criteria or a likelihood‑ratio test.  The prior run showed that the first‑order prediction under‑estimates the empirical VMR at \(k=8\), hinting at a missing higher‑order term.

**Experiment**  
1. Compute the empirical VMR for \(k=6,7,8\): \(R_k = \sigma^2_k/\mu_k\).  
2. For each \(k\) evaluate the two candidate formulas, tuning the constants \(C\) (and \(D\) for the second model) by nonlinear least‑squares to minimise the squared error \(\sum_k (R_k^{\text{obs}}-R_k^{\text{pred}})^2\).  
3. Compare the models via AIC (or BIC).  The second‑order model is preferred if its ΔAIC > 2 and it yields smaller prediction error on a hold‑out \(k=9\) test (if computationally feasible).  

---

### H 4 – **Applying a *symmetric windowing* scheme to the \(k=8\) primorial interval will eliminate the systematic VMR variation caused by boundary truncation that was observed at lower \(k\).**

**Why it is testable**  
We can deliberately cut off a fraction of the interval at both ends (the “truncation level”) and monitor how the resulting VMR changes.  If the VMR becomes independent of the truncation level when a symmetric window is used, the hypothesis is supported.

**Experiment**  
1. Generate the full gap list for \(k=8\).  
2. For truncation levels \(\tau = 0.05,0.10,\dots,0.45\) (i.e. discard the first and last \(\tau\) fraction of the interval), compute the VMR of the remaining *inner* gaps.  
3. Perform a linear‑trend test (or a simple ANOVA) across the series of VMR(\(\tau\)).  Accept H 4 if the slope is not significantly different from zero (e.g. p > 0.05).  

---

### H 5 – **The *streaming‑chunk* implementation will produce gap‑statistics (mean, variance, VMR) that are statistically indistinguishable from those obtained by a full in‑memory computation, demonstrating that the pipeline scales within typical RAM limits.**

**Why it is testable**  
We can run the pipeline twice: once loading the entire gap list into RAM (if memory permits) and once processing the data in overlapped memory‑mapped chunks.  The resulting statistics can be compared with an equivalence test.

**Experiment**  
1. For \(k=8\) (or the largest \(k\) that fits in RAM) execute the pipeline in “batch” mode, storing the complete gap array.  Record \(\bar g_{\text{batch}}, s^{2}_{\text{batch}}, R_{\text{batch}}\).  
2. Re‑run the same computation using a memory‑mapped, chunk‑wise iterator that never holds more than a preset chunk size (e.g. 10⁶ gaps).  Obtain \(\bar g_{\text{stream}}, s^{2}_{\text{stream}}, R_{\text{stream}}\).  
3. Apply a two‑sample Kolmogorov–Smirnov test (or a paired‑difference test with a pre‑specified equivalence margin \(\Delta\)) to each statistic.  Declare success if the null hypothesis of a meaningful difference is rejected at the 0.05 level, i.e. the statistics fall within the predetermined equivalence region.  

---

#### How these hypotheses build on prior findings  

| Prior observation | New hypothesis | Extension |
|-------------------|----------------|-----------|
| Sub‑quadratic variance scaling (k = 3‑7) | H 2 | Tests whether the same exponent holds at the next primorial index (k ≥ 8). |
| Simple log‑correction under‑estimates VMR at k = 8 | H 3 | Proposes a richer model and validates it with the high‑precision data. |
| Boundary truncation distorts VMR | H 4 | Verifies that symmetric windowing removes the bias at the new, larger primorial bound. |
| Need for scalable, overflow‑free arithmetic | H 1 & H 5 | Demonstrate exact, memory‑efficient computation for the full k = 8 interval. |

Together, these five hypotheses constitute a coherent research agenda: (i) **prove the computational tool works**, (ii) **confirm the statistical patterns seen at lower k persist**, (iii) **refine the theoretical description of the VMR**, and (iv) **validate the mitigation of known systematic errors**.  All are directly testable with the planned arbitrary‑precision pipeline and standard statistical methodology.