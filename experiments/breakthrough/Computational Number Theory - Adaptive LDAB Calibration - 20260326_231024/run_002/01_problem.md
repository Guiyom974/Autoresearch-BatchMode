# Research Problem: Alternative Divergence Metrics and Non-Uniform Weighting for Multi-Scale LDAB Models

## Objective
Following the observation that Kullback-Leibler (KL) divergence fails to converge below $10^{-4}$ for the standard Adaptive LDAB Calibration (yielding values > 1.0 due to extreme sensitivity to local statistical noise in large residue sets), this iteration pivots to evaluate structural distribution accuracy. The new objective is to implement and assess the **Wasserstein distance (Earth Mover's Distance)** and **non-uniform residue class weighting** to capture the true asymptotic behavior of the LDAB model across multi-scale primorial bases (210, 2310, 30030).

## Research Questions
1. **Metric Robustness:** How does the Wasserstein distance compare to KL divergence in evaluating the convergence of empirical prime distributions against LDAB predictions, particularly in the presence of statistical noise inherent to larger bases like 30030?
2. **Residue Weighting:** Can the application of a non-uniform weighting scheme to valid residue classes (accounting for secondary number-theoretic biases, such as Chebyshev-like biases) significantly reduce the measured divergence between the LDAB model and empirical data?
3. **Asymptotic Stabilization:** Does the Wasserstein metric exhibit a clear, monotonic stabilization as the prime cutoff $x$ approaches $2 \times 10^6$, indicating underlying model accuracy that KL divergence failed to capture?

## Methodology
1. **Data Generation:** Generate primes up to at least $2 \times 10^6$ and map them to their respective valid residue classes for bases 210, 2310, and 30030 using sliding windows.
2. **Metric Implementation:** Replace the strict KL divergence threshold with a dual-metric evaluation system. Implement the 1D Wasserstein distance to measure the minimal "cost" of transforming the empirical residue distribution into the LDAB-predicted distribution.
3. **Weighting Scheme:** Develop a non-uniform residue weighting algorithm that adjusts expected densities based on the multiplicative order and known prime biases of each residue class modulo the primorial base.
4. **Comparative Analysis:** Plot and compare the trajectories of both KL divergence and Wasserstein distance as a function of the prime bound $t$ to demonstrate the mitigation of high-frequency statistical noise.

## Success Criteria
1. **Metric Convergence:** The Wasserstein distance must show a clear, measurable asymptotic decline as the prime bound increases, proving that the LDAB model captures the macroscopic distribution despite microscopic noise.
2. **Weighting Efficacy:** The non-uniform weighting scheme must yield a reduction in the Wasserstein distance of at least 15% compared to the naive uniform residue assumption for base 30030.
3. **Robustness Validation:** The framework must successfully process bases up to 30030 without the metric exploding due to sparse bins, confirming that the failure in the previous iteration was metric-specific rather than a fundamental flaw in the LDAB density estimation.

## Constraints
1. **Domain Strictness:** The research must remain entirely focused on the Local Density Approximation Basis (LDAB) for primorial bases (210, 2310, 30030).
2. **Computational Limits:** Prime generation and metric evaluation should remain computationally feasible, capping the prime search space at $2 \times 10^6$ to $5 \times 10^6$ for rapid iterative testing.
3. **No External Libraries for Core Math:** Rely on standard, well-vetted statistical libraries (e.g., SciPy's `wasserstein_distance`) rather than attempting to build custom optimal transport solvers from scratch.