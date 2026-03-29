**Hypotheses – Statistical Concentration & Dispersion of the Shapley Value under Non‑trivial Stochastic Weights**  

Below are five concrete, falsifiable hypotheses that follow directly from the research problem and the lessons learned from the prior “trivial‑weight” experiments (which showed 100 % super‑additivity/monotonicity but **no variation** in Shapley pay‑offs).  
All hypotheses keep the *weight‑to‑coalition‑value* mapping unchanged (e.g. \(v(S)=\sum_{i\in S}w_i\)) so that the only factor being isolated is the stochastic nature of the player‑power weights.

---

## Hypothesis 1 – Heavy‑tailed weight distributions generate a higher Coefficient of Variation (CV) of the Shapley value than bounded or light‑tailed distributions  

**Statement**  
Among a set of stochastic weight distributions that share the same mean and comparable variance, those with heavier tails (higher kurtosis – e.g. Pareto, Lognormal, Exponential) will produce Shapley values whose CV is **significantly larger** than the CV obtained from bounded or light‑tailed distributions (Uniform, Normal, Beta).

**Why it is testable**  
* The CV is a dimensionless, scale‑free measure of dispersion: \(\mathrm{CV}= \sigma/\mu\).  
* By fixing the first two moments of every distribution we can treat “heavy‑tailedness” as the only independent variable.  
* The CV can be computed from the empirical Shapley values obtained in a Monte‑Carlo study and compared across distribution families with standard ANOVA‑type tests (Levene’s test for equality of variances, post‑hoc Tukey HSD, etc.).

**Experiment that would test it**  
1. Choose six distribution families: **Pareto (α≈2)**, **Lognormal (σ≈1)**, **Exponential (λ matched)**, **Uniform**, **Normal**, **Beta** (all scaled to mean = 1 and variance = 0.5).  
2. For each family draw **10 000 independent weight vectors** \((w_1,\dots,w_5)\).  
3. Compute the characteristic function for every coalition (additive weight sum) and evaluate the exact Shapley value for each player.  
4. Record the CV of the Shapley values **per player** and then average the five CVs.  
5. Apply Levene’s test to the five CV vectors (one per distribution) to detect a difference, and if significant, perform pairwise comparisons to rank the distributions by CV magnitude.

---

## Hypothesis 2 – Shapley‑value variance scales monotonically with the variance of the underlying weight distribution (up to a distribution‑specific constant)  

**Statement**  
For a fixed game size (N = 5) and a given weight‑distribution family, increasing the variance \(\sigma_w^2\) of the weights while keeping the mean constant will produce a Shapley variance \(\mathrm{Var}(\phi_i)\) that grows **approximately proportionally** to \(\sigma_w^2\) (i.e. \(\mathrm{Var}(\phi_i) \approx c\,\sigma_w^2\) where the coefficient \(c\) depends on the shape of the weight distribution).

**Why it is testable**  
* Both \(\sigma_w^2\) and \(\mathrm{Var}(\phi_i)\) are well‑defined, estimable quantities.  
* By varying a single parameter (the variance) we obtain a clear functional relationship that can be tested with regression analysis.  
* The null hypothesis “\(c=0\)” (no relationship) is directly falsifiable.

**Experiment that would test it**  
1. For each distribution family (Uniform, Normal, Lognormal, Exponential, Pareto, Beta) select a range of variance levels, e.g. \(\sigma_w^2\in\{0.1,0.25,0.5,1.0,2.0,5.0\}\).  
2. For each variance level generate **5 000** weight vectors, compute the exact Shapley values, and record the sample variance \(\widehat{\mathrm{Var}}(\phi_i)\).  
3. Fit a simple linear model \(\widehat{\mathrm{Var}}(\phi_i)=\beta_0+\beta_1\sigma_w^2+\varepsilon\).  
4. Test \(H_0:\beta_1=0\) (no linear dependence) and estimate \(c=\beta_1\).  
5. Compare the fitted slopes \(c\) across families; if they differ significantly, this indicates that **distribution shape modulates the scaling factor**.

---

## Hypothesis 3 – Bounded weight distributions yield tighter dispersion (smaller range/IQR) of Shapley values than unbounded distributions, even when the first two moments are matched  

**Statement**  
When all weight distributions are standardized to **identical mean and variance**, those whose support is bounded (Beta, Uniform, Dirichlet) will generate Shapley values with **smaller inter‑quartile ranges (IQR) and a narrower overall range** than distributions with unbounded support (Normal, Lognormal, Pareto).

**Why it is testable**  
* “Bounded” vs. “unbounded” is a categorical property that can be assigned before data collection.  
* IQR and range are straightforward summary statistics that can be compared with non‑parametric two‑sample tests (Kolmogorov‑Smirnov, Mann‑Whitney) or by constructing confidence intervals for the difference in IQR.

