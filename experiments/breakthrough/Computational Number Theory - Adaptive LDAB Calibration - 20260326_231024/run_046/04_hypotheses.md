**Research context (quick recap of what is already known)**  

| Prior finding | What it tells us |
|---|---|
| **run_035** – “simple overflow detection eliminates timeouts at low *k* but fails at high *k*” | The problem is **not** a trivial overflow of the primorial itself for *k* ≤ 7; something deeper in the calculation pipeline becomes unstable. |
| **run_036** – “overflow first occurs at primorial order *k* = 132 where log P exceeds 709” | Pure IEEE‑754 `float64` can only represent `exp(x)` up to *x* ≈ 709.  For *k* > 132 the naïve `exp(log P)` would overflow, but for the **target range** *k* ≤ 10 (P₁₀ ≈ 6.5 × 10⁹) the primorial never overflows.  Hence the NaNs must arise from **intermediate** operations (e.g. log‑γ, binomial‑coefficient, or division by a near‑zero quantity). |
| **run_038** – “guarded log‑γ yields finite log‑binomial terms for large primorials” | A **local** high‑precision trick can keep the log‑binomial finite; it suggests that the culprit is indeed the loss of precision in the gamma‐function evaluation, not the size of the final numbers. |

From these clues the current iteration wants to **remove all NaNs for 1 ≤ k ≤ 10**, discover **how much extra precision is truly needed**, and verify that **once the arithmetic is safe the decay‑rate physics actually behaves** as predicted by the asymptotic model.

Below are five mutually‑independent but logically‑connected hypotheses that can be tested in the laboratory (i.e. by running code, measuring outputs, and performing statistical fits).

---

## H1 – *The NaNs at k ≥ 2 are caused by overflow/underflow in the intermediate log‑γ (or equivalent) stage, and switching to arbitrary‑precision arithmetic will eliminate them.*

### 1. Statement  
When the LDAB pipeline is executed with IEEE‑754 `float64`, the first NaN appears because some **intermediate** quantity (most plausibly the log‑γ of a huge integer) overflows or underflows before the final result is formed. Replacing the whole arithmetic backend with an arbitrary‑precision library (MPFR, `mpmath.mp`, or `gmpy2`) will make every intermediate value representable, so the output for every *k* ≤ 10 will be a finite real number (no NaN) and a sensible standard error.

### 2. Why it is testable  
We can **run the identical LDAB algorithm** twice: once with the original `float64` code, once with the arbitrary‑precision wrapper. For each *k* = 2,…,10 we can record whether the produced decay rate and its standard error are `NaN` or a finite float. The test is binary – NaN *vs.* non‑NaN – and can be repeated for many random seeds to guarantee consistency.

### 3. Experiment  
1. **Instrument** the existing Python (or C++) LDAB routine to call `mpmath.mp` functions (`mpf`, `log`, `gamma`, `loggamma`) instead of the built‑in `float` equivalents.  
2. **Execute** the full pipeline for *k* = 2,…,10 with a fixed set of calibration parameters (e.g. the same window size, bootstrap repetitions).  
3. **Collect** the output values (`b_k`, `σ_k`).  
4. **Compare** with the original `float64` run – the hypothesis is supported if *all* results are finite in the arbitrary‑precision version while at least one is NaN in the `float64` version.

---

## H2 – *The minimum number of bits of precision required for stability grows linearly (or at most logarithmically) with the size of the primorial, i.e.  P_min(k) ≈ α · log₂ P_k + β.*

### 1. Statement  
Not every arbitrary precision is needed for every *k*. There is a **monotonic relationship** between the magnitude of the intermediate log‑γ values (which are roughly O(log Γ(P_k))) and the number of bits that must be kept exact to avoid underflow/overflow. The relation can be captured by a simple linear (or log‑linear) model:
\[
\text{bits}_{\min}(k)=\alpha\,\log_2 P_k+\beta,
\]
where α and β are constants to be fitted.

### 2. Why it is testable  
We can **empirically determine** the smallest working precision for each *k* by a **binary‑search‑style ascent**: start at 128 bits, run the pipeline; if a NaN appears, double the precision (256 bits, 512 bits, …) until the result becomes finite. The series of “first‑success‑precision” values can then be regressed against \(\log_2 P_k\). The test is deterministic and reproducible.

### 3. Experiment  
1. For *k* = 1,…,10:  
   * Set precision = 128 bits.  
   * While NaN: precision ← 2 × precision (stop at 4096 bits for safety).  
   * Record the **first precision that yields finite results**.  
2. **Fit** the model \(\text{bits}_{\min}(k)=\alpha\log_2 P_k+\beta\) using ordinary least squares.  
3. **Validate** the fit by checking the residual standard error and by testing the model on an out‑of‑sample *k* (e.g., *k* = 11, 12) if computationally feasible.

---

## H3 – *Once the arithmetic is numerically stable, the recovered decay rates obey the theoretical asymptotic scaling \(b_k = 1 + \dfrac{C}{\log P_k} + o\!\big(1/\log P_k\big)\).*

### 1. Statement  
The LDAB error model predicts that, after correcting the precision problem, the **bulk decay exponent** for the standard errors should approach 1 from above, with a deviation that shrinks as \(1/\log P_k\). The constant *C* encapsulates the leading‐order correction term. A statistically significant fit with a high \(R^2\) will confirm that the underlying physics is indeed well‑behaved once numerical artefacts are removed.

