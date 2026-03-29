Below are five **testable** hypotheses that directly extend the already‑validated “small‑base‑210 / 10⁵‑prime” results to the next stage of the project (bases 2310 and 30030, primes up to 10⁷).  Each hypothesis builds on the prior findings (guarded log‑γ, λ≈0.8 decay, well‑behaved cₑₘₚ(t) for base 210) and is phrased so that it can be falsified with the data the methodology will generate.

---

## Hypothesis 1 – **Baseline scaling of the asymptotic limit with the primorial**

**Statement**  
For each primorial base \(P_k\) (\(k=4,5,6\)) the empirical correction factor converges to a **base‑specific limit**  

\[
L_k \;=\;\lim_{t\to\infty}c_{\text{emp}}(t;P_k)
\]

and that limit varies smoothly with the size of the base:

\[
L_k \;=\;\alpha \;+\;\beta\,\ln P_k \qquad(\alpha,\beta\in\mathbb{R}).
\]

**Why it is testable**  
If the limit exists, we can estimate it by fitting a short‑range asymptotic model (e.g. \(c_{\text{emp}}(t)=L_k+A\,e^{-\lambda t}+ \varepsilon\)) to the tail of each \(c_{\text{emp}}(t)\) series (e.g. the last 2 × 10⁶ primes).  The resulting estimates \(\hat L_4,\hat L_5,\hat L_6\) are ordinary real numbers that can be regressed against \(\ln P_k\).

**Experiment**  

1. **Compute** \(c_{\text{emp}}(t)\) for the three bases at the full range \(t\le10^7\) using the validated guarded log‑γ algorithm and 10 000‑prime sliding windows.  
2. **Fit** the exponential‑decay model to the last 20 % of each series (≈2 × 10⁶ primes) to obtain \(\hat L_k\) and its standard error.  
3. **Perform** ordinary least‑squares regression of \(\hat L_k\) on \(\ln P_k\).  
   *Accept the hypothesis* if the slope \(\beta\) is significantly different from zero (p < 0.05) and the residuals are consistent with a normal distribution (Shapiro‑Wilk test).  

*Connection to prior work*: the earlier observation that \(c_{\text{emp}}(t)\) is already finite and positive for base 210 suggests a well‑defined limit exists; the new data will reveal whether that limit grows (or shrinks) monotonically with \(\ln P_k\).

---

## Hypothesis 2 – **Variance reduction with larger primorial bases**

**Statement**  
The **window‑to‑window variance** of the correction factor decreases as the primorial gets larger, following an inverse‑power law

\[
\operatorname{Var}_k \;\propto\; P_k^{-\gamma},
\]

with an exponent \(\gamma>0\).

**Why it is testable**  
Variance is a straightforward statistic we can compute for each base at any given \(t\).  By plotting \(\log\operatorname{Var}_k\) versus \(\log P_k\) we can estimate \(\gamma\) and test its significance.

**Experiment**  

1. For each base, compute the **sample variance** of \(c_{\text{emp}}(t)\) across all 10 000‑prime windows covering the interval \([5\times10^6,\,10^7]\) (≈500 windows).  
2. Take logarithms and fit a linear model  

   \[
   \log\operatorname{Var}_k = \delta - \gamma \log P_k + \eta .
   \]  

3. Test \(H_0:\gamma=0\) versus \(H_a:\gamma>0\) (one‑sided t‑test).  

*Prior support*: The earlier 1 000‑prime window study on base 210 already hinted at smoother behavior for larger windows; we now examine whether the effect persists across bases.

---

## Hypothesis 3 – **Exponential convergence rate matches the truncation‑error decay (λ≈0.8)**

**Statement**  
The **approach** of the correction factor to its limit follows an exponential law with a decay constant **identical to the λ≈0.8 observed for the asymptotic truncation error** of the high‑order LDAB expansion:

\[
c_{\text{emp}}(t;P_k) = L_k + A_k\,\exp\!\big(-\lambda\,t\big) + \varepsilon_t,
\qquad \lambda\approx0.8 .
\]

**Why it is testable**  
If the same λ governs both the series‑truncation error (already measured in run 041) and the empirical convergence of \(c_{\text{emp}}(t)\), we can estimate λ from the empirical trajectories and compare it to the previously reported value using a two‑sample t‑test.

**Experiment**  

1. **Fit** the exponential‑decay model (including λ as a free parameter) to each base’s \(c_{\text{emp}}(t)\) series, restricting the fit to the region where the curve is still visibly decaying (e.g. \(t\in[10^5,5\times10^6]\)).  
2. **Obtain** \(\hat\lambda_k\) and its 95 % confidence interval for \(k=4,5,6\).  
3. **Test** the null hypothesis \(H_0:\hat\lambda_k = 0.8\) for each base (t‑test).  
4. **Aggregate** the estimates (pooled or meta‑analysis) to assess overall consistency with λ≈0.8.

