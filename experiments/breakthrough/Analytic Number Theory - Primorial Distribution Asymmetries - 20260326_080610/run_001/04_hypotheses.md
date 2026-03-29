

# Testable Hypotheses for Advanced Asymmetries and Digit Constraints in Primorial Distributions

---

## Hypothesis 1: Uniform Generalization of the LDAB Model Across Primorial Bases

**1. Hypothesis Statement:**
The Logarithmic-Density-Adjusted Benford (LDAB) model for leading digit distributions will exhibit uniform generalization across all primorial bases tested (Base-30, Base-210, Base-2310, and Base-30030), maintaining Kullback-Leibler (KL) divergence below 10⁻³ without requiring base-specific parameter calibrations.

**2. Why It's Testable:**
This hypothesis is testable because KL divergence is a well-defined, computable metric that quantifies the distance between observed leading digit distributions and theoretical LDAB predictions. The primorial bases are concrete, enumerable structures, and the hypothesis makes a specific quantitative prediction (KL < 10⁻³) that can be directly measured and either confirmed or rejected through empirical computation.

**3. Experiment to Test It:**
Implement a segmented sieve to enumerate all primes up to x = 10⁹, then compute the leading digit distribution of these primes when expressed in each primorial base (30, 210, 2310, and 30030). For each base, calculate the empirical probability distribution of leading digits and compare it against the LDAB theoretical distribution using KL divergence. The experiment should use logarithmic binning to account for the scale-invariance property of Benford's Law, and baseline results against simulated random coprime sequences to confirm deviations are prime-specific. Success would require KL divergence consistently below 10⁻³ across all four bases; failure would manifest as significant base-dependent variation requiring separate calibrations.

---

## Hypothesis 2: High-Order Corrections via Li(x) and Riemann Zeta Zeros Reduce Residual KL Divergence

**1. Hypothesis Statement:**
Replacing the implicit 1/ln(x) approximation in the LDAB model with higher-order corrections using the logarithmic integral Li(x) and explicit sums over non-trivial Riemann zeta function zeros will reduce the residual KL divergence by at least 50% compared to the standard approximation.

**2. Why It's Testable:**
This hypothesis is testable because it makes a quantitative, comparative prediction amenable to direct measurement. Both the standard 1/ln(x) approximation and the proposed Li(x) + zeta-zero corrections are mathematically well-defined and computationally tractable. The 50% reduction threshold provides an objective success criterion that can be evaluated through empirical computation of KL divergence under both models.

**3. Experiment to Test It:**
First, establish baseline KL divergences using the standard 1/ln(x) approximation for primorial base leading digit distributions. Second, implement the Li(x) correction by replacing π(x) ≈ x/ln(x) with π(x) ≈ Li(x) in the LDAB density calculations. Third, incorporate explicit sums over the first 10,000 non-trivial Riemann zeta zeros (ρ = ½ + iγₙ) using the explicit formula for prime counts. Compute new KL divergences under these refined models and perform pairwise comparisons against baseline values. The experiment should be conducted across multiple primorial bases and x-bounds to ensure robustness. Statistical significance should be assessed using bootstrap resampling with 1000 replicates to generate confidence intervals for the KL divergence reductions.

---

## Hypothesis 3: Chebyshev Bias Scales Proportionally to log log x for Higher Primorials

**1. Hypothesis Statement:**
The normalized bias magnitude between quadratic non-residue (NR) and quadratic residue (QR) prime counts for primorial moduli P₆ = 30030, P₇ = 510510, and P₈ = 9699690 will scale proportionally to log log x, consistent with Rubinstein-Sarnak predictions, for bounds ranging from 10⁶ to 10⁹.

**2. Why It's Testable:**
This hypothesis is testable because the Rubinstein-Sarnak framework provides explicit theoretical predictions about the scaling behavior of Chebyshev bias. The log log x proportionality is a concrete mathematical relationship that can be verified through linear regression of empirical bias magnitudes against log log x values. The primorial moduli specified are computationally accessible, and the scaling prediction can be confirmed or refuted through systematic empirical measurement.

**3. Experiment to Test It:**
Implement an optimized segmented sieve to enumerate primes up to 10⁹ while maintaining cumulative counts for each coprime residue class modulo P₆, P₇, and P₈. Compute the normalized bias function δ(x; q) = (π_{NR}(x) - π_{QR}(x)) / (Li(x)/φ(q)) at logarithmically spaced x-values from 10⁶ to 10⁹. Fit the empirical bias magnitudes to a linear model of the form δ(x) = A·log log x + B using weighted least squares regression, where weights account for heteroscedasticity in the estimates. Test the goodness-of-fit using an F-test against a null model with no log log x dependence, requiring p < 0.01 for confirmation. Additionally, compare the fitted coefficients A against theoretical predictions from the Rubinstein-Sarnak framework using the relevant Dirichlet L-function values.

