**Overview**  
The three‑to‑five hypotheses below are designed to be tested with the exact set‑up prescribed in the problem statement (base‑210, primes ≤ 100 000, sliding windows of 1 000 primes, guarded log‑gamma arithmetic, and the fix for the Python‑array comparison bug).  Each hypothesis builds directly on the prior findings about overflow thresholds, guarded γ‑computations, and the need for stable calibration before any larger‑scale work is attempted.

---

## 1.  Numerical stability of the extracted correction factor  

**Statement** –  
Using the guarded log‑γ implementation (which prevents overflow for primorial orders *k* < 132) the empirical correction factor \(c_{\text{emp}}(t)\) will be finite, real, and free of NaN/Inf for **every** sliding window of 1 000 primes up to 100 000.

**Why it is testable** –  
Stability can be verified by a straightforward numerical check: after the calibration loop we inspect each value of \(c_{\text{emp}}(t)\) for the presence of non‑finite entries and compute its relative variation (e.g., \(\ |c_{\text{emp}}(t)|/\)machine‑epsilon ).  If any window yields a NaN/Inf the hypothesis is falsified.

**Experiment** –  
1. Generate the prime list ≤ 100 000.  
2. Form overlapping windows (step = 500 primes) of size 1 000.  
3. Run the LDAB calibration with the guarded log‑γ routine, limiting primorial indices to *k* < 132 (the safe regime identified earlier).  
4. Record the full series \(\{c_{\text{emp}}(t)\}_{t=1}^{N_{\text{windows}}}\) and check for NaN/Inf.  
5. Compute the maximum relative change between consecutive windows as a sanity‑check for “smooth” stability.

---

## 2.  Systematic trend of \(c_{\text{emp}}(t)\) toward the asymptotic RMT prediction  

**Statement** –  
The magnitude of the empirical correction factor will decrease monotonically (or at least show a statistically significant negative slope) as the window index *t* increases, reflecting the approach of the local prime density to the global Random‑Matrix‑Theory (RMT) prediction.

**Why it is testable** –  
A linear (or low‑order polynomial) regression of \(c_{\text{emp}}(t)\) versus *t* can be performed, and the significance of the slope can be assessed with a standard *t*‑test (or by bootstrap).  The hypothesis is falsified if the slope is not significantly different from zero.

**Experiment** –  
1. After obtaining the stable series from Hypothesis 1, plot \(c_{\text{emp}}(t)\) against the median prime value of each window (a proxy for *t*).  
2. Fit a simple linear model \(c_{\text{emp}}(t) = \alpha + \beta\,t + \epsilon\).  
3. Test \(H_0:\beta=0\) against \(H_1:\beta\neq0\) at the 5 % level.  A significantly negative \(\beta\) would support the claim that early windows deviate most from the asymptotic RMT value (which is expected to be ≈ 0).

---

## 3.  Quantitative agreement between empirical and RMT‑derived correction factors  

**Statement** –  
The Mean Squared Error (MSE) between the empirical correction factor series \(\{c_{\text{emp}}(t)\}\) and the theoretically computed series \(\{c_{\text{theory}}(t)\}\) (obtained from the RMT covariance framework) will be **< 10⁻⁴** for the entire set of windows.

**Why it is testable** –  
MSE is a well‑defined scalar metric; we can compute it exactly after we have both series.  The threshold 10⁻⁴ is an a‑priori target derived from the expected order‑of‑magnitude of statistical fluctuations in windows of size 1 000.

**Experiment** –  
1. Using the same window list, compute \(c_{\text{theory}}(t)\) for each window with the RMT formulas (e.g., covariance of the characteristic polynomials evaluated at the relevant spectral point).  
2. Form the difference series \(\Delta(t)=c_{\text{emp}}(t)-c_{\text{theory}}(t)\).  
3. Calculate  
   \[
   \text{MSE}= \frac{1}{N_{\text{windows}}}\sum_{t=1}^{N_{\text{windows}}}\Delta(t)^2 .
   \]  
