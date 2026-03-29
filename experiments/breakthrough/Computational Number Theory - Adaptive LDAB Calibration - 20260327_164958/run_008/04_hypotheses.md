**Hypotheses (3‑5) – each is stated, why it can be tested, and what experiment would examine it.  
All work stays inside the established LDAB correction‑factor framework (no new prime‑density models).**

---

### 1.  **Zero‑relative‑error at k = 7 ( x = 510 510 ) is a floating‑point artifact, not a genuine mathematical exactness**

**Statement**  
The observed relative error of exactly 0.0000 e + 00 at the primorial base x = 510 510 (k = 7) arises from FP64 under‑flow / catastrophic cancellation in the guarded log‑gamma routine, not from an exact cancellation of the underlying LDAB correction factor.

**Why it is testable**  
Arbitrary‑precision libraries (MPFR/GMP) can re‑evaluate the same formula with a mantissa far larger than the 53‑bit FP64 word, producing a “ground‑truth” reference value. By comparing the FP64 result with the high‑precision result we can detect whether the FP64 zero is a real value (i.e., the true relative error is truly zero) or an artifact (the high‑precision run yields a non‑zero, bounded error).

**Experiment**  
1. Implement the guarded log‑gamma LDAB correction factor in MPFR with 256‑bit (or higher) precision.  
2. Compute the correction factor and its relative error with respect to the exact (high‑precision) reference at x = 510 510 and at the two adjacent primorials (k = 6 and k = 8).  
3. Perform a step‑by‑step trace of the FP64 calculation, recording every intermediate value. Identify any operation that produces a sub‑normal number, a denormal, or a sudden drop in mantissa bits.  
4. If the MPFR run yields a non‑zero relative error bounded by the theoretical LDAB bound, and the FP64 trace shows a cancellation point, the hypothesis is confirmed.

---

### 2.  The empirical lambda (λ) trend for k ≥ 7 follows an exponential decay with λ≈0.8 and stays inside the theoretical LDAB bounds up to k = 13  

**Statement**  
The “lambda” parameter estimated from the LDAB truncation‑error decay obeys the theoretical asymptotic relation  

\[
\text{error}(k) \approx C\,e^{-\lambda k},
\]

with λ ≈ 0.8 (the value seen in earlier runs) for all primorial indices from k = 7 up to at least k = 13. Moreover, the fitted λ values will lie within the confidence interval predicted by the LDAB error analysis.

**Why it is testable**  
We can compute the LDAB correction factor for a range of k (7 ≤ k ≤ 13) using both FP64 and extended precision, extract the truncation error for each order, and fit an exponential model to obtain λ. The fit quality and the confidence interval can be compared directly with the theoretical bound on λ derived from LDAB asymptotics.

**Experiment**  
1. Using the guarded log‑gamma routine (validated for k ≤ 132), compute the LDAB correction factor at the primorial bases for k = 7, 8, …, 13.  
2. For each k, evaluate the high‑order expansion to a set of increasing orders (e.g., 5, 10, 15 terms) and record the resulting truncation error.  
3. Perform a least‑squares exponential fit on the error sequence for each k to extract λ and its standard error.  
4. Overlay the empirical λ estimates with the theoretical LDAB λ ≈ 0.8 ± Δλ (where Δλ is derived from the bound analysis). Verify that all empirical points lie inside the predicted band and that the trend does not exhibit the erratic jumps observed earlier (which were flagged as possible artifacts).

---

### 3.  The precision collapse observed at k = 16 originates from mantissa loss **after** the log‑gamma term, and the same mechanism will be observed when the calculation is repeated with arbitrary precision  

**Statement**  
The sudden drop from ≈256 effective bits to ≈10 bits at k = 16 is caused by a loss of mantissa precision in the post‑log‑gamma stage of the LDAB correction factor (e.g., during exponentiation or final combination of terms), not by the log‑gamma evaluation itself.

**Why it is testable**  
By instrumenting the computation in both FP64 and MPFR we can isolate which arithmetic operation yields the precision loss. If the loss persists after the log‑gamma term in the high‑precision run, the hypothesis is supported; if the loss disappears when higher precision is used, the hypothesis is refuted.