---

## Hypothesis 4: Machine Learning Classifiers Can Reliably Predict Prime Race Regime Shifts

**1. Hypothesis Statement:**
A machine learning classifier trained on historical prime race time-series data will achieve classification accuracy significantly above chance (>75%) in predicting upcoming regime shifts (changes in the leading residue class) for prime races modulo primorials up to P₆ = 30030, using features derived from cumulative count trajectories and their derivatives.

**2. Why It's Testable:**
This hypothesis is testable because regime shifts are binary events (the leading residue class either changes or does not) that can be labeled from historical data, making this a supervised classification problem with objectively measurable outcomes. The 75% accuracy threshold represents a meaningful departure from random guessing (50% for binary classification) and is computationally verifiable using standard machine learning evaluation metrics.

**3. Experiment to Test It:**
Construct a time-series dataset of prime race dynamics by computing cumulative prime counts for competing residue classes at fine-grained intervals (e.g., every 10⁵ primes) from x = 10⁶ to 10⁹. Engineer features from these trajectories including: (a) the current lead margin between classes, (b) the first and second derivatives of the lead margin, (c) rolling statistics over windows of 100 and 1000 observations, and (d) cross-correlation features with known oscillatory modes. Train a Long Short-Term Memory (LSTM) recurrent neural network to predict whether a regime shift will occur within the next 10,000 primes. Evaluate classifier performance using a rolling window validation scheme with 80% training, 10% validation, and 10% holdout testing. Compare LSTM performance against baseline classifiers (logistic regression, random forest) and against a theoretical probabilistic model derived from the Rubinstein-Sarnak bias framework.

---

## Hypothesis 5: Primorial Moduli Size Affects the Rate of Convergence to Dirichlet Equidistribution

**1. Hypothesis Statement:**
The rate at which the empirical distribution of primes across coprime residue classes converges to the Dirichlet uniform distribution (1/φ(n)) will be inversely related to the size of the primorial modulus, with larger primorial bases exhibiting systematically slower convergence rates as measured by the total variation distance, after controlling for sample size.

**2. Why It's Testable:**
This hypothesis is testable because total variation distance is a well-defined metric for measuring convergence to equidistribution, and the relationship between modulus size and convergence rate makes a specific directional prediction that can be empirically verified. The experiment can directly measure how quickly (or slowly) empirical distributions approach the theoretical uniform distribution for moduli of increasing size.

**3. Experiment to Test It:**
For each primorial modulus P_k in {30, 210, 2310, 30030}, compute the empirical prime distribution across all φ(P_k) coprime residue classes at x-values spanning from 10⁵ to 10⁹ (logarithmically spaced). Calculate the total variation distance D_TV(x, P_k) = (1/2) Σ |π(p; r) - π(x)/φ(P_k)| at each x-value, where π(p; r) is the count of primes ≡ r mod P_k. Fit exponential decay models of the form D_TV(x) ~ C·x^(-α) to each primorial series using non-linear least squares. Compare the fitted decay exponents α across moduli to test whether larger primorials exhibit smaller α (slower convergence). Use Akaike Information Criterion (AIC) to evaluate whether a model with modulus-dependent α provides significantly better fit than a common α. Monte Carlo simulations with random coprime sequences of equivalent size should serve as null baselines to confirm observed convergence patterns are prime-specific.

---

## Summary Table of Hypotheses

| Hypothesis | Independent Variable | Dependent Variable | Predicted Relationship |
|------------|---------------------|-------------------|------------------------|
| 1: LDAB Uniformity | Primorial base (30, 210, 2310, 30030) | KL divergence | Constant (< 10⁻³) across bases |
| 2: Li(x) Corrections | Correction method (1/ln vs Li + ζ-zeros) | Residual KL divergence | 50% reduction with refined model |
| 3: Bias Scaling | log log x | Normalized NR vs QR bias | Linear proportionality |
| 4: ML Regime Prediction | Feature set from time-series | Classification accuracy | >75% accuracy for regime shifts |
| 5: Convergence Rates | Primorial modulus size | Total variation distance | Inverse relationship (slower for larger moduli) |