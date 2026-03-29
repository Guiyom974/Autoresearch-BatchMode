

# Testable Hypotheses for RMT-Corrected Chebyshev Bias Research

Based on the research problem and search context, I propose five testable hypotheses that address the core open questions while maintaining clear experimental pathways.

---

## Hypothesis 1: RMT Covariance Model Validation Against L-Function Zeros

### 1. Statement
The covariance matrix for Chebyshev bias at modulus 210, derived from the nontrivial zeros of Dirichlet L-functions modulo 210, will reproduce the observed variance in prime count differences between quadratic residue and non-residue classes with accuracy within 10% of the theoretical variance factor α.

### 2. Why It's Testable
This hypothesis is testable because:
- **Concrete prediction**: The LMFDB provides computed zeros for Dirichlet L-functions mod 210, allowing direct construction of the predicted covariance matrix
- **Quantifiable comparison**: The variance factor α can be computed both theoretically (from zeros) and empirically (from prime counting data), enabling direct comparison
- **Statistical framework**: The Mahalanobis-distance test provides a formal statistical metric (p-value) for assessing match quality

### 3. Experimental Design
```
Experiment 1: L-Function Zero Extraction and Covariance Construction
├── Data Collection:
│   ├── Retrieve first 500 nontrivial zeros from LMFDB for each of the φ(210)=48 
│   │   Dirichlet characters modulo 210
│   └── Compute theoretical covariance matrix Σ_RMT using formula:
│       Σ_RMT[i,j] = Σ_ρ (ψ(ρ)^{-1} + ψ(1-ρ)^{-1}) where ρ are L-function zeros
│
├── Empirical Validation:
│   ├── Generate prime counts π(x; 210, a) for x up to 10^8 using segmented sieve
│   ├── Compute empirical covariance matrix Σ_emp from 1000 bootstrap samples
│   └── Calculate α_emp = trace(Σ_emp) / trace(Σ_RMT)
│
├── Comparison Metrics:
│   ├── Frobenius norm distance: ||Σ_emp - Σ_RMT||_F / ||Σ_RMT||_F < 0.10
│   ├── Mahalanobis distance of QR/NR difference using Σ_RMT yields p < 0.001
│   └── α_fitted agrees with α_predicted within 10%
│
└── Success Criterion: Both comparison metrics satisfied simultaneously
```

---

## Hypothesis 2: Analytical Formula for Variance Factor α as Function of Character Sums

### 1. Statement
The variance factor α for modulus 210 can be expressed as a convergent series involving logarithmic derivatives of L-functions at s=1, and this formula generalizes to modulus 2310 with the same functional form but modified character sum coefficients.

### 2. Why It's Testable
- **Theoretical grounding**: Rubinstein-Sarnak theory provides the framework linking α to L-function behavior at s=1
- **Computable components**: Each term in the formula (character sums, Euler products, zero densities) is independently computable
- **Comparative test**: Different candidate formulas can be tested against empirical α values for both moduli

### 3. Experimental Design
```
Experiment 2: Analytical α Derivation and Validation
├── Theoretical Development:
│   ├── Propose candidate formula: α = (2/φ(q)) × Σ_χ≠χ₀ (log L'(1,χ)/L(1,χ))^2
│   ├── Include correction terms from even zeros: α_even = Σ_n c_n (log n)^{-k}
│   └── Derive generalization coefficients for mod 2310: α_2310 = c_2310 × α_210
│
├── Numerical Verification:
│   ├── Compute L'(1,χ)/L(1,χ) for all 48 characters mod 210 using high-precision
│   │   evaluation (1000 decimal places) via Dirichlet series
│   ├── Evaluate proposed formula numerically to obtain α_predicted
│   └── Compare with empirical α from Hypothesis 1 bootstrap analysis
│
├── Generalization Test:
│   ├── Apply same formula structure to mod 2310 (φ(2310)=576 characters)
│   ├── Compute α_predicted_2310 from first 200 characters
│   └── Validate against empirical prime counting data at mod 2310 (x ≤ 10^7)
│
└── Success Criterion: 
    - |α_predicted - α_emp| / α_emp < 0.10 for both mod 210 and mod 2310
    - Generalization coefficient c_2310 differs from c_210 by >10% (proving base-dependence)
```

---

## Hypothesis 3: Universality of RMT-Corrected Bias Detection at Higher Primorials

### 1. Statement
The RMT-corrected covariance framework, validated at modulus 210, will successfully detect Chebyshev bias at modulus 30030 with p < 0.01 using primes up to 10^9, and will detect a detectable signal at modulus 510510 with p < 0.05, with bias intensity scaling approximately as log log x predicted by theory.

### 2. Why It's Testable
- **Clear signal definition**: Bias detection reduces to statistical significance testing (p-value threshold)
- **Scaling prediction**: Theory predicts specific bias magnitude scaling, allowing confirmation or rejection
- **Sequential testing**: Success at mod 30030 is prerequisite for testing mod 510510, providing internal validation

