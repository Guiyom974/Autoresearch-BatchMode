# Testable Hypotheses for RMT Variance Convergence and LDAB Validation

Based on the research problem, I propose five testable hypotheses that address the core objectives of resolving the variance discrepancy and validating the LDAB model.

---

## Hypothesis 1: Asymptotic Variance Convergence

**Hypothesis Statement:**
As the prime sieve bound $x$ increases from $10^7$ to $10^{10}$, the empirical variance of prime counts across coprime classes mod 210 converges asymptotically toward the RMT-predicted variance of 25071.87, with the proportional gap decreasing by at least a factor of 10.

**Why It's Testable:**
This hypothesis makes a specific, quantitative prediction about the relationship between computational scale and variance discrepancy. The relationship can be directly measured by computing empirical variance at multiple values of $x$ and comparing against the fixed RMT prediction. The "10× reduction" criterion provides a clear binary outcome for hypothesis testing.

**Experiment Design:**
1. Execute the multi-GPU distributed sieving framework at intervals: $x = 10^7, 10^8, 10^9, 10^{10}$
2. Calculate empirical variance $\sigma^2_{\text{emp}}(x)$ of prime counts across all $\phi(210) = 48$ coprime classes at each bound
3. Compute the proportional gap: $G(x) = |\sigma^2_{\text{RMT}} - \sigma^2_{\text{emp}}(x)| / \sigma^2_{\text{RMT}}$
4. Perform linear regression on $\log(G(x))$ vs. $\log(\log(x))$ to assess convergence rate
5. Accept hypothesis if $G(10^{10}) \leq 0.1 \times G(10^7)$

---

## Hypothesis 2: Finite-Size Correction Term Existence

**Hypothesis Statement:**
If the variance convergence rate in Hypothesis 1 is slower than predicted by standard asymptotic theory, then a lower-order correction term of the form $C/\log(x)$ or $C/\log\log(x)$ exists in the RMT variance model that accounts for the persistent discrepancy.

**Why It's Testable:**
This hypothesis is falsifiable: if empirical data shows rapid convergence without systematic residuals, the correction term is unnecessary. Conversely, if residuals follow the predicted functional form, the hypothesis is confirmed. The correction term can be estimated via nonlinear regression against the observed residuals.

**Experiment Design:**
1. Compute residuals $R(x) = \sigma^2_{\text{RMT}} - \sigma^2_{\text{emp}}(x)$ at each sieve bound
2. Fit three candidate correction models: $R(x) \sim C_1/\log(x)$, $R(x) \sim C_2/\log\log(x)$, and $R(x) \sim C_3/x^\alpha$
3. Use Akaike Information Criterion (AIC) to compare model fits
4. Test significance of the best-fit correction coefficient $C_i$ via t-test
5. Accept hypothesis if the best-fitting correction model has AIC at least 2 points lower than the uncorrected RMT model and the coefficient is statistically significant (p < 0.05)

---

## Hypothesis 3: LDAB Scale-Dependent Outperformance

**Hypothesis Statement:**
The KL divergence reduction achieved by the LDAB model relative to the standard Benford model (currently ~2.5% improvement) increases monotonically with sieve bound and becomes statistically significant (p < 0.01) at $x \geq 10^9$.

**Why It's Testable:**
The hypothesis predicts both a directional effect (monotonic improvement) and a threshold effect (significance at specific scale). Both predictions can be tested by computing KL divergence under both models at multiple scales and applying statistical tests for trend significance and threshold crossing.

**Experiment Design:**
1. Generate leading digit distributions (base-210) for prime counts at $x = 10^7, 10^8, 10^9, 10^{10}$
2. Compute KL divergence $D_{\text{std}}(x)$ against standard Benford and $D_{\text{LDAB}}(x)$ against LDAB model
3. Calculate improvement ratio: $\Delta(x) = [D_{\text{std}}(x) - D_{\text{LDAB}}(x)] / D_{\text{std}}(x)$
4. Test monotonicity using Spearman's rank correlation between $x$ and $\Delta(x)$
5. Perform bootstrap hypothesis testing (10,000 iterations) to assess significance of $\Delta(10^9)$ relative to null hypothesis of zero improvement
6. Accept hypothesis if Spearman's $\rho > 0.8$ (monotonic trend) AND bootstrap p-value < 0.01 at $x = 10^9$

