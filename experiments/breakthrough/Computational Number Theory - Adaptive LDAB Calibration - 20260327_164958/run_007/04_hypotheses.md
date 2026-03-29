**Research problem in brief**  
The empirical LDAB correction factor \(c_{\text{emp}}(t)\) loses more than five orders of magnitude of precision at the primorial base \(x=2310\) (relative error \(9.27\times10^{-5}\)). Prior work has shown that:  

* high‑order LDAB expansions reach machine‑ε after a few terms;  
* truncation error decays roughly as \(\lambda\approx0.8\) in arbitrary‑precision but the decay rate is **unstable** across primorial indices;  
* a **localised precision collapse** (≈10 bits) appears at primorial index \(k=16\);  
* the loss at \(k=16\) is **not** caused by the log‑γ term itself; and  
* the correction factor remains finite and well‑behaved in all tested windows.

From these clues we can formulate a small set of **concrete, falsifiable hypotheses** that advance the three goals of the current phase (source‑identification, error‑scaling, algorithmic stabilisation).

---

## 1.  Catastrophic‑cancellation hypothesis  

### Hypothesis statement  
The dominant source of the \(9.27\times10^{-5}\) relative error at \(x=2310\) is **catastrophic cancellation** that occurs when two (or more) large, nearly equal terms are subtracted inside the guarded log‑γ routine (e.g. the difference between the leading Stirling term and the next term of the series).

### Why it is testable  
We can isolate each term of the log‑γ series, evaluate their individual contributions in high‑precision arithmetic, and compare the sum of the first \(N\) terms with the full series. If the difference between the double‑precision result and the high‑precision reference grows dramatically only after a specific subtraction, the hypothesis is confirmed.

### Experiment that would test it  
1. **Term‑by‑term profiling** – using MPFR (≥200‑bit) compute for \(x=2310\) the exact value of every term \(a_n\) of the guarded log‑γ series (Stirling’s expansion or whatever series the implementation uses).  
2. **Cancellation map** – for each \(n\) compute the partial sum \(S_n=\sum_{i=1}^{n}a_i\) and the residual \(R_n=\sum_{i=n+1}^{\infty}a_i\). Record the magnitude \(|a_n|\) and the amount of cancellation \(|a_n|/(|a_{n-1}|+|a_n|)\).  
3. **Re‑evaluate in double** – recompute the same series in IEEE‑754 double precision, retaining each term and the running sum. Identify the first \(n\) where the double sum deviates from the MPFR sum by > 10⁻⁵.  
If the bulk of the error is traced to a single subtraction of comparable‑size terms, catastrophic cancellation is the cause.

---

## 2.  Error‑scaling law hypothesis  

### Hypothesis statement  
The relative error \(\varepsilon(k)\) of the correction factor follows a **piece‑wise exponential law** with primorial index \(k\):  

\[
\varepsilon(k)\;\approx\;
\begin{cases}
A\,10^{-\lambda_1 k}, & k < k_{\text{crit}},\\[4pt]
B\,2^{-\beta (k-k_{\text{crit}})}, & k \ge k_{\text{crit}},
\end{cases}
\]

where the **transition point** \(k_{\text{crit}}\) lies near the observed anomaly at \(k=16\) and \(\beta\) reflects the onset of round‑off domination. The early‑stage decay constant \(\lambda_1\) should agree with the arbitrary‑precision value \(\lambda\approx0.8\) once the algorithm is stabilised.

### Why it is testable  
We can directly measure \(\varepsilon(k)\) for every primorial order up to \(k=132\) (the overflow boundary) and fit the above model. The model is falsifiable: if the data do **not** follow an exponential trend (or if the transition is absent), the hypothesis must be revised.

### Experiment that would test it  
1. **Full‑range error sweep** – for each \(k=1,\dots,132\) compute \(c_{\text{emp}}(t)\) in double precision and in a high‑precision reference (MPFR with ≥200‑bit). Store the relative error \(\varepsilon(k)=|c_{\text{double}}-c_{\text{MPFR}}|/|c_{\text{MPFR}}|\).  
2. **Log‑scale visualisation** – plot \(\log_{10}\varepsilon(k)\) vs. \(k\). Look for a linear region (exponential decay) for small \(k\) and a plateau (or a second linear region) for larger \(k\).  
3. **Model fitting** – use segmented regression or AIC‑based model selection to determine \(k_{\text{crit}}\), \(\lambda_1\), \(\beta\), and the constants \(A,B\).  
If the fitted \(\lambda_1\) matches the previously observed \(\approx0.8\) (once cancellation is mitigated) and a clear transition appears near \(k=16\), the hypothesis is supported.

---

## 3.  Stabilisation‑by‑compensated‑summation hypothesis  

### Hypothesis statement  
Re‑formulating the guarded log‑γ routine with **Kahan (compensated) summation** and an **ordering of operations that avoids subtracting nearly equal large numbers** will reduce the double‑precision relative error to **below \(10^{-12}\)** for every primorial order \(k\le132\) while preserving the current \(O(k)\) or \(O(1)\) runtime.

### Why it is testable  
The statement makes a quantitative prediction that can be measured directly after the code changes. If the error after the modification exceeds \(10^{-12}\) for any \(k\), the hypothesis is falsified.

