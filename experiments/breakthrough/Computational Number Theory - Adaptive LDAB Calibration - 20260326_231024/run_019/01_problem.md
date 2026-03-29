# Research Problem: Isolating Asymptotic Scaling of Primorial Gap Variance through Truncation-Effect Mitigation

## Objective
Recent extensions of the primorial gap variance-to-mean ratio $R(k)$ up to $k = 15$ yielded a near-tie between the power-law model (exponent $\approx 2.19$) and the logarithmic model ($\Delta \text{AIC} = 0.0303$), while leave-one-out cross-validation (LOOCV) favored a stretched exponential model. The objective of this phase is to break this statistical tie by **investigating and mitigating finite-size boundary and truncation effects** in the gap computation, and subsequently extending the corrected analysis to $k > 15$ to isolate the true asymptotic scaling behavior.

## Research Questions
1. **Truncation Artifacts:** To what extent do boundary gaps (at the beginning and end of the primorial interval $P_k$) artificially skew the empirical variance $R(k)$ for $k \le 15$?
2. **Asymptotic Dominance:** Once finite-size boundary effects are filtered out, does the power-law scaling stabilize, or does the stretched exponential model (suggested by the lowest LOOCV error) emerge as the true asymptotic trajectory for larger primorial indices ($k > 15$)?

## Methodology
1. **Boundary-Corrected Estimator:** Develop a modified variance estimator that systematically excludes or appropriately weights boundary gaps near $0$ and $P_k$ to eliminate edge-effect pollution.
2. **Extended Computation ($k > 15$):** Implement a randomized gap-sampling algorithm or optimized partial sieve to estimate the corrected $R(k)$ for $k = 16$ through $18$, bypassing the memory constraints of full interval enumeration.
3. **Statistical Re-evaluation:** Fit the corrected $R(k)$ data to the logarithmic, power-law, and stretched exponential models, evaluating them using AIC, BIC, and LOOCV to determine definitive statistical superiority.

## Success Criteria
1. **Clear Model Separation:** Achieve a $\Delta \text{AIC}$ and $\Delta \text{BIC} > 2.0$ between the best-fitting model and its closest competitor, definitively resolving the current $0.0303$ ambiguity.
2. **Quantified Truncation Error:** Formally quantify the deviation between the naive full-interval variance and the boundary-corrected variance for $k \le 15$.
3. **Stable Exponent/Parameters:** Demonstrate parameter stability (e.g., a consistent power-law exponent or stretch factor) when extending the fit from $k=15$ to $k=18$.

## Constraints
1. **Computational Feasibility:** Full enumeration of gaps for $k > 15$ ($P_{16} \approx 3.25 \times 10^{17}$) is computationally intractable; the methodology must rely on statistically rigorous sampling or localized sieving.
2. **Domain Adherence:** The study must remain strictly focused on the variance-to-mean ratio $R(k)$ of primorial gaps and its scaling implications, avoiding generalized prime number theory derivations outside this specific metric.