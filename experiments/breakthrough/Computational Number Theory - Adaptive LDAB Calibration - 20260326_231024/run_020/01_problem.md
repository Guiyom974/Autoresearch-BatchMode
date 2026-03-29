# Research Problem: Theoretical Grounding of Primorial Gap Variance Scaling via Number-Theoretic Distributions

## Objective
Recent empirical efforts to mitigate truncation effects in primorial gap computations revealed a near-perfect statistical tie between a power-law model (exponent $\approx 2.19$) and a logarithmic trend for the variance-to-mean ratio $R(k)$. Since finite-size empirical data up to $k=15$ is insufficient to break this tie, the objective of this phase is to **develop a theoretical framework linking primorial gaps to known number-theoretic distributions** (such as Cramér’s random model or the distribution of smooth numbers). By deriving the asymptotic behavior analytically, we aim to definitively resolve the scaling ambiguity without requiring computationally prohibitive gap calculations for larger primorials.

## Research Questions
1. **Analytic Mapping:** How can the gap distribution of integers coprime to a primorial $P_k$ be analytically mapped to established probabilistic models of prime distributions (e.g., Poisson-Dirichlet distribution, random matrix theory predictions)?
2. **Asymptotic Scaling:** Does a rigorous theoretical derivation of the variance-to-mean ratio $R(k)$ asymptotically favor a power-law growth, a logarithmic growth, or a stretched exponential model as $k \to \infty$?
3. **Empirical Reconciliation:** How well does the derived theoretical asymptotic limit align with the empirical exponent of $\approx 2.19$ observed for $k \le 15$?

## Methodology
1. **Theoretical Modeling:** Construct a probabilistic model of coprime gaps using sieve theory and the properties of Jacobsthal's function, treating the gaps as a specialized case of the inclusion-exclusion principle applied to prime multiples.
2. **Asymptotic Derivation:** Utilize analytic number theory techniques to derive a closed-form approximation or bounds for the variance and the mean of the gaps as a function of $P_k$ or $k$.
3. **Model Evaluation:** Evaluate the derived $R(k)$ formula in the limit as $k \to \infty$ to determine its fundamental mathematical class (power-law vs. logarithmic).
4. **Validation:** Cross-reference the theoretical curve against the existing clean, truncation-mitigated empirical dataset for $k \in [1, 15]$.

## Success Criteria
- Formulation of a mathematically rigorous theoretical model that predicts the variance-to-mean ratio of primorial gaps.
- A definitive, analytically justified resolution to the power-law vs. logarithmic tie.
- The theoretical model must yield predictions that mathematically converge with the empirical exponent $\approx 2.19$ in the low-$k$ regime ($k \le 15$).

## Constraints
- **Computational Scope:** Do not attempt to compute exact gaps for $k > 15$; rely strictly on theoretical derivations and existing empirical data.
- **Domain Focus:** The framework must remain strictly focused on primorial gap distributions and not drift into general prime gap conjectures (e.g., Twin Prime or Polignac's) unless directly mathematically necessary to evaluate $R(k)$.