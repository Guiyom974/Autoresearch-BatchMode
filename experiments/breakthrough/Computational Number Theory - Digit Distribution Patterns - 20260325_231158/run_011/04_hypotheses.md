

**Testable Hypotheses for the “Logarithmic Density & Prime‑Gap Corrections” Research Problem**  

Below are five concrete, computationally testable hypotheses that directly address the three research questions (Benford‑deviation origin, logarithmic‑density correction, and gap‑adjustment added value).  For each hypothesis we state the idea, explain why it can be examined with a finite data set, and outline the concrete numerical experiment that would accept or reject it.

---

### Hypothesis 1 – *Logarithmic‑Density‑Adjusted Benford (LDAB) model outperforms standard Benford’s Law*  

**1. Hypothesis statement**  
Integrating the prime‑density function \(1/\ln x\) over the base‑210 digit intervals (the LDAB model) yields predicted leading‑digit frequencies that are statistically closer to the empirical prime distribution than the classic Benford formula \(\log_{210}(1+1/d)\).  Consequently the KL‑divergence between the LDAB predictions and the observed frequencies will be **significantly lower** than the baseline value of ≈ 0.64.

**2. Why it is testable**  
* We can generate a large, exact list of primes (e.g. up to \(10^8\) or \(10^9\)) with a fast sieve.  
* For each leading digit \(d\in[1,209]\) we can evaluate the integral  

\[
P_{\text{LDAB}}(d)=\sum_{k=1}^{K}\int_{d\cdot210^{k-1}}^{(d+1)\cdot210^{k-1}}\frac{1}{\ln x}\,dx
\]

by numeric quadrature (or by summing the discrete approximation \(1/\ln n\) over the same range).  
* The KL‑divergence  

\[
D_{\text{KL}}(P_{\text{obs}}\|P_{\text{LDAB}})=\sum_{d}P_{\text{obs}}(d)\log\frac{P_{\text{obs}}(d)}{P_{\text{LDAB}}(d)}
\]

is a well‑defined, non‑negative scalar that can be computed directly from the empirical frequencies \(P_{\text{obs}}(d)\).

**3. Experiment that would test it**  
1. **Data generation** – Use a segmented sieve to collect all primes ≤ \(N\) (try several \(N\) such as \(10^6,10^7,10^8,10^9\)).  
2. **Empirical histogram** – Convert each prime to base‑210, record the first “digit” (most‑significant non‑zero symbol) and tally the relative frequencies \(P_{\text{obs}}(d)\).  
3. **LDAB prediction** – For each \(d\) compute \(P_{\text{LDAB}}(d)\) by the integral sum described above (choose a modest \(K\) such that \(210^{K}\approx N\)).  
4. **Comparison** – Calculate the KL‑divergence for both the standard Benford model and the LDAB model.  Use a bootstrap (or a chi‑square goodness‑of‑fit test) to assess whether the LDAB KL is statistically smaller (e.g. at the 5 % level).  

*Expected outcome:* The LDAB KL should fall well below 0.64 (perhaps around 0.2–0.3) and the chi‑square p‑value should favour the LDAB model.

---

### Hypothesis 2 – *Adding explicit prime‑gap scaling further reduces KL‑divergence*  

**1. Hypothesis statement**  
For each leading digit \(d\) the average gap between consecutive primes whose base‑210 representation starts with \(d\) is larger (or smaller) than the overall average gap.  Multiplying the LDAB probability of \(d\) by a **gap‑adjustment factor**  

\[
g_d = \frac{\text{mean gap for digit }d}{\text{overall mean gap}}
\]

produces a “LDAB + Gap” model whose KL‑divergence is **even lower** than the unadjusted LDAB model.

**2. Why it is testable**  
* The mean gap for each digit is a simple aggregate statistic that can be computed from the same prime list used in Hypothesis 1.  
* The adjustment factor is a deterministic, data‑driven scaling; once computed we can recompute the predicted distribution and re‑evaluate the KL‑divergence.  
* The statistical significance of the improvement can be assessed with a paired comparison (e.g., a Wilcoxon signed‑rank test on KL values across many random sub‑samples).

