# Research Problem: Game Theory - Cooperative Games

## Objective
Formulate and validate a robust mathematical framework for generating coalition values (the characteristic function) in minimal $N$-player cooperative games ($N \le 5$). The primary goal is to ensure the theoretical consistency (e.g., superadditivity, monotonicity) of the $2^N - 1$ coalition subsets before scaling to complex, non-Dirichlet weight distributions.

## Research Questions
1. How can we construct a robust, deterministic mathematical model for generating valid characteristic functions for all possible coalition subsets in small-scale ($N \le 5$) games?
2. What are the necessary boundary conditions and structural constraints required to ensure algorithmic and theoretical stability when calculating marginal contributions?
3. How do varying foundational weight structures behave at a minimal scale ($N=3$) compared to the target scale ($N=5$) when subjected to strict structural validation?

## Methodology
1. **Mathematical Formulation**: Explicitly define the subset generation logic and characteristic function mapping for a minimal case ($N=3$), ensuring all $2^N - 1$ coalitions are accurately represented.
2. **Structural Validation**: Implement strict theoretical checks on generated coalition values, specifically testing for monotonicity and superadditivity ($v(A \cup B) \ge v(A) + v(B)$).
3. **Incremental Scaling**: Gradually increase the player count from $N=3$ to $N=5$, validating the integrity of the coalition space at each increment.
4. **Baseline Computation**: Compute standard Shapley values for the validated minimal games using uniform baseline weights to confirm the stability of the core allocation mechanism.

## Success Criteria
- Successful, complete generation of theoretically sound characteristic functions for $N=3, 4,$ and $5$ player games without structural collapse.
- 100% pass rate on superadditivity and monotonicity checks for the generated coalition values.
- Stable, replicable computation of Shapley values for the validated baseline models, demonstrating that the sum of allocations equals the grand coalition value (efficiency axiom).

## Constraints
- The investigation must temporarily restrict itself to standard, well-behaved weight distributions (e.g., uniform or simple Dirichlet) until the subset generation framework is proven stable.
- The maximum number of players ($N$) must not exceed 5 during this validation phase to isolate scaling complexities.
- The theoretical model must strictly adhere to the fundamental axioms of cooperative game theory.