---

## Hypothesis 4: Anderson-Darling Superior Sensitivity

**Hypothesis Statement:**
The Anderson-Darling goodness-of-fit test provides greater statistical power than the Kolmogorov-Smirnov test and KL divergence for distinguishing between standard Benford and LDAB model fits to the empirical leading digit distribution.

**Why It's Testable:**
This is testable through a direct comparative power analysis. Under a fixed alternative hypothesis (that LDAB is true), both tests can be applied to simulated data, and their power (probability of correctly rejecting the null) can be estimated.

**Experiment Design:**
1. Generate 1,000 synthetic datasets from the confirmed LDAB distribution at each scale
2. Apply both Anderson-Darling (AD) and Kolmogorov-Smirnov (KS) tests, comparing each dataset to both Benford and LDAB theoretical distributions
3. Define "correct rejection" as: AD/LDAB p-value > AD/Benford p-value (and equivalent for KS)
4. Calculate empirical power as proportion of correct rejections for each test
5. Compare power curves across scales using paired t-tests on the p-value differences
6. Accept hypothesis if AD test power exceeds KS test power by >10 percentage points at $x = 10^9$

---

## Hypothesis 5: Logarithmic Scaling of Variance Error

**Hypothesis Statement:**
The variance error $E(x) = |\sigma^2_{\text{emp}}(x) - \sigma^2_{\text{RMT}}|$ follows a logarithmic scaling law $E(x) \approx A \cdot \log(\log(x)) + B$ across the range $10^7 \leq x \leq 10^{10}$.

**Why It's Testable:**
This hypothesis specifies a precise functional form for the error scaling. The parameters $A$ and $B$ can be estimated via nonlinear least squares, and the goodness-of-fit of the logarithmic model can be compared against alternatives (power law, polynomial, etc.) using standard model selection techniques.

**Experiment Design:**
1. Collect variance measurements $E(x_i)$ at $x_i \in \{10^7, 2\times10^7, 5\times10^7, 10^8, 2\times10^8, 5\times10^8, 10^9, 2\times10^9, 5\times10^9, 10^{10}\}$
2. Fit logarithmic model: $E(x) = A \cdot \log(\log(x)) + B$ via nonlinear regression
3. Compare against alternative models: $E(x) = C \cdot (\log(x))^\gamma + D$ (power-log), $E(x) = \alpha/x^\beta + \gamma$ (power-law decay), and $E(x) = a(\log(x))^2 + b\log(x) + c$ (polynomial)
4. Use residual standard error (RSE) and adjusted $R^2$ to compare fits
5. Apply Vuong's closeness test to determine if logarithmic model is significantly closer than alternatives
6. Accept hypothesis if: (a) logarithmic model has lowest RSE among compared models, (b) residuals show no systematic pattern, and (c) parameter $A$ is significantly different from zero (p < 0.05)

---

## Summary Table

| Hypothesis | Primary Testable Quantity | Key Metric | Success Threshold |
|------------|---------------------------|------------|-------------------|
| H1: Convergence | Variance gap reduction | $G(x)$ | 10× decrease from $10^7$ to $10^{10}$ |
| H2: Correction term | Residual functional form | AIC comparison | Best fit + p < 0.05 |
| H3: LDAB scaling | KL divergence improvement | $\Delta(x)$ | Monotonic + p < 0.01 |
| H4: AD sensitivity | Test power comparison | Power difference | >10 percentage points |
| H5: Error scaling | Log-log scaling law | RSE + $R^2$ | Lowest RSE, $A \neq 0$ |

These hypotheses are designed to be mutually complementary: H1 and H2 address the variance discrepancy directly, H3-H4 address LDAB validation methodology, and H5 provides a theoretical characterization of the convergence behavior.