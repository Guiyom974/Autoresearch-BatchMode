**Hypothesis 1 – The “0.80‑scaling” is a genuine asymptotic law for the variance‑to‑mean ratio**  
*Statement:* For integers coprime to the \(k\)-th primorial \(P_{k}\), the gap‑ratio \(R(k)\) satisfies  
\[
R(k)=\alpha\;(\log P_{k})^{\beta}\qquad\text{with }\beta\approx0.80
\]  
for the whole range \(k\le 15\) (and, conjecturally, for all larger \(k\)).  

*Why it is testable:* The relationship can be expressed as a linear law in log‑log space, \(\log R(k)=\log\alpha+\beta\log\log P_{k}\).  A statistically significant linear fit with \(\beta\) in the interval \([0.76,0.84]\) would confirm the hypothesis; any value outside this interval (e.g., near 1.17) would falsify it.  

*Experiment:*  
1. Compute exact (or rigorously sampled) gap sequences for each primorial \(P_{k}\) with \(k=10,11,\dots ,15\).  
2. Use arbitrary‑precision arithmetic to obtain the exact mean and variance of the gaps, then form \(R(k)=\operatorname{Var}/\operatorname{Mean}\).  
3. Perform a weighted ordinary‑least‑squares regression of \(\log R(k)\) versus \(\log\log P_{k}\) and extract \(\beta\) together with its 95 % confidence interval.  
4. Require that the fitted \(\beta\) lie within 5 % of 0.80 and that the coefficient of determination \(R^{2}>0.98\).  

---

**Hypothesis 2 – The observed exponent is pre‑asymptotic and will drift toward 1.0 (or another limit) for larger \(k\)**  
*Statement:* The exponent \(\beta(k)\) estimated from successive windows of \(k\) is not constant but converges monotonically (or oscillates) toward a limit \(\beta_{\infty}\neq0.80\).  In particular, the “0.80” value is a transient feature that will be replaced by a larger exponent (e.g., \(\beta\to1.0\) or \(\beta\to1.17\)) as \(k\) grows beyond 15.  

*Why it is testable:* If the exponent truly changes with \(k\), the slope of \(\log R(k)\) versus \(\log\log P_{k}\) will be statistically different for early and late segments of the data.  A sequence of regressions (e.g., for \(k\in[1,9]\), \([6,12]\), \([10,15]\)) will reveal a systematic trend.  

*Experiment:*  
1. Compute \(R(k)\) for \(k=1\) up to \(15\).  
2. For each moving window of width 3–4 (e.g., \(k=1\!-\!5\), \(3\!-\!7\), \(5\!-\!9\), …, \(12\!-\!15\)), fit \(\beta\) as above.  
3. Apply a non‑parametric trend test (e.g., Mann–Kendall) to the series \(\beta(k_{\text{window}})\).  
4. If a statistically significant monotone increase (or decrease) is detected, the hypothesis is supported; otherwise it is rejected.  

---

**Hypothesis 3 – The 1.17 exponent reported in earlier work is an artifact of truncation‑induced underestimation of the variance**  
*Statement:* The truncation of gap sequences (i.e., discarding the final incomplete block of gaps) systematically under‑estimates the true variance by roughly 2.16 %.  When the correct multiplicative correction factor \(\mathcal{C}(k)=1/(1-0.0216)\) is applied, the revised exponent drops from ≈1.17 to ≈0.80.  

*Why it is testable:* The correction is a deterministic transformation of the data.  If the hypothesis is correct, applying the factor should shift the fitted exponent by a predictable amount (≈0.37) and eliminate the bias.  If the shift is absent or smaller, the hypothesis is false.  

*Experiment:*  
1. Generate the raw gap data for each primorial, compute the “raw” variance \(\sigma^{2}_{\text{raw}}\) and mean \(\mu\).  
2. Apply the truncation correction: \(\sigma^{2}_{\text{corr}}=\sigma^{2}_{\text{raw}}\times\mathcal{C}(k)\) with \(\mathcal{C}(k)=\frac{1}{1-0.0216}\).  
3. Form \(R_{\text{corr}}(k)=\sigma^{2}_{\text{corr}}/\mu\) and repeat the log‑log regression to obtain \(\beta_{\text{corr}}\).  
4. Compare \(\beta_{\text{corr}}\) to the uncorrected \(\beta_{\text{raw}}\) and to the target 0.80.  Require that the correction reduces the systematic bias to <0.5 % (i.e., \(|\beta_{\text{corr}}-0.80|<0.02\)).  

---

