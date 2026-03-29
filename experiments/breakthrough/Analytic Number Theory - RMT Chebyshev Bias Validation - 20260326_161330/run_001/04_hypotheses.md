# Testable Hypotheses for RMT-Corrected Chebyshev Bias and LDAB Validation

Based on the research problem, I propose five testable hypotheses that address the core theoretical and empirical questions while building on the confirmed breakthroughs.

---

## Hypothesis 1: RMT-Derived Covariance Model Validation

### 1. The Hypothesis Statement
The covariance matrix for Chebyshev bias statistics at modulus 210, derived from L-function zero distributions via random matrix theory (specifically from the Gaussian Orthogonal Ensemble), will agree with empirically computed covariance estimates from prime counting data to within statistical uncertainty (≤5% relative error).

### 2. Why It's Testable
This hypothesis is directly testable because:
- The LMFDB provides validated data for the first 1000+ non-trivial zeros of Dirichlet L-functions for characters modulo 210
- We can compute the theoretical RMT covariance matrix analytically from these zeros using established formulas relating zero spacing to prime count variances
- We can independently compute the empirical covariance matrix from observed prime residue class counts at large N
- The comparison yields quantitative disagreement measures (relative error, Mahalanobis distance) that can be assessed against a 5% threshold

### 3. Experimental Design
**Step 1: Theoretical covariance computation**
- Retrieve L-function zero data for the 8 Dirichlet characters modulo 210 from LMFDB or compute locally using zero-finders (e.g., mpmath with 50-digit precision)
- Compute the predicted covariance matrix Σ_RMT using the formula relating character sum variances to zero correlations

**Step 2: Empirical covariance computation**
- Generate prime counts π(x; q, a) for all residue classes modulo 210 at x = 10^8, 10^9 using the segmented sieve
- Compute the sample covariance matrix Σ_emp from repeated bootstrap samples or multiple x-values
- Use hierarchical summation across 4 GPUs to maintain FP64 precision

**Step 3: Statistical comparison**
- Compute Frobenius norm of Σ_RMT - Σ_emp normalized by ||Σ_RMT||
- Apply the Mahalanobis-distance-based test using Σ_RMT as the reference
- Compare detection power: RMT-corrected test vs. empirical Σ_emp test

**Expected outcome:** Agreement within 5% validates the RMT covariance model; disagreement >10% indicates missing terms in the theoretical derivation.

---

## Hypothesis 2: Analytical Formula for Variance Factor α

### 1. The Hypothesis Statement
The variance factor α (scaling constant relating primitive character contributions to total bias variance) admits a closed-form expression as α = Σ_χ≠χ_0 (c_χ / L(1, χ))^2, where c_χ are coefficients depending on character type and the sum runs over primitive characters modulo 210. This formula will generalize to modulus 2310 with the same structural form but different character coefficients.

### 2. Why It's Testable
This hypothesis is testable because:
- We can fit α empirically from the observed bias variance across multiple x-values
- We can compute the proposed analytical expression from character sum data
- Direct numerical comparison (fitted α vs. predicted α) yields a quantitative test
- The generalization claim is testable by repeating the procedure at modulus 2310

### 3. Experimental Design
**Step 1: Empirical α fitting**
- For modulus 210, collect bias measurements B(x) = (π(x; 210, NR) - π(x; 210, QR)) / π(x) at x = 10^7, 10^8, 10^9, 10^10
- Fit α_emp by regressing Var(B(x)) against the theoretical variance expression containing α as unknown constant
- Compute 95% confidence intervals via bootstrap resampling

**Step 2: Analytical α computation**
- Compute L(1, χ) for all primitive characters modulo 210 using high-precision evaluation
- Determine c_χ coefficients from the character sum structure (derived from quadratic field discriminants)
- Evaluate the proposed sum formula to obtain α_pred

**Step 3: Generalization test**
- Repeat Steps 1-2 for modulus 2310 using primes up to N = 10^9
- Verify the structural form holds (same formula, new coefficients)
- Compare α_pred / α_emp ratio across both moduli

**Expected outcome:** α_pred agrees with α_emp within confidence intervals, confirming the analytical formula and its generalizability.

---

## Hypothesis 3: Universality of RMT-Corrected Detection at Higher Primorials

### 1. The Hypothesis Statement
The RMT-corrected Mahalanobis-distance test, using the theoretically predicted covariance structure, will detect Chebyshev bias at modulus 30030 with statistical significance p < 0.01 using prime data up to N = 10^9, and at modulus 510510 with p < 0.05 using N = 10^10. The bias intensity will scale as predicted by the Rubinstein-Sarnak framework (proportional to the number of independent primitive characters).

### 2. Why It's Testable
This hypothesis is testable because:
- We can implement the RMT-corrected test at arbitrary moduli given the character structure
- The prediction of increasing bias intensity with more characters is quantitative (scales with √(number of primitive characters))
- Statistical significance thresholds (p-values) are directly computable from the Mahalanobis distance distribution
- We can compare detection power between moduli to test the scaling prediction

### 3. Experimental Design
**Step 1: Covariance matrix construction for new moduli**
- For mod 30030: Identify all primitive Dirichlet characters (should be φ(30030)/2 - 1 = 23 independent characters)
- Compute the L-function zero correlations required for the covariance matrix
- For mod 510510: Repeat with corresponding character set

**Step 2: Prime data generation**
- Use segmented sieve to generate all primes up to 10^9 (for mod 30030) and 10^10 (for mod 510510)
- Apply chunked processing across 4-8 GPUs with hierarchical summation for FP precision
- Count primes in each residue class for 100+ independent x-values to build the distribution

