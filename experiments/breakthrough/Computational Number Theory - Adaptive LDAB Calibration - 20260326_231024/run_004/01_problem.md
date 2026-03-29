# Research Problem: Scaling Adaptive Wasserstein Weighting to High-Order Primorial Bases

## Objective
Following our findings that variance-based adaptive weighting yields negligible temporal variance reduction (-1.35%) for prime residue classes modulo 210, this iteration shifts focus to the scale of the modulus. The objective is to investigate whether this failure is an artifact of the low modulus scale, and to determine if expanding the adaptive Wasserstein framework to larger primorial bases (e.g., 2310 and 30030)—where coprime residue classes are significantly sparser and structural noise is theoretically more heterogeneous—unlocks statistically significant variance reductions.

## Research Questions
1. **Scale Dependency of Adaptive Weighting:** Does the temporal variance reduction achieved by dynamic variance-based weighting improve as the primorial modulus scales from 210 to larger bases like 2310 and 30030?
2. **Residue Sparsity Effects:** How does the increased sparsity of coprime residue classes at higher primorials (e.g., 480 classes for 2310; 5760 classes for 30030) impact the efficacy of real-time variance discounting in the Wasserstein proxy metric?
3. **Threshold Attainment:** Can scaling the modulus alone push the temporal variance reduction of the adaptive scheme past the previously established 20% significance threshold compared to a static weighting scheme?

## Methodology
1. **Extended Data Generation:** Generate prime streams up to at least $10^7$ to ensure sufficient data density for higher-order moduli.
2. **Multi-Scale Implementation:** Adapt the existing Wasserstein proxy metric and rolling variance-based weighting algorithm to support modulo 2310 and modulo 30030.
3. **Comparative Tracking:** Simultaneously track the temporal variance of both the *static* weighted Wasserstein distance and the *adaptive* variance-weighted Wasserstein distance across rolling windows for each modulus.
4. **Statistical Evaluation:** Calculate the percentage reduction in temporal variance for each base independently, mapping the relationship between modulus size and adaptive weighting performance.

## Success Criteria
1. **Successful Execution at Scale:** The adaptive weighting algorithm computes without memory or performance bottlenecks for the 5760 coprime classes of modulo 30030.
2. **Definitive Scale Analysis:** A clear, quantified comparison showing the variance reduction percentages for bases 210, 2310, and 30030.
3. **Hypothesis Resolution:** A definitive conclusion on whether scaling to higher primorial bases allows the adaptive weighting scheme to meet or exceed the >20% variance reduction threshold.

## Constraints
1. **Algorithmic Consistency:** The core mechanism of the Wasserstein proxy and the rolling variance penalty must remain identical to the previous iteration; only the modulus and associated residue classes may change.
2. **Computational Overhead:** The real-time computation for modulo 30030 must be optimized to handle a 12-fold increase in residue classes compared to 2310 without exceeding reasonable execution time limits.
3. **Domain Strictness:** The investigation must strictly remain within the LDAB and prime density calibration domain.