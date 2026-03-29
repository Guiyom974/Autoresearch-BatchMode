

# Testable Hypotheses for RMT-Corrected Chebyshev Bias Research

Based on the research problem and search context regarding Chebyshev bias, Rubinstein-Sarnak theory, and primorial moduli, I propose the following five testable hypotheses:

---

## Hypothesis 1: RMT Covariance Model Validates α for Mod 210

**Statement:**  
The variance factor α in the Chebyshev bias distribution for mod 210 can be accurately predicted from the L-function zero structure via the formula:

$$\alpha = \frac{1}{2\pi}\sum_{\chi \neq \chi_0}\sum_{\gamma>0}\frac{1}{\frac{1}{4}+\gamma^2}\log\left(\frac{q}{\pi}\right) + O\left(\frac{1}{q}\right)$$

where γ denotes the imaginary parts of non-trivial zeros of Dirichlet L-functions modulo 210.

**Why it's testable:**  
This hypothesis makes a quantitative prediction linking directly observable L-function zeros (available from LMFDB or computed via zero-finders) to the empirically measured variance of prime count differences between quadratic residue and non-residue classes. The prediction is falsifiable—if computed α from zeros differs from observed α by >10%, the hypothesis fails.

**Experiment:**  
1. Retrieve/compute the first 500 non-trivial zeros for all 48 non-principal Dirichlet characters modulo 210 (using LMFDB API or `mpmath.zeta_zeros` with character-specific computation).  
2. Numerically evaluate the theoretical variance integral using the extracted zeros.  
3. Generate prime counts π(x; 210, *q*) for all 96 quadratic character classes up to x = 10^8.  
4. Compute empirical variance of (QR − NQR) differences and extract fitted α.  
5. Compare predicted vs. empirical α; accept if agreement within 10% and p < 0.001 on Mahalanobis distance test.

---

## Hypothesis 2: RMT-Corrected Bias Detection Extends Universally to Higher Primorials

**Statement:**  
The RMT-corrected statistical framework using L-function-derived covariance matrices will detect statistically significant Chebyshev bias (p < 0.01) at mod 30030 and mod 510510, with bias intensity scaling as:

$$\text{bias magnitude} \sim \alpha_P \cdot \log\log N$$

where α_P is the primorial-specific variance factor predicted by the generalized RMT model.

**Why it's testable:**  
This hypothesis predicts both detection significance and functional form of scaling. It can be tested by implementing the Mahalanobis-distance test with primorial-specific covariance matrices and applying it to computed prime data. The prediction of scaling behavior provides an additional quantitative constraint beyond mere detection.

**Experiment:**  
1. Implement Mahalanobis-distance-based hypothesis test using RMT covariance matrices computed from L-function zeros for mod 30030 (480 characters, φ(30030)/2 = 1920 quadratic character classes) and mod 510510.  
2. Generate prime sieves up to N = 10^9 for both moduli (using segmented Eratosthenes with residue class tracking).  
3. For each primorial, compute the observed QR/NQR count vector and its Mahalanobis distance from the RMT-predicted mean (zero under GRH).  
4. Perform 10,000 Monte Carlo simulations under the RMT null to determine empirical p-values.  
5. Fit bias magnitude vs. log log N to verify α_P scaling; reject hypothesis if p > 0.01 for either primorial.

---

## Hypothesis 3: LDAB Model Generalizes to Base-2310 and Base-30030 with KL Divergence < 10⁻³

**Statement:**  
The Logarithmic-Density-Adjusted Benford (LDAB) model, previously validated for Base-210, will achieve KL divergence < 10⁻³ when applied to prime leading digits in Base-2310 and Base-30030, provided that:

1. The base-specific logarithmic density is computed as D_B(d) = log₁₀(1 + 10^(-d·log₁₀(B))) / log₁₀(B), and  
2. Hierarchical FP64 summation is used for the prime-count weighting function.

**Why it's testable:**  
This is a direct quantitative prediction about KL divergence values achievable with a specified algorithm. It can be tested by running the established GPU-accelerated LDAB computation on new primorial bases and measuring KL divergence against the theoretical distribution.

**Experiment:**  
1. Using the existing 4-GPU distributed chunked architecture, implement Base-2310 and Base-30030 prime generation with leading-digit extraction (first digit in base B representation).  
2. Compute hierarchical summation of prime weights w(p) = 1/ln(p) across chunks, aggregating via FP64 accumulation on CPU.  
3. Calculate empirical digit distribution and compute KL divergence:  

$$D_{KL}(P_{\text{obs}}||P_{\text{LDAB}}) = \sum_{d=1}^{B-1} P_{\text{obs}}(d)\ln\frac{P_{\text{obs}}(d)}{P_{\text{LDAB}}(d)}$$

