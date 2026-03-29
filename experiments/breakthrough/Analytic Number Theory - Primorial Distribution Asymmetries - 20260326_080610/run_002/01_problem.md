# Research Problem: Refining the LDAB Model for Base-Specific Digit Constraints in Primorial Distributions

## Objective
Recent experimental findings demonstrate that while Chebyshev's bias remains negligible across primorial moduli (primes are uniformly distributed among coprime residue classes), the Logarithmic-Density-Adjusted Benford (LDAB) model fails significantly for leading digits in primorial bases (e.g., bases 30, 210, 2310, and 30030), consistently yielding a Kullback-Leibler (KL) divergence of approximately 0.19. The objective of this research phase is to investigate the mathematical source of this severe deviation from Benford's law and to formulate a revised LDAB model that accurately incorporates the strict digit constraints and restricted sample spaces inherent to primorial coprimality.

## Research Questions
1. **Source of Deviation:** What specific structural constraints within primorial bases (e.g., the elimination of specific leading digits due to $\gcd(d, P_k) \neq 1$) cause the consistent ~0.19 KL divergence from the standard LDAB predictions?
2. **Model Refinement:** How can the LDAB model be mathematically reformulated to account for the restricted allowed leading digits in primorial bases, creating a base-specific probability mass function?
3. **Generalization of the Revised Model:** Does the newly refined, constraint-aware LDAB model successfully reduce the KL divergence to near-zero across a wider range of primorial bases (up to $P_6 = 30030$) as the prime limit scales to $10^8$?

## Methodology
1. **Empirical Distribution Analysis:** Extract and map the exact empirical distribution of leading digits for primes up to $10^8$ represented in bases 30, 210, 2310, and 30030. 
2. **Constraint Mapping:** Analytically determine the allowed leading digits for each base by evaluating the coprimality condition $\gcd(\text{digit}, P_k) = 1$ and its interaction with positional magnitude.
3. **Model Formulation:** Develop a Restricted-Digit LDAB model. This will involve re-normalizing the logarithmic probabilities over only the mathematically permitted leading digits for each specific primorial base, rather than the standard $1$ through $b-1$ range.
4. **Validation:** Run KL divergence tests comparing the empirical leading digit distributions of primes against the predictions of the newly formulated Restricted-Digit LDAB model.

## Success Criteria
- **Analytical Explanation:** A rigorous mathematical explanation is provided for the ~0.19 KL divergence observed in the previous standard LDAB model tests.
- **Model Accuracy:** The refined Restricted-Digit LDAB model achieves a KL divergence of less than $0.01$ (indicating a strong fit) across all tested primorial bases (30, 210, 2310, 30030).
- **Scalability:** The theoretical adjustments hold true and maintain low KL divergence as the prime generation limit is extended from $10^7$ to $10^8$.

## Constraints
- **Computational Limits:** Prime generation and base-conversion algorithms must be optimized to handle limits up to $10^8$ without exceeding standard memory constraints, avoiding the previously proposed bounds of $10^{12}$ until the base model is proven.
- **Domain Focus:** The research must strictly remain focused on primorial bases and leading digit distributions (Benford's law variants); it should not drift into general prime gap theory or unrelated cryptographic applications.