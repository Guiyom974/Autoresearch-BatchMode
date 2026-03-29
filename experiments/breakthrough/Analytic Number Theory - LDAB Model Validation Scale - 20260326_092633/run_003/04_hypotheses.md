

**Research Problem Overview**  
Empirical counts of primes modulo 210 show a clear Chebyshev‑bias (more primes in non‑quadratic‑residue (NR) than in quadratic‑residue (QR) classes), yet a naïve chi‑square Goodness‑of‑Fit test returns a perfect‑fit p‑value of 1.0.  
The goal is to build a **variance‑covariance model** that (i) uses the true asymptotic variance of primes in arithmetic progressions (derived from Dirichlet L‑function zeros), (ii) replaces natural density \(\pi(x)\) by logarithmic density \(\delta(x)=\sum_{p\le x}1/p\) (or \(1/\log p\)), and (iii) delivers a test that reliably detects the bias for \(X=5\,000\,000\) (and for the larger primorial modulus 2310).

Below are **five mutually complementary, testable hypotheses** that address the paradox and the required methodological advances.

---

## 1.  Hypothesis – *The p = 1.0 anomaly stems from a gross under‑estimate of the per‑class variance*

**Hypothesis statement**  
The standard chi‑square statistic for the prime race modulo 210 is artificially small because the usual Poisson/multinomial variance assumption **severely underestimates** the true variance of \(\pi(x;q,a)\). Consequently the ratio  
\[
\chi^2_{\text{naïve}} \;=\; \sum_{a\in(\mathbb Z/210\mathbb Z)^\times}
\frac{(\text{obs}_a-\text{exp}_a)^2}{\text{exp}_a}
\]  
yields a value far below the critical value for any reasonable degrees of freedom, producing \(p\approx1\).

**Why it is testable**  
We can directly compute the **observed variance** of the excess counts \(E_a(x)=\pi(x;210,a)-\frac{\pi(x)}{\phi(210)}\) over many independent intervals (e.g., sliding windows of length \(10^5\) up to \(X\)) and compare it with the Poisson variance \(\sigma^2_{\text{Pois}}=\text{exp}_a\). If the empirical variance is orders of magnitude larger, the hypothesis is confirmed.

**Experiment**  

