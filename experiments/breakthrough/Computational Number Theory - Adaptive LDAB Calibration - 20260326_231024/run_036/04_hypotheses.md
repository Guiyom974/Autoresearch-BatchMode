**Background**  
Prior work (runs 026 & 035) showed that **no overflow occurs for the LDAB calibration up to k ≈ 12**. The new program is designed to push the test range to k ≥ 13 (up to ≈ 150) and to capture the exact moment at which standard 64‑bit floating‑point arithmetic fails.  
The four hypotheses below **(i)** build directly on the “no‑overflow‑yet” observation, **(ii)** are each testable with the planned k‑sweep and dual‑precision tracking, and **(iii)** propose concrete experiments that will either confirm, refute, or refine the current understanding.

---

## Hypothesis 1 – A Finite Overflow Threshold Exists and Lies Within a Predictable k‑Range  

**Statement**  
There is a smallest primorial order \(k_{\text{crit}}\) such that for any \(k\ge k_{\text{crit}}\) the ordinary double‑precision evaluation of *any* LDAB quantity (primorial product \(p_k\# ,\) its logarithm, or the correction term \(c(t)\)) produces **Inf** or **NaN**. Moreover, based on the growth rate of \(\log(p_k\#)\) we expect \(k_{\text{crit}}\) to fall between **30 ≤ \(k_{\text{crit}}\) ≤ 70**.

**Why it is testable**  
* The existence of a finite threshold is guaranteed by the finite exponent range of IEEE‑754 doubles (≈10³⁰⁸).  
* The exact value can be discovered empirically by iterating the computation and testing for overflow flags (`math.isinf` / `math.isnan`).  

**Experiment**  
1. **Automated k‑sweep** – for \(k = 13,14,\dots,150\) (or until total failure) compute:  
   * \(p_k\# = \prod_{i=1}^{k} p_i\) (naïve multiplication)  
   * \(\log(p_k\#)\) (standard `log`)  
   * the LDAB correction factor \(c(t)\) (including any exponential term)  
2. **Overflow detection** – after each operation record whether an `Inf`/`NaN` appears.  
3. **Stop‑rule** – halt at the first \(k\) where any of the three values is non‑finite; this yields the empirical \(k_{\text{crit}}\).  
4. **Comparison with arbitrary‑precision baseline** – repeat the same loop using `mpmath` with, say, 50‑decimal precision; the first \(k\) where the double result differs from the high‑precision result marks the *effective* overflow point.

*If the observed \(k_{\text{crit}}\) lies inside the 30‑70 interval, the hypothesis is confirmed; otherwise the interval can be narrowed for the next round of experiments.*

---

## Hypothesis 2 – Overflow First Appears in the LDAB Exponential Term, Not in the Primorial Product  

**Statement**  
Because the LDAB calibration contains an exponential scaling of the (already huge) log‑density, **the first overflow will be triggered by the exponentiation step**, well before the raw primorial multiplication itself exceeds the double range.

**Why it is testable**  
We can separate the two operations in code and log which one raises an `Inf`/`NaN` first. By instrumenting the primorial accumulator and the exponential evaluation independently, we obtain a clear causal indicator.

**Experiment**  
1. **Component‑wise logging** – during the k‑sweep described in Hypothesis 1, maintain three flags:  
   * `prim_overflow` – set when the running primorial product becomes infinite.  
   * `exp_overflow` – set when the argument to `exp()` (or any equivalent high‑order power) would exceed the representable range.  
   * `overall_overflow` – set when any downstream LDAB term becomes non‑finite.  
2. **Order detection** – after each \(k\) record which flag triggered first.  
3. **Statistical summary** – across the sweep compute the proportion of cases where `exp_overflow` precedes `prim_overflow`.  

*If ≥ 80 % of the overflow events are `exp_overflow`, the hypothesis is supported.*

---

## Hypothesis 3 – Precision Degradation Follows a Predictable Functional Form  

**Statement**  
The relative error between the double‑precision LDAB values and the arbitrary‑precision ground truth grows **smoothly and modelably** as \(k\) approaches \(k_{\text{crit}}\). Specifically, the error trajectory can be described by either a **power‑law**  
\[
E(k) \;\approx\; C\,k^{\alpha},
\]  
or an **exponential** law  
\[
E(k) \;\approx\; C\,\exp(\beta k),
\]  
where the parameters \(C,\alpha\) (or \(C,\beta\)) are estimable from the pre‑overflow data.

**Why it is testable**  
We can compute the exact error at each \(k\) (using the dual‑precision pipeline) and then fit candidate models via standard regression. The predictive power of the fitted model can be tested by extrapolating to higher \(k\) and comparing the predicted error to the empirically observed error (or to the presence of overflow).

**Experiment**  
1. **Error collection** – for each \(k\) from 13 up to, say, 40 (or the last safe value before overflow) compute  
   \[
   E_{\text{prim}}(k)=\frac{|p_k\#_{\text{double}}-p_k\#_{\text{high}}|}{p_k\#_{\text{high}}},
   \]  
   and analogous errors for \(\log(p_k\#)\) and \(c(t)\).  
2. **Model fitting** – apply nonlinear least‑squares to the power‑law and exponential models; select the better fit by AIC/BIC.  
3. **Validation** – use the fitted model to **predict** the error at \(k=45,50,\dots\) and compare with the actual double‑precision results (or with the high‑precision results if overflow has not yet occurred).  
4. **Threshold estimation** – set an acceptable error tolerance (e.g., \(10^{-6}\)) and solve the chosen model for the maximal \(k\) that satisfies it; compare that \(k\) to the empirical \(k_{\text{crit}}\) from Hypothesis 1.

*If the predicted \(k_{\text{crit}}\) from the error model lies within ±5 of the observed overflow point, the hypothesis is validated.*

---

## Hypothesis 4 – Overflow Occurs When the LDAB Log‑Density Exceeds the Double‑Precision Exponential Limit (~709)  

**Statement**  
Because the IEEE‑754 double can represent numbers up to ≈ 1.8 × 10³⁰⁸, the function `exp(x)` overflows when **\(x \gtrsim 709\)** (since \(\exp(709) \approx 1.0\times10^{308}\)). Consequently, the LDAB calibration will first overflow **exactly when the combined log‑density term**  
\[
L(k)=\log(p_k\#)+ \text{(any additive correction)}\]  
surpasses ≈ 709. This provides a simple analytical predictor of \(k_{\text{crit}}\).

**Why it is testable**  
We can compute \(L(k)\) with arbitrary precision for all \(k\) up to 150, locate the smallest \(k\) where \(L(k)>709\), and compare that \(k\) to the empirical overflow \(k\) observed in double precision.

**Experiment**  
1. **High‑precision log‑density** – using `mpmath` with ≥ 50‑digit precision, evaluate \(L(k)\) for each \(k\) (including all LDAB correction terms).  
2. **Threshold crossing** – identify the first \(k\) with \(L(k) > 709\) (or a slightly lower safe bound, e.g., 700, to account for rounding in intermediate steps).  
3. **Cross‑check** – run the double‑precision sweep in parallel and record the exact \(k\) where overflow appears.  
4. **Agreement measure** – compute the absolute difference \(\Delta k = |k_{\text{overflow}}-k_{L>709}|\).  

*If \(\Delta k \le 2\) (i.e., overflow occurs within one or two steps of the theoretical crossing), the hypothesis is strongly supported.*

---

### How These Hypotheses Build on Prior Findings  

| Prior Observation | New Hypothesis Built on It |
|-------------------|-----------------------------|
| No overflow up to k ≈ 7 (and hints up to k ≈ 12) | **H1** explicitly searches for the *first* overflow beyond this safe zone, predicting a concrete range. |
| Overflow detection model was suggested but not validated | **H2** determines *which* component (exponential vs. product) is responsible, directly testing the proposed model. |
| Error growth not yet quantified | **H3** quantifies the pre‑overflow degradation, turning the “no‑overflow‑yet” observation into a quantitative trajectory. |
| Theoretical overflow limit (≈ 709) was noted for plain exponentials | **H4** applies that limit to the LDAB log‑density, providing an analytical shortcut to locate \(k_{\text{crit}}\). |

---

## Summary of Experiments (Quick‑Reference)

| Hypothesis | Core Experiment | Primary Output |
|------------|------------------|----------------|
| **H1** – Threshold existence & range | k‑sweep 13 → 150 with overflow flags; arbitrary‑precision baseline | Empirical \(k_{\text{crit}}\) |
| **H2** – Overflow modality | Component‑wise overflow logging (prim product vs. exp term) | Which part overflows first ( % exp‑first) |
| **H3** – Predictable error growth | Dual‑precision error collection + model fitting (power‑law vs. exponential) | Error‑model parameters & predicted \(k_{\text{crit}}\) |
| **H4** – Log‑density threshold crossing | High‑precision computation of \(L(k)\); compare to double‑precision overflow point | \(\Delta k\) between theory and observation |

These four (or optionally a fifth) testable hypotheses directly address the research questions, leverage the existing “no‑overflow‑yet” evidence, and provide a concrete experimental roadmap for locating the precise numerical overflow threshold in hyper‑scale LDAB calibration.