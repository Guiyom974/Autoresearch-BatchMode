# Proposed Testable Hypotheses for Primorial Gap Variance Scaling

Based on the research problem and prior findings that established (log P_k)^1.17 scaling for gap variances with floating-point precision concerns, I propose the following testable hypotheses:

---

## Hypothesis 1: Power-Law Dominance in R(k) Scaling

**Statement:** The variance-to-mean ratio R(k) follows a power-law scaling of the form R(k) ≈ A·k^β rather than logarithmic scaling, with β significantly different from zero.

**Why it's testable:** This hypothesis is testable because the prior findings (run 007 and 008) already suggest a power-law exponent of approximately 1.17 for the variance itself. If the mean scales at a different rate, R(k) should exhibit a non-zero β. The extended computations to k=14 can directly measure this exponent with higher precision.

**Experiment to test:** Implement arbitrary-precision arithmetic (to avoid the underflow issues identified in run 006) and compute R(k) for primorials P₃ through P₁₄. Fit both power-law (R(k) = A·k^β) and logarithmic (R(k) = a·log(k) + b) models using non-linear least squares. Compare using AIC/BIC with small-sample corrections (AICc). Reject the logarithmic model if the best-fit power-law has ΔAIC > 10 and β ≠ 0 within 2σ confidence.

---

## Hypothesis 2: Unified Inverse-Logarithmic Model for R(k)

**Statement:** R(k) follows an inverse-logarithmic asymptotic form R(k) ≈ c / (log k + d) + e rather than pure power-law, reflecting the known diminishing returns in prime gap distributions at large scales.

**Why it's testable:** The research problem mentions this specific functional form as a candidate model. This hypothesis is testable by direct model comparison—if the inverse-logarithmic form provides better AIC/BIC fit than pure power-law, this would support the conjecture that R(k) growth decelerates, consistent with expected properties of primorial gap statistics.

**Experiment to test:** Perform a three-way model comparison (power-law vs. logarithmic vs. inverse-logarithmic) on the extended R(k) dataset using AICc and BIC weights. Compute model probabilities P(Model | Data). If the inverse-logarithmic model achieves >95% posterior probability, accept this hypothesis. Validate by checking whether residuals show systematic structure in the power-law fit.

---

## Hypothesis 3: Critical Crossover Point for Model Divergence

**Statement:** The divergence between logarithmic and power-law models for R(k) becomes statistically distinguishable (ΔAIC > 10) at or before k=12, indicating that earlier data was already sufficient for model selection.

**Why it's testable:** This addresses the research question about when statistical divergence becomes "definitive." If the crossover occurs early, it suggests the power-law signature was present but overlooked. Retrospective analysis of existing data combined with k=13-14 validation can pinpoint when the models diverge.

**Experiment to test:** Compute R(k) for k=3 to 14 with high precision. For each consecutive k value, recalculate AIC/BIC for both models using only data up to that point. Track ΔAIC(k) as a function of k. Identify the smallest k where ΔAIC consistently exceeds 10 and verify this threshold holds for all subsequent k values.

---

## Hypothesis 4: Parameter Stability Across Data Sub-Windows

**Statement:** The fitted coefficients of the winning scaling model remain stable (within ±10% relative variation) when computed over different sub-intervals of k, confirming genuine structural trend rather than overfitting to a limited range.

**Why it's testable:** Parameter instability would indicate that the apparent trend is an artifact of the specific k-range, undermining confidence in any model selection. This is testable by jackknife-style sub-sampling, which the research problem explicitly identifies as a validation criterion.

**Experiment to test:** Divide the k-range into overlapping windows (e.g., [3,8], [5,10], [8,14], [3,14]). Fit the winning model to each window independently. Compare extracted coefficients using a bootstrap resampling procedure to estimate variance. Reject parameter stability if coefficient variation exceeds 10% across windows, triggering reconsideration of model selection.

---

## Hypothesis 5: Predictive Accuracy of Holdout Validation

**Statement:** The winning scaling model can predict R(k) for a held-out primorial (k=15) with relative error < 1%, satisfying the success criterion and confirming genuine model validity.

**Why it's testable:** Predictive validation is the strongest form of model confirmation. The hypothesis is testable by withholding P₁₅ from the fitting procedure, fitting all candidate models to k=3 through k=14, and then comparing predicted vs. actual R(15) values.

**Experiment to test:** After computing R(k) for k=3 to k=14, fit each model (logarithmic, inverse-logarithmic, power-law) and generate predictions for k=15 using extrapolation. Compute the exact gap distribution for P₁₅ (if computationally feasible given the ~10¹⁷ size constraint). Compare predictions against actual values. Accept the model only if it achieves <1% relative error AND has the best AIC/BIC score; otherwise, flag this as a model failure requiring revised hypotheses.

---

## Summary Table

| Hypothesis | Core Claim | Key Test | Expected Outcome |
|------------|-----------|----------|-------------------|
| H1 | R(k) ~ power-law (β ≠ 0) | AIC/BIC vs. log model | Reject pure log if ΔAIC > 10 |
| H2 | R(k) ~ inverse-log form | 3-way model comparison | Accept if P(model) > 95% |
| H3 | Crossover at k ≤ 12 | Sequential ΔAIC tracking | Identify first definitive k |
| H4 | Coefficient stability | Jackknife sub-sampling | Accept if CV < 10% |
| H5 | Predictive accuracy | Holdout k=15 validation | Accept if error < 1% |

These hypotheses build on the prior findings by (1) using arbitrary-precision arithmetic to address the underflow artifact, (2) testing whether the observed 1.17 exponent reflects a power-law in R(k) itself, and (3) adding robustness checks that the research problem requires for conclusive determination.