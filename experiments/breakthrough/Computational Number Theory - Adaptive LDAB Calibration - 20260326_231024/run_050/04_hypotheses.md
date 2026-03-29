
**Research context**  
Prior work has shown that:

* Unguarded gamma‑function calls overflow at very low primorial indices (run 037, k = 5).  
* A guarded log‑gamma formulation prevents that overflow and restores stability up to at least k = 5 (run 038).  
* The double‑precision exponent limit (≈ log P ≈ 709) is first hit at k = 132, but the **64‑bit truncation at k = 16** occurs far earlier, suggesting a *local* loss of mantissa bits rather than a global exponent overflow.

The hypotheses below are designed to **isolate the exact arithmetic step** that initiates the collapse and to verify, component‑by‑component, whether a higher‑precision substitute eliminates the problem.  All experiments respect the constraint that the underlying LDAB theory must not be altered.

---

## 1.  Log‑Gamma Overflow / Under‑flow at the 16‑th Primorial Prime  

**Statement** – The first loss of precision in the LDAB pipeline at k = 16 originates from the evaluation of  
\[
\log\Gamma(p_{k}) \;\;\text{or}\;\; \Gamma(p_{k})
\]  
for the 16‑th prime ( p₁₆ = 53 ).  Because the naïve implementation first computes the raw gamma value, it can overflow (or under‑flow) the 64‑bit floating‑point range before the logarithm is taken, thereby destroying the leading mantissa bits.

**Why it is testable** – This step can be replaced independently of the rest of the pipeline (the “shadow” execution).  By using an arbitrary‑precision library (MPFR, GMP) we obtain a *ground‑truth* value for \(\log\Gamma(p_{k})\) and can compare it with the native double result at each k.

**Experiment** –  
1. Implement three parallel pipelines for k = 14, 15, 16, 17:  

   * **A – Native double** (current implementation).  
   * **B – Arbitrary‑precision log‑gamma** (MPFR `lgamma` with 256‑bit precision).  
   * **C – Guarded log‑gamma** (the formula used in run 038).  

2. After each step record: the raw gamma value, the logged value, the accumulated KL divergence, and the bit‑error (difference from the arbitrary‑precision baseline).  

3. **Success condition**: If pipeline B (or C) restores the KL divergence to < 10⁻⁴ and eliminates the 10‑bit collapse, the hypothesis is confirmed.  If only the guarded version succeeds, we have a refinement of the prior finding (run 038) that the guard must be applied **specifically** at k = 16.

---

## 2.  Rounding‑Error Accumulation in the Primorial Product  

**Statement** – The product  

\[
P_{k}= \prod_{i=1}^{k} p_i
\]  

is accumulated using 64‑bit floating‑point multiplication.  By k = 16 the product is large enough (≈ 6 × 10¹⁸) that the relative rounding error of each multiplication (≈ ½ ULP) begins to dominate the subsequent log‑density calculation, producing a systematic low‑order‑bit loss that cascades into the 10‑bit collapse.

**Why it is testable** – The primorial can be computed exactly with arbitrary‑precision integer arithmetic (GMP) and then cast to a double only when the pipeline truly requires a floating‑point value.  By comparing the two strategies we can isolate the effect of the multiplication rounding.

**Experiment** –  
1. **Baseline**: run the native LDAB pipeline with floating‑point primorial accumulation.  
2. **Variant**: replace the primorial accumulation step with an exact integer product (GMP) and **only** convert to double *after* the log‑density has been evaluated (or keep it as an arbitrary‑precision rational and compute the log directly).  
3. Compare the two pipelines at k = 14‑17 for:  

   * The numerical value of \(P_k\) (relative error vs. the exact GMP value).  
   * The KL divergence after calibration.  
   * The first point where the native pipeline deviates by more than one unit in the last place (ULP) from the GMP reference.

**Success condition**: Restoring the KL divergence to < 10⁻⁴ in the GMP‑based pipeline while the native pipeline collapses would confirm the hypothesis.

---

## 3.  Catastrophic Cancellation in the Density‑Factor Scaling  

**Statement** – The density‑factor scaling step computes a ratio  

\[
\frac{A}{B}
\]  

where both A and B are large, nearly equal numbers (e.g., the log‑density of the primorial and the normalizing constant).  When performed in double precision, this subtraction‑like operation (division of near‑equal magnitudes) destroys the leading mantissa bits, producing the observed 10‑bit loss.

**Why it is testable** – The scaling operation can be performed in isolation using MPFR with a sufficiently large mantissa (e.g., 256 bits) and then fed back into the rest of the pipeline.  The effect on the final KL divergence can be measured without altering any other component.

**Experiment** –  
1. Identify the exact line of code (or algorithmic step) that performs the scaling.  
2. Create a **modular patch**: replace only that step with an MPFR division using 256‑bit precision.  
3. Run the patched pipeline for k = 14‑17, keeping every other step identical to the native implementation.  
4. Measure:  

   * Relative error of the scaling result vs. an arbitrary‑precision reference.  
   * Final KL divergence.  
   * Bit‑wise comparison of the scaled density vector.