### 3. Experimental Design
```
Experiment 3: Bias Detection Scaling Across Primorials
├── Phase 1: Modulus 30030 (P_6)
│   ├── Implementation:
│   │   ├── Construct RMT covariance matrix using first 300 L-function zeros
│   │   ├── Implement Mahalanobis-distance test for QR vs NR comparison
│   │   └── Apply to π(x; 30030, a) for all invertible classes
│   │
│   ├── Data Collection (GPU-accelerated):
│   │   ├── Generate primes up to 10^9 using distributed sieve
│   │   ├── Count primes in each of φ(30030)=5760 residue classes
│   │   └── Compute quadratic character χ_30030 for each class
│   │
│   └── Validation:
│       ├── Mahalanobis distance yields p < 0.01
│       └── Bias magnitude: Δ(x) = π_χ(x) - π(x)/φ(30030) scales as log log x
│
├── Phase 2: Modulus 510510 (P_7)
│   ├── Computational adaptations:
│   │   ├── φ(510510)=92160 classes requires sparse covariance matrix
│   │   ├── Sample 1000 random invertible classes for initial test
│   │   └── Use subset of L-function zeros (first 200) due to computational limits
│   │
│   ├── Data Collection:
│   │   ├── Primes up to 10^9 (same upper bound, denser class structure)
│   │   └── Classify primes by residue modulo 510510 using optimized hashing
│   │
│   └── Validation:
│       ├── Mahalanobis-distance p < 0.05 for sampled classes
│       └── Extrapolate to full class set using bootstrap resampling
│
├── Phase 3: Scaling Verification
│   └── Compute Δ(x) at x = 10^6, 10^7, 10^8, 10^9
│       └── Verify Δ(x) ∝ log log x within 20% tolerance
│
└── Success Criteria:
    - p < 0.01 at mod 30030
    - p < 0.05 at mod 510510 (or upper bound established)
    - Scaling exponent within [0.8, 1.2] of theoretical prediction
```

---

## Hypothesis 4: LDAB Model Generalization to Base-2310 and Base-30030

### 1. Statement
The Logarithmic-Density-Adjusted Benford (LDAB) model will achieve KL divergence below 10^-3 for prime leading digits in Base-2310 and Base-30030 when evaluated at N=10^10, confirming that the model structure (but not specific parameters) generalizes across primorial bases, while the known failure at Base-30 persists due to insufficient averaging over small logarithmic intervals.

### 2. Why It's Testable
- **Quantitative threshold**: KL divergence < 10^-3 provides unambiguous success/failure criterion
- **Comparative design**: Testing multiple bases simultaneously reveals whether LDAB has universal or base-specific structure
- **Diagnostic power**: By testing Base-30 failure explicitly, we can isolate the failure mechanism

### 3. Experimental Design
```
Experiment 4: LDAB Generalization and Failure Mode Analysis
├── Part A: Large-Scale LDAB Evaluation
│   ├── Infrastructure (4-GPU distributed system):
│   │   ├── Chunk primes into 10^8-size blocks
│   │   ├── Distribute blocks across GPUs with hierarchical FP64 summation
│   │   └── Process 10^10 total primes in approximately 100 chunks
│   │
│   ├── Base-2310 Evaluation:
│   │   ├── Convert each prime to Base-2310 representation
│   │   ├── Extract leading digit in this base
│   │   ├── Count occurrences of digits 1-2310 (actually analyze first-digit distribution)
│   │   └── Compute KL(P_obs || P_LDAB) where P_LDAB is theoretical Benford distribution
│   │
│   ├── Base-30030 Evaluation:
│   │   └── Same procedure as Base-2310
│   │
│   └── Expected Results:
│       ├── KL_2310 < 10^-3: confirms generalization
│       ├── KL_30030 < 10^-3: confirms scalability across bases
│       └── If KL > 10^-3: triggers failure mode analysis
│
├── Part B: Base-30 Failure Mode Investigation
│   ├── Hypothesis for failure:
│   │   H_0: LDAB requires averaging over log-intervals >> 1/χ(30) to be accurate
│   │   H_1: Small base (30) has insufficient "resolution" for logarithmic density
│   │
│   ├── Diagnostic experiments:
│   │   ├── Vary N from 10^6 to 10^10 at Base-30
│   │   ├── Measure KL(N) convergence behavior
│   │   ├── Compute effective sample size per logarithmic bin
│   │   └── Compare with theoretical predictions from Granville-Nguyen refinement
│   │
│   └── Structural characterization:
│       ├── If KL decreases as N increases: convergence issue (supports H_0)
│       └── If KL plateaus: fundamental model limitation (supports H_1)
│
└── Success Criteria:
    - KL divergence < 10^-3 for at least one of {Base-2310, Base-30030}
    - OR: Failure mode analytically characterized with mathematical proof
    - OR: Both criteria partially met with quantitative bounds established
```