1. **Data generation:** List all primes \(\le5\,000\,000\).  
2. **Interval sampling:** Partition \([2,5\,000\,000]\) into 50 non‑overlapping blocks of length \(100\,000\). For each block compute the excess count \(E_a\) for every admissible residue class \(a\) modulo 210.  
3. **Variance estimation:** Calculate the sample variance \(\hat\sigma^2_a\) of the 50 excess values for each \(a\).  
4. **Comparison:** Plot \(\hat\sigma^2_a\) against the Poisson estimate \(\text{exp}_a/\)block‑size. Compute the ratio \(R_a=\hat\sigma^2_a / (\text{exp}_a/\)block‑size\().  
5. **Decision rule:** If the median of \(R_a\) across the \(\phi(210)=48\) classes exceeds 10 (or any pre‑specified threshold), reject the Poisson variance assumption and accept the hypothesis.

*Outcome:* A dramatically larger empirical variance would explain why the naïve \(\chi^2\) statistic collapses.

---

## 2.  Hypothesis – *The true asymptotic variance grows like \(\log\log x\) and can be expressed through L‑function zeros*

**Hypothesis statement**  
For a fixed modulus \(q\) and a non‑principal Dirichlet character \(\chi\), the variance of the normalized prime count in the progression \(a \pmod q\) satisfies  
\[
\operatorname{Var}\bigl(\pi(x;q,a)\bigr)
\;=\;
C_q\,\log\log x \;+\; o(\log\log x),
\]  
where the constant \(C_q\) is explicitly given by a sum over the non‑trivial zeros \(\rho= \tfrac12 + i\gamma\) of the associated Dirichlet L‑function:
\[
C_q \;=\;
\frac{2}{\phi(q)^2}\sum_{\chi\neq\chi_0}\;
\sum_{\gamma>0}
\frac{1}{\bigl|\rho\bigr|^{2}}\,
\Re\!\bigl(\chi(a)\,\overline{\chi(b)}\bigr),
\]  
with \(b\) any reference class (e.g., \(b=1\)).  

**Why it is testable**  
We can (i) compute the theoretical prediction \(C_{210}\log\log X\) using a numerically evaluated series of L‑zeros (available in databases such as L‑MF and the OEIS), and (ii) compare it with the **empirical variance** obtained from the sliding‑window experiment of Hypothesis 1. The two should agree to within sampling error if the hypothesis is correct.

**Experiment**  

1. **Theoretical constant:** Using the first 10 000 non‑trivial zeros of each non‑principal L‑function modulo 210 (computed via *mpmath* or *Sage*), evaluate the series above to obtain \(C_{210}\).  
2. **Empirical variance:** From the 50 block variance estimates of Hypothesis 1, compute the average variance \(\bar\sigma^2\) across the 48 residue classes.  
3. **Scaling test:** Plot \(\bar\sigma^2\) versus \(\log\log X\) for several upper bounds \(X\) (e.g., \(10^5, 10^6, 5\times10^6\)). Fit a linear regression \(\bar\sigma^2 = A + B\log\log X\).  
4. **Compare constants:** Check whether the fitted slope \(B\) coincides (within 95 % confidence intervals) with the theoretical constant \(C_{210}\).  

*Outcome:* A linear relationship with slope matching \(C_{210}\) would confirm the \(\log\log x\) scaling predicted by Rubinstein–Sarnak.

---

## 3.  Hypothesis – *Switching from natural density \(\pi(x)\) to logarithmic density \(\delta(x)\) amplifies the early‑term bias and yields a detectable signal*

**Hypothesis statement**  
Because the Chebyshev bias originates primarily from the *early* primes (where \(\frac1p\) is large), weighting each prime by \(1/p\) (or \(1/\log p\)) concentrates the analysis on the region where the bias is strongest. A Goodness‑of‑Fit test built on the **logarithmic density**  
\[
\delta(x;210,a)=\sum_{\substack{p\le x\\ p\equiv a\;(\bmod 210)}}\frac1p
\]  
will produce a test statistic that is substantially larger than the one based on raw counts, allowing rejection of the uniform hypothesis at the conventional \(\alpha=0.05\) level for \(X=5\,000\,000\).

**Why it is testable**  
We can construct both a *natural‑density* and a *log‑density* version of the same chi‑square‑type statistic, apply them to the same prime data set, and compare the resulting p‑values. If the log‑density version yields a dramatically lower p‑value, the hypothesis is supported.

**Experiment**  

1. **Compute \(\delta(x;210,a)\):** For each admissible class \(a\), accumulate the reciprocals \(\frac1p\) for all primes \(p\le5\,000\,000\).  
2. **Define expected log‑density:** Under the uniform (no‑bias) null, the expected logarithmic density for each class is \(\frac{1}{\phi(210)}\delta(x)\), where \(\delta(x)=\sum_{p\le x}\frac1p\).  
3. **Construct test statistic:**  
   \[
   \chi^2_{\log}\;=\;\sum_{a}
   \frac{\bigl(\delta_{\text{obs}}(x;210,a)-\delta_{\text{exp}}(x;210,a)\bigr)^2}
        {\operatorname{Var}\bigl(\delta(x;210,a)\bigr)},
   \]  
   where the variance term is estimated from the L‑function zero formula (Hypothesis 2) applied to the logarithmic weighting.  
4. **Obtain p‑values:** Using the asymptotic distribution (either a \(\chi^2_{48-1}\) or a Monte‑Carlo null built by permuting prime assignments), compute p‑values for both the raw‑count and the log‑density versions.  
5. **Decision:** If the log‑density p‑value is \(<0.05\) while the raw‑count p‑value remains \(>0.5\), the hypothesis is validated.  

*Outcome:* A much smaller p‑value for the log‑density statistic demonstrates that the weighting scheme recovers the hidden bias.

---

## 4.  Hypothesis – *A full variance‑covariance matrix that includes off‑diagonal (inter‑class) terms yields a test statistic that follows a non‑central \(\chi^2\) distribution, producing a significant p‑value*

**Hypothesis statement**  
The counts \(\pi(x;210,a)\) for different residue classes are **mutually correlated** because all share the overall prime pool. The true covariance matrix \(\Sigma\) has off‑diagonal entries \(\Sigma_{ab}= -\frac{2}{\phi(210)^2}\sum_{\chi\neq\chi_0}\sum_{\gamma>0}\frac{\Re(\chi(a)\overline{\chi(b)})}{|\rho|^{2}}\) (the same L‑function sum as in Hypothesis 2).  
A *corrected* Goodness‑of‑Fit statistic defined as  
\[
T \;=\; \mathbf{d}^{\!\top}\,\Sigma^{-1}\,\mathbf{d},
\qquad 
\mathbf{d}_a = \pi_{\text{obs}}(x;210,a)-\pi_{\text{exp}}(x;210,a),
\]  
will be asymptotically \(\chi^2_{48-1}(\lambda)\) with a non‑centrality parameter \(\lambda>0\) reflecting the Rubinstein–Sarnak bias. For \(X=5\,000\,000\) this yields a *significant* departure from uniformity (p < 0.05).

**Why it is testable**  
We can (i) numerically compute \(\Sigma\) using the L‑function zero data, (ii) evaluate the quadratic form \(T\) on the observed excess vector, (iii) compare the distribution of \(T\) under the null (obtained by simulation of independent Poisson counts with the same covariance structure) with its observed value. If the observed \(T\) lies in the upper 5 % tail, the hypothesis is accepted.

**Experiment**  

1. **Build \(\Sigma\):** Using the first 5 000 zeros of each non‑principal Dirichlet L‑function modulo 210, compute the full \(48\times48\) covariance matrix with the formula above (precision ~\(10^{-6}\)).  
2. **Compute observed excess vector:** \(\mathbf{d} = \bigl(\pi(x;210,a)-\frac{\pi(x)}{48}\bigr)_{a\in(\mathbb Z/210)^\times}\).  
3. **Evaluate test statistic:** \(T_{\text{obs}} = \mathbf{d}^{\!\top}\Sigma^{-1}\mathbf{d}\).  
4. **Null simulation:**  
   - Generate 10 000 synthetic data sets where each data set consists of a multinomial draw of \(\pi(x)\) primes into the 48 classes with *means* \(\frac{\pi(x)}{48}\) and *covariance* \(\Sigma\).  
   - For each synthetic draw compute the corresponding \(T\).  
5. **p‑value:** The proportion of simulated \(T\) exceeding \(T_{\text{obs}}\) is the empirical p‑value.  

*Outcome:* A p‑value below 0.05 confirms that accounting for inter‑class correlation reveals the bias.

---

## 5.  Hypothesis – *The bias detected with modulus 210 is not an artifact of that particular modulus; the same corrected test will also reject uniformity for modulus 2310*

**Hypothesis statement**  
The Chebyshev bias (NR > QR) is a **universal** phenomenon for all primorial moduli \(q\) for which the corresponding Dirichlet L‑functions have at least one non‑principal character. Consequently, applying the variance‑covariance‑corrected test (Hypothesis 4) to primes modulo 2310 (\(\phi(2310)=480\)) will again produce a significant p‑value (< 0.05) at the same data size \(X=5\,000\,000\).

**Why it is testable**  
We can repeat the entire pipeline of Hypothesis 4 for the larger modulus \(q=2310\) and observe whether the p‑value remains significant. The theoretical covariance matrix for \(q=2310\) can be built from the L‑functions modulo 2310, and the same quadratic form \(T\) can be computed.

**Experiment**  

1. **Prime list up to 5 000 000:** Identify all primes \(\le5\,000\,000\).  
2. **Compute excess vector:** For each of the 480 admissible residue classes modulo 2310, calculate \(\mathbf{d}_a\).  
3. **Construct covariance matrix \(\Sigma_{2310}\):** Using the same zero‑sum methodology as in Hypothesis 4 (now summing over the non‑principal characters modulo 2310).  
4. **Evaluate \(T_{2310}\):** Compute the quadratic form with the inverse of \(\Sigma_{2310}\).  
5. **Null simulation for 2310:** Generate 10 000 synthetic multinomial draws with mean \(\frac{\pi(X)}{480}\) and covariance \(\Sigma_{2310}\). Obtain an empirical p‑value.  
6. **Decision:** If the p‑value < 0.05, the hypothesis is supported, confirming universality of the bias.

*Outcome:* A comparable significance level for both moduli would demonstrate that the detected bias is a genuine feature of prime distributions in any primorial base, not a peculiarity of 210.

---

### How the Five Hypotheses Form a Coherent Research Plan

| Step | Hypothesis | Core Idea | Primary Evidence |
|------|------------|-----------|-------------------|
| 1 | **Under‑estimated variance** | Naïve \(\chi^2\) uses wrong variance → p = 1.0. | Empirical variance ≫ Poisson variance. |
| 2 | **Log‑log variance scaling** | True variance ∝ \(\log\log x\) (L‑function zeros). | Fit slope ≈ theoretical constant \(C_q\). |
| 3 | **Log‑density weighting** | Weighting by \(1/p\) (or \(1/\log p\)) highlights early bias. | Log‑density statistic yields p < 0.05, raw‑count does not. |
| 4 | **Covariance‑aware statistic** | Off‑diagonal covariances produce non‑central \(\chi^2\). | Corrected test rejects uniformity for 210 at p < 0.05. |
| 5 | **Universality across primorials** | Same bias appears for larger modulus 2310. | Significant p‑value repeats for \(q=2310\). |

Together, these hypotheses provide a **complete, testable roadmap**:  
1. Diagnose why the naïve test fails.  
2. Replace the variance model with a theoretically grounded, \(\log\log x\)‑scaling covariance matrix derived from L‑function zeros.  
3. Adopt a logarithmic density measure that accentuates the early‑prime bias.  
4. Build a new test statistic that incorporates the full covariance structure and demonstrates statistical significance for the observed data.  
5. Verify that the improvement is not a one‑off by confirming the effect for a second primorial modulus.

Each hypothesis is **operationalizable**—it can be examined with existing prime tables (up to 5 million) and modern computational algebra systems that provide high‑precision values of Dirichlet L‑function zeros. The experimental designs above are concrete, replicable, and directly address the research questions laid out in the problem statement.