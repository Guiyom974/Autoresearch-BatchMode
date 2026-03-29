# Research Problem: Theoretical Modeling and High-Precision Validation of the 1.17 Scaling Exponent in Primorial Gap Variance-to-Mean Ratios

## Objective
Recent exact calculations up to the 8th primorial ($k=8$) have decisively rejected the previously hypothesized $0.56$ scaling exponent for the variance-to-mean ratio $R(k)$ of gaps between integers coprime to the $k$-th primorial. Instead, empirical scaling demonstrates an exponent of $\beta \approx 1.17$ for $k \ge 3$. The objective of this research is to pivot away from the $0.56$ conjecture and develop a theoretical model based on inclusion-exclusion principles that accurately predicts this $\approx 1.17$ scaling. Furthermore, this model must be validated by extending exact gap computations to larger primorials ($k > 8$) using high-precision, memory-efficient arithmetic to assess whether this exponent is truly asymptotic or subject to finite-size effects.

## Research Questions
1. **Theoretical Derivation:** How can the inclusion-exclusion structure of coprime distributions be mathematically modeled to derive a variance-to-mean ratio scaling exponent of $\beta \approx 1.17$?
2. **Asymptotic vs. Finite-Size Effects:** Is the observed $\beta \approx 1.1746$ exponent an artifact of finite-size effects at $k \le 8$, and does the exponent shift as $k$ approaches mathematically significant thresholds (e.g., $k=9$ through $k=12$)?
3. **Discrepancy Origin:** What specific theoretical assumptions led to the erroneous $0.56$ conjecture, and how does the new model correct these assumptions?

## Methodology
1. **Theoretical Modeling:** Construct a rigorous combinatorial or probabilistic model of coprime gaps that predicts the variance and mean as functions of $k$, specifically isolating the variance-to-mean ratio $R(k)$.
2. **Algorithm Development:** Design and implement a memory-efficient, high-precision algorithm (e.g., using sieve methods or generator-based gap extraction) to compute exact gap distributions for $k=9$ ($P_9 = 223,092,870$) and $k=10$ ($P_{10} = 6,469,693,230$), avoiding the memory bottlenecks of full array instantiation.
3. **Data Analysis:** Fit the extended data ($k \ge 3$ up to at least $k=10$) to the power-law model $R(k) \sim k^\beta$ to refine the exponent and compare it against the theoretical model's predictions.

## Success Criteria
1. **Theoretical Framework:** Formulation of a closed-form approximation or rigorous bound for $R(k)$ that explains the $\approx 1.17$ scaling.
2. **Extended Computation:** Successful, exact calculation of the mean, variance, and $R(k)$ for at least $k=9$ and $k=10$ without integer overflow or out-of-memory errors.
3. **Model Validation:** The extended empirical data must align with the new theoretical prediction, maintaining a tight power-law fit ($R^2 > 0.99$) or demonstrating a predictable asymptotic convergence.

## Constraints
1. **Computational Resources:** The sheer size of $P_k$ grows exponentially; exact gap extraction for $k \ge 10$ requires strictly $O(1)$ memory overhead and highly optimized time complexity.
2. **Precision Limits:** Calculations of variance for large gaps must maintain high precision (e.g., `float64` or arbitrary precision) to prevent catastrophic cancellation or overflow.