**Success condition**: If the patched pipeline recovers the expected KL divergence ( < 10⁻⁴) at k = 16 while the native pipeline fails, the hypothesis is supported.

---

## 4.  Loss of Precision During the Logarithm of the Primorial (log P)  

**Statement** – The LDAB calibration computes \(\log P_k\) as a separate step.  At k = 16 the primorial is already ≈ 6 × 10¹⁸, a magnitude that exceeds the **53‑bit mantissa** of a double, so the conversion from integer to floating‑point already discards about 4–5 bits of relative accuracy.  This loss feeds directly into the log‑density evaluation and ultimately causes the 10‑bit collapse.

**Why it is testable** – The log of the primorial can be obtained **exactly** (up to the chosen arbitrary precision) by first forming the integer primorial with GMP and then applying MPFR’s `log` function.  We can compare this “true” log P with the native double log P.

**Experiment** –  
1. **Native path**: compute `log(P_k)` using the current code (likely a single `log` call on a double).  
2. **Arbitrary‑precision path**: compute `log(GMP_Pk)` using MPFR with 256‑bit precision.  
3. Inject the two results into the rest of the LDAB pipeline (which remains unchanged) and compare downstream outputs (log‑density vectors, KL divergence).  

**Success condition**: If using the arbitrary‑precision log P restores the KL divergence to the target, we have pinpointed the conversion as the root cause.

---

## 5.  Compound Arithmetic Bottleneck (Interaction) Hypothesis  

**Statement** – The precision collapse at k = 16 is not the product of a *single* faulty operation but of **multiple** sub‑operations each introducing a small, tolerable error (e.g., a modest gamma overflow, a modest primorial rounding, a modest cancellation).  Individually these errors are harmless, but their **cumulative effect** overwhelms the double‑precision mantissa, leading to the observed 10‑bit loss.

**Why it is testable** – By sequentially upgrading each component (gamma → arbitrary‑precision, primorial → integer exact, scaling → arbitrary‑precision division, log P → arbitrary‑precision log) we can observe a *gradual* recovery of precision.  If the collapse disappears only after **all** high‑precision replacements are applied, the hypothesis is confirmed.

**Experiment** –  
1. Start with the fully native pipeline (baseline).  
2. Apply the arbitrary‑precision replacement **only** to the log‑gamma step; record the KL divergence at k = 16.  
3. Add the primorial‑exact replacement (still keeping gamma arbitrary‑precision); record again.  
4. Add the high‑precision scaling step; record again.  
5. Finally, replace the log P conversion as well; record the final KL divergence.  

If the KL divergence improves incrementally (e.g., from 0.1 bits → 0.05 bits → 0.01 bits) and reaches the target only after the fourth upgrade, the hypothesis is supported.

**Success condition**: A clear, monotonic reduction in KL divergence with each added high‑precision component, culminating in a value < 10⁻⁴ after all four upgrades, would demonstrate a compound origin.

---

### Summary Table of Hypotheses

| # | Core Arithmetic Step | Suspected Failure Mode | Primary Evidence from Prior Work | Test Strategy |
|---|----------------------|------------------------|-----------------------------------|----------------|
| 1 | Log‑Gamma evaluation | Overflow / under‑flow before log | Unguarded gamma overflow at k = 5 (run 037); guarded version works (run 038) | Replace with MPFR `lgamma` (256 bit) |
| 2 | Primorial accumulation | Rounding error from double mult. | Overflow threshold at k = 132 (run 036) shows large numbers are problematic | Exact integer primorial (GMP) |
| 3 | Density‑factor scaling | Catastrophic cancellation | Not yet examined – new direction | Arbitrary‑precision division (MPFR) |
| 4 | Logarithm of primorial (log P) | Loss of mantissa bits in conversion | Double‑precision log overflow at k = 132 (run 036) suggests large argument issues | Compute log with MPFR on exact GMP primorial |
| 5 | Interaction of 1‑4 | Cumulative small errors | Prior runs show isolated fixes insufficient to reach target KL divergence | Incremental “step‑wise” high‑precision upgrades |

---

**Next steps (derived from the hypotheses)**  

1. **Implement the shadow pipeline** using MPFR/GMP.  
2. **Run the modular experiments** in the order above, logging the exact point of first deviation (the *first‑bit‑loss* marker).  
3. **Produce the error‑propagation map** for the hypothesis that receives the strongest support (likely Hypothesis 1 or a combination of 1 + 4).  
4. **Verify the baseline restoration** by patching the identified failing component(s) and confirming KL < 10⁻⁴ at k = 16.  

These experiments respect the problem constraints (no theoretical changes, focus on arithmetic fidelity, boundary focus k = 15‑17) and directly address the three research questions posed.