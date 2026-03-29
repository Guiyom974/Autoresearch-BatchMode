Below are **four concrete, testable hypotheses** that address the three core questions in the problem statement.  
Each hypothesis (i) states what we expect to find, (ii) explains why the claim can be examined with existing or easily‑implemented tools, and (iii) outlines a concrete numerical experiment that will either confirm or refute it.

---

## 1.  Hypothesis 1 – **Algebraic tautology in the definition of \(c_{\text{emp}}(t)\)**  

### 1.1 Statement  
The perfect‑unity result (\(c_{\text{emp}}(t)=1.000000\) with zero variance) is **not** a deep property of the LDAB model but originates from an **implicit self‑normalisation** that appears in the current formula (e.g., the numerator and denominator both contain the same LDAB‑derived quantity, or the algorithm divides by the sum of the very terms it is trying to correct).  

### 1.2 Why it is testable  
If the factor is a trivial ratio of a quantity to itself, then any *re‑definition* that decouples the numerator from the denominator must produce a non‑trivial, base‑dependent value.  The test simply compares two mathematically equivalent but algebraically distinct expressions for the correction factor.

### 1.3 Experiment  

| Step | Detail |
|------|--------|
| **a. Refactor the code** | Re‑implement \(c_{\text{emp}}(t)\) in two ways: <br>  • **Original** – keep the current algorithm exactly as used in the earlier runs.<br>  • **Alt‑Form** – rewrite the factor as \(\displaystyle \frac{\sum_{p\le t} w(p)}{\sum_{p\le t} w(p)}\) where the weight \(w(p)\) is the LDAB density, but **omit** any division by the same sum (i.e. treat the numerator as the raw LDAB count and the denominator as the *expected* count from the Prime Number Theorem for the arithmetic progression of the primorial base). |
| **b. High‑precision evaluation** | Use an arbitrary‑precision library (e.g., `mpmath` with 50‑digit precision) to evaluate both forms for the three bases (210, 2310, 30030) at log‑spaced points \(t=10^3,10^4,10^5,10^6,10^7\). |
| **c. Compare** | Record the numerical value of each form.  If the **Alt‑Form** yields values ≠ 1 (and shows variance across bases), the unity is an artefact of the original normalisation.  If it still returns 1, the tautology hypothesis is falsified. |

*Success criterion:*  The **Alt‑Form** shows a statistically significant deviation from 1 (e.g., ≥ 10⁻⁶) for at least one base.

---

## 2.  Hypothesis 2 – **The raw absolute error \(\Delta(t)=|\pi(t)-\text{LDAB}(t)|\) is non‑zero and exhibits systematic base‑dependent structure**  

### 2.1 Statement  
Even though \(c_{\text{emp}}(t)=1\), the **uncorrected** LDAB count diverges from the true prime‑counting function \(\pi(t)\).  The divergence is not random noise but follows a predictable pattern that depends on the primorial modulus (210 vs 2310 vs 30030).  

### 2.2 Why it is testable  
Absolute and relative errors are straightforward to compute once we have a reliable source for \(\pi(t)\) (e.g., a pre‑computed table or a fast prime‑counting routine).  Systematic structure can be detected with standard statistical tests (e.g., runs test, regression on \(\log t\)).  

### 2.3 Experiment  

| Step | Detail |
|------|--------|
| **a. Obtain ground‑truth \(\pi(t)\)** | Use the `primepi` function from the `sympy` library (or a static list of primes up to 10⁷) to retrieve \(\pi(t)\) at each test point. |
| **b. Compute LDAB(t)** | Run the LDAB algorithm (with the *original* definition of the correction factor, i.e. the one that produced 1.0) for each primorial base, again at the same log‑spaced \(t\) values. |
| **c. Calculate errors** | Compute \(\Delta(t)\) and the relative error \(\Delta_{\text{rel}}(t)=\Delta(t)/\pi(t)\). |
| **d. Analyse** | • Plot \(\Delta(t)\) vs. \(t\) for each base.<br>• Fit a linear regression of the form \(\Delta(t)=a\log t+b\) and test whether the coefficients differ significantly across bases (ANOVA on the residuals).<br>• Perform a runs test on the sign of \(\Delta(t)\) to check for systematic drift. |
| **e. Interpretation** | If the errors are consistently non‑zero and show distinct slopes or patterns for different bases, the unity of \(c_{\text{emp}}(t)\) is a cancellation effect. |

*Success criterion:*  Reject the null hypothesis that the error curves are identical across bases (p < 0.05) or that the mean absolute error is zero.

---

## 3.  Hypothesis 3 – **Kullback–Leibler (KL) divergence of prime‑gap distributions differs across primorial bases**  

### 3.1 Statement  
The LDAB model’s prediction of the *distribution* of prime gaps deviates from the empirical gap distribution, and the magnitude of this divergence is **base‑dependent**.  This metric is independent of the scalar correction factor and therefore can expose hidden inaccuracies.  

### 3.2 Why it is testable  
KL divergence is a well‑defined, non‑negative quantity that is zero only when two distributions are identical.  By constructing empirical gap histograms from the actual primes ≤ 10⁷ and from the LDAB‑predicted gap probabilities, we can evaluate the divergence for each base.  

### 3.3 Experiment  

