**Premise**

The earlier series of runs ( run 005–007 ) showed that ordinary double‑precision arithmetic can mask a true growth of the variance‑to‑mean ratio \(R(k)\) through floating‑point under‑overflow and that, when arbitrary‑precision arithmetic is used, the observed variance differential follows a \((\log P_{k})^{1.17}\) scaling.  
Those observations were, however, obtained on *truncated* linear intervals and therefore may still be contaminated by the boundary‑effects that the present project wants to eliminate.  

Below are **four** testable hypotheses that (i) build directly on the prior findings, (ii) stay strictly within the scope of primorial‑gap statistics for \(k=1\ldots9\), and (iii) are designed to be answered with the exact periodic gap sequences described in the methodology.

---

## Hypothesis 1 – **Boundary‑truncation bias scales with the relative interval length**

**Statement**  
For each primorial \(P_{k}\) the bias introduced by using a finite linear interval of length \(L\) (with \(1\ll L<P_{k}\)) instead of the full period can be approximated by  

\[
\mathrm{Bias}\bigl[R_{\text{naive}}(k;L)\bigr]\;=\;\frac{c_{k}}{L/P_{k}}\;+\;O\!\bigl((L/P_{k})^{2}\bigr),
\]

where the constant \(c_{k}\) depends only on the *shape* of the gap‑distribution of the \(k\)‑th primorial and **not** on the absolute size of \(P_{k}\).

**Why it is testable**  
* We can generate the exact circular gap list for every \(k\) (size \(\phi(P_{k})\le 223 092 870\)).  
* By sliding a window of length \(L\) over the *linear* copy of that list we can compute the naive estimator \(R_{\text{naive}}(k;L)\) for any prescribed \(L\).  
* The true periodic value \(R_{\text{true}}(k)\) is obtained from the full circular list. The difference \(\Delta R = R_{\text{naive}}-R_{\text{true}}\) can therefore be measured directly.

**Experiment**  

1. **Exact gap generation** – for each \(k=1\ldots9\) produce the sorted list of integers \(1\le n\le P_{k}\) that are coprime to \(P_{k}\).  
2. **Compute the periodic baseline** – using the circular variance formula (see §2 of the methodology) obtain \(R_{\text{true}}(k)\).  
3. **Window sampling** – for each \(k\) draw 500 random starting points \(s\) and cut the linear interval \([s,\,s+L-1]\) for the following lengths:  
   \[
   L \in \{0.01P_{k},\;0.05P_{k},\;0.10P_{k},\;0.25P_{k},\;0.50P_{k},\;0.75P_{k}\}.
   \]  
4. **Naïve estimate** – on each window compute the ordinary sample mean \(\hat\mu\) and sample variance \(\hat\sigma^{2}\) (no wrap‑around) and form \(\hat R = \hat\sigma^{2}/\hat\mu\).  
5. **Bias extraction** – for each \((k,L)\) average the differences \(\Delta R = \hat R - R_{\text{true}}(k)\) over the 500 windows, then plot \(\Delta R\) versus \(L/P_{k}\).  
6. **Fit** – perform a linear regression \(\Delta R = c_{k}\,(P_{k}/L) + d_{k}\,(P_{k}/L)^{2}\) to test the predicted scaling and to estimate \(c_{k}\).

*Success criterion*: a coefficient of determination \(R^{2}>0.95\) for the leading term confirms the hypothesis.

---

## Hypothesis 2 – **A periodic (circular) variance estimator removes the length‑dependence and meets the ≤10⁻⁴ stability target**

**Statement**  
When \(R(k)\) is recomputed with a *circular* variance estimator—i.e. using the true period mean \(\mu_{k}\) and the sum \(\sum_{i=1}^{\phi(P_{k})}(g_{i}-\mu_{k})^{2}\) divided by \(\phi(P_{k})\)—the resulting value is independent of the window start or length and its sampling variance across arbitrarily chosen sub‑intervals of the period is **< 10⁻⁴**.

