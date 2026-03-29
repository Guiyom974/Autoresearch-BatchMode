# Research Problem: Hybrid Variance-Wasserstein Weighting Schemes for High-Order Primorial Bases

## Objective
Following our recent findings that pure adaptive Wasserstein weighting fails to produce consistent, monotonic variance reduction as the primorial modulus increases (yielding an erratic 11.42% reduction at base 210, 24.02% at 2310, but dropping to 8.71% at 30030), this iteration pivots to a composite metric approach. The objective is to develop and evaluate a **hybrid adaptive weighting framework** that combines both variance-based and Wasserstein-based penalties. By leveraging the local distributional sensitivity of Wasserstein metrics and the global stability of variance metrics, we aim to stabilize the correction factor $c(t)$ and achieve consistent variance reduction in highly sparse coprime residue classes, specifically targeting moduli up to 510510.

## Research Questions
1. **Hybrid Metric Stabilization:** How does a blended weighting scheme—combining variance-based penalties with Wasserstein distances—mitigate the non-monotonic variance reduction observed in pure Wasserstein models across scaling primorial bases (210, 2310, 30030)?
2. **Optimal Blending Parameter:** What is the optimal dynamic blending parameter $\alpha(t)$ between variance and Wasserstein metrics as the sparsity of coprime residue classes increases in higher-order bases (e.g., 510510)?
3. **Structural Noise Resilience:** Does the hybrid approach consistently outperform static LDAB calibration under injected structural noise at large modulus scales, where previous pure metrics failed to generalize?

## Methodology
1. **Hybrid Metric Formulation:** Define a composite adaptive weighting function $W_{hybrid} = \alpha \cdot W_{var} + (1-\alpha) \cdot W_{wasserstein}$, where $\alpha \in [0, 1]$ controls the influence of each metric.
2. **Parameter Sweeping:** Conduct a systematic grid search over $\alpha$ for primorial bases $P_k$ where $k \in \{4, 5, 6, 7\}$ (i.e., 210, 2310, 30030, 510510) to identify the optimal blend for each scale.
3. **Simulation and Benchmarking:** Simulate the streaming real-world prime stream and apply the hybrid LDAB correction factor $c(t)$. Compare the temporal variance of the hybrid model against both the static LDAB baseline and the pure Wasserstein/Variance models from previous iterations.
4. **Statistical Validation:** Run all evaluations across multiple random seeds and calculate 95% confidence intervals to ensure the observed variance reductions are statistically significant and not artifacts of specific prime bounds.

## Success Criteria
1. **Consistent Scaling:** Demonstrate a stable or monotonically increasing variance reduction as the modulus scales from 210 to 510510, eliminating the performance drop previously observed at 30030.
2. **Performance Threshold:** Achieve a minimum of 20% variance reduction relative to the static LDAB baseline consistently across moduli 2310, 30030, and 510510.
3. **Statistical Robustness:** The correlation between coprime residue sparsity and variance reduction under the hybrid scheme must yield a statistically significant trend ($p < 0.05$).

## Constraints
1. **Computational Complexity:** Calculating exact Wasserstein distances for the 510510 modulus is computationally expensive; approximations (e.g., Sinkhorn distances) must be utilized if calculation time exceeds real-time streaming constraints.
2. **Domain Strictness:** The investigation must remain strictly confined to prime residue classes and the dynamic calibration of the LDAB model; introducing alternative sieve theories or non-LDAB base models is out of scope.