### Experiment that would test it  
1. **Algorithmic modification** – replace the naïve summation of the Stirling series terms with Kahan’s algorithm; reorder the series to sum the smallest‑magnitude terms first (a classic technique to mitigate cancellation).  
2. **Error measurement** – recompute \(c_{\text{emp}}(t)\) for the full set of primorial bases using the modified routine, and compare each result with the same high‑precision reference used in Hypothesis 2.  
3. **Statistical test** – compute the maximum, mean, and 95th‑percentile of the relative error distribution. Verify that **all** values are < \(10^{-12}\) and that the runtime remains within a factor of 2 of the original implementation (to satisfy the “real‑time” constraint).  
If the error bound is met without a substantial performance penalty, the hypothesis is confirmed.

---

## 4.  Mantissa‑truncation‑at‑\(2^{64}\) hypothesis  

### Hypothesis statement  
The isolated precision collapse observed at **\(k=16\)** (where only ~10 bits survive) is caused by **hardware mantissa truncation** when an intermediate value first exceeds \(2^{64}\) (i.e. when the integer part of the logarithm of the primorial crosses 64 bits). By **scaling** the inputs so that all intermediate values stay ≤ \(2^{63}\), the collapse can be eliminated.

### Why it is testable  
We can deliberately force the computation to stay below the 64‑bit boundary and observe whether the anomaly disappears. Conversely, if we artificially push a value just over \(2^{64}\) for a different \(k\) and see the same collapse, the hypothesis is strongly supported.

### Experiment that would test it  
1. **Identify the offending magnitude** – compute \(\log_2(P_{k})\) for each primorial \(P_k\). At \(k=16\) this value is ≈ 64 (the exact threshold may be slightly less because of the gamma ratio).  
2. **Controlled scaling** – for the run at \(k=16\) divide all intermediate floating‑point numbers by a power of two (e.g. \(2^{70}\)) before they are added, then multiply the final result back. This keeps every mantissa well inside the 53‑bit significand.  
3. **Bit‑exactness check** – after the scaled computation, compare the resulting mantissa bits (after re‑scaling) with the high‑precision reference; verify that at least 50 bits agree (i.e. the 10‑bit loss disappears).  
4. **Cross‑validation** – repeat the same scaling experiment for several \(k\) where \(\log_2(P_k)\) is just below, at, and just above 64. The disappearance of the collapse only in the “above” case after scaling would confirm the hypothesis.  

If scaling restores the expected 53‑bit mantissa for \(k=16\) without harming other \(k\), the mantissa‑truncation explanation is validated.

---

## 5.  λ‑stabilisation hypothesis (optional but encouraged)  

### Hypothesis statement  
Once the cancellation and mantissa‑truncation effects are removed (Hypotheses 1 & 4) and the compensated summation is in place (Hypothesis 3), the **truncation‑error decay constant** \(\lambda\) of the LDAB asymptotic series will **stabilise to the theoretical value ≈ 0.8** for **all** primorial orders up to \(k=132\).

### Why it is testable  
The value of \(\lambda\) can be estimated from the high‑precision runs after stabilisation and compared to the known theoretical prediction. If the estimated \(\lambda\) deviates systematically, the hypothesis is falsified.

### Experiment that would test it  
1. **After‑stabilisation error series** – using the modified routine, compute the difference between the exact LDAB sum (obtained with MPFR) and the truncated series after each added term for each \(k\).  
2. **Exponential fit** – for each \(k\) fit \(\Delta_m(k) \approx C\,10^{-\lambda m}\) where \(m\) is the term index, and extract \(\lambda(k)\).  
3. **Statistical analysis** – compute the mean and standard deviation of \(\lambda(k)\) over \(k=1\ldots132\). If the mean equals 0.8 ± 0.05 and the standard deviation is < 0.02, the hypothesis is confirmed.  

If the spread remains large, the decay law may require a more sophisticated model (e.g. a sum of two exponentials) and the hypothesis would need revision.

---

### How the hypotheses together satisfy the “success criteria”

| Criterion | Matching hypothesis |
|-----------|----------------------|
| **Error reduction to < 10⁻¹² at x=2310** | Hypothesis 3 (stabilisation) |
| **Comprehensive error map for all k ≤ 132** | Hypothesis 2 (scaling law) |
| **Algorithmic efficiency (no arbitrary‑precision)** | Hypothesis 3 + Hypothesis 4 (targeted scaling) |
| **Identification of the error source** | Hypothesis 1 (catastrophic cancellation) and Hypothesis 4 (mantissa truncation) |
| **Theoretical validation of λ** | Hypothesis 5 (λ‑stabilisation) |

---

## Summary of Proposed Hypotheses  

1. **Catastrophic‑cancellation hypothesis** – the large error at \(x=2310\) is caused by subtraction of nearly equal large terms in the log‑γ series.  
2. **Piece‑wise exponential error‑scaling hypothesis** – the relative error follows an exponential decay for small \(k\) and a second exponential/round‑off plateau for larger \(k\), with a transition near \(k=16\).  
3. **Compensated‑summation hypothesis** – Kahan summation plus term re‑ordering will drive the error below \(10^{-12}\) for all \(k\le132\) while keeping the algorithm fast.  
4. **Mantissa‑truncation‑at‑\(2^{64}\) hypothesis** – the precision collapse at \(k=16\) is a hardware mantissa‑bit loss when an intermediate value exceeds \(2^{64}\); scaling eliminates it.  
5. **λ‑stabilisation hypothesis** – after the above fixes, the truncation‑error decay constant λ will converge to the theoretical ≈ 0.8 across all primorial orders.

Each hypothesis is **directly testable** with the computational infrastructure already described (MPFR reference, double‑precision runs, statistical fitting, and targeted scaling experiments). The combined experimental program will pinpoint the source(s) of precision loss, characterise the error growth, and deliver a **stabilised, high‑speed double‑precision implementation** that meets the required error bound.