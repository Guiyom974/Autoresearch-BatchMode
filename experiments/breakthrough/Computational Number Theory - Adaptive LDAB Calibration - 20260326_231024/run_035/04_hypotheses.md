**Research problem in one sentence**  
Numerical overflow in the LDAB calibration algorithm makes the system time‑out for high‑primorial orders ( k ≥ 15 ). We need a formal model that predicts when the overflow occurs and a practical fix that keeps the estimator accurate and fast enough for real‑time use.

Below are **four concrete, testable hypotheses** that build directly on the earlier observations (e.g. VMR drops and possible overflow at k ≈ 8).  Each hypothesis is accompanied by (i) a clear statement, (ii) why it can be tested, and (iii) a concrete experimental plan.

---

## 1.  **Overflow‑detection failure is caused by the detection test itself exceeding double‑precision limits**

**Statement**  
For k ≥ 15 the conditional test `if (term > MAX_DOUBLE)` overflows **before** the actual term overflows, so the guard is never reached and the computation proceeds with an unreported overflow.  

**Why it is testable**  
We can instrument the existing overflow‑check code, replace the naïve comparison with a safe “bit‑length” or arbitrary‑precision check, and see whether the guard now fires reliably for k ≥ 15. If the safe version reports overflow while the original does not, the hypothesis is confirmed.

**Experiment**  
1. **Baseline run** – Run the original LDAB calibration (20 trials each at k = 12, 13, 14, 15) and record the number of times the overflow flag is set (should be 0 % for k = 15).  
2. **Instrumented run** – Insert a tiny wrapper that first evaluates `if (bit_length(term) > 1023)` (the approximate exponent limit of IEEE‑754 double) before the original `if (term > DBL_MAX)`.  Use arbitrary‑precision integers only for this test; the rest of the code stays unchanged.  
3. **Metric** – Ratio of detected overflows to trials.  If the instrumented version reports overflows for k ≥ 15 while the baseline never does, the hypothesis is supported.  

*Resultant data also give us an empirical “overflow‑detection‑threshold k₀” that can be used later for model fitting.*

---

## 2.  **Log‑domain arithmetic eliminates overflow for all k ≤ 20 while preserving statistical fidelity**

**Statement**  
Re‑computing the dynamic correction factor *c(t)* and all LDAB log‑density terms entirely in the logarithmic domain (i.e. storing `log term` instead of `term`) prevents any value from ever exceeding the double exponent range, thereby driving the timeout rate to 0 % for k ≤ 20.  Moreover, because all downstream operations are additive (log‑domain addition via `logAdd`), the KL divergence between the corrected LDAB density and the true prime stream remains < 10⁻⁴.

**Why it is testable**  
We can implement a parallel version of the calibration that works **exclusively** in log‑space, run the same benchmark suite, and compare (a) timeout incidence and (b) KL divergence against a reference (e.g. a high‑precision arbitrary‑precision run at low k).

**Experiment**  
1. **Implementation** – Write a `LogLDAB` module that stores `log p`, `log c(t)`, etc., and provides a `logAdd(x, y) = max(x, y) + log1p(exp(-abs(x-y)))` routine.  All other prime‑sieve logic stays untouched.  
2. **Benchmark** – Execute 20 independent trials at each k = 12, 13, 14, 15, 16, 18, 20 for both the original double‑precision version and the `LogLDAB` version.  
3. **Metrics**  
   * **Timeout rate** – % of runs exceeding the preset wall‑clock limit (e.g. 5 s per trial).  
   * **KL divergence** – Compute the empirical distribution of the LDAB density estimate (e.g. histogram of estimated probabilities over a fixed test window) and compare to a “ground‑truth” distribution obtained from a high‑precision arbitrary‑precision reference run (target < 10⁻⁴).  
4. **Analysis** – If LogLDAB achieves 0 % timeout for all k ≤ 20 **and** the KL divergence is consistently < 10⁻⁴, the hypothesis holds.  Any degradation in KL would indicate a loss of fidelity that must be addressed (e.g. by higher‑precision log‑addition).

---

## 3.  **The latency overhead of log‑domain computation remains ≤ 10 % for real‑time streaming (up to 10⁶ updates / s)**  

**Statement**  
Even though log‑domain arithmetic replaces each multiplication with a `logAdd` call (which involves a `log1p` and an `exp`), the overall per‑update latency increase is bounded by 10 % compared with the original double‑precision implementation, making it compatible with a real‑time adaptive correction framework.

**Why it is testable**  
Latency can be measured on a per‑update basis using high‑resolution timers and compared between the two implementations under identical streaming workloads.