**Hypothesis 4 – A probabilistic model that includes **higher‑order residue correlations** analytically predicts \(\beta=0.80\)**  
*Statement:* The gap distribution among integers coprime to \(P_{k}\) is not a simple Bernoulli process; pairwise independence fails beyond the first few primes, and the cumulative effect of triple‑wise (or higher) residue interactions introduces a multiplicative factor \((\log P_{k})^{-0.20}\) that depresses the variance relative to a naïve independence model (which would give \(\beta=1.0\)).  A model that incorporates these correlations yields \(\beta=0.80\).  

*Why it is testable:* The model makes a concrete quantitative prediction for the dependence of \(R(k)\) on \(\log P_{k}\) (the exponent 0.80) **and** for the functional form of the sub‑leading term (e.g., \(R(k)=C(\log P_{k})^{0.80}\,[1+o(1)]\)).  Simulating the model (e.g., using inclusion–exclusion or a Markov‑chain representation of residue constraints) and comparing its output with the empirical data provides a direct test.  

*Experiment:*  
1. Construct an explicit probabilistic framework:  
   - Represent the set \(\{n\le N:\gcd(n,P_{k})=1\}\) as a renewal process with state space given by the residues modulo the first \(m\) primes (choose \(m=3\) for a first test).  
   - Derive the variance‑to‑mean ratio analytically (or by exact enumeration for moderate \(N\)).  
2. For each \(k=10,\dots ,15\), simulate the process for a large \(N\) (e.g., \(N=10^{6}\) times the modulus) and compute the simulated \(R_{\text{model}}(k)\).  
3. Compare the simulated exponent \(\beta_{\text{model}}\) (via log‑log regression) with the empirical \(\beta_{\text{exp}}\).  Require that \(\beta_{\text{model}}\) fall within 5 % of 0.80 and that the simulated scaling curve overlays the empirical data within their confidence bands.  

---

**Hypothesis 5 – The scaling exponent is independent of the computational method (full‑period enumeration vs. statistical sampling) and of the precision level used**  
*Statement:* The exponent \(\beta\) derived from a rigorous probabilistic sampling scheme (e.g., stratified Monte‑Carlo with controlled error < 10⁻⁶) will be statistically indistinguishable from the exponent obtained by exhaustive enumeration of all coprime gaps (where feasible).  Likewise, using arbitrary‑precision integers versus high‑precision floating‑point arithmetic will not alter the observed \(\beta\).  

*Why it is testable:* If two independent methodologies produce the same estimate of \(\beta\) within statistical error, the result is robust; divergence would indicate a methodological artifact.  

*Experiment:*  
1. **Full‑period computation (where possible):** For \(k\le10\) the primorial \(P_{k}\) is small enough to enumerate every integer up to \(P_{k}\) (or up to a few multiples) and record all gaps.  Compute \(R_{\text{exact}}(k)\).  
2. **Statistical sampling:** For the same \(k\), draw a large stratified sample (≥ 10⁷ coprime integers) and estimate \(R_{\text{sample}}(k)\) with confidence intervals via bootstrap or Hoeffding bounds.  
3. **Precision comparison:** Perform the sampling calculation using (a) arbitrary‑precision integer arithmetic (e.g., GMP) and (b) double‑precision floating‑point with a guard digit, both using the same random seed where possible.  
4. Perform a two‑sample t‑test (or a Bayesian model comparison) to assess whether the differences in \(\beta\) are less than the pre‑specified tolerance (≤ 0.02).  A non‑significant result supports the hypothesis.  

---

### Summary Table of Hypotheses

| # | Hypothesis | Core Prediction | Primary Test |
|---|------------|------------------|--------------|
| 1 | True asymptotic scaling \(R(k)\propto(\log P_k)^{0.80}\) for \(k\le15\) | \(\beta\approx0.80\) (≥ 0.98 \(R^2\)) | Log‑log regression on corrected \(R(k)\) data |
| 2 | Exponent drifts with \(k\) (pre‑asymptotic) | \(\beta(k)\) changes systematically | Moving‑window regression + trend test |
| 3 | 1.17 exponent arises from truncation bias | After correction \(\beta\) falls to ≈0.80 | Apply 2.16 % correction factor and re‑fit |
| 4 | Higher‑order residue correlations generate the 0.80 exponent | Analytic model predicts \(\beta=0.80\) | Simulate model and compare with empirical \(\beta\) |
| 5 | Exponent is method‑independent (sampling vs. exhaustive, precision) | Same \(\beta\) from multiple techniques | Cross‑method comparison with statistical equivalence test |

Each hypothesis is **falsifiable**: a statistically significant deviation from the predicted exponent, a failure to correct bias, a mismatch with a derived analytic model, or a dependence on computational methodology would constitute a rejection.  The proposed experiments directly address the three research questions (origin, asymptotic stability, and truncation impact) while building on the earlier 1.17‑exponent findings and the identified truncation artifact.