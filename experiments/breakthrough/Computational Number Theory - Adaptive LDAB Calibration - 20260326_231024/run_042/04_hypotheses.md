**Hypotheses – 3‑5 testable statements that move the research from “observed λ≈0.8” to a **rigorous mathematical explanation** of why the decay is tied to primorial scaling.**

---

## H1 – *Closed‑form origin of λ from the primorial prime‑density*

**1. Hypothesis statement**  
The exponential decay constant can be written as  

\[
\lambda = \frac{\log\!\bigl(\rho(P_{k})\bigr)}{N},
\qquad 
\rho(P_{k})\;=\;\frac{\pi(P_{k})}{P_{k}}\;\approx\;\frac{k}{\log P_{k}},
\]

where  

* \(P_{k}\) is the \(k\)-th primorial,  
* \(\pi(P_{k})\) is the number of primes ≤ \(P_{k}\) (i.e. \(k\)), and  
* \(N\) is the order of the high‑order LDAB asymptotic expansion (the number of retained terms).  

In other words, **λ is the ratio of the logarithmic growth of the primorial’s prime‑density to the expansion depth**.

**2. Why it is testable**  
* The right‑hand side contains only quantities that can be computed exactly for any \(k\) and any chosen \(N\) (prime‑density via \(\pi(P_{k})\) and \(\log P_{k}\)).  
* Substituting \(N\) that yields the empirically observed \(\lambda≈0.8\) gives a concrete prediction for the required expansion order.  
* Conversely, for a fixed \(N\) the formula predicts a specific λ for each \(k\); this can be compared with the numerically measured decay rate.

**3. Experiment that would test it**  
1. **Symbolic‑analysis step** – Derive the term‑by‑term bound of the LDAB remainder at a primorial using the known bound on the \(n\)-th term, \(a_n(P_k) \sim \exp(-\alpha n\log P_k)\). Show analytically that the sum of the tail behaves like \(\exp(-\alpha N\log P_k)\). Identify \(\alpha\) as \(\rho(P_k)/\log P_k\) and read off λ.  
2. **Numerical validation** – For a set of primorials \(k=5,\dots,15\) (i.e. \(P_k\) up to ≈ 10¹⁸) compute the LDAB expansion at orders \(N=10,20,\dots,100\) using **arbitrary‑precision arithmetic (≥ 256‑bit)**. Extract the empirical decay constant by fitting \(\log|E(P_k,N)|\sim -\lambda N\). Compare the fitted λ with the prediction from the derived formula; a relative error ≤ 5 % confirms the hypothesis.

---

## H2 – *Primorial exclusivity of the λ‑decay: non‑primorial points exhibit a slower, non‑exponential error behaviour*