**3. Experiment that would test it**  
1. **From the prime list** – For each digit \(d\) compute the list of gaps \(\Delta_i = p_{i+1}-p_i\) for all primes whose first base‑210 digit equals \(d\).  Compute the mean gap \(\bar\Delta_d\) and the overall mean \(\bar\Delta\).  
2. **Gap scaling** – Set \(g_d = \bar\Delta_d/\bar\Delta\).  Define the adjusted probability  

   \[
   P_{\text{LDAB+GAP}}(d) = g_d\;P_{\text{LDAB}}(d)\quad\text{followed by normalisation.}
   \]  

3. **KL evaluation** – Compute the KL‑divergence \(D_{\text{KL}}(P_{\text{obs}}\|P_{\text{LDAB+GAP}})\).  
4. **Statistical test** – Compare this KL with the LDAB KL using a paired t‑test (or non‑parametric analogue) on the two values obtained from several independent prime intervals (e.g., sliding windows of length \(10^6\)).  

*Expected outcome:* The LDAB + Gap model should shave off another 0.05–0.10 units of KL, with the improvement significant at the 5 % level.

---

### Hypothesis 3 – *The KL‑gain from the logarithmic‑density correction grows with the magnitude of the data set*  

**1. Hypothesis statement**  
Because the PNT‐derived thinning (\(1/\ln x\)) becomes increasingly accurate as numbers get larger, the reduction in KL‑divergence achieved by the LDAB model (relative to Benford) should **increase monotonically** with the upper bound \(N\) of the prime sample.  In other words, the “logarithmic thinning” explanation for the Benford deviation is **magnitude‑dependent**.

**2. Why it is testable**  
* We can generate prime lists for a series of increasing caps \(N_1 < N_2 < \dots < N_M\) (e.g. \(10^5,10^6,\dots,10^9\)).  
* For each cap we can compute both the Benford KL and the LDAB KL.  
* A trend test (e.g., Spearman rank correlation or linear regression of KL‑reduction on \(\log N\)) can reveal whether the improvement grows as predicted.

**3. Experiment that would test it**  
1. **Multi‑scale prime generation** – Produce independent prime sets for \(N = 10^5, 10^6, 10^7, 10^8, 10^9\).  
2. **Compute both KLs** – For each \(N\) record \(D_{\text{KL}}^{\text{Benford}}(N)\) and \(D_{\text{KL}}^{\text{LDAB}}(N)\).  
3. **Trend analysis** – Plot the difference \(\Delta D(N) = D_{\text{KL}}^{\text{Benford}} - D_{\text{KL}}^{\text{LDAB}}\) versus \(\log N\).  Perform a Spearman correlation (or a linear regression) to test whether \(\Delta D\) increases significantly with \(\log N\).  

*Expected outcome:* A statistically significant positive trend (p < 0.05) confirming that larger samples show a larger “logarithmic thinning” benefit.

---

### Hypothesis 4 – *The gap‑adjustment factor is linearly correlated with the average prime‑gap size for each leading digit*  

**1. Hypothesis statement**  
If the average gap for numbers beginning with digit \(d\) is larger (smaller) than the global average, then the probability mass that LDAB assigns to \(d\) is **over‑(under‑)estimated**.  The optimal adjustment factor \(g_d^{\text{opt}}\) scales **linearly** with \(\bar\Delta_d\); i.e.  

\[
g_d^{\text{opt}} = a\,\bar\Delta_d + b
\]  

for some constants \(a,b\) that are independent of the sample size.

**2. Why it is testable**  
* We can obtain an empirical estimate of the optimal factor for each digit by minimizing the KL‑divergence (or by a simple grid search) for a given data set.  
* We can then test the linear relationship between these optimal factors and the measured \(\bar\Delta_d\) using standard regression diagnostics.

