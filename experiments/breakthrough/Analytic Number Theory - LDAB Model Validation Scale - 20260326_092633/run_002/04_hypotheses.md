

Below are four concrete, testable hypotheses that speak directly to the methodological goals of the project.  Each hypothesis is written in a form that can be evaluated with a concrete experiment (i.e., a well‑defined data set, a clear statistical test, and an unambiguous criterion for success/failure).

---

## Hypothesis 1 – Corrected expected frequencies give a **better fit** than the naïve uniform model  

**Statement**  
For the primes \(p\le X\) (with \(X=5\,000\,000\) and later \(X=10\,000\,000\)), the Goodness‑of‑Fit statistic  
\[
\chi^{2}_{\text{cor}}=\sum_{a\;(\bmod q)}\frac{\bigl(N_{X}(a)-\widehat{E}_{X}(a)\bigr)^{2}}{\widehat{E}_{X}(a)},
\]  
where \(\widehat{E}_{X}(a)=\operatorname{Li}(X)/\phi(q)\) is the Dirichlet‑approximation expected count and \(N_{X}(a)\) is the observed count of primes in class \(a\), will be **smaller** (i.e. will have a larger p‑value) than the corresponding \(\chi^{2}_{\text{uni}}\) obtained under the assumption of a uniform prior \(\widehat{E}_{X}^{\text{uni}}(a)=\#\{a\} \cdot \pi(X)/q\).

**Why it is testable**  
* The quantities \(N_{X}(a)\) can be enumerated directly from a prime table (e.g., using a segmented sieve).  
* The Dirichlet approximation \(\operatorname{Li}(X)/\phi(q)\) is a deterministic function of \(X\) and the modulus \(q\); thus \(\widehat{E}_{X}(a)\) is known exactly before the experiment.  
* Both \(\chi^{2}\) statistics are *real numbers* that can be compared statistically; a paired Wilcoxon signed‑rank test or a simple bootstrap on the two statistics will tell us whether the reduction is significant.

**Experiment**  
1. Generate the list of all primes \(\le 5\,000\,000\).  
2. For each modulus \(q\in\{210,2310\}\) and each residue class \(a\) coprime to \(q\), count \(N_{X}(a)\).  
3. Compute \(\widehat{E}_{X}(a)\) and \(\widehat{E}_{X}^{\text{uni}}(a)\).  
4. Calculate \(\chi^{2}_{\text{cor}}\) and \(\chi^{2}_{\text{uni}}\).  
5. Repeat the whole procedure on an independent set of the same size drawn from the next interval \(5\,000\,000<p\le10\,000\,000\).  
6. Use a paired comparison (or a bootstrap) to test whether \(\chi^{2}_{\text{cor}}<\chi^{2}_{\text{uni}}\) with a pre‑specified \(\alpha=0.05\).

---

## Hypothesis 2 – Under the corrected model the **NR – QR prime‑count differences are centered at zero**  

**Statement**  
Define for each modulus \(q\) the signed difference  
\[
\Delta_{X}^{\text{QR/NR}}=N_{X}(\text{QR})-N_{X}(\text{NR}),
\]  
where “QR’’ aggregates all quadratic‑residue classes and “NR’’ all quadratic‑non‑residue classes (both modulo \(q\)).  Under the Dirichlet‑approximation expected frequencies, the sampling distribution of \(\Delta_{X}\) (after standardising by its theoretical standard deviation \(\sigma_{\Delta}\)) will converge to a **standard normal distribution** as \(X\) grows.

**Why it is testable**  
* The expected value of \(\Delta_{X}\) under the model is exactly zero because \(\sum_{a\in\text{QR}}1=\sum_{a\in\text{NR}}1=\phi(q)/2\).  
* The variance \(\sigma_{\Delta}^{2}\) can be derived analytically from the independence of prime counts across residue classes (or estimated by Monte‑Carlo simulation).  
* One can directly compare the empirical distribution of \(\Delta_{X}/\sigma_{\Delta}\) to a normal CDF (e.g., Kolmogorov–Smirnov test).

**Experiment**  
1. For \(q=210\) and \(q=2310\), compute the observed \(\Delta_{X}\) for a series of increasing cut‑offs \(X_{1}=10^{5}, X_{2}=5\times10^{5}, X_{3}=10^{6}, \dots, X_{10}=5\times10^{6}\).  
2. For each \(X_i\) calculate the standard deviate \(Z_i=\Delta_{X_i}/\widehat{\sigma}_{\Delta}(X_i)\) where \(\widehat{\sigma}_{\Delta}\) is either the analytic variance or the bootstrap estimate.  
3. Perform a Kolmogorov–Smirnov test of the set \(\{Z_i\}\) against the standard normal distribution.  
4. Additionally, simulate 10 000 synthetic prime‑data sets (by sampling from the Dirichlet model) and overlay the empirical quantiles of \(\Delta\) to visualise convergence.

---

## Hypothesis 3 – **Grouping sparse residue classes** (minimum‑count threshold) stabilises the chi‑square test without destroying the QR/NR signal  

**Statement**  
When a minimum‑expected‑count threshold of \(E_{\min}=5\) is imposed, any class with \(\widehat{E}_{X}(a)<5\) is merged with a neighbour class of the same parity (QR or NR) to form a *pooled* group.  After this grouping, the resulting chi‑square statistic \(\chi^{2}_{\text{grp}}\) will have:  

* (a) **fewer degrees of freedom** (by the number of groups eliminated), and  
* (b) **greater statistical power** (i.e., a higher probability of correctly rejecting the null of no bias) than the un‑grouped test, while still preserving the QR versus NR distinction.

**Why it is testable**  
* The grouping rule is deterministic (once the threshold is fixed).  
* The degrees‑of‑freedom loss can be counted exactly, and the corresponding critical chi‑square value can be looked up.  
* Power can be estimated by Monte‑Carlo simulation under a true‑bias alternative (e.g., a small additive term \(\delta\) to the NR probabilities).

**Experiment**  
1. Using the same prime list up to \(5\,000\,000\), compute the expected counts \(\widehat{E}(a)\) for each residue class modulo \(210\) and \(2310\).  
2. Identify all classes with \(\widehat{E}(a)<5\); for each such class, create a pooled class by merging it with the nearest class of the same quadratic character (QR or NR).  
3. Compute \(\chi^{2}_{\text{grp}}\) on the grouped contingency table, noting the reduced degrees of freedom.  
4. Run a simulation study: generate 5 000 synthetic data sets from a model that imposes a modest NR bias (e.g., shift each NR probability by \(+0.5\%\)).  For each synthetic set, apply both the un‑grouped and the grouped chi‑square tests and record the rejection rates.  
5. Compare the two rejection rates with a two‑sample proportion test to confirm that grouping does **not** lower power (ideally it should increase it).

---

## Hypothesis 4 – The **Chebyshev‑type bias modulo 210 and 2310 remains statistically significant** after the corrected methodology  

**Statement**  
After implementing (i) the Dirichlet‑approximation expected frequencies, (ii) the \(E_{\min}=5\) grouping rule, and (iii) a properly calibrated chi‑square test (or an exact Fisher‑exact test for any remaining sparse cells), the null hypothesis  

\[
H_{0}:\; N_{X}(\text{NR})=N_{X}(\text{QR})\quad\text{(no bias)}
\]  

will be **rejected at the 5 % level** for the empirical data set with \(X=5\,000\,000\).

**Why it is testable**  
* The null is a precise statement about equality of two aggregated counts, which can be evaluated directly from the data.  
* The alternative (bias) is one‑sided in the direction predicted by Chebyshev (preference for NR), so a one‑tailed test can be used.  
* The p‑value is a well‑defined random variable; replicating the analysis on an independent larger data set (e.g., up to \(10^{7}\)) provides a validation check.

**Experiment**  
1. Using the corrected expected frequencies and the grouping strategy, build the full contingency table for each modulus.  
2. Compute the chi‑square statistic (or, for any remaining cells with expected counts still <5, use an exact Fisher‑exact test) to obtain a p‑value.  
3. Compare the p‑value to the pre‑chosen significance level \(\alpha=0.05\).  
4. To assess robustness, repeat the entire pipeline on a second, independent prime interval (e.g., \(5\,000\,001\le p\le10\,000\,000\)).  The bias should again be significant, and the p‑values should be of the same order of magnitude (allowing for random fluctuation).  
5. As a further check, compute the *effect size* (e.g., Cramér’s \(V\) or the difference in proportions) and verify it is consistent with the theoretical bias magnitude predicted by Rubinstein‑Sarnak.

---

### How to Use These Hypotheses

| Hypothesis | Primary Statistical Tool | Desired Outcome |
|------------|--------------------------|-----------------|
| 1 – Better fit of corrected expectations | Paired χ² comparison (or bootstrap) | Smaller χ², larger p‑value for corrected model |
| 2 – Normal‑distributed NR‑QR differences | Kolmogorov‑Smirnov test vs. N(0,1) | Non‑significant KS statistic; QQ‑plot aligns with diagonal |
| 3 – Grouping stabilises & preserves power | Monte‑Carlo power simulation | Grouped test rejects at ≥ same rate as un‑grouped, with fewer df |
| 4 – Bias remains significant after correction | χ² (or exact) Goodness‑of‑Fit with corrected expectations | Rejection of \(H_{0}\) at \(\alpha=0.05\); consistent result on independent data set |

If each of these hypotheses is supported by the empirical evidence, the study will have demonstrated a **rigorous, mathematically grounded statistical framework** for evaluating Chebyshev bias in the primorial bases 210 and 2310, satisfying all of the success criteria outlined in the problem statement.