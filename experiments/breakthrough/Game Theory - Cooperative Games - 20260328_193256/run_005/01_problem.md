# Research Problem: Game Theory - Cooperative Games

## Objective
Analyze the statistical concentration and variance of the Shapley value in 5-player cooperative games under stochastic player "power" weights. Previous experiments demonstrated that baseline superadditivity and monotonicity are trivially satisfied (100%) across standard probability distributions (Beta, Dirichlet, Uniform, Truncated Gaussian). Therefore, this phase shifts focus from coalition formation viability to the predictability and stability of payoffs. The objective is to evaluate how different stochastic weight models influence the Coefficient of Variation (CV) of the Shapley value, determining if certain distributions lead to highly concentrated (predictable) or highly dispersed (uncertain) fair payoff allocations.

## Research Questions
1. How does the choice of stochastic weight distribution (bounded vs. unbounded, symmetric vs. skewed) impact the variance and Coefficient of Variation of the Shapley value for individual players?
2. Do heavy-tailed distributions of player power weights lead to disproportionate volatility in the resulting Shapley values compared to uniform or Gaussian distributions?
3. Can we establish an analytical relationship between the variance of the input power weights and the variance of the expected Shapley value in $N$-player games ($N = 5$)?

## Methodology
1. **Data Generation**: Simulate a 5-player cooperative game environment where player characteristic functions are driven by stochastic weights drawn from a diverse set of distributions (e.g., Lognormal, Pareto, Exponential) to introduce non-trivial variance.
2. **Feature Extraction**: Calculate the Shapley value for each player across thousands of simulations per distribution. Extract metrics of dispersion, specifically the variance, standard deviation, and Coefficient of Variation (CV) for the Shapley values.
3. **Statistical Testing**: Perform ANOVA and Levene’s test to assess the equality of variances in Shapley values across different underlying weight distributions. 
4. **Visualization**: Generate kernel density estimate (KDE) plots and box plots to visualize the spread and concentration of Shapley values for specific players under different stochastic regimes.

## Success Criteria
1. Empirical demonstration of statistically significant differences in the Coefficient of Variation of the Shapley value across at least three distinct stochastic weight distributions.
2. Formulation of a clear mapping between input weight volatility and output Shapley value dispersion.
3. Successful bypass of previous trivial superadditivity outcomes by focusing entirely on the statistical distribution of the solution concept (payoff allocations).

## Constraints
1. The analysis must remain restricted to the Shapley value within the domain of Cooperative Game Theory.
2. Simulations are limited to $N=5$ players to ensure computational feasibility while allowing for exact Shapley calculations.
3. The characteristic function mapping weights to coalition values must remain consistent with the previous iteration to isolate the effect of weight distribution variance.