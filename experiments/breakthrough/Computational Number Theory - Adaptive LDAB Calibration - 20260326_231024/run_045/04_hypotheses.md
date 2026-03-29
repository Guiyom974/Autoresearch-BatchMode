
# Testable Hypotheses for LDAB Calibration Error Models

Based on the research problem and prior findings (particularly the guarded log-gamma formulation in run_038 and the high-order asymptotic expansion framework in run_039), I propose the following five testable hypotheses:

---

## Hypothesis 1: Log-Space Error Parameterization Eliminates Precision Collapse at k ≥ 4

**Statement:** Reformulating the LDAB error model entirely within logarithmic space will yield numerically stable decay rate estimates (finite standard errors) for all primorial indices k ≥ 4 using standard float64 arithmetic, without requiring arbitrary-precision libraries.

**Why it's testable:** This hypothesis makes a concrete quantitative prediction: that log-transformed error metrics will produce finite, non-NaN outputs where raw floating-point computations overflow or underflow. The testable outcome is binary (stable vs. unstable).

**Experiment:**
1. Implement dual-track LDAB calibration: (a) raw floating-point computation following the original formulation, and (b) log-space transformation using the log-gamma guard principle from run_038 extended to the full error term
2. Test both implementations across primorial bases k = 4, 5, 6, ..., 132 (the observed overflow threshold from run_037)
3. Compare outputs: record whether each implementation produces finite estimates, and compute relative difference where both are finite
4. **Metric:** Proportion of k values yielding finite decay rate estimates (target: 100% for log-space formulation)

---

## Hypothesis 2: Normalized Relative Error Bounds Exhibit k-Independent Convergence

**Statement:** A normalized relative error metric (error divided by the magnitude of the leading asymptotic term) will exhibit convergence properties that are asymptotically independent of primorial order k, enabling uniform error bounds across bases 210, 2310, and 30030.

**Why it's testable:** This hypothesis predicts a specific mathematical property—k-independence in the normalized error—which can be directly verified by computing the normalized error across multiple k values and testing for statistical stationarity.

**Experiment:**
1. Using the high-order asymptotic expansion from run_039, compute both raw error and normalized error (error / leading asymptotic term) for each primorial base
2. Perform a trend analysis: fit a linear or power-law model of normalized error vs. k and test whether the slope differs significantly from zero
3. Apply a one-way ANOVA or Kruskal-Wallis test to assess whether normalized error distributions are homogeneous across k = 4, 5, 6
4. **Metric:** p-value for k-independence test (target: p > 0.05 indicates independence)

---

## Hypothesis 3: Guarded Log-Gamma Error Propagation Remains Bounded Below 10⁻³

**Statement:** The numerical error introduced by the guarded log-gamma approximation (run_038) will propagate through the full LDAB calibration pipeline with cumulative error no greater than 10⁻³, measured against arbitrary-precision ground truth.

**Why it's testable:** This hypothesis quantifies error propagation from an existing intervention, making it directly measurable by comparing guarded implementations against a high-precision reference (e.g., Python's `mpmath` with 50+ decimal places).

**Experiment:**
1. Implement three calibration pipelines:
   - **Reference:** Arbitrary-precision computation (≥50 decimal places)
   - **Guarded:** Float64 with guarded log-gamma (run_038)
   - **Naive:** Standard float64 without guards
2. Run all three on streaming prime sequences up to 10⁸ for bases 210, 2310, and 30030
3. Compute λ estimates and KL divergence for each
4. Calculate cumulative error: |λ_guarded - λ_reference| and |λ_naive - λ_reference|
5. **Metric:** Maximum observed error across all bases (target: < 10⁻³ for guarded, > 10⁻³ for naive)

---

## Hypothesis 4: Float64 with Log-Space Reformulation Achieves KL Divergence < 10⁻⁴

**Statement:** The combination of log-space error parameterization (Hypothesis 1) and guarded log-gamma approximation will achieve KL divergence below 10⁻⁴ across all three primorial bases without any arbitrary-precision arithmetic.

**Why it's testable:** This directly addresses the success criteria #3 (KL divergence < 10⁻⁴) and is testable by end-to-end evaluation of the full adaptive correction framework using only standard float64.

**Experiment:**
1. Implement the integrated reformulation: log-space error parameterization + guarded log-gamma + adaptive correction framework
2. Process streaming prime sequences (10⁸ elements) with real-time calibration
3. Measure KL divergence between calibrated LDAB density and empirical distribution at checkpoints (10⁶, 10⁷, 10⁸)
4. Run 30 independent trials to assess variability
5. **Metric:** Mean KL divergence with 95% confidence interval (target: upper bound < 10⁻⁴)

---

## Hypothesis 5: Computational Latency Overhead Remains Below 5% Threshold

**Statement:** The log-space reformulation and guarded computations will introduce less than 5% additional latency compared to the original uncalibrated LDAB model, satisfying the real-time performance constraint.

**Why it's testable:** Latency is a directly measurable performance metric that can be compared between baseline and reformulated implementations under identical workloads.

**Experiment:**
1. Benchmark baseline LDAB model (uncalibrated) on streaming prime data: measure per-element processing time over 10⁶ iterations
2. Benchmark reformulated model (log-space + guarded) on identical data stream
3. Compute overhead: (T_reformulated - T_baseline) / T_baseline × 100%
4. Test both with fixed and variable streaming rates to assess robustness
5. **Metric:** Percentage latency overhead (target: < 5%)

---

## Summary Table

| Hypothesis | Core Claim | Primary Metric | Target Threshold |
|------------|-----------|-----------------|------------------|
| H1 | Log-space eliminates precision collapse | % finite estimates at k ≥ 4 | 100% |
| H2 | Normalized error is k-independent | p-value for stationarity | > 0.05 |
| H3 | Guarded error propagation < 10⁻³ | Max | error vs. reference |
| H4 | KL divergence < 10⁻⁴ (float64 only) | Mean KL with CI | < 10⁻⁴ |
| H5 | Latency overhead < 5% | % additional latency | < 5% |

---

These hypotheses build sequentially on the prior findings: run_038's guarded log-gamma is extended in H1-H3, run_039's asymptotic framework is validated in H2, and the combined approach is evaluated against all three success criteria in H4-H5.