### 2. Why it is testable  
We can **compute** the empirical decay rates \(b_k\) (and their standard errors) for *k* ≥ 4 using the arbitrary‑precision pipeline. Then we can **fit** the model \(b_k = 1 + C / \log P_k\) by non‑linear least squares (or by linear regression after rearranging). The fit yields a *C* estimate, a *p*‑value for *C* ≠ 0, and an \(R^2\). The hypothesis is accepted if *C* is significantly positive and \(R^2\) > 0.95.

### 3. Experiment  
1. With the arbitrary‑precision run from **H1**, extract the vector \((b_k, \sigma_{b_k})\) for *k* = 4,…,10.  
2. **Fit** the model using e.g. `scipy.optimize.curve_fit`.  
3. **Compute** confidence intervals for *C* (via bootstrap or analytical covariance).  
4. **Report** \(R^2\) of the fit; the hypothesis is supported if \(R^2\) ≥ 0.95 and the residual plot shows no systematic structure.

---

## H4 – *The computational overhead introduced by arbitrary‑precision arithmetic grows at most quadratically with the number of precision bits, making real‑time adaptive correction feasible for the target range.*

### 1. Statement  
The dominant cost of MPFR/MPmath operations is the multiplication of *big integers* whose length is proportional to the number of bits. Classical analysis suggests a **\(O(p^2)\)** growth (or better with Karatsuba/FFT tricks) for multiplication of *p*-bit numbers. If the observed scaling is sub‑quadratic, then raising precision from 128 bits to 1024 bits for *k* ≤ 10 will increase runtime by less than a factor of 64, which is acceptable for offline calibration and even for modest real‑time use.

### 2. Why it is testable  
We can **measure** wall‑time for the entire LDAB pipeline at several precision levels (128, 256, 512, 1024, 2048 bits) and **fit** a power‑law or polynomial model to the data. The exponent of the fitted term tells us the scaling class.

### 3. Experiment  
1. Run the pipeline for *k* = 10 (the most expensive case) at each precision setting, repeating each run ≥ 10 times to obtain a stable mean ± σ wall‑time.  
2. **Fit** a model \(\text{time}(p)=a\,p^b\) (log‑log linear regression) or a second‑order polynomial \(\text{time}(p)=a p^2+b p +c\).  
3. **Interpret** the exponent *b*: if *b* ≤ 2 (or the quadratic coefficient is negligible), the hypothesis is supported.  

If the overhead is found to be prohibitive (e.g., > 10 × slower at 1024 bits than at 128 bits), the research will have a concrete metric for why a hybrid or guarded‑log‑γ approach is preferable.

---

## H5 – *A hybrid strategy that combines the **guarded log‑γ** trick (prior finding) with modest arbitrary‑precision (≈ 256 bits) reproduces the results of full high‑precision (≈ 1024 bits) for all *k* ≤ 10, but at a lower computational cost.*

### 1. Statement  
The guarded log‑γ formula already yields **finite** log‑binomial terms. If we then evaluate the remaining arithmetic (e.g., the binomial‑coefficient accumulation and the final exponentiation) in a *moderate* arbitrary‑precision context (256 bits), the outcome will be numerically identical (within machine‑epsilon of the high‑precision run) while the runtime will be noticeably shorter.

### 2. Why it is testable  
We can **implement** two versions of the pipeline:  

* **Version A** – full MPFR with 1024 bits everywhere.  
* **Version B** – guarded log‑γ (as described in run_038) followed by 256‑bit MPFR arithmetic.

By comparing the outputs (b_k and σ_k) and the runtimes, we can test whether the two versions agree to, say, 10 decimal places and whether Version B is faster.

### 3. Experiment  
1. **Code** the guarded log‑γ routine (or import the existing snippet) and embed it in the LDAB pipeline.  
2. **Run** both versions for *k* = 2,…,10, each with ≥ 5 independent seeds.  
3. **Compute** the relative error \(|b_k^{(A)}-b_k^{(B)}|/|b_k^{(A)}|\) and the same for σ_k.  
4. **Perform** a paired‑t test (or a non‑parametric Wilcoxon test) to verify that the median difference is indistinguishable from zero.  
5. **Record** mean wall‑times; the hypothesis is supported if the hybrid version is **significantly faster** (e.g., > 30 % speed‑up) while meeting the accuracy criterion.

---

### How the five hypotheses together advance the research

| Hypothesis | What it decides |
|---|---|
| **H1** – NaN elimination via arbitrary precision | Confirms that the failure mode is indeed numerical instability of intermediate values. |
| **H2** – Precision‑vs‑k scaling | Provides a **quantitative rule** for how much extra precision is needed, guiding future hardware or software choices. |
| **H3** – Asymptotic decay‑rate model | Proves that the underlying **physics** is well‑behaved once the arithmetic is fixed, fulfilling the ultimate scientific objective. |
| **H4** – Overhead scaling | Gives a **performance feasibility** bound for deploying the solution in production (real‑time calibration). |
| **H5** – Hybrid vs. full high‑precision | Identifies a **practical compromise** that retains scientific fidelity while reducing computational cost. |

All five are **testable in silico** with the existing LDAB pipeline and standard arbitrary‑precision libraries, require no new hardware, and together cover both the **diagnostic** (where the failure occurs) and the **corrective** (how much precision is needed, how fast it can be, and whether a cheaper workaround suffices) aspects of the research problem.