**Step 3: Statistical testing**
- Compute Mahalanobis distance D = √((μ_obs - μ_pred)^T Σ^{-1} (μ_obs - μ_pred)) where μ_pred = 0 under null hypothesis
- Determine p-value from chi-square distribution with appropriate degrees of freedom (number of residue classes - 1)
- Test both the significance threshold and the scaling relationship with number of characters

**Expected outcome:** Significant detection at mod 30030 confirms universality; scaling agreement validates the RMT framework extension.

---

## Hypothesis 4: LDAB Model Generalization to Base-2310 and Base-30030

### 1. The Hypothesis Statement
The Logarithmic-Density-Adjusted Benford (LDAB) model for prime leading digits will achieve KL divergence < 10^{-3} when applied to primes in Base-2310 and Base-30030 at N = 10^{10}, matching or exceeding performance achieved at Base-210. Failure at Base-30 (if confirmed) results from the insufficient number of digit classes (only 8) to capture Benford dynamics, not from base-specific mathematical constraints.

### 2. Why It's Testable
This hypothesis is testable because:
- KL divergence is a well-defined, computable metric for comparing distributions
- We can directly implement LDAB for arbitrary bases using the same formula: P(d) = log_10(1 + 1/(B^{L-1} · d)) where B is the base and L is the digit position
- The structural failure hypothesis makes a specific prediction that can be tested by analyzing the distribution of digit frequencies
- GPU infrastructure allows evaluation at N = 10^{10} within reasonable time

### 3. Experimental Design
**Step 1: LDAB evaluation at Base-2310**
- Implement digit extraction for Base-2310 (requires representation of primes in this mixed-radix system)
- Process all primes up to 10^{10} using 4-GPU distributed chunked architecture
- Compute observed leading digit distribution empirically
- Calculate KL divergence: D_KL(P_obs || P_LDAB)

**Step 2: LDAB evaluation at Base-30030**
- Repeat the same procedure for Base-30030
- Compare KL divergence values between bases

**Step 3: Failure mode analysis for Base-30**
- If KL divergence ≥ 10^{-3} for Base-30 at matching scale, analyze the specific digit classes contributing to divergence
- Test the hypothesis that few digit classes (only 8 possible leading digits vs. many more in larger bases) cause the failure
- Simulate LDAB with artificially restricted digit sets to confirm the mechanism

**Expected outcome:** KL divergence < 10^{-3} for both new bases confirms generalization; if not, the structural analysis explains why Base-30 is a special case.

---

## Hypothesis 5: Li(x) Correction Improves LDAB Performance

### 1. The Hypothesis Statement
Replacing the PNT approximation π(x) ~ x/log(x) with the logarithmic integral Li(x) = ∫₂ˣ dt/log(t) in the LDAB model will reduce KL divergence by at least one order of magnitude at N = 10^{10}, with further improvement possible by incorporating oscillatory corrections from the first 10 Riemann zeta zeros. The combined Li(x) + zero-correction model will achieve KL divergence < 10^{-6}.

### 2. Why It's Testable
This hypothesis is testable because:
- Li(x) and its zero-corrected variant have explicit, computable formulas
- KL divergence improvement is directly measurable by comparing two models on the same data
- The theoretical justification (better prime counting approximation) makes specific predictions about where improvements will appear (in the tail of the distribution, affecting rare digit frequencies)
- The magnitude of improvement (one order of magnitude minimum) provides a clear threshold

### 3. Experimental Design
**Step 1: Standard PNT-LDAB baseline**
- Replicate the LDAB evaluation for Base-2310 at N = 10^{10} using the standard formula P(d) = log_10(1 + 1/d) adjusted for logarithmic density
- Record KL divergence D_KL(standard)

**Step 2: Li(x)-corrected LDAB**
- Modify the logarithmic density calculation to use dP/dx = Li'(x) = 1/log(x) instead of 1/(x·log(x))
- Implement the corrected leading digit probability formula incorporating Li(x) for the density adjustment
- Evaluate on the same prime dataset, computing D_KL(Li-corrected)

**Step 3: Zero-corrected variant**
- Retrieve the first 10 non-trivial zeros of ζ(s): ρ_n = 0.5 + i·t_n for n = 1,...,10
- Implement the explicit formula approximation for π(x) including oscillatory terms
- Evaluate the resulting LDAB distribution and compute D_KL(zero-corrected)

**Step 4: Statistical comparison**
- Compare all three KL divergence values
- Test whether Li(x) correction achieves the one-order-of-magnitude improvement threshold
- Analyze which digit classes benefit most from the correction

**Expected outcome:** Measurable improvement from Li(x) correction confirms the PNT approximation as a limiting factor; zero corrections provide additional refinement at the 10^{-6} level.

---

## Summary Table

| Hypothesis | Independent Variable | Dependent Variable | Expected Effect Size |
|------------|---------------------|-------------------|---------------------|
| H1 | RMT covariance matrix | Empirical covariance agreement | ≤5% relative error |
| H2 | Character sum formula | Fitted variance factor α | Agreement within CI |
| H3 | Modulus (30030, 510510) | p-value of bias detection | p < 0.01, p < 0.05 |
| H4 | Base (2310, 30030) | KL divergence | < 10^{-3} |
| H5 | Li(x) + zero corrections | KL divergence improvement | ≥1 order of magnitude |

Each hypothesis is falsifiable through the proposed experiments, addresses a specific research question from the problem statement, and builds cumulatively toward the overall research objectives.