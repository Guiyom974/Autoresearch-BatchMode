# Testable Hypotheses for Stochastic Cooperative Games with Probabilistic Weights

Based on the research problem, prior findings (Runs 18-20), and web search results, I propose the following 5 testable hypotheses that build on the established foundation without repeating prior experiments.

---

## Hypothesis 1: Bounded Weight Distributions Preserve Superadditivity More Frequently Than Unbounded Distributions

**Statement:** Stochastic cooperative games with weights sampled from bounded distributions (Beta, Dirichlet) will exhibit strict superadditivity and monotonicity with significantly higher frequency (>85%) compared to games with weights from unbounded distributions (truncated Gaussian), even when distributions are matched for mean and variance.

**Why it's testable:**
- Prior findings (Run 20) established that deterministic weight-based characteristic functions are superadditive for N≤4, but the impact of distribution shape remains uncharacterized.
- Monte Carlo simulation can generate 10,000+ games per distribution type, enabling statistical comparison of superadditivity frequencies.
- Superadditivity can be verified deterministically for each generated game by checking all coalition pair comparisons.

**Experiment design:**
1. Implement Monte Carlo simulation with N=5 players
2. Generate 10,000 stochastic games using each distribution family (Beta(α,β), Dirichlet(α), truncated Gaussian with matched moments)
3. For each game, compute v(S) for all 2⁵-1 coalitions using the weight-based characteristic function
4. Calculate superadditivity preservation rate (proportion of games where v(S∪T) > v(S) + v(T) for all disjoint S,T)
5. Apply chi-squared tests to compare preservation rates across distributions

---

## Hypothesis 2: Shapley Value Variance Scales Linearly with Input Weight Variance

**Statement:** The variance of the Shapley value for each player i scales approximately linearly with the variance of the input weight distribution, following σ²(φᵢ) ≈ kᵢ · σ²(w), where kᵢ is a player-specific coefficient determined by the game structure and N.

**Why it's testable:**
- Run 18 confirmed that Shapley values from Dirichlet weights are computationally feasible but require statistical validation.
- The relationship between input variance and output variance can be quantified through systematic variance manipulation and regression analysis.
- ANOVA testing can distinguish between linear and non-linear scaling relationships.

**Experiment design:**
1. Fix N=4 players with fixed mean weights μ = (0.25, 0.25, 0.25, 0.25)
2. Generate 5,000 games each at 10 distinct variance levels (σ² ∈ {0.001, 0.005, 0.01, 0.02, ..., 0.1})
3. Compute Shapley values for each game instance
4. Record mean and variance of Shapley payoffs for each player across variance levels
5. Fit linear regression: σ²(φᵢ) ~ σ²(w) and test goodness-of-fit with R² values
6. Apply ANOVA to determine if player-specific coefficients kᵢ differ significantly

---

## Hypothesis 3: Existence of Critical Variance Thresholds for Coalition Stability

**Statement:** There exists a critical input weight variance σ²crit such that for σ² < σ²crit, at least 95% of stochastic games maintain strict superadditivity, but this confidence level drops below 80% when σ² > σ²crit. This threshold depends on the number of players N and the distribution family.

**Why it's testable:**
- Research Question 3 explicitly asks for variance thresholds, representing a novel empirical contribution beyond prior deterministic findings.
- Binary classification (stable vs. unstable) enables clear threshold identification through receiver operating characteristic (ROC) analysis.
- The phenomenon can be demonstrated through systematic variance sweeps with confidence interval estimation.

**Experiment design:**
1. Implement variance sweep protocol: generate 5,000 games at each of 20 variance levels from 0.001 to 0.2 for N=3, 4, and 5
2. For each game, classify as "stable" if superadditivity holds across all coalitions
3. Compute rolling confidence intervals for stability rate at each variance level
4. Use logistic regression to model P(stable) ~ σ² and identify σ²crit where P(stable) = 0.95
5. Validate threshold via separate holdout simulation (10,000 additional games per condition)
6. Apply sensitivity analysis to determine if σ²crit varies by distribution family (Beta vs. Dirichlet)

---

## Hypothesis 4: Monotonicity Violations Are More Sensitive to Weight Distribution Kurtosis Than to Variance

**Statement:** Monotonicity violations in stochastic characteristic functions correlate more strongly with the kurtosis (fourth moment) of the weight distribution than with its variance, suggesting that extreme weight values disproportionately destabilize coalition formation.

**Why it's testable:**
- Prior findings (Run 20) confirmed monotonicity preservation for deterministic weights, but the impact of distributional shape remains unexplored.
- Kurtosis can be independently manipulated using Beta distributions with varying shape parameters while holding mean and variance constant.
- Correlation analysis between kurtosis and monotonicity violation rate provides direct statistical evidence.

**Experiment design:**
1. Construct Beta distributions with constant mean μ=0.5 and constant variance σ²=0.02 but varying kurtosis (by selecting appropriate (α,β) pairs: e.g., Beta(2,2), Beta(5,5), Beta(0.5,0.5), Beta(10,10))
2. Generate 8,000 stochastic games (2,000 per kurtosis condition) for N=4 players
3. Compute characteristic function and test monotonicity: v(S) ≤ v(T) whenever S ⊂ T
4. Record monotonicity violation frequency and compute empirical kurtosis for each weight sample
5. Perform correlation analysis: Spearman's ρ between weight kurtosis and monotonicity violation rate
6. Compare explanatory power: hierarchical regression adding variance first, then kurtosis, to assess incremental R²

---

## Hypothesis 5: Player Position Effects in Shapley Value Distributions Diminish with Increasing Weight Variance

**Statement:** As weight variance increases, the variance in Shapley value rankings across players (positional effects) decreases, converging toward a uniform distribution of expected payoffs in high-variance regimes, regardless of initial weight configuration.

**Why it's testable:**
- This hypothesis addresses how stochasticity redistributes advantage among players with heterogeneous deterministic weights.
- Rank-based statistics (Kendall's W, Friedman test) can quantify convergence to uniform distributions.
- Monte Carlo simulation with fixed weight configurations but varying stochastic noise can isolate variance effects.

**Experiment design:**
1. Define 6 distinct deterministic weight configurations for N=5 (ranging from equal weights to highly asymmetric, e.g., μ = [0.6, 0.1, 0.1, 0.1, 0.1])
2. For each configuration, generate 3,000 stochastic games at each of 5 variance levels (σ² ∈ {0.005, 0.01, 0.05, 0.1, 0.2})
3. Compute Shapley values and rank players by payoff within each game
4. Calculate Kendall's coefficient of concordance (W) for player rankings at each variance level
5. Apply Friedman's test to determine if ranking variance differs significantly across variance conditions
6. Model convergence rate using exponential decay: W(σ²) = W₀ + (1 - W₀) · (1 - exp(-λσ²))

---

## Summary Table

| Hypothesis | Primary Variable | Comparison | Expected Outcome |
|------------|------------------|------------|------------------|
| H1 | Distribution family (bounded vs. unbounded) | Superadditivity frequency | Bounded distributions yield >85% stability |
| H2 | Input weight variance | Shapley value variance | Linear scaling with player-specific coefficients |
| H3 | Input weight variance | Coalition stability confidence | Critical threshold exists at σ²crit |
| H4 | Weight distribution kurtosis | Monotonicity violation rate | Higher kurtosis → more violations |
| H5 | Input weight variance | Player ranking concordance | Uniform convergence in high-variance regime |

These hypotheses are designed to be mutually complementary, collectively addressing all three research questions while building directly on the computational feasibility (Run 18) and baseline properties (Run 20) established in prior work.