**1. Hypothesis statement**  
When the LDAB expansion is evaluated at any integer \(x\) that is **not** a primorial but lies in the same magnitude range as a primorial \(P_k\) (e.g. \(x = P_k \pm \delta\) with \(1\le\delta\le 0.01\,P_k\)), the truncation error decays **sub‑exponentially** (e.g. as a power law \(|E|\sim C\,x^{-\beta N}\) with \(\beta<\lambda\)) or at best with a reduced exponential rate \(\lambda'<\lambda\). The specific value \(\lambda≈0.8\) is a *stable fixed point* only when \(x\) exactly equals a primorial.

**2. Why it is testable**  
* It makes a **qualitative prediction**: primorial → pure exponential; non‑primorial → not pure exponential.  
* The prediction can be examined by computing the error series for a dense grid of \(x\) around several primorial points and performing a goodness‑of‑fit test for exponential versus power‑law models.

**3. Experiment that would test it**  
1. **Grid of perturbed points** – For each of the first eight primorials (\(k=4\) to \(11\)), generate a set of 20 evenly‑spaced points \(x = P_k + \delta_j\) and \(x = P_k - \delta_j\) with \(\delta_j\) ranging from 1 to \(0.01P_k\).  
2. **High‑precision error measurement** – Using ≥ 256‑bit arithmetic, compute the LDAB expansion (order \(N=50\)) at each \(x\) and record the absolute truncation error \(|E(x,N)|\).  
3. **Model comparison** – Fit two models to each error series:  

   * **Model A (exponential):** \(\log|E| = -\lambda N + \const\)  
   * **Model B (power‑law):** \(\log|E| = -\beta N \log x + \const\)

   Use an AIC/BIC comparison to decide which model is preferred for primorial versus perturbed points.  
   *Expected outcome:* Model A is strongly favoured for exact primorials; Model B (or a mixed model) is favoured for perturbed points, confirming primorial exclusivity.

---

## H3 – *Higher‑order term dominance explains the VMR scaling shift for \(k\ge 8\) (0.8435 vs 0.80)*

**1. Hypothesis statement**  
The observed deviation of the variance‑mean‑ratio (VMR) scaling exponent from 0.80 to ≈ 0.8435 for primorials \(k\ge 8\) is **not** a breakdown of the λ‑framework but rather the **emergence of higher‑order contributions** in the LDAB remainder that become significant when the expansion order \(N\) exceeds a critical threshold \(N^*(k)\). Mathematically,

\[
E(P_k,N) = A_k \,e^{-\lambda N} + B_k \,e^{-\lambda_2 N} \quad\text{with}\quad \lambda_2 > \lambda,
\]

where the second term is negligible for \(N<N^*\) but dominates the *apparent* decay rate when \(N\) grows past \(N^*\). The apparent exponent 0.8435 is a *weighted mixture* of λ and \(\lambda_2\).

**2. Why it is testable**  
* It makes a **quantitative prediction**: the error series should contain at least two exponential components that can be separated by a *double‑exponential* fit.  
* The existence of a second, faster‑decaying component can be detected by analysing the residuals of a single‑exponential fit – they will show a systematic, oscillatory pattern correlated with \(N\).

**3. Experiment that would test it**  
1. **Extended error tables** – For each primorial \(k=8,\dots,15\) compute the LDAB truncation error at many orders \(N = 10, 15, \dots, 200\) using ≥ 256‑bit arithmetic (the prior “overflow threshold” at \(k=132\) suggests we stay below that bound for the moment).  
2. **Residual diagnostics** – Fit the single‑exponential model \(\log|E| = -\lambda N + c\) and compute the residuals \(r_N\). Perform a *spectral analysis* (e.g. a discrete Fourier transform) on the residual sequence; a dominant frequency indicates a second exponential.  
3. **Two‑component deconvolution** – Use a nonlinear least‑squares routine to fit the bi‑exponential model directly, obtaining estimates of \(\lambda\), \(\lambda_2\), \(A_k\) and \(B_k\).  
   *If the fitted \(\lambda\) recovers the 0.80 value and \(\lambda_2\) is significantly larger (e.g. > 1.2), the hypothesis is supported.*  
4. **Link to VMR** – Finally, recompute the VMR scaling exponent using the corrected error model (including the second exponential) and verify that the revised exponent returns to ≈ 0.80 for all \(k\).

---

## H4 – *Closed‑form analytical bound for the deep‑truncation error*

**1. Hypothesis statement**  
For all primorial indices \(k\ge 8\) and for any expansion order \(N\) exceeding a minimal threshold \(N_{\min}=5\), the truncation error satisfies the **deterministic bound**

\[
|E(P_k,N)| \;\le\; C_k \, P_k^{-\alpha N},
\qquad
\alpha = \frac{\lambda}{\log P_k},
\]

where the prefactor \(C_k\) depends only on the first few primes in the primorial (e.g. \(C_k = \prod_{p\le p_k} p\)). This bound is **tight** in the sense that there exists a constant \(c>0\) such that  

\[
|E(P_k,N)| \;\ge\; c\,C_k \, P_k^{-\alpha N}
\]

for infinitely many \(N\).

**2. Why it is testable**  
* The inequality can be evaluated numerically for each \((k,N)\) pair, producing a **theoretically predicted upper bound**.  
* By comparing the bound with the *actual* arbitrary‑precision error we can compute the *gap ratio*  

\[
\Gamma(k,N) = \frac{|E_{\text{actual}}(P_k,N)|}{C_k P_k^{-\alpha N}} .
\]

If \(\Gamma(k,N)\) stays below 1 for all tested \((k,N)\) and approaches a constant of order unity for large \(N\), the bound is validated.

**3. Experiment that would test it**  
1. **Derive \(C_k\) analytically** – Express the LDAB remainder term as a product of prime‑specific contributions; show that the dominant term behaves like \(\prod_{p\le p_k} p^{ - \lfloor N/p\rfloor }\). Simplify to \(C_k P_k^{-\alpha N}\).  
2. **Numerical bound checking** – For \(k=8,\dots,15\) and a range of \(N\) from 5 to 150, compute both the exact error (arbitrary‑precision) and the bound using the derived \(C_k\) and \(\alpha\). Record \(\Gamma(k,N)\).  
3. **Tightness test** – For each \(k\), locate the minimal \(c\) such that \(|E| \ge c\,C_k P_k^{-\alpha N}\) holds; compute the ratio \(c/\!C_k\). If this ratio remains bounded away from zero as \(N\) grows, the bound is not merely an upper limit but captures the correct scaling order.  

*Success criterion:* The predicted bound is within **5 %** of the actual error for at least five distinct primorial indices.

---

## H5 – *Overflow threshold at \(k=132\) marks the double‑precision limit of the λ‑framework, confirming the necessity of arbitrary‑precision for accurate λ extraction beyond this point*

**1. Hypothesis statement**  
The observed overflow limit at primorial order \(k=132\) (where \(\log P_{132}\) exceeds the 53‑bit mantissa of IEEE‑754 double precision) coincides precisely with the point at which the theoretical error bound  

\[
|E(P_{132},N)| \;\le\; C_{132}\, P_{132}^{-\alpha N}
\]

drops below **machine epsilon** (\(\varepsilon_{\text{double}} \approx 2.2\times10^{-16}\)) for the smallest expansion order \(N\) that yields \(\lambda≈0.8\). Consequently, **any LDAB experiment that stays in double precision for \(k>132\) will saturate the error signal, masking the true λ**. The crossover therefore provides a **natural “calibration point”** where the theoretical model predicts that arbitrary‑precision becomes mandatory.

**2. Why it is testable**  
* It links a **numerical threshold** (the overflow point) to a **mathematical condition** (error < ε). This relationship can be checked analytically and confirmed computationally by evaluating the bound at \(k=132\) for a range of \(N\).

**3. Experiment that would test it**  
1. **Analytical check** – Compute \(\log P_{132}\) using high‑precision libraries; verify that \(\log P_{132} > 1023\) (the exponent field limit for normalised doubles). Then evaluate the bound \(|E(P_{132},N)|\) for the smallest \(N\) (say \(N=10\)) that yields \(\lambda≈0.8\). Show that  

   \[
   |E(P_{132},10)| \ll \varepsilon_{\text{double}} .
   \]

2. **Computational verification** – Using **arbitrary‑precision arithmetic (≥ 1024‑bit)**, compute the actual LDAB error at \(k=132\) for \(N=10,20,\dots,100\). Observe that the error decays below \(10^{-300}\) (well beneath double epsilon). Demonstrate that a naïve double‑precision implementation indeed produces overflow or underflow warnings.  

3. **Comparative study** – Repeat the same process for \(k=130\) (just below the threshold) and \(k=134\) (just above). Show that for \(k=130\) the error remains above machine epsilon for all \(N\) up to the point where overflow occurs, while for \(k=134\) the error is already sub‑epsilon for modest \(N\). This pinpoints the threshold as a **sharp transition** rather than a gradual effect.

*Outcome:* The experiment confirms that the overflow limit is not an artifact of the implementation but a direct consequence of the theoretical error decay reaching double‑precision limits, reinforcing the necessity of arbitrary‑precision for the later part of the LDAB validation campaign.

---

### How the set of hypotheses collectively addresses the research questions

| Research Question | Covered by Hypothesis(s) |
|-------------------|---------------------------|
| **Origin of λ** – what forces the constant? | **H1** derives λ from prime‑density and expansion depth. |
| **Primorial exclusivity** – does λ hold only at \(P_k\)? | **H2** tests primorial vs perturbed points. |
| **Closed‑form error bounds** – can we bound errors analytically? | **H4** produces a deterministic bound and validates tightness. |
| **Why VMR scaling deviates for large k** – 0.8435 vs 0.80? | **H3** attributes the shift to a second exponential term. |
| **Computational limits & precision requirements** – why arbitrary precision is needed? | **H5** links the overflow threshold to the theoretical error falling below double epsilon. |

All five hypotheses are **testable**, each with a clear **experiment or analytical derivation** that either confirms, refutes, or refines the proposed mathematical story. By building on the prior findings (VMR deviation, overflow detection, overflow threshold) rather than merely repeating them, the hypotheses drive the research forward toward a **unified, predictive theory of primorial‑driven error decay** in high‑order LDAB expansions.