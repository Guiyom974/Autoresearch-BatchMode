

Below are five concrete, testable hypotheses that together address the three research questions in the problem statement.  
Each hypothesis is given as a clear, falsifiable claim, followed by a short explanation of *why* the claim can be examined with data and a description of the *exact computational experiment* that would provide the evidence.

---

## 1.  The ~0.19 KL divergence of the **standard** LDAB model is fully explained by the exclusion of non‑coprime leading digits.

**Hypothesis statement**  
For a primorial base \(b=P_{k}\) (e.g. 30, 210, 2310, 30030) the probability mass that the standard LDAB model assigns to any digit \(d\) with \(\gcd(d,b)>1\) is *lost* in the empirical distribution of prime leading digits. Consequently, the Kullback‑Leibler divergence between the **standard** LDAB predictions and the true empirical distribution is exactly the divergence that arises from renormalising the standard probabilities over the *allowed* digit set  

\[
\mathcal{D}_{b}=\{d\in\{1,\dots ,b-1\}:\gcd(d,b)=1\}.
\]

In symbols  

\[
\operatorname{KL}\!\bigl(P_{\text{std}}\;\|\;P_{\text{restricted}}\bigr)\;\approx\;0.19
\qquad\text{for all }b\in\{30,210,2310,30030\}.
\]

**Why it is testable**  
The set \(\mathcal{D}_{b}\) and the standard LDAB probabilities \(P_{\text{std}}(d)=\log_{b}(1+1/d)\) are known analytically. We can therefore compute the “restricted’’ distribution  

\[
P_{\text{restricted}}(d)=\frac{P_{\text{std}}(d)}{\sum_{e\in\mathcal{D}_{b}}P_{\text{std}}(e)},
\qquad d\in\mathcal{D}_{b},
\]

and evaluate the KL divergence between the two *theoretical* distributions without ever touching real primes. If the computed value matches the empirical ≈0.19, the hypothesis is supported.

**Experiment**  

1. For each base \(b\in\{30,210,2310,30030\}\)  
   * List the allowed digits \(\mathcal{D}_{b}\) (those with \(\gcd(d,b)=1\)).  
   * Compute \(P_{\text{std}}(d)=\log_{b}(1+1/d)\) for all \(d=1,\dots ,b-1\).  
   * Form \(P_{\text{restricted}}(d)\) by normalising \(P_{\text{std}}\) over \(\mathcal{D}_{b}\) only.  
2. Evaluate  

   \[
   \operatorname{KL}\!\bigl(P_{\text{restricted}}\;\|\;P_{\text{std}}\bigr)
   =\sum_{d\in\mathcal{D}_{b}}P_{\text{restricted}}(d)\,
     \ln\!\frac{P_{\text{restricted}}(d)}{P_{\text{std}}(d)} .
   \]

3. Compare the resulting KL values to the previously observed ≈0.19.  
   *A match (within 0.01) for every base confirms the hypothesis; a systematic deviation would indicate additional factors.*

---

## 2.  The **Restricted‑Digit LDAB** model (renormalised over \(\mathcal{D}_{b}\)) reduces the KL divergence to **< 0.01** for all listed primorial bases.

**Hypothesis statement**  
When the LDAB probabilities are recomputed only over the digit set \(\mathcal{D}_{b}\) (i.e. the *restricted* model), the resulting predictive distribution \(P_{\text{RD‑LDAB}}\) will agree with the empirical leading‑digit distribution of primes (up to \(10^{8}\)) so closely that  

\[
\operatorname{KL}\!\bigl(P_{\text{obs}}\;\|\;P_{\text{RD‑LDAB}}\bigr)<0.01
\quad\text{for every }b\in\{30,210,2310,30030\}.
\]

**Why it is testable**  
Both the predictive distribution \(P_{\text{RD‑LDAB}}\) (analytic) and the empirical distribution \(P_{\text{obs}}\) (observable by computation) are finite, discrete probability vectors. Their KL divergence can be calculated directly, providing a quantitative measure of model fit.

**Experiment**  

