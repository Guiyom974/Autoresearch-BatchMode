# Research Problem: Modeling the Asymptotic Growth of the Variance-to-Mean Ratio $R(k)$ in Primorial Gap Distributions

## Objective
Recent empirical analysis of primorial gap scaling has definitively falsified the hypothesis that the variance-to-mean ratio $R(k)$ of gaps between integers coprime to the $k$-th primorial $P_k$ is invariant at 1. Instead, experimental results from $k=1$ to $k=9$ reveal a clear, systematic increase in $R(k)$, reaching approximately 2.30 at $k=9$. The objective of this research is to characterize the asymptotic growth rate of $R(k)$ as a function of $k$ (or $P_k$), and to directly compare this empirical growth trend with existing theoretical models of primorial gap distributions and pseudo-random reduced residue systems.

## Research Questions
1. **Growth Trajectory:** What is the functional form of the growth of $R(k)$? Does it scale logarithmically with $P_k$ (linearly with $k$), or does it follow another asymptotic trajectory?
2. **Theoretical Alignment:** How does the observed empirical scaling of $R(k)$ compare with predictions derived from theoretical models, such as Cramér's random model or modified Poisson models for the reduced residue system modulo $P_k$?
3. **Higher-Order Moments:** Do higher-order statistics (e.g., skewness, kurtosis) of the gap distribution exhibit similar scaling behavior, and what does this imply about the underlying distribution as $k \to \infty$?

## Methodology
1. **Algorithmic Optimization:** Develop memory-efficient, highly optimized algorithms to compute exact gap statistics for $k \ge 10$, overcoming previous computational bottlenecks that caused errors for larger $k$.
2. **Empirical Computation:** Calculate the exact mean, variance, and $R(k)$ for the full reduced residue system modulo $P_k$ for as large a $k$ as computationally feasible. For extremely large $k$, use rigorous Monte Carlo sampling of the gap distribution.
3. **Statistical Modeling:** Perform regression analysis on the sequence $\{R(k)\}$ to test various growth models (e.g., $R(k) \approx A \cdot k + B$, or $R(k) \approx C \log(P_k)$).
4. **Theoretical Comparison:** Derive the expected variance-to-mean ratio under established probabilistic number theory frameworks and compare these analytical expectations with the empirical fits.

## Success Criteria
- Successful exact computation of $R(k)$ up to at least $k=12$, or robust statistical estimation up to $k=15$.
- A statistically significant fit for the growth rate of $R(k)$ with an $R^2$ value $> 0.99$.
- A formal comparison demonstrating whether the empirical growth of $R(k)$ aligns with or diverges from standard probabilistic models of prime gaps.

## Constraints
- **Computational Complexity:** The size of the reduced residue system $\phi(P_k)$ grows exponentially, making exact computation for $k > 12$ highly resource-intensive.
- **Precision:** Large integer arithmetic and floating-point precision issues must be carefully managed when calculating the variance of massive datasets.