# Research Problem: Theoretical and Empirical Characterization of the $0.80$ Scaling Exponent in the Variance-to-Mean Ratio of Primorial Gaps

## Objective
Recent empirical studies of the variance-to-mean ratio $R(k)$ for gaps between integers coprime to the $k$-th primorial $P_k$ have revealed an unexpected scaling law. Contrary to prior models suggesting an exponent of $1.17$, experimental results across $k \in [1, 9]$ demonstrate that $R(k)$ scales proportionally to $(\log P_k)^{0.80}$ while strictly increasing with $k$. The objective of this research is to develop a rigorous theoretical framework that explains this $0.80$ exponent, and to empirically validate the stability of this scaling behavior by extending the analysis to larger primorials ($k \le 15$), while accounting for identified truncation underestimations.

## Research Questions
1. **Theoretical Origin of the Exponent:** What underlying number-theoretic or probabilistic mechanisms dictate the $\sim 0.80$ exponent in the scaling of $R(k)$ with respect to $\log P_k$, and why do previous models over-predict both the exponent and the absolute magnitude of $R(k)$?
2. **Asymptotic Stability:** Does the scaling relationship $R(k) \propto (\log P_k)^{0.80}$ remain stable as $k$ increases up to $15$, or is the observed exponent a transient pre-asymptotic phenomenon?
3. **Impact of Truncation:** How can the consistent $\sim 2.16\%$ underestimation of $R(k)$ due to gap truncation be analytically corrected in the extended $k$ regime to ensure accurate exponent estimation?

## Methodology
1. **Theoretical Modeling:** Formulate a revised probability model for the distribution of coprimes to $P_k$ that accounts for higher-order correlations among residue classes, aiming to derive the $0.80$ scaling exponent analytically.
2. **Extended Empirical Computation:** Develop highly optimized, arbitrary-precision algorithms to compute exact or statistically robust estimates of $R(k)$ for $k \in [10, 15]$. Use full-period gap sequences where computationally feasible, and rigorous statistical sampling for larger $k$.
3. **Artifact Correction:** Apply a systematic correction factor or modified estimator to compensate for the known truncation-induced underestimation of $R(k)$, ensuring that the regression of $\log R(k)$ against $\log \log P_k$ remains unbiased.
4. **Data Analysis:** Perform weighted linear and non-linear regression on the expanded dataset to determine the precise asymptotic exponent, calculating $R^2$ metrics and confidence intervals.

## Success Criteria
- **Theoretical alignment:** A proposed theoretical model successfully predicts a scaling exponent within $5\%$ of the empirically observed value.
- **Empirical validation:** Successful computation of $R(k)$ up to at least $k = 15$, demonstrating a stable scaling exponent (e.g., $R^2 > 0.98$ for the log-log fit).
- **Artifact mitigation:** The application of the truncation correction reduces the systematic underestimation bias to below $0.5\%$.

## Constraints
- **Computational Complexity:** The size of $P_k$ grows superexponentially; full-period computations for $k > 10$ will require optimized sampling techniques or sieve methods rather than naive enumeration.
- **Precision:** All arithmetic must continue to use arbitrary-precision integers to entirely avoid floating-point underflow and precision loss.
- **Domain Focus:** The research must strictly remain focused on the primorial gap variance-to-mean ratio and its implications for adaptive density calibration frameworks.