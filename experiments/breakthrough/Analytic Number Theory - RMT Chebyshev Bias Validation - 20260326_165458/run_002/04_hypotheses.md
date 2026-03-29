# Testable Hypotheses for RMT Covariance Model Recalibration

Based on the research problem and search context, I propose the following five testable hypotheses:

---

## Hypothesis 1: Low-Lying Zeros of Dirichlet L-Functions Cause Systematic Variance Underestimation

**Statement:** The massive variance discrepancy (28,268% relative error) in RMT covariance predictions for Chebyshev bias at modulus 210 arises from contributions of low-lying zeros (height < 50) of specific Dirichlet L-functions associated with characters modulo 210 that are systematically excluded from asymptotic RMT averaging.

**Why it's testable:** This hypothesis generates a specific, falsifiable prediction: when explicit low-lying zeros are incorporated into the covariance calculation via a truncated Explicit Formula, the predicted variance should increase from ~1.39 toward the empirical ~394.3. The contribution of each L-function's low zeros can be computed independently and summed.

**Experiment to test it:**
1. Compute the first 1,000 non-trivial zeros for all φ(210) = 48 Dirichlet L-functions modulo 210
2. For each L-function, calculate the contribution to the variance using the Explicit Formula truncated at the first N zeros (test N = 10, 50, 100, 500, 1000)
3. Sum these contributions and compare to the empirical variance of Chebyshev bias observed for primes up to 10⁹
4. Identify the minimum number of low zeros required to achieve ±10% relative error

---

## Hypothesis 2: Constructive Interference from Cross-Class Correlations Amplifies Variance

**Statement:** The standard RMT covariance model fails because it assumes independent zero spectra across prime character classes. However, for highly composite moduli like 210, quadratic residues and non-residues exhibit positive cross-correlation at low heights, causing constructive interference that amplifies variance by approximately 2-3 orders of magnitude beyond what independent-spectra RMT predicts.

**Why it's testable:** Cross-correlation coefficients between zero spectra can be computed explicitly using the first 1,000 zeros. If the hypothesis is correct, the empirical cross-correlation will be significantly positive (r > 0.3) for heights below a critical threshold, and the variance amplification factor will correlate with this cross-correlation strength.

**Experiment to test it:**
1. Construct empirical covariance matrices from explicit zeros for: (a) quadratic residues mod 210, (b) non-residues mod 210, (c) mixed cross-correlations
2. Compute Pearson correlation coefficients between zero height distributions for each character pair
3. Compare the eigenvalue spectra of the empirical covariance matrix against:
   - Standard RMT predictions (Wishart/Marčenko-Pastur)
   - Independent-block diagonal model (assuming zero cross-correlation)
4. Test whether variance amplification scales with the measured cross-correlation magnitude

---

## Hypothesis 3: The Variance Failure is Modulus-Dependent and Scales with Number of Distinct Prime Factors

**Statement:** The variance underestimation is not intrinsic to RMT but rather a function of the primorial's factorization structure. The ratio of empirical-to-predicted variance should increase monotonically with the number of distinct prime factors in the modulus, because each additional prime introduces new low-lying zeros that violate the RMT bulk-smoothing assumption.

**Why it's testable:** This hypothesis generates a clear comparative prediction: moduli with more prime factors (e.g., 2310 = 2×3×5×7×11) should exhibit larger variance discrepancies than moduli with fewer factors (e.g., 30 = 2×3×5), following a predictable scaling law.

**Experiment to test it:**
1. Compute empirical variance of Chebyshev bias for moduli: 6 (2×3), 30 (2×3×5), 210 (2×3×5×7), 2310 (2×3×5×7×11)
2. Compute theoretical RMT-predicted variance for each modulus using standard asymptotic formulas
3. Calculate the empirical-to-predicted variance ratio for each modulus
4. Fit a regression model: log(Variance Ratio) ~ f(number of distinct primes, discriminant size)
5. Test whether the fitted scaling function is statistically significant (p < 0.05) and achieves R² > 0.85

---

## Hypothesis 4: A Hybrid RMT-Explicit Model Can Achieve ±10% Variance Accuracy Without Degrading Mahalanobis Distance Performance

**Statement:** A covariance model that uses standard RMT asymptotics for zeros above a height threshold H_crit but exact Explicit Formula contributions for zeros below H_crit will simultaneously: (a) reduce variance prediction error from >28,000% to within ±10%, and (b) maintain or improve the existing Mahalanobis distance accuracy (currently 9.28%).

**Why it's testable:** This hypothesis specifies a concrete model architecture and dual success criteria. The model can be constructed, tested, and either validated or falsified based on whether both conditions are simultaneously satisfied. The critical height H_crit can be determined empirically by grid search.

**Experiment to test it:**
1. Implement the Hybrid RMT-Explicit covariance model with H_crit as a tunable parameter (test H_crit = 10, 25, 50, 100, 200)
2. For each H_crit value:
   - Compute the covariance matrix using explicit zeros below H_crit and RMT asymptotics above
   - Calculate predicted variance and compare to empirical variance
   - Calculate Mahalanobis distance error on the test dataset
3. Identify the optimal H_crit that minimizes total error: minimize |Variance Error| + |Mahalanobis Error| subject to both < 10%
4. Validate the optimal model on held-out prime data segments

---

## Hypothesis 5: The Log-Log Growth Anomaly (R² = 0.623) is a Consequence of Incorrect Variance Scaling, Not a Fundamental Bias Growth Phenomenon

**Statement:** The poor log-log fit (R² = 0.623) for Chebyshev bias magnitude growth is an artifact of incorrect variance normalization in the regression model, not evidence of non-power-law bias behavior. Correcting the variance scaling to the empirical ~394.3 (for mod 210) will improve the log-log R² to >0.90, consistent with power-law growth predicted by number theory.

**Why it's testable:** This is a classic specification error hypothesis. If the log-log regression is re-run with correctly scaled variance, the R² should increase dramatically. This can be tested by:
1. Standardizing the bias variable using the corrected variance estimate
2. Re-fitting the log-log linear regression
3. Comparing R² values using F-test for nested models

**Experiment to test it:**
1. Compute empirical Chebyshev bias values B(p) for all primes p ≤ 10⁹ grouped by modulus class
2. Fit baseline log-log regression: log|B(p)| ~ log(p) + log(σ_predicted) using the incorrect RMT variance (σ_predicted ≈ 1.39)
3. Re-fit corrected regression: log|B(p)/σ_corrected| ~ log(p) using the empirical variance (σ_corrected ≈ 19.86 for mod 210)
4. Compare R² values using ANOVA F-test for nested regressions
5. Test whether the corrected model's residuals exhibit homoscedasticity (Breusch-Pagan test), confirming proper variance normalization

---

## Summary Table

| Hypothesis | Primary Variable | Expected Effect | Test Statistic |
|------------|------------------|-----------------|----------------|
| H1 | Low-lying zeros (N < 100) | Variance ↑ by ~280× | |Variance Error| < 10% |
| H2 | Cross-class correlation | Variance amplification factor ~283× | r > 0.3 at low heights |
| H3 | Number of prime factors | Variance ratio scales with ω(n) | R² > 0.85 |
| H4 | Hybrid model with H_crit | Dual optimization success | Both errors < 10% |
| H5 | Corrected variance normalization | R² increases to >0.90 | F-test p < 0.001 |

These hypotheses are designed to be mutually complementary—H1 and H2 identify the *source* of the discrepancy, H3 establishes its *generality*, H4 provides a *solution*, and H5 confirms the *consequence* of the fix.