# Research Problem: Resolving the RMT-Empirical Variance Discrepancy in Chebyshev Bias via Exact L-Function Zeros and Finite-Scale Corrections

## Objective
Recent experiments investigating the Random Matrix Theory (RMT)-corrected Chebyshev bias for modulo 210 up to $x = 2 \times 10^6$ revealed a massive 430x discrepancy between the empirical variance ($72,593.42$) and the theoretical RMT approximation ($168.08$). This indicates a severe breakdown in the predictive power of the current theoretical model at this scale. The objective of this research iteration is to isolate the root cause of this variance gap. We will pivot away from broad LDAB validation to focus strictly on resolving this discrepancy by replacing logarithmic approximations with exact Dirichlet L-function zero computations and introducing finite-scale corrections to the RMT variance formula.

## Research Questions
1. **L-Function Zero Accuracy:** What percentage of the 430x variance discrepancy is directly attributable to the use of logarithmic approximations for L-function zeros rather than exact non-trivial zeros?
2. **Finite-Sample Effects:** How does the empirical variance scale and converge as the evaluation bound $x$ is extended from $2 \times 10^6$ up to $10^8$? 
3. **Theoretical Formulation:** What specific finite-scale correction terms must be introduced to the Rubinstein-Sarnak RMT variance formula to accurately model the empirical variance at computationally accessible bounds?

## Methodology
1. **Exact Zero Computation:** Discard the logarithmic approximation of L-function zeros. Implement or integrate a high-precision numerical method (e.g., using the Hardy Z-function or Riemann-Siegel formula adaptations) to compute the exact imaginary parts of the non-trivial zeros of Dirichlet L-functions modulo 210.
2. **Formula Derivation:** Re-examine the theoretical RMT variance derivation. Formulate a finite-scale correction term that accounts for the truncation of the zero sum and lower-order terms that are negligible as $x \to \infty$ but dominant at $x \sim 10^6$.
3. **Scaled Empirical Validation:** Leverage our established Multi-GPU Distributed Scaling pipeline to extend the empirical variance calculation up to $x = 10^7$ and $x = 10^8$. 
4. **Comparative Analysis:** Compare the new empirical variance at $x = 10^8$ against the updated theoretical variance (using exact zeros + finite-scale corrections) to assess convergence.

## Success Criteria
1. **Discrepancy Reduction:** The theoretical variance calculated using exact L-function zeros and finite-scale corrections must reduce the discrepancy with the empirical variance from 43,088% to less than 15%.
2. **Asymptotic Convergence:** The scaling experiments up to $x = 10^8$ must demonstrate a clear asymptotic convergence trend between the empirical and theoretical variance.
3. **Computational Pipeline:** Successful integration of exact Dirichlet L-function zero computations for $q=210$ into the existing GPU-accelerated framework without violating memory limits.

## Constraints
1. **Computational Complexity:** Calculating exact L-function zeros high up the critical line is computationally intensive and may require careful optimization to avoid bottlenecking the GPU pipeline.
2. **Domain Focus:** This iteration must strictly focus on the Chebyshev bias variance discrepancy modulo 210. We will temporarily suspend higher-order LDAB model validation until the base RMT variance model is corrected.
3. **Precision Limits:** High-precision floating-point arithmetic (FP64 minimum) will be required for the exact zero computations to prevent numerical instability from polluting the theoretical variance calculations.