4. Run at N = 10^10 for Base-2310 and N = 10^10 for Base-30030 (using chunked processing with chunk size 10^8).  
5. Accept hypothesis if both KL divergences < 10⁻³; if failure occurs, investigate whether failure is systematic (base-specific correction needed) or random (precision artifact).

---

## Hypothesis 4: Li(x) Correction Reduces KL Divergence by ≥1 Order of Magnitude vs. PNT-LDAB

**Statement:**  
Replacing the PNT approximation 1/ln(x) with the logarithmic integral Li(x) in the LDAB weight function will reduce KL divergence by at least one order of magnitude at N ≥ 10^10, because:

$$\text{weight}_{\text{Li}}(p) = \frac{d}{dx}\text{Li}(x)\bigg|_{x=p} = \frac{1}{\ln p} - \frac{1}{\pi}\sin\left(\frac{2\pi\ln p}{\ln 2}\right) + O\left(\frac{1}{\ln^2 p}\right)$$

introduces oscillatory corrections that better match actual prime distribution irregularities.

**Why it's testable:**  
This hypothesis predicts a specific improvement (≥10× reduction in KL divergence) from a defined algorithmic modification. It compares two computable quantities under controlled conditions, making it directly falsifiable through empirical benchmarking.

**Experiment:**  
1. Implement the Li(x)-based weight function using the complete formula with oscillatory terms derived from the first 10 Riemann zeta zeros (via the explicit formula for π(x)).  
2. Run parallel LDAB evaluations at N = 10^10 using both PNT-LDAB (weight = 1/ln p) and Li-LDAB (weight = dLi/dp with zero corrections).  
3. Use identical prime data, chunk boundaries, and hierarchical summation to ensure fair comparison.  
4. Compute KL divergence for both methods; hypothesis succeeds if:  

$$\frac{D_{\text{PNT}}}{D_{\text{Li}}} \geq 10$$

5. Also test whether improvement persists at N = 10^12 (extrapolation test) or whether correction magnitude diminishes.

---

## Hypothesis 5: Base-30 LDAB Failure Originates from Anomalous Prime Density in Character Subset

**Statement:**  
The documented failure of LDAB at Base-30 (KL divergence = 0.511 vs. < 0.000034 at Base-210) arises because the multiplicative group (Z/30Z)× ≅ C₂ × C₄ contains characters whose L-function zeros produce systematically larger variance corrections than other bases at comparable N, leading to visible deviations from Benford's law that the basic LDAB cannot absorb.

**Why it's testable:**  
This is a mechanistic hypothesis that predicts a specific causal structure. It can be tested by: (a) decomposing the Base-30 character contributions to variance, (b) identifying which characters produce outsized corrections, and (c) showing that a character-specific LDAB variant reduces KL divergence.

**Experiment:**  
1. Compute L-function zero contributions for each of the φ(30) = 8 Dirichlet characters modulo 30.  
2. Calculate the predicted variance contribution per character:  

$$\alpha_\chi = \frac{1}{2\pi}\sum_{\gamma>0}\frac{L'(1,\chi)}{L(1,\chi)}\frac{1}{\frac{1}{4}+\gamma^2}$$

3. Identify whether 1–2 characters dominate total variance (analogous to "exceptional characters" in other contexts).  
4. Implement a modified LDAB with character-specific scaling factors f_χ applied to the Benford density:  

$$P_{\text{char-LDAB}}(d) = \sum_\chi f_\chi \cdot D_B(d)$$

5. Optimize f_χ via least squares on empirical data; test whether resulting KL divergence < 10⁻³.  
6. Verify that the structural failure mode (if unremediable) is due to insufficient N rather than algorithmic deficiency by testing at N = 10^12.

---

## Summary Table

| Hypothesis | Key Prediction | Primary Test Metric | Required Data Scale |
|------------|----------------|---------------------|---------------------|
| H1: RMT α Validation | α_pred ≈ α_obs (±10%) | |  | Relative error in α | 100–500 L-function zeros + N = 10^8 primes |
| H2: Universality | p < 0.01 at mod 30030, 510510 | Mahalanobis p-value | N = 10^9 primes per modulus |
| H3: LDAB Generalization | KL < 10⁻³ at Base-2310/30030 | KL divergence | N = 10^10 primes (GPU) |
| H4: Li(x) Improvement | ≥10× KL reduction | KL ratio | N = 10^10 primes (paired test) |
| H5: Base-30 Mechanism | Character-specific variance decomposition | KL after correction | L-function zeros + N = 10^9 primes |

Each hypothesis is designed to be independently testable, builds on the confirmed results in the problem statement, and addresses a specific open question identified in the research framework.