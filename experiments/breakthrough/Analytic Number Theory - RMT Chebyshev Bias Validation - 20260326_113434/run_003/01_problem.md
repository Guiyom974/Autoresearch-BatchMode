# Research Problem: Computing Exact Dirichlet L-Function Zeros Modulo 210 to Resolve Chebyshev Bias Variance Discrepancies

## Objective
Recent experiments demonstrated that using simulated exact L-function zeros instead of logarithmic approximations increased the theoretical variance of the RMT-corrected Chebyshev bias by 61% for modulus 210. This confirms that low-lying zero approximation errors are a primary driver of the massive discrepancy between empirical variance and theoretical RMT approximations at finite scales. The objective of this research iteration is to compute the exact non-trivial zeros of Dirichlet L-functions modulo 210 and evaluate their precise impact on the Rubinstein-Sarnak variance formula as $x$ scales beyond $2 \times 10^6$.

## Research Questions
1. How can we efficiently compute and verify the exact low-lying non-trivial zeros (up to a sufficient height $T$) for all Dirichlet L-functions modulo 210?
2. By what exact factor does the theoretical variance increase when utilizing rigorously computed exact zeros compared to both logarithmic approximations and previously simulated exact zeros?
3. How does the exact-zero correction factor scale with increasing $x$ (for $x > 2 \times 10^6$), and how much of the original 430x empirical-theoretical discrepancy remains after applying this correction?

## Methodology
1. **L-Function Zero Computation:** Implement or integrate robust numerical algorithms (e.g., using the Riemann-Siegel formula or Rubinstein's `lcalc` library) to compute the exact imaginary parts ($\gamma$) of the non-trivial zeros for Dirichlet characters modulo 210 up to a height $T = 10^4$.
2. **Variance Re-evaluation:** Substitute the computed exact zeros into the Rubinstein-Sarnak logarithmic variance formula. Compare the newly computed theoretical variance against the baseline logarithmic approximation variance and the previous simulated variance.
3. **Scaling Analysis:** Evaluate the empirical variance and the exact-zero theoretical variance across logarithmic intervals up to $x = 10^8$. Plot the ratio of empirical to theoretical variance to determine if the exact-zero correction stabilizes the discrepancy at higher scales.
4. **Residual Analysis:** Isolate the remaining variance discrepancy after exact-zero insertion to determine if additional finite-scale correction terms (e.g., lower-order terms in the prime number theorem for arithmetic progressions) are required.

## Success Criteria
1. Successful computation and verification of the low-lying zeros for Dirichlet L-functions modulo 210.
2. The exact-zero theoretical variance must be quantified, aiming to reduce the empirical-theoretical discrepancy ratio significantly from the baseline 430x.
3. Clear empirical demonstration of how the exact-zero variance correction scales with $x$ up to at least $x = 10^7$.
4. Identification of the residual discrepancy percentage, establishing whether further finite-scale corrections are mathematically necessary.

## Constraints
1. **Computational Accuracy:** The computed exact zeros must be verified to high precision to ensure they do not introduce numerical instability into the variance summation.
2. **Domain Strictness:** The investigation must remain strictly focused on Chebyshev bias modulo 210 and the associated Dirichlet L-functions.
3. **Hardware Limits:** Computations of L-function zeros and empirical variance scaling must be optimized to run efficiently within available multi-GPU/CPU constraints without FP32 drift.