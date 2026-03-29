# Research Problem: Game Theory - Cooperative Games

## Objective
Investigate the distribution of Shapley values in 5-player cooperative games using non-Dirichlet weight structures to identify the specific conditions under which the resulting power allocations significantly deviate from the standard Dirichlet(1) baseline distribution.

## Research Questions
1. How do non-Dirichlet weight generation schemes (such as heavy-tailed Pareto or highly skewed Log-Normal distributions) impact the resulting distribution of Shapley values?
2. Under what specific weight structure configurations do Shapley values exhibit statistically significant deviations from the expected Dirichlet(1) distribution?
3. What is the mathematical or empirical relationship between the variance/skewness of the input player weights and the variance of the resulting Shapley power indices?

## Methodology
1. **Data Generation**: Implement a simulation for a 5-player cooperative game where player "power" weights are drawn from various non-Dirichlet distributions (e.g., Log-Normal, Exponential, Pareto) across at least 500,000 iterations.
2. **Value Computation**: Calculate the exact Shapley values for all players based on characteristic functions derived from these novel weight vectors.
3. **Statistical Testing**: Employ robust statistical distance metrics (such as the Kolmogorov-Smirnov test or Wasserstein distance) to compare the observed Shapley value distributions against a mathematically generated Dirichlet(1) baseline, avoiding standard chi-square binning vulnerabilities.
4. **Analysis & Visualization**: Map the magnitude of distribution deviation against the statistical moments (variance, skewness, kurtosis) of the input weight structures.

## Success Criteria
1. Successful identification of at least one non-Dirichlet weight structure that produces a statistically significant deviation from the Dirichlet(1) distribution (p < 0.01).
2. Robust, error-free computation of statistical distances (e.g., Wasserstein distance) that quantify the exact magnitude of the deviation.
3. Clear visualization mapping the input weight distribution parameters to the resulting Shapley value distribution shapes.

## Constraints
1. The simulation scope must remain restricted to 5-player games to ensure the exact computation of Shapley values remains computationally feasible across hundreds of thousands of iterations.
2. Statistical testing methodologies must use non-parametric tests or robust binning strategies to prevent zero-frequency artifacts during baseline comparisons. 
3. The research must strictly remain within the domain of Cooperative Game Theory and focus purely on the Shapley value index.