**Overall context**  
- Prior work showed that the usual KL‑divergence never drops below ≈10⁻⁴ for the standard Adaptive LDAB Calibration (especially for the large primorial bases 210, 2310, 30030).  
- The same work hinted that “non‑uniform residue‑class weighting” and a more robust divergence metric (e.g. Earth‑Mover’s/Wasserstein distance) could resolve the apparent instability.  
- No experiment to date has actually **computed** the Wasserstein distance for these bases or measured the impact of a principled weighting scheme.

Below are **3 – 5** concrete, testable hypotheses that directly build on those insights and are designed to be answered with the data‑generation and metric‑evaluation pipeline already described in the problem statement.

---

## Hypothesis 1 – *Metric‑robustness of the Wasserstein distance*  

**Statement**  
*The 1‑D Wasserstein distance (Earth‑Mover’s distance) between the empirical residue‑class distribution of primes up to \(x\) and the LDAB‑predicted distribution will show a monotonically decreasing trend as the prime bound \(x\) increases from \(10^{5}\) to \(2\times10^{6}\) for each primorial base (210, 2310, 30030).*

**Why it is testable**  
*   The Wasserstein distance can be computed directly with SciPy’s `wasserstein_distance` on the two discrete probability vectors (empirical vs. LDAB).  
*   By generating primes up to several cut‑offs and evaluating the distance at each cut‑off we obtain a time‑series that can be inspected for monotonicity.

**Experiment that would test it**  
1. **Data generation** – produce the list of primes ≤ 2 × 10⁶, assign each prime to its valid residue class modulo 210, 2310 and 30030, and build the empirical frequency vector \(\hat{p}_r(x)\) for each base at 10 logarithmically spaced cut‑offs (e.g. \(x = 10^{5}, 2\times10^{5}, \dots, 2\times10^{6}\)).  
2. **Model prediction** – compute the LDAB‑predicted distribution \(q_r(x)\) for the same cut‑offs using the current LDAB formalism.  
3. **Metric evaluation** – for each base and each cut‑off, calculate  
   \[
   W(x)=\text{wasserstein\_distance}(\hat{p}(x),\,q(x)).
   \]  
4. **Trend analysis** – plot \(W(x)\) vs. \(x\) and apply a simple linear regression or a Mann‑Kendall trend test to verify that the slope is negative and statistically significant (p < 0.05).  

*Outcome*: a clear, measurable asymptotic decline (or at least non‑increase) of \(W(x)\) would confirm that the LDAB model captures the macroscopic prime‑distribution behavior once the proper metric is used.

---

## Hypothesis 2 – *Efficacy of non‑uniform residue‑class weighting*  

**Statement**  
*Applying a non‑uniform weighting scheme that accounts for the multiplicative order and known Chebyshev‑type prime biases of each residue class will reduce the Wasserstein distance for the largest base (30030) by at least **15 %** relative to the naive uniform‑weight assumption.*

**Why it is testable**  
*   The weighting scheme can be implemented as a deterministic transformation of the predicted vector \(q_r\) (e.g. \(q_r^{\text{w}} = w_r\,q_r\) with \(\sum w_r q_r =1\)).  
*   The same empirical data set can be evaluated twice—once with uniform weights and once with the new weights—allowing a direct, paired comparison.

**Experiment that would test it**  
1. **Define the weight function** – for each residue class \(r\) modulo 30030, compute a weight \(w_r = f(\text{ord}_r,\,B_r)\) where \(\text{ord}_r\) is the multiplicative order of the generator of the class and \(B_r\) is a bias coefficient derived from known prime‑gap statistics (e.g., Chebyshev’s bias).  
2. **Re‑compute LDAB predictions** – multiply the uniform LDAB vector \(q_r(x)\) by \(w_r\) and renormalise to obtain the weighted prediction \(q_r^{\text{w}}(x)\).  
3. **Compute distances** – for each cut‑off \(x\) in the same set as Hypothesis 1, evaluate both  
   \[
   W_{\text{unif}}(x)=\text{wasserstein\_distance}(\hat{p}(x),\,q^{\text{unif}}(x)),\\
   W_{\text{weight}}(x)=\text{wasserstein\_distance}(\hat{p}(x),\,q^{\text{w}}(x)).
   \]  
4. **Quantify improvement** – calculate the percentage reduction \(\Delta W(x)=\frac{W_{\text{unif}}(x)-W_{\text{weight}}(x)}{W_{\text{unif}}(x)}\) and test whether the average reduction across the 10 cut‑offs exceeds 15 % using a one‑sample t‑test (null hypothesis: mean reduction ≤ 15 %).  

*Outcome*: a statistically significant mean reduction ≥ 15 % would validate the weighting hypothesis and satisfy the “Success Criterion 2” from the problem statement.

---

## Hypothesis 3 – *Statistical significance of the weighting benefit*  

**Statement**  
*The reduction in Wasserstein distance achieved by the non‑uniform weighting scheme (Hypothesis 2) is not an artifact of a single prime‑generation run; it will be reproducible across multiple independent Monte‑Carlo replicates of prime generation (e.g., using different random seeds for the sliding‑window selection of residues).*

**Why it is testable**  
*   The prime list up to a fixed bound is deterministic, but the *empirical* distribution can be “sampled” by randomly sub‑sampling the residue windows (e.g., take a random 80 % subset of the residues). Repeating this yields a distribution of Wasserstein distances that can be subjected to a standard two‑sample test.

