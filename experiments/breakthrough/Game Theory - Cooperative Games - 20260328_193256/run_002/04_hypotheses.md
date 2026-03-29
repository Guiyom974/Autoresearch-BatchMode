# Proposed Testable Hypotheses for Shapley Value Distribution Analysis

Based on the research problem, prior findings (which revealed a need for robust non-Dirichlet weight generation after a failed baseline verification attempt), and web search results on weighted Shapley values, I propose the following 5 testable hypotheses:

---

## Hypothesis 1: Pareto Weight Distributions Cause Measurable Deviations from Dirichlet(1)

**Statement**: When player weights are drawn from Pareto distributions with shape parameter α < 3, the resulting Shapley value distributions will exhibit statistically significant deviations (p < 0.01) from the Dirichlet(1) baseline, as measured by Wasserstein distance.

**Why it's testable**: Pareto distributions with finite mean but infinite variance (α ≤ 2) or finite variance but infinite higher moments (2 < α ≤ 3) create fundamentally different weight structures than Dirichlet(1). We can systematically vary α and measure the resulting Wasserstein distances.

**Experiment to test it**:
1. Generate 500,000+ iterations of 5-player weight vectors where each weight vector is normalized from Pareto(α, xₘ) draws
2. Compute exact Shapley values for each iteration using the weighted Shapley value framework
3. Compare resulting distributions to analytically derived Dirichlet(1) using Wasserstein distance and KS tests
4. Vary α across values: 1.5, 2.0, 2.5, 3.0, 3.5, 4.0 (with fixed xₘ)

**Expected outcome**: Deviations increase as α decreases below 3, with the most severe deviations occurring when α ≤ 2 (infinite variance regime).

---

## Hypothesis 2: Log-Normal Weight Variance Drives Linear Increases in Shapley Value Variance

**Statement**: For 5-player games with weights drawn from Log-Normal(μ, σ²), the variance of the resulting Shapley values scales approximately linearly with σ², the log-variance of the input weights.

**Why it's testable**: The web search confirms Log-Normal distributions model multiplicative processes with controllable variance. Since Shapley values are weighted averages of marginal contributions, the CLT suggests variance propagation should be predictable.

**Experiment to test it**:
1. Fix μ = 0 and vary σ ∈ {0.5, 1.0, 1.5, 2.0, 2.5}
2. For each σ, generate 500,000+ normalized weight vectors
3. Compute Shapley values and measure Var(φᵢ) across all players and iterations
4. Fit a regression model: Var(Shapley) = β₀ + β₁·σ² + β₂·σ⁴ + ε

**Expected outcome**: β₁ > 0 and statistically significant, with R² > 0.8 indicating strong relationship between input variance and Shapley value variance.

---

## Hypothesis 3: Skewness in Input Weights Transfers to Kurtosis in Output Shapley Values

**Statement**: The kurtosis of the Shapley value distribution increases monotonically with the skewness of the input weight distribution, independent of the specific distributional family (Pareto vs. Log-Normal).

**Why it's testable**: Both Pareto and Log-Normal can be parameterized to produce identical skewness but different kurtosis profiles, allowing controlled isolation of the skewness-kurtosis relationship.

**Experiment to test it**:
1. For each distribution family (Pareto, Log-Normal, Exponential), find parameter combinations that produce skewness values of 1, 2, 3, 4, 5
2. Generate 500,000+ weight vectors for each configuration
3. Compute Shapley values and measure excess kurtosis of the resulting distributions
4. Plot kurtosis(SV) vs. skewness(weights) with separate curves per family

**Expected outcome**: A single monotonic relationship across families, suggesting universal transfer of heavy-tailed input characteristics to heavy-tailed output distributions.

---

## Hypothesis 4: Critical Variance Threshold for Detectable Dirichlet(1) Deviations

**Statement**: There exists a critical input weight variance threshold (V*) below which Shapley value distributions remain statistically indistinguishable from Dirichlet(1), regardless of the weight distribution family.

**Why it's testable**: The prior failure to validate Dirichlet(1) suggests low-variance weights produce near-symmetric outcomes. We can empirically locate this threshold.

**Experiment to test it**:
1. Define a normalized variance metric: CV = Var(weights) / Mean(weights)²
2. For each distribution family, generate weight vectors at CV values: 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0
3. For each CV level, conduct KS tests comparing to Dirichlet(1) baseline
4. Use logistic regression to estimate the probability of rejecting H₀ (Dirichlet(1)) as function of CV

**Expected outcome**: Sigmoid-shaped probability curve with V* ≈ 0.1–0.3, indicating that modest weight heterogeneity (CV > 0.2) consistently produces detectable deviations.

---

## Hypothesis 5: Distribution Family Classification from Shapley Value Moments Alone

**Statement**: The first four moments of the Shapley value distribution (mean, variance, skewness, kurtosis) contain sufficient information to classify the generating weight distribution family with >80% accuracy.

**Why it's testable**: If different input distributions produce distinctive moment signatures in the output, we can build a classifier and validate its accuracy.

**Experiment to test it**:
1. Generate training data: 100,000 iterations each from Pareto(α=2), Log-Normal(σ=1), Exponential(λ=1), and Dirichlet(1) as control
2. Compute 4 moment-based features from each Shapley value vector
3. Train a random forest classifier with 10-fold cross-validation
4. Test on held-out 50,000 iterations per family

**Expected outcome**: Classification accuracy >80%, with Log-Normal and Pareto most frequently confused due to overlapping heavy-tail characteristics.

---

## Integration with Prior Findings

The failed baseline verification (Run 20) underscores that **Hypothesis 4** should be prioritized—the runtime error may have occurred because the simulation parameters inadvertently crossed V*, causing numerical instability. Validating the threshold will ensure robust future experiments.

The web search results confirm that weighted Shapley values framework directly supports these hypotheses, as the mathematical foundation already accounts for asymmetric weights that arise from non-Dirichlet structures.