4. Reject the hypothesis if MSE ≥ 10⁻⁴.  (A complementary statistic—Pearson correlation—should also be reported; a correlation > 0.95 would further corroborate the alignment.)

---

## 4.  LDAB model fit after calibration (KL‑divergence criterion)  

**Statement** –  
After incorporating the empirically extracted \(c_{\text{emp}}(t)\) into the LDAB log‑density, the Kullback–Leibler (KL) divergence between the resulting density estimate and the true indicator function of the primes will be **< 10⁻³** for **each** window.

**Why it is testable** –  
KL divergence can be computed point‑wise because we have the exact prime indicator (0/1) for every integer in the window.  The bound 10⁻³ is the “acceptable threshold” stipulated in the problem statement.

**Experiment** –  
1. For window *t* construct the LDAB log‑density  
   \[
   \log \hat{p}_t(n) = \log p_{\text{LDAB}}(n) + c_{\text{emp}}(t) ,
   \]  
   and normalise to a probability vector \(\hat{p}_t\).  
2. Compute the true distribution \(q_t(n)\) (1 for primes, 0 otherwise).  
3. Evaluate the KL divergence  
   \[
   D_{\text{KL}}(q_t\|\hat{p}_t)=\sum_{n\in\text{window}} q_t(n)\log\frac{q_t(n)}{\hat{p}_t(n)} .
   \]  
4. Verify that every window yields a value < 10⁻³.  If any window exceeds the bound, the hypothesis is falsified.

---

## 5.  Necessity of arbitrary‑precision arithmetic for the highest‑range windows  

**Statement** –  
For windows whose median prime exceeds **≈ 50 000**, the double‑precision computation of \(c_{\text{emp}}(t)\) will differ from the result obtained with an arbitrary‑precision (e.g., `mpmath`) implementation by more than **10⁻⁶**, indicating that high‑precision arithmetic is required to achieve the target accuracy (MSE < 10⁻⁴) near the upper bound.

**Why it is testable** –  
We can run the same calibration algorithm twice: once in standard IEEE‑754 double precision and once with `mpmath` (or Python’s `decimal` with sufficient context).  By comparing the outputs we can directly measure the discrepancy.  The 10⁻⁶ threshold is chosen as a conservative fraction of the MSE target.

**Experiment** –  
1. Identify the subset of windows with median prime > 50 000 (≈ the upper 30 % of the 100 k range).  
2. Execute the LDAB calibration for those windows both in `float64` and in arbitrary‑precision (e.g., 50‑decimal‑digit precision).  
3. Compute the absolute difference \(\delta(t)=|c_{\text{emp}}^{\text{double}}(t)-c_{\text{emp}}^{\text{high‑prec}}(t)|\).  
4. Reject the hypothesis if **any** \(\delta(t)\) exceeds 10⁻⁶.  (If the differences are consistently smaller, we can safely use double precision for the whole range.)

---

### How these hypotheses together satisfy the research goals  

| Goal in the problem statement | Hypothesis(s) that address it |
|-------------------------------|--------------------------------|
| **Stable extraction of \(c(t)\)** | H1 (numerical stability) |
| **Behavior of \(c(t)\) across windows** | H2 (systematic trend) |
| **Comparison with RMT theory** | H3 (MSE & correlation) |
| **Model‑fit validation (KL divergence)** | H4 (KL < 10⁻³) |
| **Practical numerical considerations** | H5 (need for high‑precision) |

All experiments are **self‑contained**, require only the prescribed data (primes ≤ 100 000, base‑210 LDAB, sliding windows of 1 000), and build directly on the earlier findings about overflow thresholds, guarded log‑γ, and the array‑comparison bug fix.  By testing these hypotheses we obtain both *qualitative* insight (stability, trend) and *quantitative* metrics (MSE, KL) that will decide whether the adaptive LDAB calibration can be trusted for larger‑scale or multi‑base extensions.