*Rationale*: If λ truly matches, it would suggest a unified error‑generation mechanism (truncation ↔ finite‑sample bias) and would provide a theoretical anchor for the asymptotic modeling step in the methodology.

---

## Hypothesis 4 – **Cross‑base baseline shift is linear in the primorial index**

**Statement**  
The **difference** between the asymptotic limits of successive primorial bases is constant:

\[
\Delta L_{k\to k+1} \;=\; L_{k+1} - L_{k} \;=\; \kappa,
\qquad\text{for }k=4,5,
\]

where \(\kappa\) does **not** depend on \(k\).

**Why it is testable**  
If the baseline shift is truly constant, the set \(\{L_4, L_5, L_6\}\) will lie on a straight line with slope 1 in the \((L_k,\,L_{k+1})\) plane.  We can test the additivity of the shifts with a simple ANOVA on the three pairwise differences.

**Experiment**  

1. Using the \(\hat L_k\) from Hypothesis 1, compute the two differences:  
   \(\Delta_{4\to5} = \hat L_5-\hat L_4\) and \(\Delta_{5\to6} = \hat L_6-\hat L_5\).  
2. **Perform** a two‑sample t‑test (or an exact permutation test) of \(H_0:\Delta_{4\to5}=\Delta_{5\to6}\).  
   *Accept* the hypothesis if the p‑value exceeds 0.05 (i.e., we cannot reject equality).  

*Motivation*: A constant shift would give a compact “cross‑base mapping” formula: \(L_k = L_4 + (k-4)\kappa\), directly linking the primorial index to the correction‑factor baseline.

---

## Hypothesis 5 – **Guarded log‑γ remains numerically stable for the extended parameter space**

**Statement**  
When the algorithm is run on **base 2310 (P₅)** and **base 30030 (P₆)** with **prime bounds up to \(10^7\)**, the guarded log‑γ implementation **produces no overflow, underflow, or NaN values**, and the relative error versus an arbitrary‑precision reference stays below \(10^{-12}\).

**Why it is testable**  
Stability is a binary condition (overflow occurs / does not occur) that can be instrumented directly in the code.  The relative‑error bound can be checked on a representative subset of arguments where a high‑precision gold‑standard can be computed (e.g. using Python’s `mpmath.gamma` with 50‑digit precision).

**Experiment**  

1. **Instrument** the LDAB routine to log any occurrence of `inf`, `-inf`, or `nan` and to record the computed `log_gamma` value for every call.  
2. **Execute** the full pipeline for both P₅ and P₆ at the maximum bound (≈10⁷ primes).  
3. **Subset** a random sample of 10⁴ argument values (evenly spaced in the factorial argument range) and compare each guarded log‑γ result with the high‑precision `mpmath.loggamma`.  Compute  

   \[
   \delta = \frac{|\log\gamma_{\text{guarded}}-\log\gamma_{\text{exact}}|}{|\log\gamma_{\text{exact}}|}.
   \]  

4. **Assert** that \(\max(\delta) < 10^{-12}\) and that no overflow/NaN flags were raised.  

*Prior support*: Run 038 already demonstrated finite log‑binomial terms for large primorials; run 037 showed that unguarded gamma overflows at factorial index 5.  This hypothesis verifies that the **guarded** version indeed solves the problem for the target bases.

---

### Summary Table

| # | Hypothesis | Core Prediction | Key Evidence Required |
|---|------------|----------------|-----------------------|
| 1 | Baseline scales with \(\ln P_k\) | \(L_k = \alpha + \beta\ln P_k\) | \(\hat L_k\) from exponential fits; linear regression |
| 2 | Variance decreases as \(P_k^{-\gamma}\) | \(\operatorname{Var}_k \propto P_k^{-\gamma}\) | Sample variance across windows; power‑law fit |
| 3 | Convergence rate λ matches truncation‑error λ≈0.8 | Exponential decay with λ≈0.8 | Free‑parameter exponential fit; compare \(\hat\lambda_k\) to 0.8 |
| 4 | Constant inter‑base shift | \(L_{k+1}-L_k = \kappa\) (same κ) | Pairwise differences of \(\hat L_k\) |
| 5 | Guarded log‑γ is overflow‑free & accurate for P₅,P₆ up to 10⁷ | No inf/NaN; relative error < 10⁻¹² | Instrumentation + high‑precision reference |

These hypotheses together address the three success criteria of the project:

1. **Computational stability** – H5 guarantees the guarded log‑γ survives the larger bases.  
2. **Asymptotic profiling** – H1 & H3 pinpoint whether a limit exists and how fast we reach it.  
3. **Cross‑base mapping** – H2, H4 quantify how the magnitude (H1) and dispersion (H2) of the correction factor evolve with the primorial index.

Running the experiments described for each hypothesis will generate the quantitative evidence needed to either accept, refine, or reject each claim, thereby delivering the rigorous multi‑base, asymptotic analysis the project aims for.