1. **Prime generation** – use a segmented sieve to list all primes \(\le 10^{8}\).  
2. **Base conversion** – for each prime \(p\) and each base \(b\) convert to its base‑\(b\) representation and record the most‑significant digit \(d(p,b)\).  
3. **Empirical frequencies** – for each base, count the occurrences of each allowed digit and form the observed probability vector \(P_{\text{obs}}(d)=\#\{p:d(p,b)=d\}/\#\{p\}\).  
4. **Model probabilities** – compute \(P_{\text{RD‑LDAB}}(d)=\log_{b}(1+1/d)/\sum_{e\in\mathcal{D}_{b}}\log_{b}(1+1/e)\).  
5. **KL calculation** – evaluate  

   \[
   \operatorname{KL}\!\bigl(P_{\text{obs}}\;\|\;P_{\text{RD‑LDAB}}\bigr)
   =\sum_{d\in\mathcal{D}_{b}}P_{\text{obs}}(d)\,\ln\!\frac{P_{\text{obs}}(d)}{P_{\text{RD‑LDAB}}(d)} .
   \]

6. **Decision rule** – if the KL is < 0.01 for **all** four bases, the hypothesis holds; otherwise note which bases fail and by how much.

---

## 3.  The KL divergence of the **standard** LDAB model is asymptotically **constant** (≈ 0.19) and does **not** shrink with larger prime samples.

**Hypothesis statement**  
Because the discrepancy originates from a *structural* constraint (the forbidden digit set) that is independent of sample size, the KL divergence between the standard LDAB predictions and the empirical leading‑digit distribution will *stabilise* at ≈ 0.19 as the number of primes examined grows.

Formally,

\[
\lim_{N\to\infty}\operatorname{KL}_{N}\!\bigl(P_{\text{obs}}^{(N)}\;\|\;P_{\text{std}}\bigr)=0.19,
\]

where \(\operatorname{KL}_{N}\) denotes the KL computed from the first \(N\) primes (or all primes ≤ \(N\)).

**Why it is testable**  
We can compute the KL divergence for a range of upper limits \(N\) (e.g. \(10^{6},10^{7},10^{8},\dots\)). If the values converge to a non‑zero constant, the hypothesis is confirmed.

**Experiment**  

1. Generate primes up to \(10^{6},10^{7},10^{8}\) (and, if resources allow, \(10^{9}\)).  
2. For each limit \(N\) and each base \(b\), extract leading digits and form \(P_{\text{obs}}^{(N)}\).  
3. Compute \(\operatorname{KL}_{N}= \operatorname{KL}(P_{\text{obs}}^{(N)}\|P_{\text{std}})\) using the *standard* LDAB probabilities.  
4. Plot \(\operatorname{KL}_{N}\) versus \(\log N\). A horizontal asymptote near 0.19 confirms the hypothesis; a trend toward zero would reject it.

---

## 4.  The KL divergence under the **Restricted‑Digit LDAB** model **decreases monotonically** as the primorial base grows (i.e. larger bases give a better fit).

**Hypothesis statement**  
Larger primorial bases contain a higher proportion of allowed digits (|𝒟𝑏| grows), so the renormalisation correction becomes smaller and the predicted distribution approaches the empirical one more accurately. Consequently,

\[
\operatorname{KL}\!\bigl(P_{\text{obs}}\;\|\;P_{\text{RD‑LDAB}}(b_{1})\bigr)
\;>\;
\operatorname{KL}\!\bigl(P_{\text{obs}}\;\|\;P_{\text{RD‑LDAB}}(b_{2})\bigr)
\qquad\text{whenever }b_{1}<b_{2}.
\]

**Why it is testable**  
We can compute the KL for each base using the restricted model (as in Hypothesis 2) and compare the numerical values. The ordering can be tested statistically (e.g., a Spearman rank correlation between base size and KL).

**Experiment**  

1. Perform the steps of Hypothesis 2 for all four bases.  
2. Record the KL value for each base.  
3. Test monotonicity:  
   * Compute the Spearman correlation coefficient ρ between the base index (or \(\log b\)) and the KL values.  
   * A significantly negative ρ (p < 0.05) supports the hypothesis.  
   * Additionally, visualise the trend with a bar‑plot or line‑plot of KL vs. base.

---

## 5.  The KL divergence of the **Restricted‑Digit LDAB** model tends **to zero** as the prime‑sample size increases without bound.

**Hypothesis statement**  
Because the restricted model *exactly* encodes the structural constraint of primorial coprimality, the empirical frequencies should converge to the model’s predictions as more primes are observed. In the limit,

\[
\lim_{N\to\infty}\operatorname{KL}_{N}\!\bigl(P_{\text{obs}}^{(N)}\;\|\;P_{\text{RD‑LDAB}}\bigr)=0 .
\]

**Why it is testable**  
We can repeatedly compute the KL for increasing \(N\) (as in Hypothesis 3) but now using the *restricted* probabilities. If the KL sequence decays to zero, the hypothesis is supported.

**Experiment**  

1. Using the same prime lists as in Hypothesis 3 (up to at least \(10^{8}\) and preferably beyond), compute the empirical leading‑digit distributions for each \(N\).  
2. For each \(N\) compute the restricted‑model probabilities \(P_{\text{RD‑LDAB}}\) (they are independent of \(N\)).  
3. Evaluate \(\operatorname{KL}_{N}= \operatorname{KL}(P_{\text{obs}}^{(N)}\|P_{\text{RD‑LDAB}})\).  
4. Fit a simple decay model (e.g. \(\operatorname{KL}_{N}\approx c/\ln N\) or \(\operatorname{KL}_{N}\approx c/N^{\alpha}\)) and test whether the fitted constant \(c>0\) and whether the predicted limit at infinite \(N\) is zero.  
   *A statistically significant decline to near‑zero (e.g. KL < 10⁻⁴ at the largest \(N\) examined) confirms the hypothesis.*

---

### How these hypotheses address the research questions

| Research Question | Relevant Hypothesis(s) |
|-------------------|------------------------|
| **Source of the ~0.19 deviation** | H1 (analytic origin) |
| **How to reformulate LDAB for primorial bases** | H2 (new restricted‑digit model) |
| **Does the refined model work across all bases?** | H2 (KL < 0.01) |
| **Scalability / asymptotic behavior** | H3 (standard model stays wrong), H4 (larger bases improve fit), H5 (restricted model converges) |

Together, they provide a concrete, stepwise programme:

1. **Verify** the cause (H1).  
2. **Build** the corrected model (H2).  
3. **Validate** its performance and limits (H3–H5).  

All experiments are computationally feasible with a modern PC (a few hundred gigabytes of RAM for the sieve up to \(10^{8}\) and modest CPU time for base conversion) and rely only on standard number‑theoretic operations, making the hypotheses directly testable within the project’s scope.