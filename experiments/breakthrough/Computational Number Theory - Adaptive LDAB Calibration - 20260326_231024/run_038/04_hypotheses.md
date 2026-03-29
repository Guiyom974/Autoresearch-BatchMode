# Testable Hypotheses for Guarded Log-Gamma LDAB Calibration

Based on the research problem and prior findings showing that unguarded gamma evaluations fail at primorial index k=5 and that simple overflow guards are insufficient, I propose the following testable hypotheses:

---

## Hypothesis 1: Strictly Logarithmic Gamma Computation with Asymptotic Expansion Will Eliminate Numerical Overflow at k=5

**Statement:** Implementing a custom log-gamma function using asymptotic expansions (e.g., high-order Stirling's approximation with Bernoulli numbers) will prevent numerical overflow at primorial index k=5, allowing continuous computation of log-binomial terms.

**Why It's Testable:** This hypothesis makes a concrete, falsifiable prediction: the baseline implementation that fails at k=5 will successfully execute beyond k=5 when using the guarded log-domain approach. Overflow occurrence (binary outcome) can be directly measured.

**Experiment:** 
1. Implement a custom `log_gamma(x)` function using Stirling's asymptotic expansion with terms up to O(1/x^5)
2. Replace all direct `gamma()` calls in the LDAB calibration pipeline with `log(gamma(x))` computed via the new function
3. Execute the pipeline for primorial indices k=1 through k=150
4. Record overflow flags (presence/absence of IEEE-754 infinity or NaN values)
5. Compare to baseline (which fails at k=5)

---

## Hypothesis 2: Guarded Log-Gamma Implementation Will Introduce Less Than 20% Computational Overhead Across All Primorial Indices

**Statement:** The computational overhead introduced by guarded log-gamma computations will remain below 20% of native high-precision operations for all primorial indices k from 1 to 131.

**Why It's Testable:** Execution time is a quantitative metric that can be precisely measured and compared. The 20% threshold provides an objective success criterion against which the hypothesis can be evaluated.

**Experiment:**
1. Benchmark execution time for the original LDAB calibration (unmodified) as baseline
2. Benchmark execution time for the guarded log-gamma implementation
3. Calculate overhead percentage: ((T_guarded - T_baseline) / T_baseline) × 100%
4. Test across k=1 to k=131
5. Apply statistical analysis (mean, standard deviation, confidence intervals) to determine if overhead consistently remains <20%

---

## Hypothesis 3: KL Divergence of LDAB Density Estimates Will Remain Below 10⁻⁴ When Using Guarded Log-Gamma Formulations

**Statement:** The Kullback-Leibler divergence between density estimates computed with guarded log-gamma and reference high-precision computations will remain below 10⁻⁴ for all primorial indices up to k=131.

**Why It's Testable:** KL divergence is a mathematically well-defined metric that quantifies information loss. By comparing guarded implementations against a reference standard (e.g., arbitrary-precision rational computations or verified lookup tables), the hypothesis can be directly tested.

**Experiment:**
1. Establish reference density estimates using arbitrary-precision arithmetic (e.g., Python's `decimal` module with 100+ digits) for k=1 to k=131
2. Compute density estimates using the guarded log-gamma implementation
3. Calculate KL divergence: D_KL(P_ref || P_guarded)
4. Track divergence values across all k
5. Verify divergence < 10⁻⁴ threshold

---

## Hypothesis 4: Dynamic Precision Scaling Will Extend Operational Capacity Beyond k=131 While Maintaining KL Divergence < 10⁻⁴

**Statement:** Implementing adaptive precision scaling (dynamically increasing bit precision as k increases) will enable stable LDAB calibration beyond k=131 while maintaining KL divergence below 10⁻⁴.

**Why It's Testable:** This hypothesis predicts a causal relationship between dynamic precision adjustment and extended operational range. The experiment can measure both the maximum achievable k and associated KL divergence values.

**Experiment:**
1. Implement a dynamic precision module that increases precision by 16 bits whenever KL divergence exceeds a sliding threshold (e.g., 5×10⁻⁵)
2. Run LDAB calibration with dynamic precision from k=1 upward
3. Record: (a) precision level at each k, (b) KL divergence at each k, (c) maximum k achieved without overflow
4. Compare against fixed-precision guarded implementation
5. Identify the precision-threshold mapping where accuracy degrades below acceptable levels

---

## Hypothesis 5: Different Asymptotic Expansions (Stirling, Lanczos, Burnside) Will Exhibit Distinct Efficiency-Accuracy Tradeoffs at Large k

**Statement:** The choice of asymptotic expansion method for log-gamma computation will significantly affect the efficiency-accuracy tradeoff at large primorial indices, with Stirling's approximation favoring speed at low k while Lanczos coefficients providing better accuracy at high k.

**Why It's Testable:** This hypothesis predicts differential performance characteristics across three distinct mathematical methods. Comparative benchmarking can measure both accuracy (KL divergence) and efficiency (execution time) for each method.

**Experiment:**
1. Implement three guarded log-gamma variants:
   - **Stirling:** Using terms up to 1/(12x) - 1/(360x³) + 1/(1260x⁵)
   - **Lanczos:** Using the g=5 Lanczos approximation with 6 coefficients
   - **Burnside:** Using the log-gamma formula with cosine terms
2. Benchmark each variant for k=1 to k=150
3. Measure: execution time, KL divergence (vs. reference), overflow occurrence
4. Analyze tradeoffs: Does Stirling become inaccurate at lower k than Lanczos? Does Burnside offer superior stability?
5. Determine optimal method selection as a function of primorial index

---

## Summary Table

| Hypothesis | Key Variable | Success Metric | Falsification Criterion |
|------------|--------------|----------------|-------------------------|
| H1 | Overflow occurrence | Binary (overflow yes/no) | Overflow still occurs at k=5 |
| H2 | Execution time overhead | Percentage | Overhead ≥ 20% |
| H3 | KL divergence | Numeric value | KL ≥ 10⁻⁴ at any k ≤ 131 |
| H4 | Maximum stable k | Primorial index | Cannot reach k > 131 with KL < 10⁻⁴ |
| H5 | Method accuracy | KL divergence per method | No significant difference between methods |

These hypotheses build on prior findings by directly addressing the k=5 overflow failure point (H1), extending evaluation beyond the observed limits (H4), and systematically exploring solution approaches rather than relying on ad-hoc overflow guards.