**Experiment**  
1. Code the LDAB correction factor routine in MPFR with 512‑bit precision, and insert debug hooks that record the precision (effective number of correct bits) after each elementary operation.  
2. Run the routine for k = 16 and for a “control” index where no collapse is expected (e.g., k = 10).  
3. At each step, compute the difference between the high‑precision result and the FP64 result, and track when the discrepancy exceeds a threshold (e.g., > 10 bits).  
4. Identify the first operation where the discrepancy appears; if it occurs after the log‑gamma evaluation (e.g., during the final exponential or summation), the hypothesis is confirmed.

---

### 4.  The guarded log‑gamma routine maintains overflow‑free, stable precision for the LDAB correction factor up to at least k = 132 (and consequently up to k = 13)  

**Statement**  
The “guarded” version of the log‑gamma approximation (which was shown to avoid overflow up to k = 132) will keep the relative error of the LDAB correction factor well below the theoretical bound for all primorial indices up to k = 13, with no occurrence of overflow or catastrophic cancellation.

**Why it is testable**  
We can directly execute the guarded routine for a dense set of k values spanning the interval [1, 13] (including the previously problematic points 7 and 16) and verify that every intermediate value stays within the representable range of the chosen arbitrary‑precision format, and that the final relative error conforms to the LDAB bound.

**Experiment**  
1. Implement the guarded log‑gamma in MPFR with a safety margin of 256‑bit precision.  
2. Iterate k from 1 to 13, compute the LDAB correction factor at each primorial base, and record any overflow, under‑flow, or denormal flags.  
3. Compute the relative error with respect to the high‑precision reference (the same reference used in Hypothesis 1).  
4. Verify that:  
   - No overflow/under‑flow occurs.  
   - The relative error is ≤ the theoretical LDAB bound for every k.  

If both conditions hold, the hypothesis is supported.

---

### 5.  Extended‑precision recomputation will replace the zero relative error at k = 7 with a non‑zero, bounded error that lies within the LDAB theoretical error envelope  

**Statement**  
When the LDAB correction factor at x = 510 510 (k = 7) is evaluated with sufficient arbitrary precision (≥ 256 bits), the resulting relative error will be **non‑zero** and will satisfy the inequality  

\[
|\epsilon_{\text{emp}}(k=7)| \le \epsilon_{\text{LDAB}}(k=7),
\]

where \(\epsilon_{\text{LDAB}}(k)\) is the upper bound derived from the LDAB asymptotic expansion.

**Why it is testable**  
We can compare the high‑precision result (ground truth) to the FP64 result, compute the relative error in both precisions, and check whether the FP64 error is exactly zero (artifact) while the high‑precision error is a small, bounded quantity. This test directly answers the “Anomaly Resolution” success criterion.

**Experiment**  
1. With MPFR set to 256‑bit precision, compute the exact LDAB correction factor at x = 510 510 and determine its value to at least 50 decimal places.  
2. Compute the relative error of the FP64 result against this reference.  
3. Compute the relative error of the MPFR result (at 256 bits) against the same reference; it will be essentially the machine‑epsilon of the chosen precision.  
4. Verify that:  
   - FP64 yields 0.0000 e + 00 (confirming the reported anomaly).  
   - MPFR yields a non‑zero value, orders of magnitude smaller than the theoretical LDAB bound.  

If the high‑precision error is non‑zero and ≤ the bound, the hypothesis is confirmed, resolving the anomaly.

---

### How these hypotheses together satisfy the research objectives  

| Objective | Hypothesis(s) that address it |
|-----------|--------------------------------|
| **Resolve the zero‑error anomaly** | H1, H5 |
| **Validate the λ trend** | H2 |
| **Identify the source of precision loss at larger k** | H3 |
| **Confirm stability of the guarded log‑gamma for the range of interest** | H4 |
| **Provide a rigorous, non‑zero bounded error** | H5 |

All proposed experiments rely on existing arbitrary‑precision tools (MPFR/GMP) and on the established LDAB correction‑factor formalism, respecting the domain‑strictness constraint. By building directly on the prior guarded‑log‑gamma, high‑order expansion, and observed λ ≈ 0.8 results, we avoid duplicating experiments that already have clear outcomes.