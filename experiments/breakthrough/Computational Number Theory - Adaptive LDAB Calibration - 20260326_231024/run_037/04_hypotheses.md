# Testable Hypotheses for High-Precision LDAB Calibration Anomaly

Based on the research problem and prior findings indicating overflow artifacts masquerading as data anomalies, I propose the following hypotheses:

---

## Hypothesis 1: Premature Overflow at k=13 Originates from Unguarded Factorial/Gamma Computations

**Statement:** The early failure of high-precision LDAB calibration at k=13 is caused by unguarded factorial or gamma function evaluations in intermediate combinatorial calculations that produce values exceeding the high-precision library's internal exponent range, despite the final result being representable.

**Why it's testable:** This hypothesis makes a specific, falsifiable claim about which computational step causes the overflow. By instrumenting the code to track the magnitude of each intermediate value (particularly factorial and gamma operations), we can identify the exact operation where the anomaly occurs.

**Experiment to test it:**
1. Implement per-operation logging in the high-precision LDAB code that records the exponent (log-base-2) of every intermediate value
2. Execute the algorithm for k=12 (successful) and k=13 (failed)
3. Compare the logged exponent trajectories to identify the first operation exceeding a threshold (e.g., 10^6)
4. Verify whether surrounding operations in the k=12 run stay below this threshold

---

## Hypothesis 2: Pure Log-Space Refactoring Eliminates Intermediate Overflow Without Altering Final Density Estimates

**Statement:** Redesigning the LDAB density estimation formulas to operate entirely in logarithmic space—using log-gamma, log-factorial identities, and log-sum accumulations—will prevent intermediate value overflow while producing numerically identical results (within ε = 10⁻¹²) to the original implementation for k ≤ 131.

**Why it's testable:** This hypothesis makes two testable claims: (a) the refactored code won't overflow, and (b) it will produce equivalent results. Both can be verified through controlled comparison.

**Experiment to test it:**
1. Implement parallel versions of the LDAB density functions: original (mixed arithmetic) and refactored (pure log-space)
2. Run both implementations for k = 1 through 131
3. For each k, compute the absolute difference between density estimates
4. Verify: (a) refactored version completes without overflow for all k, (b) all differences < ε

---

## Hypothesis 3: High-Precision Overflow at k=13 Correlates with Specific Library Constraints in the Rmpfr or GMP Backend

**Statement:** The premature failure at k=13 results from internal constraints in the MPFR/GMP libraries (specifically, the default 53-bit mantissa or exponent range limits for intermediate calculations), rather than algorithmic instability, and increasing the precision parameter will delay—but not prevent—the failure.

**Why it's testable:** This hypothesis makes a specific claim about the library's role. If true, increasing precision should shift the failure point to a higher k value. If false, the failure point should remain fixed regardless of precision settings.

**Experiment to test it:**
1. Run the existing high-precision implementation with MPFR precision set to 80, 128, 256, and 512 bits
2. Record the k value at which each precision level fails
3. Plot the relationship between precision (bits) and maximum stable k
4. If the failure point shifts proportionally, the hypothesis is supported; if it remains at k=13 regardless of precision, the hypothesis is refuted

---

## Hypothesis 4: The Extended-Precision LDAB Framework Maintains Deterministic, Overflow-Free Execution Through k ≥ 150

**Statement:** Once the log-space refactoring is complete, the extended-precision LDAB framework will execute deterministically (without overflow, NaN, or infinite values) for all primorial orders from k=13 to k=150, with monotonically increasing computational time bounded by O(k²).

**Why it's testable:** This is a direct test of the success criteria. We can run the refactored algorithm across the specified range and verify both the absence of errors and the scaling behavior.

**Experiment to test it:**
1. Implement the log-space refactored algorithm
2. Execute a sweep from k=13 to k=150
3. For each k, verify: (a) successful completion, (b) all output values are finite and non-NaN, (c) execution time is recorded
4. Fit execution time against k to confirm O(k²) or better scaling

---

## Hypothesis 5: Cross-Validation Against Double-Precision Results Will Reveal a Precision Threshold Below Which High-Precision Offers No Advantage

**Statement:** For LDAB calibration tasks in the range k ≤ 131, there exists a precision threshold (likely between 64-128 bits) above which additional precision provides no meaningful improvement in calibration fidelity, as the limiting factor becomes the algorithm itself rather than floating-point representation.

**Why it's testable:** This hypothesis proposes a specific relationship between precision and fidelity. We can test it by comparing calibration outputs at different precision levels against a "ground truth" (the verified double-precision results for k ≤ 131).

**Experiment to test it:**
1. Run the refactored algorithm at precision levels: 64, 128, 256, 512, 1024 bits
2. Compare each output against the validated double-precision baseline for k = 1 through 131
3. Compute fidelity metrics (e.g., relative error, correlation)
4. Identify the precision level beyond which additional bits yield < 1% improvement in fidelity

---

## Summary Table

| Hypothesis | Primary Focus | Key Experiment |
|------------|---------------|----------------|
| 1 | Root cause diagnosis | Instrumented tracing at k=12 vs k=13 |
| 2 | Solution validation | Parallel implementation comparison |
| 3 | Library constraint analysis | Precision sweep (80-512 bits) |
| 4 | Scalability verification | k=13 to k=150 sweep |
| 5 | Precision benchmarking | Multi-level precision comparison |

These hypotheses are ordered to follow the natural research flow: diagnose the problem (H1), develop and validate the fix (H2-H3), verify it meets success criteria (H4), and establish its practical utility bounds (H5).