**Experiment that would test it**  
1. Calibrate six distributions to mean = 1 and variance = 0.5 (e.g. Uniform on \([a,b]\) solving the moment equations; Beta with appropriate α,β; Normal with μ=1, σ=√0.5; Lognormal solving for log‑mean/log‑sd; Pareto with scale \(x_m\) and shape α; Exponential with λ = 1/μ).  
2. Draw **10 000** weight vectors per distribution, compute the exact Shapley values.  
3. For each replication compute the **range** \(R = \max_i\phi_i - \min_i\phi_i\) and the **IQR** across the five players.  
4. Perform a **Kolmogorov‑Smirnov test** for each bounded‑vs‑unbounded pair to assess distributional differences; also compare mean IQRs with a Welch t‑test.  

---

## Hypothesis 4 – The skewness of the weight distribution is positively transferred to the skewness of the Shapley value distribution for each player  

**Statement**  
If a weight distribution is positively (negatively) skewed, the empirical Shapley value distribution for each player will also be positively (negatively) skewed, and the **magnitude** of the Shapley‑value skewness will increase monotonically with the weight‑distribution skewness.

**Why it is testable**  
* Skewness is a well‑defined moment‑based statistic (Fisher‑Pearson coefficient).  
* By selecting distributions that span a wide skewness spectrum (Beta with α < β, Normal (≈0), Exponential (positive), Lognormal (positive), Pareto (positive)) we can examine the correlation between the two skewness measures.

**Experiment that would test it**  
1. Choose **five** representative distributions covering a range of skewness:  
   - Beta(2,5) → negative skew,  
   - Normal(μ=1,σ=0.7) → ≈0,  
   - Exponential(λ=1) → positive skew,  
   - Lognormal(logμ=0,logσ=0.8) → positive skew,  
   - Pareto(α=2.5, xₘ=1) → strong positive skew.  
2. For each distribution generate **8 000** weight vectors, compute the exact Shapley values for each player, and calculate the **sample skewness** \(\hat{\gamma}_1(\phi_i)\) across replications.  
3. Compute the **population skewness** of the weight draws (or the theoretical skewness of the distribution).  
4. Run a **Spearman rank correlation** (or Pearson) between weight‑distribution skewness and the average Shapley‑value skewness across the five players; test significance at α = 0.05.  

---

## Hypothesis 5 – The empirical distribution of Shapley values converges to a normal distribution as the number of simulation draws grows, irrespective of the underlying weight‑distribution family  

**Statement**  
Because the Shapley value is a weighted sum of marginal contributions, the Central Limit Theorem predicts that, for a fixed N = 5, the **sampling distribution** of the Shapley value for each player will become increasingly Gaussian as the number of replicated games increases, even when the weights themselves are drawn from heavy‑tailed or skewed distributions.

**Why it is testable**  
* Normality can be assessed formally (Shapiro‑Wilk, Kolmogorov‑Smirnov) and informally (kurtosis approaching 3, skewness approaching 0).  
* Convergence can be tracked as a function of sample size, providing a clear falsifiable prediction (the null hypothesis of non‑normality should be rejected more often as M grows).

**Experiment that would test it**  
1. For each of the six weight distributions (Uniform, Normal, Lognormal, Exponential, Pareto, Beta) generate **sequential** sets of Shapley values for each player with **M = 500, 1 000, 2 000, 5 000, 10 000, 20 000** replicates.  
2. At each M perform a **Shapiro‑Wilk test** (or KS test) for normality on the 5 × M vector of Shapley values for each player.  
3. Record the **p‑value** (or the KS statistic) and plot it versus M; also compute the sample kurtosis and skewness.  
4. Expectation: the proportion of “non‑rejections” (p > 0.05) should rise with M, approaching 1.0 for all families, indicating convergence to normality. Deviations (e.g., heavy‑tailed families remain non‑normal even at large M) would falsify the hypothesis.  

---

### How these hypotheses extend the prior work  

* **Prior experiments** (runs 002‑004) showed *no variation* in Shapley pay‑offs because the weight models were either deterministic or trivially stochastic (simple Beta/Dirichlet/Uniform).  
* The hypotheses above deliberately **introduce non‑trivial stochasticity** (heavy tails, unbounded support, skewness) and focus on **quantitative dispersion metrics** (CV, variance, IQR, skewness) rather than on the binary properties (super‑additivity/monotonicity).  
* By keeping the **same deterministic mapping from weights to coalition values**, we isolate the **impact of the weight distribution’s shape** on the Shapley value’s statistical concentration, directly addressing the research questions about variance, heavy‑tails, and possible analytical relationships.  

These hypotheses are **specific, measurable, and statistically testable** within the computational constraints (N = 5, exact Shapley calculation, ≥ 5 000–10 000 Monte‑Carlo replicates).  Once empirical support (or refutation) is obtained, they can guide the development of a **compact analytical mapping** between input weight volatility and output Shapley‑value dispersion, satisfying the “success criteria” of the current research phase.