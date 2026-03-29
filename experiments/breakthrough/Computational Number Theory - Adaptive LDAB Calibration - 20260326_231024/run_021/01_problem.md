# Research Problem: Theoretical Investigation of the $R(k)=1$ Invariance in Primorial Gap Distributions

## Objective
Recent empirical analysis of primorial gap scaling yielded a surprising result: the variance-to-mean ratio $R(k)$ of gaps between integers coprime to the $k$-th primorial $P_k$ is exactly $1.000000$ for all $k \le 15$. This exact invariance suggests either a fundamental number-theoretic property (such as exact Poisson-like behavior over the full reduced residue system) or a systematic artifact related to gap definition, truncation, or boundary conditions. The objective of this phase is to **investigate the exactness of $R(k)=1$, determine if it is a fundamental theoretical identity for the complete period of primorial gaps, and identify any systematic biases in the empirical formulation.**

## Research Questions
1. **Fundamental Identity vs. Artifact:** Is the observation $R(k) \equiv 1$ an exact mathematical identity for the full cycle of gaps in the reduced residue system modulo $P_k$, or is it an artifact of the statistical definitions (e.g., truncation, boundary handling) used in previous iterations?
2. **Algebraic Formulation:** Can the variance and mean of the gaps coprime to $P_k$ be expressed algebraically in terms of Euler's totient function $\phi(P_k)$ and $P_k$ to definitively prove the ratio?
3. **Higher-Order Moments:** If the variance-to-mean ratio is strictly 1, do the higher-order moments (skewness, kurtosis) also match a known theoretical distribution exactly for the full period?

## Methodology
1. **Rigorous Algebraic Proof:** Formulate the exact expressions for the mean and variance of the gaps between consecutive units modulo $P_k$. Evaluate the sums $\sum g_i$ and $\sum g_i^2$ over the complete period $P_k$ using combinatorial properties of the inclusion-exclusion principle.
2. **Exact Arithmetic Verification:** Re-run the empirical evaluations for $k \le 15$ utilizing exact rational arithmetic (e.g., fractions) instead of floating-point approximations to confirm that $R(k)$ is analytically exactly 1, ruling out any rounding coincidences.
3. **Boundary Condition Analysis:** Systematically vary the boundary conditions (e.g., strictly periodic gaps wrapping around $P_k$ vs. truncated intervals up to $P_k/2$) to observe if the $R(k)=1$ invariance breaks under specific topological constraints.

## Success Criteria
1. **Formal Proof/Refutation:** A definitive mathematical proof or disproof that $R(k) = 1$ is an exact identity for the full period of gaps coprime to $P_k$.
2. **Artifact Identification:** A clear explanation of why the previous empirical models (power-law and logarithmic) collapsed, identifying the specific mechanism (e.g., period-matching) that forced the variance and mean to equate.
3. **Verified Moment Equations:** Exact, closed-form equations for the mean and variance of primorial gaps as a function of $k$.

## Constraints
1. **Computational Exactness:** All programmatic verification must utilize arbitrary-precision integer and rational arithmetic; standard floating-point operations are prohibited for moment calculations.
2. **Domain Focus:** The investigation must remain strictly focused on the properties of gaps coprime to primorial bases, avoiding divergence into general prime gap conjectures unless directly applicable to the $P_k$ residue system.