**3. Experiment that would test it**  
1. **Collect data** – For each digit \(d\) compute both \(\bar\Delta_d\) (mean empirical gap) and the optimal scaling factor \(g_d^{\text{opt}}\) that yields the smallest KL when applied to the LDAB probabilities.  The optimal factor can be found by a one‑parameter line search (or by solving the analytic condition for minimum KL).  
2. **Regression** – Fit the linear model \(g_d^{\text{opt}} = a\,\bar\Delta_d + b\) and evaluate the goodness‑of‑fit (R², residual analysis).  
3. **Cross‑validation** – Use a separate prime interval (e.g., primes between \(10^8\) and \(2\times10^8\)) to see whether the same linear relationship holds.  

*Expected outcome:* A high correlation (R² > 0.8) and non‑zero slope, indicating that the gap‑adjustment can be predicted from the simple statistic \(\bar\Delta_d\).

---

### Hypothesis 5 – *The LDAB + Gap model yields lower KL‑divergence in other primorial bases (e.g., base‑30, base‑2310), demonstrating a universal correction mechanism*  

**1. Hypothesis statement**  
The improvements observed in base‑210 are not an artefact of that particular base.  When the same LDAB + Gap methodology is applied to primes expressed in **any primorial base** (base‑30, base‑210, base‑2310, …), the resulting KL‑divergence will be **lower than the corresponding Benford baseline** for that base, and the reduction will be of comparable magnitude.

**2. Why it is testable**  
* The mathematical construction of the LDAB model relies only on the intervals defined by the leading digit in the chosen base, which is straightforward to replicate for any integer base.  
* Gap statistics can be collected in exactly the same way for each base.  
* KL‑divergence is base‑independent and can be compared directly.

**3. Experiment that would test it**  
1. **Select bases** – Choose three primorial bases: 30 (= 2·3·5), 210 (= 2·3·5·7) and 2310 (= 2·3·5·7·11).  
2. **Prime generation** – Produce a single large prime list (e.g., up to \(10^8\); the same list can be used for all bases).  
3. **Per‑base analysis** – For each base:  
   - Convert the prime list to that base and record the empirical leading‑digit frequencies.  
   - Compute the standard Benford KL for that base.  
   - Build the LDAB probabilities by integrating \(1/\ln x\) over the appropriate digit intervals.  
   - Compute the gap‑adjustment factors as in Hypothesis 2 and obtain the LDAB + Gap KL.  
4. **Statistical comparison** – For each base, perform a paired t‑test (or a Wilcoxon test) on the KL values obtained from several random sub‑samples of the prime list to test whether the LDAB + Gap KL is significantly lower than the Benford KL.  

*Expected outcome:* Across all three bases the LDAB + Gap model yields a KL‑reduction that is statistically significant (p < 0.05) and of similar magnitude (e.g., a drop of 0.3–0.5 units), supporting the universality of the correction mechanism.

---

#### Summary of Experimental Workflow
| Step | Action | Output |
|------|--------|--------|
| 1 | Generate primes up to \(10^9\) using a segmented sieve | Exact prime list \(P\) |
| 2 | Convert \(P\) to base‑210 (and optionally to bases 30, 2310) | List of leading‑digit observations |
| 3 | Compute empirical frequencies \(P_{\text{obs}}(d)\) | Observed distribution |
| 4 | Implement LDAB integration (log‑density) | \(P_{\text{LDAB}}(d)\) |
| 5 | Compute gap statistics → gap factors \(g_d\) | Gap‑adjusted distribution \(P_{\text{LDAB+GAP}}(d)\) |
| 6 | Evaluate KL‑divergence for **Benford**, **LDAB**, **LDAB + Gap** | Scalar KL values |
| 7 | Perform statistical tests (chi‑square, bootstrap, trend tests, regression) | p‑values, confidence intervals |
| 8 | Repeat for multiple bases and magnitude caps | Cross‑base and scale‑dependence evidence |

Each hypothesis can be **directly examined** with the above workflow, providing quantitative evidence (KL reductions, p‑values, regression coefficients) that either supports or refutes the proposed mechanisms of logarithmic thinning and prime‑gap corrections.