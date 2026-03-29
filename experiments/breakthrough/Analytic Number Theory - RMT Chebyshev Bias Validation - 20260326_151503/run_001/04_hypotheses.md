# Testable Hypotheses for RMT-Corrected Chebyshev Bias Research

---

## Hypothesis 1: RMT Covariance Matrix Validation

**Statement:** The covariance matrix derived from the first 100–1000 non-trivial zeros of Dirichlet L-functions modulo 210 will accurately predict the variance structure of Chebyshev bias, with the fitted variance factor α agreeing within 10% of the theoretically computed value.

**Why it's testable:** This hypothesis makes a quantitative prediction that can be directly verified by:
- Computing L-function zeros using LMFDB data or local zero-finders
- Constructing the RMT-predicted covariance matrix
- Fitting α to observed prime count data across residue classes
- Comparing fitted values against analytical predictions

**Experiment:** 
1. Retrieve or compute the first 500 non-trivial zeros of L-functions for all characters modulo 210
2. Using these zeros, compute the theoretical covariance matrix Σ_RMT according to Rubinstein-Sarnak framework
3. Generate prime counts π(x; q, a) for all valid residue classes up to x = 10^8
4. Fit α by maximum likelihood using the Mahalanobis distance framework
5. Compare fitted α against the analytically derived value from character sum computations

**Expected outcome:** Strong agreement (within 10%) would confirm the RMT covariance model's validity; disagreement would indicate missing terms or computational inaccuracies in zero data.

---

## Hypothesis 2: Universality of RMT-Corrected Bias Detection at Higher Primorials

**Statement:** The RMT-corrected statistical framework (using Mahalanobis-distance-based tests with L-function-derived covariance) will successfully detect statistically significant Chebyshev bias at moduli 30030 and 510510, with p < 0.01, and the detected bias intensity will scale as log log x in agreement with Rubinstein-Sarnak asymptotics.

**Why it's testable:** This hypothesis predicts both detection success and a specific scaling law:
- Detection success can be measured via statistical significance (p-value)
- Scaling behavior can be tested by comparing bias magnitude at different x values
- The prediction is concrete: p < 0.01 for mod 30030, with measurable scaling

**Experiment:**
1. Implement RMT-corrected Mahalanobis test for moduli 30030 and 510510
2. Obtain L-function zeros for characters modulo these primorials (use LMFDB or compute first 200 zeros)
3. Generate prime counts up to N = 10^9 (distributed across GPU infrastructure)
4. Compute Mahalanobis distance D = √((π - μ)ᵀΣ⁻¹(π - μ))
5. Compare D against chi-square distribution with appropriate degrees of freedom
6. Repeat at multiple x values (10^7, 10^8, 10^9) to test log log x scaling

**Expected outcome:** Significant detection (p < 0.01) at both moduli, with bias magnitude M(x) satisfying M(x) ≈ c·log log x for constant c predicted by theory.

---

## Hypothesis 3: LDAB Model Generalization to Higher Primorial Bases

**Statement:** The Logarithmic-Density-Adjusted Benford (LDAB) model will achieve KL divergence < 10⁻³ for prime leading digits in Base-2310 and Base-30030 at N = 10¹⁰, while failure at Base-30 persists due to the structural artifact of overlapping digit-length boundaries in that base.

**Why it's testable:** This hypothesis makes two separable predictions:
- KL divergence threshold achievement for new bases
- A specific structural cause for Base-30 failure

Both can be verified through direct computation and analytical investigation.

**Experiment:**
1. Deploy 4-GPU distributed architecture to generate primes up to 10¹⁰ (chunked processing)
2. Count leading digit distributions in Base-2310 and Base-30030 representations
3. Compute LDAB-predicted distributions using hierarchical summation for FP precision
4. Calculate KL divergence D_KL(observed || LDAB) for each base
5. For Base-30 analysis: examine the specific distribution of digit lengths and their overlap structure
6. Compare LDAB performance across bases to identify systematic patterns

**Expected outcome:** KL divergence < 10⁻³ for Base-2310 and Base-30030, with Base-30 failure linked to digit-length distribution properties (measurable via entropy analysis of digit lengths).

---

## Hypothesis 4: Li(x) Correction Superiority Over PNT-Based LDAB

**Statement:** Replacing the PNT approximation π'(x) ~ x/ln(x) with the logarithmic integral π'(x) ~ Li(x) in the LDAB framework will reduce KL divergence by at least one order of magnitude at N ≥ 10¹⁰, with further improvement possible through inclusion of oscillatory corrections from the first 10 Riemann zeta zeros.

**Why it's testable:** This is a direct comparative hypothesis:
- Two models can be implemented and evaluated on identical data
- KL divergence provides a quantitative comparison metric
- The improvement is directional (Li(x) better than 1/ln(x))

**Experiment:**
1. Implement baseline LDAB using PNT: P(d) ∝ log₁₀(1 + 1/d)
2. Implement Li(x)-corrected LDAB: replace 1/ln(x) weighting with Li(x) - Li(previous_prime)
3. Optionally implement ζ-zero-corrected variant: add oscillatory terms Σ A_k·cos(γ_k log x)
4. Evaluate all three models at N = 10¹⁰ using primes up to that bound
5. Compute KL divergence for each model with hierarchical summation for precision
6. Test significance of improvements using bootstrapped confidence intervals

**Expected outcome:** Li(x)-corrected model achieves measurably lower KL divergence; oscillatory corrections provide additional refinement measurable at the 10⁻⁶ precision level.

---

## Hypothesis 5: Analytical Derivation of Generalized Variance Factor α

**Statement:** The variance factor α(q) for Chebyshev bias can be expressed as α(q) = f(χ, ρ_L) where f is a computable function of Dirichlet character sums and L-function zero densities, and this formula generalizes from q = 210 to q = 2310 with testable predictions for α(2310).

**Why it's testable:** This hypothesis makes a concrete structural prediction:
- An explicit formula exists relating α to character and zero data
- The formula can be computed independently for q = 210 and q = 2310
- Predictions for α(2310) can be verified against empirical fitting

**Experiment:**
1. Using known character sums for mod 210, derive the analytical expression for α(210) via:
   - Compute ∑_χ χ(n) log n type sums
   - Calculate zero density contributions from L-function zeros
   - Express α = α(char_sums, zero_density)
2. Apply same derivation framework to mod 2310 characters
3. Predict α(2310) from this formula
4. Fit α(2310) empirically from prime count data (N = 10⁹)
5. Compare predicted α(2310) against empirical fit (expect agreement within 15%)
6. If disagreement occurs, refine the analytical formula by identifying missing terms

**Expected outcome:** Successful derivation of α(q) formula that correctly predicts variance factors for both moduli, confirming the theoretical framework's completeness.

---

## Summary Table

| Hypothesis | Core Prediction | Key Metrics | Test Scale |
|------------|-----------------|-------------|------------|
| H1 | RMT covariance validates α within 10% | | N = 10⁸ (mod 210) |
| H2 | Bias detected at p < 0.01 for mod 30030, 510510 | p-value, scaling coefficient | N = 10⁹ |
| H3 | LDAB KL < 10⁻³ for bases 2310, 30030 | KL divergence | N = 10¹⁰ |
| H4 | Li(x) improves KL by ≥1 order of magnitude | KL divergence ratio | N = 10¹⁰ |
| H5 | α(q) formula correctly predicts α(2310) | Prediction error | N = 10⁹ |