**Experiment that would test it**  
1. **Resample the empirical data** – generate 30 independent sub‑samples of the empirical residue distribution by randomly selecting 80 % of the residues for each primorial base.  
2. **Compute paired distances** – for each sub‑sample, evaluate both \(W_{\text{unif}}\) and \(W_{\text{weight}}\) as in Hypothesis 2.  
3. **Statistical test** – perform a paired Wilcoxon signed‑rank test (or a paired t‑test if normality holds) on the 30 paired differences \(\Delta W_i\). The null hypothesis is that the median reduction is ≤ 0.  
4. **Report effect size** – calculate Cohen’s d or rank‑biserial correlation to gauge the magnitude of the weighting effect.

*Outcome*: a p‑value < 0.05 with a moderate-to‑large effect size would confirm that the 15 % reduction is robust and not due to lucky sampling.

---

## Hypothesis 4 – *Metric‑specific failure of KL divergence versus LDAB correctness*  

**Statement**  
*The inability of KL divergence to converge (observed in earlier runs) is a limitation of the metric, not a fundamental flaw in the LDAB density estimates; consequently, when the same data are evaluated with the Wasserstein distance (with or without weighting), the LDAB predictions will show clear convergence, whereas KL divergence will remain erratic.*

**Why it is testable**  
*   Both metrics can be computed on identical data sets; the contrasting behavior can be demonstrated by a side‑by‑side analysis.

**Experiment that would test it**  
1. **Dual‑metric evaluation** – for each primorial base and each cut‑off \(x\), compute both  
   \[
   D_{\text{KL}}(x)=D_{\text{KL}}(\hat{p}(x)\|q(x)),\qquad
   W(x)=\text{wasserstein\_distance}(\hat{p}(x),\,q(x)).
   \]  
   (KL divergence can be calculated with `scipy.special.rel_entr` or `scipy.stats.entropy`; Wasserstein as before.)  
2. **Visual and quantitative comparison** – produce overlay plots of \(D_{\text{KL}}(x)\) and \(W(x)\) versus \(x\).  
3. **Convergence criteria** – define “convergence” as a decline of at least two orders of magnitude (or a slope significantly negative) over the range of \(x\). Apply a linear‑regression‑based trend test to each series.  
4. **Interpret** – if only the Wasserstein series meets the convergence criterion, the hypothesis is supported.

*Outcome*: demonstration that the LDAB model is sound and that the previous KL‑failure was metric‑specific, satisfying “Success Criterion 3”.

---

## Hypothesis 5 – *Scalability of the weighted LDAB beyond the original bound*  

**Statement**  
*The weighted LDAB model (using the non‑uniform weights from Hypothesis 2) will retain a Wasserstein distance that is ≤ 5 % of the uniform‑weight distance when the prime bound is increased to \(5\times10^{6}\), indicating that the weighting scheme improves robustness for larger data sets.*

**Why it is testable**  
*   The same algorithmic pipeline can be re‑run with a larger prime bound; the ratio of distances provides a direct scalability metric.

**Experiment that would test it**  
1. **Extended prime generation** – generate all primes ≤ 5 × 10⁶ (or the maximum feasible within the computational budget).  
2. **Recompute weighted and uniform predictions** – for base 30030, produce both \(q^{\text{unif}}(5\text{M})\) and \(q^{\text{w}}(5\text{M})\).  
3. **Distance evaluation** – compute the Wasserstein distances \(W_{\text{unif}}(5\text{M})\) and \(W_{\text{weight}}(5\text{M})\).  
4. **Ratio test** – verify that  
   \[
   \frac{W_{\text{weight}}(5\text{M})}{W_{\text{unif}}(5\text{M})}\le 0.95.
   \]  
   Additionally, compare the absolute values to the 2 × 10⁶ results to confirm that both distances do not explode (i.e., they stay within a factor of 2 of the smaller‑\(x\) values).

*Outcome*: a relative reduction ≤ 5 % (i.e., a 95 % retention of the improvement) would show that the weighting scheme scales gracefully, satisfying the “Computational Limits” constraint while extending the validation range.

---

### How these hypotheses together address the research questions

| Research Question | Hypothesis(s) | Core Evidence |
|--------------------|---------------|---------------|
| **Metric Robustness** – Does the Wasserstein distance outperform KL? | H1, H4 | Monotonic decline of \(W(x)\) vs. erratic \(D_{\text{KL}}(x)\); statistical trend tests. |
| **Residue Weighting** – Can non‑uniform weighting improve the model? | H2, H3 | ≥15 % reduction in \(W\) for base 30030; reproducible across resamples (p < 0.05). |
| **Asymptotic Stabilization** – Does the model converge? | H1, H5 | Clear drop of \(W(x)\) as \(x→2\)–\(5\) × 10⁶; ratio test shows sustained improvement. |
| **Robustness Validation** – Is the prior KL failure metric‑specific? | H4 | Direct dual‑metric comparison proves LDAB correctness. |
| **Scalability** – Does the method stay feasible for larger bounds? | H5 | Feasible run at 5 × 10⁶; no metric explosion. |

These hypotheses are **specific, measurable, and directly testable** with the tools already prescribed (prime generation, SciPy’s `wasserstein_distance`, and standard statistical tests). They build on the earlier findings (KL divergence failure, need for weighting) without duplicating prior experiments, and they collectively satisfy the three success criteria outlined in the problem statement.