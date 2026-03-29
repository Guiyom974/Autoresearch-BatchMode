# Research Problem: Statistical Discrimination of Asymptotic Scaling Models for Primorial Gap Variance

## Objective
Following the empirical observation that the variance-to-mean ratio $R(k)$ of primorial gaps up to $k=12$ exhibits slow growth contradicting earlier power-law expectations, this phase focuses on applying rigorous statistical model comparison. The objective is to **definitively distinguish between logarithmic and power-law scaling for $R(k)$** by extending gap distribution computations to higher primorial indices ($k \ge 13$) and evaluating competing asymptotic models using information criteria (AIC/BIC). 

## Research Questions
1. **Model Discrimination:** Does the variance-to-mean ratio $R(k)$ strictly adhere to a logarithmic scaling model (e.g., $R(k) \approx a \log(k) + b$ or $a / (\log k + b) + c$) rather than a fractional power-law when evaluated across extended primorials?
2. **Asymptotic Divergence:** At what specific primorial index $k$ does the statistical divergence between the best-fit logarithmic model and the best-fit power-law model become definitive (e.g., $\Delta \text{AIC} > 10$)?
3. **Parameter Stability:** How stable are the extracted coefficients (e.g., $a, b, c$) of the winning model when computed over sub-intervals of $k$ (e.g., $k \in [3, 8]$ vs $k \in [8, 14]$)?

## Methodology
1. **Algorithmic Extension:** Implement an optimized, highly parallelized wheel factorization sieve to compute the exact gap distribution for primorials $P_{13}$ ($3.04 \times 10^{14}$), $P_{14}$ ($1.30 \times 10^{16}$), and potentially $P_{15}$.
2. **Statistical Fitting:** Perform non-linear least squares regression on the extended $R(k)$ dataset using competing functional forms (logarithmic, inverse-logarithmic, and power-law).
3. **Model Selection:** Apply rigorous statistical model selection frameworks, including Akaike Information Criterion (AIC), Bayesian Information Criterion (BIC), and adjusted $R^2$, to penalize overfitting and identify the true underlying trend.

## Success Criteria
1. **Computational Milestone:** Successful computation of exact mean and variance statistics for primorial gaps up to at least $k=14$.
2. **Statistical Resolution:** A conclusive statistical determination ($\Delta \text{AIC} > 10$ and $\Delta \text{BIC} > 10$) favoring one scaling model over the other.
3. **Predictive Accuracy:** The winning model must predict the $R(k)$ value for a holdout calculation (e.g., $k=15$) with a relative error of less than $1\%$.

## Constraints
1. **Computational Complexity:** The size of the primorial $P_k$ grows exponentially ($P_{14} > 10^{16}$), imposing severe memory and time constraints on computing the exact gap variance.
2. **Data Sparsity:** Even with extensions, the dataset consists of a small number of discrete data points ($k \le 15$), requiring careful handling of small-sample statistical penalties.