---

## Hypothesis 5: Li(x) Correction Improves LDAB at Scale N ≥ 10^10

### 1. Statement
Replacing the PNT approximation π(x) ~ x/log(x) with the logarithmic integral Li(x) in the LDAB density calculation will reduce KL divergence by at least one order of magnitude at N=10^10, and incorporating the first 10 Riemann zeta zeros as oscillatory corrections will yield further measurable improvement.

### 2. Why It's Testable
- **Discrete comparison**: Two competing models (PNT-LDAB vs Li-LDAB) can be evaluated on identical data
- **Quantifiable improvement**: "At least one order of magnitude" provides measurable threshold
- **Additive contributions**: Testing zeros incrementally isolates their individual effects

### 3. Experimental Design
```
Experiment 5: Li(x) Correction and Zero Oscillation Effects
├── Part A: Li(x) vs PNT Correction
│   ├── Theoretical background:
│   │   ├── PNT-LDAB uses: ρ(d) ∝ log(d+1) - log(d) = log(1 + 1/d) ≈ 1/d
│   │   └── Li-LDAB uses: ρ(d) ∝ Li(b_d) - Li(b_{d-1}) where b_d = base^d
│   │       This accounts for non-uniform spacing of powers in exponential scale
│   │
│   ├── Implementation:
│   │   ├── Compute Li(x) = ∫_2^x dt/log(t) using exponential integral
│   │   ├── For digit d in base B: P_Li(d) = [Li(B^d) - Li(B^{d-1})] / Li(B^N)
│   │   └── Compare with standard P_LDAB(d) = log(1 + 1/d) / log(B)
│   │
│   ├── Evaluation protocol:
│   │   ├── Generate primes up to N = 10^10 using GPU infrastructure
│   │   ├── Compute leading digit distribution empirically: P_obs(d)
│   │   ├── Compute KL_standard = KL(P_obs || P_LDAB_PNT)
│   │   ├── Compute KL_Li = KL(P_obs || P_LDAB_Li)
│   │   └── Measure ratio: KL_Li / KL_standard
│   │
│   └── Success threshold: KL_Li ≤ 0.1 × KL_standard (one order of magnitude improvement)
│
├── Part B: Zero Oscillation Corrections
│   ├── Theoretical framework (from Riemann-Siegel formula):
│   │   ├── π_Li(x) ≈ Li(x) + Σ_{ρ} Li(x^ρ)/ρ + corrections
│   │   ├── Leading digit distribution inherits oscillatory terms from zeros
│   │   └── First 10 zeros: ρ_n = 1/2 + iγ_n where γ_n are imaginary parts
│   │
│   ├── Implementation:
│   │   ├── Extract zeros: γ_1=14.135, γ_2=21.022, ..., γ_10=52.970
│   │   ├── Compute oscillatory correction:
│   │   │   δ(x; k) = Σ_{n=1}^k [cos(γ_n log x) + i sin(γ_n log x)] / √2
│   │   │   (simplified from full Riemann-Siegel)
│   │   └── Modify LDAB: P_zero(d) = P_Li(d) × [1 + ε × δ(B^d)]
│   │
│   ├── Evaluation (sequential):
│   │   ├── KL_10 = KL(P_obs || P_zero_10) using first 10 zeros
│   │   ├── KL_5 = KL(P_obs || P_zero_5) using first 5 zeros
│   │   ├── KL_1 = KL(P_obs || P_zero_1) using first zero only
│   │   └── Verify monotonic decrease: KL_10 < KL_5 < KL_1 < KL_Li
│   │
│   └── Success criterion: KL_10 < KL_Li with statistical significance (paired t-test, p < 0.05)
│
└── Success Criteria:
    - KL_Li < 0.1 × KL_PNT at N = 10^10
    - Zero-corrected model shows additional measurable improvement
    - OR: Upper bound established for zero correction effect (e.g., <5% improvement = negligible)
```

---

## Summary Table: Hypothesis Mapping to Research Questions

| Hypothesis | Research Question Addressed | Primary Testable Output |
|------------|------------------------------|------------------------|
| H1: RMT Covariance Validation | Q1: L-function zero validation | α agreement within 10% |
| H2: Analytical α Formula | Q2: Closed-form expression | Formula accuracy < 10% error |
| H3: Universality at Higher Primorials | Q3: Detection at 30030, 510510 | p < 0.01, p < 0.05 respectively |
| H4: LDAB Generalization | Q4: Base-specific corrections | KL < 10^-3 for new bases |
| H5: Li(x) Correction | Q5: Li(x) improvement | ≥10× KL reduction |

Each hypothesis is designed to produce either a confirmed result or a quantitative upper bound, ensuring productive outcomes regardless of which direction the data points.