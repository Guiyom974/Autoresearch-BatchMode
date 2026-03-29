# Research Problem: Resolving the Logarithmic vs. Power-Law Scaling Conflict in Primorial Gap Variance

## Objective
Recent experimental evaluations on primorial gap distributions for $k \le 8$ yielded conflicting scaling indicators: while the variance-to-mean ratio $R(k)$ demonstrated a statistically significant power-law growth (exponent $\approx 2.6$), information criteria (AIC and BIC) strongly favored a logarithmic model ($\Delta \text{AIC/BIC} = 4.20$). The objective of this phase is to **definitively resolve this scaling conflict** by extending the index range to $k > 8$ (targeting $k \le 15$) and introducing alternative transitional models (e.g., stretched exponential) to determine the true asymptotic trajectory of primorial gap variance.

## Research Questions
1. **Asymptotic Dominance:** Does the logarithmic model maintain its strictly superior AIC/BIC performance over the power-law model as the primorial index $k$ extends into the $9 \le k \le 15$ regime?
2. **Alternative Model Fit:** Can a stretched exponential model ($R(k) = a e^{b k^\gamma} + c$) better bridge the observed rapid initial growth and the theoretically anticipated slower asymptotic scaling, outperforming both pure logarithmic and power-law models?
3. **Exponent Stability:** If power-law scaling persists, how does the estimated exponent ($\beta \approx 2.6$) shift when larger primorial indices are included in the regression?

## Methodology
1. **Extended Data Generation:** Compute the exact variance-to-mean ratio $R(k)$ for primorials $k=9$ through $k=12$. For $k=13$ to $k=15$, where exact exhaustive computation becomes computationally prohibitive, utilize high-precision Monte Carlo sampling of the primorial residue classes to estimate $R(k)$.
2. **Model Formulation:** Define three competing regression models:
   * Power-law: $R(k) = a k^\beta + c$
   * Logarithmic: $R(k) = a \ln(k) + c$
   * Stretched Exponential: $R(k) = a e^{b k^\gamma} + c$
3. **Rigorous Model Selection:** Fit all models to the expanded dataset ($k=2$ to $15$). Apply robust statistical criteria (AIC, BIC, and leave-one-out cross-validation) to penalize overfitting and select the model with the highest predictive validity.

## Success Criteria
* Computation or high-confidence statistical estimation of $R(k)$ successfully extended up to at least $k=15$.
* A conclusive model selection outcome, defined as a $\Delta \text{AIC} > 5$ and $\Delta \text{BIC} > 5$ favoring a single asymptotic model over the other candidates.
* A quantified assessment of the power-law exponent's stability as $k$ increases, demonstrating whether the $2.6$ exponent is an artifact of small-$k$ finite-size effects.

## Constraints
* **Computational Complexity:** Exact computation of gap distributions for $k > 12$ requires navigating factorial time complexity; approximations must strictly bound their margin of error to avoid skewing the variance statistics.
* **Scope Limits:** The investigation must remain tightly focused on the macroscopic variance-to-mean scaling of primorial gaps $R(k)$, avoiding tangential exploration into specific extremal gap occurrences or individual prime distributions.