**Why it is testable**  
* The exact circular gap sequence is known, so the population mean \(\mu_{k}\) and the population variance \(\sigma^{2}_{k}\) can be calculated exactly (no sampling error).  
* By *artificially* slicing the period into overlapping windows of any length we can treat the circular estimator exactly on each slice and measure the spread of the obtained \(R\) values.

**Experiment**  

1. **Circular estimator definition** – for a window of length \(w\) (expressed as a number of gaps) centred at position \(t\) on the circle, define  
   \[
   R_{\text{circ}}(k;t,w)=\frac{\displaystyle\frac{1}{w}\sum_{i=0}^{w-1}(g_{t+i}-\mu_{k})^{2}}{\displaystyle\frac{1}{w}\sum_{i=0}^{w-1}g_{t+i}} .
   \]  
   (All indices are taken modulo \(\phi(P_{k})\).)  
2. **Window set** – for each \(k\) choose \(w\) = 0.05 · \(\phi(P_{k})\), 0.10 · \(\phi(P_{k})\), 0.25 · \(\phi(P_{k})\) and generate 1 000 random start positions \(t\).  
3. **Stability test** – compute the *empirical variance* of the 1 000 values \(\{R_{\text{circ}}(k;t,w)\}\) for each \((k,w)\).  
4. **Comparison** – also compute the naïve linear estimator on the same windows and show that its variance is orders of magnitude larger.

*Success criterion*: For **all** combinations of \(k\) and \(w\) the empirical variance of \(R_{\text{circ}}\) is < 10⁻⁴, while the naïve variance exceeds this threshold by at least two orders of magnitude.

---

## Hypothesis 3 – **After boundary correction, the true periodic \(R(k)\) follows a \((\log P_{k})^{\alpha}\) growth with \(\alpha\approx1.17\)**

**Statement**  
The exact periodic variance‑to‑mean ratio for primorial gaps satisfies  

\[
R_{\text{true}}(k)=A\;(\log P_{k})^{\alpha}+B,\qquad\text{with } \alpha\approx1.17,
\]

where the exponent \(\alpha\) is *the same* as the scaling uncovered in the earlier arbitrary‑precision runs (run 007) and \(A,B\) are constants that are independent of \(k\).

**Why it is testable**  
* The prior finding already suggested the scaling, but it was obtained on a truncated data set.  
* With the exact periodic values \(R_{\text{true}}(k)\) we can perform a rigorous log‑log regression and test whether \(\alpha\) stays at 1.17.

**Experiment**  

1. **Obtain \(R_{\text{true}}(k)\)** – as described in Hypothesis 2, compute the circular variance‑to‑mean ratio for each \(k=1\ldots9\).  
2. **Fit the model** – use non‑linear least squares (or a linear fit on \(\log R\) vs. \(\log\log P_{k}\)) to estimate \(\alpha\), \(A\), and \(B\).  
3. **Statistical validation** –  
   * compute the residual standard error;  
   * perform a *bootstrap* (10 000 resamples) on the nine data points to obtain a 95 % confidence interval for \(\alpha\);  
   * compare the fitted \(\alpha\) to the prior value 1.17 using a two‑sided t‑test.  

*Success criterion*: The 95 % CI for \(\alpha\) includes 1.17 **and** the coefficient of determination \(R^{2}>0.90\).

---

## Hypothesis 4 – **Corrected \(R(k)\) is **not** invariant; it exhibits a statistically significant monotonic increase with \(k\)**  

**Statement**  
After the boundary‑artifact correction (circular estimator) the sequence \(\{R_{\text{true}}(k)\}_{k=1}^{9}\) shows a **significant upward trend**, contradicting the null hypothesis that \(R(k)\) is constant (the “baseline invariance” model).

**Why it is testable**  
* The nine values are independent across different primorials.  
* Standard non‑parametric trend tests (Mann‑Kendall, Spearman ρ) can be applied directly to the exact \(R_{\text{true}}(k)\) series.

**Experiment**  