**Experiment**  
1. **Streaming test‑bed** – Generate a synthetic prime stream that mimics the real‑time input (e.g. one new prime each 1 µs, corresponding to ~10⁶ primes per second).  
2. **Latency measurement** – For each incoming prime, record the wall‑clock time from receipt to completion of the LDAB update (including the correction factor recomputation).  Aggregate over 10 000 updates for each k (12, 15, 20).  
3. **Baseline & LogLDAB** – Perform the same measurement with the original double‑precision code and with the LogLDAB module.  
4. **Metric** – **Δ latency = (LogLDAB mean – Original mean) / Original mean**.  If Δ ≤ 0.10 (10 %) for all tested k, the hypothesis is validated.  Any Δ > 0.10 suggests a need for optimisation (e.g. SIMD‑vectorised `logAdd`, pre‑computed tables).

---

## 4.  **Overflow probability as a function of primorial order follows a logistic rise with a sharp inflection near k ≈ 15**  

**Statement**  
The chance that a given trial at order k incurs an overflow (and consequently a timeout) obeys  
\[
P_{\text{overflow}}(k)=\frac{1}{1+e^{-\alpha\,(k-k_{c})}} ,
\]  
where the inflection point \(k_{c}\) is ≈ 15 and the slope \(\alpha\) reflects the exponential growth of the LDAB terms.  This model can predict timeout rates for any \(k\) up to 20 and beyond.

**Why it is testable**  
We can directly observe overflow/timEOUT events across many trials for a range of k, fit the logistic curve, and test the goodness‑of‑fit.  If the fitted \(k_{c}\) lies within the 95 % confidence interval around 15 and the slope is statistically significant, the hypothesis is confirmed.

**Experiment**  
1. **Data collection** – Use the instrumented overflow detector from **Hypothesis 1** (or the safe bit‑length check) to run **≥ 200 trials** at each \(k = 10, 11, 12, 13, 14, 15, 16, 17, 18, 20\).  Record for each trial whether an overflow (or timeout) occurred.  
2. **Model fitting** – Perform a logistic regression with \(k\) as the predictor and overflow occurrence (0/1) as the response.  Obtain estimates \(\hat{\alpha}\) and \(\hat{k}_{c}\) together with 95 % confidence intervals.  
3. **Goodness‑of‑fit** – Compute the pseudo‑R² and conduct a Hosmer‑Lemeshow test (or a deviance‑based test) to assess calibration.  A non‑significant Hosmer‑Lemeshow statistic (p > 0.05) would indicate the logistic curve captures the trend.  
4. **Validation** – Use the fitted model to predict overflow probabilities for \(k = 19\) and \(k = 21\) and verify with an additional set of 50 trials each.  Prediction intervals should cover the observed proportions.

*If the logistic model holds, it gives us a **formal overflow‑probability model** that can be embedded in the LDAB calibration framework to trigger preemptive scaling (e.g. automatically switch to log‑domain arithmetic) before the system hits the critical k.*

---

### How the Hypotheses Interlock

| Hypothesis | Primary Question Addressed | Next Practical Step |
|------------|-----------------------------|----------------------|
| **H1** – detection‑overflow cause | Why do current guards fail at k ≥ 15? | Replace naïve guard → immediate reduction of silent overflows |
| **H2** – log‑domain mitigation | Can we eliminate overflow without breaking the math? | Implement LogLDAB; verify 0 % timeout + KL < 10⁻⁴ |
| **H3** – latency bound | Is the mitigation fast enough for real‑time? | Benchmarks → ensure ≤ 10 % overhead |
| **H4** – probabilistic model | Can we predict and perhaps prevent overflows? | Fit logistic curve → embed early‑warning trigger |

Together, they provide a **complete research loop**:  
1️⃣ diagnose the root cause (H1),  
2️⃣ propose a mathematically faithful fix (H2),  
3️⃣ verify the fix meets the real‑time constraint (H3), and  
4️⃣ formalise the relationship between \(k\) and overflow risk so the system can **autonomously** decide when to invoke the fix (H4).

---

**Expected Outcomes**

* If **H1** is true, a single‑line change (safe overflow check) will raise the detection rate from 0 % to > 90 % for k = 15.  
* If **H2** holds, the LogLDAB implementation will show **0 % timeout** for all k ≤ 20 while keeping KL divergence < 10⁻⁴.  
* **H3** will demonstrate that the LogLDAB overhead stays within the permissible budget, preserving the “real‑time” nature of the adaptive framework.  
* **H4** will give a compact analytical model that predicts overflow risk as a function of \(k\), enabling proactive scaling and providing a formal answer to the second research question.

These hypotheses are **independent enough to be tested in parallel** but collectively move the project from “we see overflow” to a **predictive, mitigated, and validated LDAB calibration system**.