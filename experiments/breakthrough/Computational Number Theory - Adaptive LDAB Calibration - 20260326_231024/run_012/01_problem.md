# Research Problem: Theoretical Modeling of Sub-Quadratic Scaling in Primorial Gap Variances

## Objective
Following the definitive rejection of both the geometric distribution and standard quadratic scaling hypotheses for artifact-free primorial gaps, this phase aims to **develop and validate a refined theoretical model that explicitly explains the observed sub‑quadratic scaling** of gap variances in reduced residue systems modulo $P_k$. The primary goal is to derive an analytical function that captures the empirical variance-to-mean² ratio—which scales from ~0.173 at $k=3$ to ~0.333 at $k=7$—and establish a rigorous mathematical framework for the structural suppression of gap variance.

## Research Questions
1. **Variance Suppression Mechanism:** What specific algebraic or combinatorial properties of the reduced residue group modulo $P_k$ cause the heavy suppression of gap variance relative to a purely random (Poisson/geometric) model?
2. **Asymptotic Scaling Law:** Can the progression of the variance-to-mean² ratio (0.17, 0.23, 0.27, 0.30, 0.33...) be modeled by a closed-form logarithmic or fractional-power asymptotic function as $k \to \infty$?
3. **Predictive Modeling:** How accurately can a structurally-aware sieve model predict the exact gap variance and higher moments for $k \ge 8$?

## Methodology
1. **Combinatorial Sieve Modeling:** Construct a theoretical model of gap probabilities utilizing exact inclusion-exclusion principles over the prime factors of $P_k$ to account for the local periodicity that suppresses extreme gap lengths.
2. **Empirical Curve Fitting:** Analyze the trajectory of the variance-to-mean² ratio for $k=3 \dots 7$ to identify candidate asymptotic scaling laws (e.g., $c_1 - c_2/\log(k)$ or similar structural dependencies).
3. **Model Validation & Extrapolation:** Calibrate the derived model against the exact artifact-free statistical outputs for $k \le 7$. Use the finalized model to formulate a strict quantitative prediction for the variance and variance-to-mean² ratio at $k=8$ and $k=9$.

## Success Criteria
1. **Predictive Accuracy:** The refined theoretical model must retroactively predict the gap variance for $k=3$ through $k=7$ with less than $5\%$ relative error (a vast improvement over the ~70% error of the geometric baseline).
2. **Falsifiable Forward Prediction:** The model successfully outputs a rigorous, falsifiable prediction for the variance-to-mean² ratio at $k=8$ prior to the execution of the next computationally intensive extraction.
3. **Mathematical Rigor:** The sub-quadratic scaling behavior is formally linked to the underlying number-theoretic properties of primorials, providing a sound baseline for future LDAB density calibrations.

## Constraints
1. **Computational Limits:** Exact extraction for $k \ge 8$ ($P_8 = 9,699,690$) is computationally expensive; therefore, model formulation must rely purely on the high-fidelity $k=3 \dots 7$ dataset before verifying against heavier computations.
2. **Domain Scope:** The model must remain specifically focused on the structural gap distributions of reduced residue systems modulo primorials, avoiding unrelated probabilistic prime gap models (e.g., standard Cramér model) unless formally mapped to the modulo $P_k$ context.