1. **Data** – the nine exact periodic ratios obtained in Hypothesis 3.  
2. **Trend tests** –  
   * **Mann‑Kendall** statistic \(S\) with its variance under the null of no trend;  
   * **Spearman** rank correlation coefficient \(\rho\).  
3. **Monte‑Carlo reference** – generate 10 000 surrogate series by *bootstrapping* the nine gaps (reshuffling the gap vectors) to obtain the null distribution of \(S\) and \(\rho\);  
4. **Significance** – compare the observed \(S\) and \(\rho\) to the 95th percentile of the null distribution.

*Success criterion*: Both the Mann‑Kendall and Spearman tests reject the null of invariance at the 5 % level (p < 0.05).

---

## Hypothesis 5 – **Truncating the maximum admissible gap introduces an exponential bias that can be analytically corrected**

**Statement**  
If gaps larger than a threshold \(T\) are discarded (as often happens when the data set is “maximum‑gap‑capped”), the resulting biased ratio obeys  

\[
R_{\text{trunc}}(k;T)=R_{\text{true}}(k)-C_{k}\,\exp(-\lambda_{k} T)+o\!\bigl(e^{-\lambda_{k}T}\bigr),
\]

where \(\lambda_{k}>0\) is the tail‑decay rate of the empirical gap‑distribution for the \(k\)‑th primorial and \(C_{k}\) is a constant that depends on the moments of the tail.

**Why it is testable**  
* By varying \(T\) (e.g., \(T=10,20,30,\dots,200\) for each \(k\)) we can observe the bias directly and fit the exponential model.

**Experiment**  

1. **Full periodic gap list** – for each \(k\) keep the complete list of gaps (no truncation).  
2. **Threshold series** – for a grid of thresholds \(T\) (10 – 200 in steps of 5) compute the sample variance and mean using **only** gaps \(\le T\). Obtain \(R_{\text{trunc}}(k;T)\).  
3. **Tail‑rate estimation** – fit an exponential tail \(\Pr[G> t]\approx e^{-\lambda_{k} t}\) to the upper 20 % of the gap distribution (least‑squares on log‑histogram).  
4. **Bias correction** – for each \(k\) and each \(T\) compute the correction term \(C_{k}e^{-\lambda_{k}T}\) by regressing \(\bigl(R_{\text{true}}(k)-R_{\text{trunc}}(k;T)\bigr)\) on \(e^{-\lambda_{k}T}\).  
5. **Validation** – apply the fitted correction to the *truncated* values and compare the corrected \(R\) to the true periodic \(R_{\text{true}}(k)\); the residual error should be < 10⁻⁶.

*Success criterion*: The exponential model explains > 95 % of the variance of the bias across the whole threshold range and the corrected values recover the true periodic ratio within numerical noise.

---

### How the hypotheses fit together

| Hypothesis | Primary focus | Builds on prior work? |
|------------|---------------|------------------------|
| 1 | Quantify the *size* of the boundary‑truncation bias | Directly addresses the “boundary‑effects” question (R.Q. 1) |
| 2 | Provide a **stable, artifact‑free** estimator (≤10⁻⁴) | Satisfies the *Robust estimator* requirement (R.Q. 2) |
| 3 | Identify the **true scaling law** of \(R(k)\) after correction | Uses the arbitrary‑precision scaling insight from run 007 |
| 4 | Test the **invariance claim** of the baseline model | Directly answers R.Q. 3 (does corrected \(R(k)\) stay flat?) |
| 5 | Quantify and correct the **maximum‑gap‑truncation** bias | Extends the methodology to another source of systematic error |

All four (or five) hypotheses are **operationally testable** with the exact periodic gap sequences for \(k=1\ldots9\) and with the computational resources allowed (full generation of ≤ 223 million integers, use of arbitrary‑precision integers where needed to avoid the floating‑point under‑flow problem identified in run 005‑007).  

Once each hypothesis is validated, the resulting **artifact‑free, stable estimator** can be applied to the previously collected data sets, delivering the *definitive conclusion* on whether the variance‑to‑mean ratio of primorial gap distributions truly grows or remains invariant as \(k\) increases.