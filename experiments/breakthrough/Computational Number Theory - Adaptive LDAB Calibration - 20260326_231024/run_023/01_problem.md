# Research Problem: Mitigating Boundary and Truncation Artifacts in the Estimation of the Variance-to-Mean Ratio $R(k)$ for Primorial Gap Distributions

## Objective
Recent empirical analyses investigating the variance-to-mean ratio $R(k)$ of gaps between integers coprime to the $k$-th primorial $P_k$ yielded inconclusive results regarding its departure from prior models. Because finite-interval computations of gap distributions are highly susceptible to edge effects and maximum-gap truncation, the apparent growth in $R(k)$ may be a methodological artifact rather than a true asymptotic property. The objective of this research is to systematically evaluate, quantify, and correct for boundary and truncation artifacts in the measurement of $R(k)$, thereby establishing a rigorously validated methodology for assessing the statistical properties of primorial gap distributions up to $k=9$.

## Research Questions
1. **Impact of Boundary Effects:** To what extent do finite-interval boundaries and the truncation of maximum gap sizes artificially inflate or deflate the empirical variance-to-mean ratio $R(k)$ for primorials $k=1$ through $k=9$?
2. **Robust Estimator Formulation:** Can we develop a corrected, artifact-free statistical estimator for $R(k)$ (e.g., utilizing periodic boundary conditions) that remains stable regardless of the sampling window size or interval starting point?
3. **Re-evaluation of Invariance:** Once boundary artifacts are mathematically neutralized, does the corrected $R(k)$ still exhibit systematic growth, or does it revert to the invariant behavior predicted by prior baseline models?

## Methodology
1. **Periodic Gap Generation:** Instead of relying on linear truncated intervals, generate complete, exact sets of gaps for $k=1$ to $k=9$ by exploiting the inherent periodicity of the coprimes modulo $P_k$. 
2. **Estimator Comparison:** Compute $R(k)$ using standard sample variance estimators and compare the results against specialized circular/periodic variance estimators designed to eliminate edge effects.
3. **Sensitivity Analysis:** Induce controlled truncation by artificially slicing the exact periodic gap sequence into smaller windows of varying sizes. Measure the divergence of the resulting $R(k)$ from the true periodic $R(k)$ to quantify the artifact error bounds.
4. **Data Re-analysis:** Apply the validated, artifact-free estimator to the previously generated datasets to determine the true trajectory of $R(k)$.

## Success Criteria
1. **Error Quantification:** A clear mathematical or empirical quantification of the error term introduced by boundary truncation in previous $R(k)$ calculations.
2. **Stable Estimator:** Formulation and successful implementation of a corrected $R(k)$ estimator that demonstrates less than $10^{-4}$ variance when computed across different arbitrary sub-intervals of $P_k$.
3. **Conclusive Baseline Comparison:** A definitive conclusion on whether the artifact-corrected $R(k)$ deviates from baseline model predictions, supported by high-confidence statistical validation.

## Constraints
1. **Scope Limitation:** The investigation must remain strictly focused on the statistical estimation of $R(k)$ for primorial gap distributions; do not expand into generalized prime gap distributions or other heuristic models.
2. **Computational Feasibility:** The exact periodic gap generation must be strictly bounded up to $k=9$ ($P_9 = 223,092,870$) to ensure that memory and computational time remain within practical limits for exact, un-sampled sequence generation.