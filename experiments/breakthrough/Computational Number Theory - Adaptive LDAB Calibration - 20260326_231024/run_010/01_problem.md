# Research Problem: Methodological Validation and Correction of Primorial Gap Variance Extraction

## Objective
Following the anomalous results of the previous iteration—where variance calculations yielded inconsistent, non-scaling values due to a severe methodological artifact (capturing only 2 gaps per primorial)—this phase pivots to correcting the foundational data extraction. The objective is to **rigorously define, extract, and validate the full distribution of gaps within the reduced residue system modulo $P_k$ (primorials)**, establishing a verified empirical baseline of gap variances before attempting higher-order scaling fits or LDAB calibration.

## Research Questions
1. **Algorithmic Correctness:** How can we ensure the extraction algorithm accurately captures the complete set of $\phi(P_k)$ gaps between consecutive integers coprime to $P_k$, rather than truncated edge cases?
2. **True Empirical Variance:** Once the full reduced residue system is correctly modeled, what is the true empirical variance of these gaps for primorial indices $3 \le k \le 10$?
3. **Theoretical Baseline Comparison:** How does the rigorously computed empirical variance for these small-to-medium primorials compare against theoretical variance predictions derived from random models (e.g., a modified Cramér model adjusted for primorial constraints)?

## Methodology
1. **Algorithm Redesign:** Rewrite the gap extraction logic to compute the differences between *all* consecutive elements in the reduced residue group $(\mathbb{Z}/P_k\mathbb{Z})^\times$. 
2. **Invariant Testing:** Implement strict mathematical assertions during data generation. Specifically, verify that for each $k$, the number of extracted gaps is exactly $\phi(P_k)$ (Euler's totient function) and that the sum of these gaps equals exactly $P_k$.
3. **High-Fidelity Variance Computation:** Compute the exact population variance of the validated gap sets for $k \le 10$. For larger $k$ approaching computational limits, employ memory-efficient segmented sieving or wheel factorization techniques.
4. **Model Comparison:** Plot the newly validated variance values against theoretical random-distribution expectations to establish a reliable baseline before re-introducing logarithmic scaling hypotheses.

## Success Criteria
1. **Data Integrity:** The extraction script reliably outputs exactly $\phi(P_k)$ gaps for every tested primorial, completely resolving the previous artifact (where `gaps=2`).
2. **Consistent Variance Metric:** The computed variance values are mathematically consistent, non-zero (for $k \ge 3$), and exhibit a clear, reproducible trend across $k$.
3. **Baseline Establishment:** A definitive statistical comparison is made between the corrected empirical gap variance and the theoretical random model, providing a stable foundation for future predictive scaling.

## Constraints
1. **Computational Complexity:** The size of the reduced residue system grows exponentially. Full extraction must be limited to $k \le 10$ ($P_{10} \approx 6.4 \times 10^9$) to avoid memory exhaustion, utilizing optimized prime sieves.
2. **Domain Focus:** The investigation must remain strictly on the variance of gaps within primorial bases and its relation to theoretical models, avoiding unrelated number theory explorations.