| Step | Detail |
|------|--------|
| **a. Generate empirical gap list** | For each base \(B\in\{210,2310,30030\}\), extract all primes \(p\le 10^7\) that lie in the arithmetic progression \(p\equiv a \pmod{B}\) (where \(a\) is the primitive root used in the LDAB model).  Record the gaps \(g_i=p_{i+1}-p_i\). |
| **b. Compute LDAB‑predicted gap probabilities** | Using the LDAB density function \(f_B(x)\) (the local density of primes for modulus \(B\)), compute the probability that a gap falls in a bin \([g,g+\delta)\).  This can be done by integrating the LDAB density over the interval \([x, x+\delta]\) for each integer \(x\) in the range of interest. |
| **c. Estimate KL divergence** | Build normalized histograms \(P_{\text{emp}}(g)\) and \(P_{\text{LDAB}}(g)\) with a bin width \(\delta=2\) (or optimal binning).  Compute \(\displaystyle D_{\text{KL}}(P_{\text{emp}}\|P_{\text{LDAB}})=\sum_g P_{\text{emp}}(g)\log\frac{P_{\text{emp}}(g)}{P_{\text{LDAB}}(g)}\).  Use high‑precision arithmetic to avoid log(0) issues (add a tiny epsilon). |
| **d. Compare across bases** | Perform a **permutation test** or a **bootstrap** to assess whether the observed KL values differ significantly among the three bases. |
| **e. Interpretation** | A statistically significant base‑dependence would demonstrate that the LDAB model captures the gap structure differently for each modulus, confirming that the scalar factor of 1 conceals model imperfections. |

*Success criterion:*  At least one pair of bases shows a KL divergence significantly larger than the others (p < 0.05) and the divergence is > 10⁻⁴ (well above numerical noise).

---

## 4.  Hypothesis 4 – **The “correction factor” can be expressed as a non‑constant function of \(\log t\) and the primorial modulus, indicating a missing scaling term**  

### 4.1 Statement  
If the true scaling behavior of the LDAB model is \(\text{LDAB}(t)=c(t)\cdot\pi(t)\) with \(c(t)=1+\alpha\frac{\log t}{t}+O\!\big((\log t)/t^{2}\big)\), then the empirical factor appears unity only because the higher‑order terms are **masked by the current normalising procedure**.  A properly isolated estimate of \(c(t)\) will reveal a modest but systematic trend with \(t\) and with the base.  

### 4.2 Why it is testable  
Fitting a small‑parameter model to the observed ratio \(\hat c(t)=\text{LDAB}(t)/\pi(t)\) (or to the raw error) is a standard regression problem.  The functional form can be motivated by known asymptotic expansions of the Prime Number Theorem for arithmetic progressions.  

### 4.3 Experiment  

| Step | Detail |
|------|--------|
| **a. Compute raw ratio** | Using the **uncorrected** LDAB output (i.e. the quantity before the scalar division that forces 1.0), compute \(\hat c(t)=\text{LDAB}(t)/\pi(t)\) at each test point. |
| **b. Model specification** | Fit a linear mixed‑effects model: \(\hat c(t) = 1 + \beta_0 \frac{\log t}{t} + \beta_1 \frac{1}{t} + \gamma_B + \epsilon\), where \(\gamma_B\) is a random effect for each primorial base \(B\) and \(\epsilon\) is residual noise.  Use ordinary least squares (OLS) for a first pass, then a Bayesian hierarchical model if more flexibility is needed. |
| **c. Assess significance** | Test whether \(\beta_0\) (or \(\beta_1\)) is significantly different from zero (t‑test, p < 0.05).  Also test whether the base‑specific intercepts \(\gamma_B\) differ across the three bases (F‑test). |
| **d. Validate** | Use the fitted model to **predict** \(\hat c(t)\) for a hold‑out set of points (e.g., t = 2 × 10⁶, 5 × 10⁶, 9 × 10⁶) and compare predictions to the observed values. |
| **e. Interpretation** | If the model yields a non‑zero \(\beta_0\) or \(\gamma_B\) that improves prediction, we have identified a genuine scaling term that the original scalar factor suppressed. |

*Success criterion:*  The fitted coefficients for the log‑term or base‑effect are statistically significant and reduce the prediction error by at least 20 % compared with a constant‑1 model.

---

### Summary of Expected Outcomes  

| Hypothesis | What we expect to find | Key diagnostics |
|------------|------------------------|-----------------|
| **1 – Algebraic tautology** | The original factor is a self‑normalising ratio → alternative form ≠ 1 | Deviation of Alt‑Form from 1 |
| **2 – Non‑zero raw error** | Systematic, base‑dependent errors → reject “error = 0” | ANOVA on Δ(t) curves |
| **3 – KL gap divergence** | Base‑dependent KL → hidden model flaw | Significant KL differences |
| **4 – Missing scaling term** | \(\hat c(t)=1+\beta_0\frac{\log t}{t}+…\) → non‑zero β₀ | Regression significance |

Each hypothesis is **self‑contained**, uses **high‑precision arithmetic** (to avoid machine‑epsilon artefacts), stays **within the prescribed data bound \(t\le10^7\)**, and **does not introduce unrelated sieve methods**.  Running the four experiments in the order listed will efficiently isolate whether the unity of \(c_{\text{emp}}(t)\) is a mathematical artefact, a computational rounding issue, or a genuine asymptotic property of the LDAB model.