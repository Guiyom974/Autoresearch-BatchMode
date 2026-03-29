# Testable Hypotheses for Primorial Gap Variance Asymptotic Scaling

Based on the research problem and prior findings indicating that boundary artifacts in base-210 can be effectively mitigated, I propose the following testable hypotheses:

---

## Hypothesis 1: Boundary-Corrected Variance Will Reveal Clearer Model Separation

**Statement:** The boundary-corrected variance estimator will produce a ΔAIC and ΔBIC greater than 2.0 between the best-fitting and second-best model for the existing k ≤ 15 data, indicating that the current near-tie (ΔAIC = 0.0303) was an artifact of boundary truncation effects rather than genuine model equivalence.

**Why it's testable:** This hypothesis is directly testable by applying the boundary correction methodology to the already-computed R(k) values for k ≤ 15 and re-running the model comparison without requiring new primorial computations.

**Experiment to test it:**
1. Implement the boundary-corrected variance estimator that excludes or down-weights gaps within ε·P_k of interval boundaries (where ε is a tunable parameter)
2. Recompute R(k) for k = 1 through 15 using this corrected estimator
3. Fit logarithmic, power-law, and stretched exponential models to the corrected data
4. Calculate AIC, BIC, and LOOCV metrics for each model
5. Compare ΔAIC and ΔBIC to the success criterion of >2.0

---

## Hypothesis 2: Parameter Stability After Boundary Correction

**Statement:** The power-law exponent α in R(k) ~ k^α will demonstrate greater parameter stability (reduced variance in α estimates) when comparing fits from k ≤ 15 versus k ≤ 18 after boundary correction, compared to the uncorrected estimates.

**Why it's testable:** Parameter stability is quantifiable through standard errors of fitted parameters and confidence interval widths, providing a direct statistical measure.

**Experiment to test it:**
1. Fit power-law models to boundary-corrected R(k) data for two ranges: (a) k = 5 to 15, and (b) k = 5 to 18
2. Compare the fitted exponent values and their standard errors between the two ranges
3. Test whether the exponents are statistically indistinguishable (within 2 standard errors) between the two ranges
4. Contrast these results with the same analysis performed on uncorrected data to demonstrate improvement

---

## Hypothesis 3: Randomized Sampling Will Preserve Model Discrimination

**Statement:** Gap samples obtained via randomized sampling from P₁₆ and P₁₇ intervals will produce boundary-corrected R(k) estimates that maintain the same model ranking (relative ordering of AIC/BIC scores) as would be obtained from full enumeration, with sampling variance controllable to within ±0.1 ΔAIC units at 95% confidence.

**Why it's testable:** This hypothesis addresses the computational constraint by proposing a method; its validity can be tested through replication with varying sample sizes.

**Experiment to test it:**
1. Implement a randomized gap-sampling algorithm that:
   - Selects N random positions within P₁₆
   - Identifies all gaps centered within a window of size W around each position
   - Records gap lengths and their positions relative to interval boundaries
2. Apply boundary correction using only gaps with positions > ε·P₁₆ from boundaries
3. Estimate R(16) from this sample; repeat M = 100 times with different random seeds
4. Compute mean and standard deviation of R(16) estimates
5. Compare the model fit ranking from sampled estimates to theoretical predictions
6. Increase N until the standard error of R(16) falls below a threshold that permits reliable model discrimination

---

## Hypothesis 4: Stretched Exponential Emergence Hypothesis

**Statement:** For k > 15, after boundary correction, the stretched exponential model will become statistically favored over the power-law model, indicating that the LOOCV preference observed in prior analysis reflected genuine asymptotic behavior rather than overfitting to boundary-contaminated data.

**Why it's testable:** This is the core asymptotic question; if boundary correction eliminates the near-tie at k ≤ 15, the extension to higher k provides a clear test.

**Experiment to test it:**
1. Obtain boundary-corrected R(k) for k = 16, 17, and 18 using the validated sampling approach from Hypothesis 3
2. Fit all three models (logarithmic, power-law, stretched exponential) to the extended dataset
3. Calculate ΔAIC and ΔBIC for each model pair
4. If stretched exponential emerges as preferred (ΔAIC > 2.0), test whether the fitted stretch parameter β remains stable when comparing fits from k ≤ 15 to k ≤ 18
5. Use Bayesian model averaging if no single model achieves clear preference to quantify relative model probabilities

---

## Hypothesis 5: Quantified Truncation Error Bounds

**Statement:** The deviation between naive full-interval variance and boundary-corrected variance follows a systematic scaling law proportional to (1/P_k)^γ for some exponent γ > 0, allowing extrapolation of correction magnitudes for future primorial indices without full recomputation.

**Why it's testable:** The relationship between interval size and correction magnitude can be fitted empirically and tested through goodness-of-fit metrics.

**Experiment to test it:**
1. For each k from 1 to 15, compute both naive and boundary-corrected variance estimates
2. Calculate the relative deviation: δ(k) = |R_naive(k) - R_corrected(k)| / R_corrected(k)
3. Fit the relationship δ(k) ~ (1/P_k)^γ using nonlinear regression
4. Test the goodness-of-fit of this scaling law using R² and residual analysis
5. Validate by comparing predicted correction magnitude for k = 16 against actual sampled correction (from Hypothesis 3)
6. If validated, use the scaling law to estimate computational requirements for future k values

---

## Integration with Prior Findings

These hypotheses build directly on the breakthrough finding that boundary artifacts in base-210 were mitigated (KL divergence reduced from 0.622 to 0.000354) by:

- Extending the calibration framework from distribution matching (KL divergence) to variance estimation
- Addressing the instability noted in high-order primorial bases by applying systematic boundary corrections
- Moving beyond the failed variance reduction attempts by focusing on correction rather than artificial reduction