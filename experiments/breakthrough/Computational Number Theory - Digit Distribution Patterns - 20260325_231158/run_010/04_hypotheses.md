

# Testable Hypotheses for Primorial-Adjusted Benford Model Failure

---

## Hypothesis 1: Normalization Overcorrection via Coprime Filtering

**Hypothesis Statement:**
The original primorial-adjusted model applies an excessive weighting correction for coprime digits, causing it to deviate *further* from the true prime distribution than if no Benford adjustment were applied at all.

**Why It's Testable:**
If the model overcorrects, then reducing the coprime weighting strength should produce distributions progressively closer to the empirical Base-210 data. We can systematically vary the normalization exponent and measure KL divergence.

**Experiment:**
1. Compute the empirical distribution from the existing Base-210 dataset
2. Generate theoretical distributions with a scaling parameter α that interpolates between uniform (α = 0), the original Benford-adjusted coprime model (α = 1), and a continuum of intermediate corrections
3. Calculate KL divergence for each α value
4. Identify the α value that minimizes divergence, and test whether α ≠ 1 (i.e., overcorrection occurred)

---

## Hypothesis 2: Base-Scaling Incompatibility with Logarithmic Weighting

**Hypothesis Statement:**
The logarithmic density function log₁₀(d) used to weight leading digit probabilities is not appropriately scaled for the geometric structure of Base-210, where the "first digit" is determined by membership in a specific residue class modulo 210 rather than by the decimal scale-invariant mechanism that produces Benford's law.

**Why It's Testable:**
We can compare two alternative density formulations: (a) the original logarithmic base-10 weighting, and (b) a density based on the natural logarithm of the primorial base itself. If the model fails due to base-scaling, switching density formulations should improve fit.

**Experiment:**
1. Derive an alternative expected distribution using P(d) ∝ ln(1 + 1/d) scaled to the primorial base modulus rather than log₁₀
2. Compare this new theoretical distribution against the empirical Base-210 data
3. Test whether the primorial-scaled density produces lower KL divergence than both the original model and uniform distribution

---

## Hypothesis 3: Asymptotic Uniformity Override

**Hypothesis Statement:**
Diaconis's theorem establishing asymptotic uniformity of prime leading digits dominates over any primorial-based adjustment. The original model failed because it attempted to impose Benford-weighted probabilities when the data should converge toward uniformity regardless of base representation.

**Why It's Testable:**
If this hypothesis is correct, then the empirical Base-210 distribution should show only marginal deviations from uniformity, concentrated in specific digit classes. A model incorporating uniform baseline with small perturbation terms for coprime effects should outperform both the original Benford model and pure uniformity.

**Experiment:**
1. Fit a model of the form: P(d) = (1/9)(1 - ε) + ε × w_d, where w_d represents coprime-based perturbation weights normalized to sum zero
2. Estimate ε (the perturbation strength) by minimizing KL divergence against empirical data
3. Test whether ε is small but nonzero (confirming uniform baseline with slight coprime effects)

---

## Hypothesis 4: Subset Density vs. Full-Set Density Mismatch

**Hypothesis Statement:**
The original derivation computed coprime densities over the full set of 210 residues but then applied these weights only to the subset of digits that can actually appear as leading digits in Base-210. This inclusion of non-leading-digit residues in the normalization corrupts the probability mass assignments.

**Why It's Testable:**
We can derive a corrected model by restricting the normalization to only those residues that can serve as leading digits in Base-210, then test whether this restricted normalization yields better alignment with empirical frequencies.

**Experiment:**
1. Identify all residues modulo 210 that can appear as the "first non-zero digit" in Base-210 representation
2. Recompute coprime density weights using only this restricted residue set
3. Calculate the revised theoretical distribution and compare KL divergence to original model and uniform baseline

---

## Hypothesis 5: Finite-Sample Oscillatory Phase artifact

**Hypothesis Statement:**
The Base-210 dataset captures primes in a specific numerical range where distribution oscillatory terms (known to exist from number theory results) have a particular phase that makes the distribution resemble uniformity more than Benford's law. The original model implicitly assumed convergence to Benford distribution, which requires ranges far beyond the empirical sample.

**Why It's Testable:**
If oscillatory phase effects are responsible, then examining the distribution *conditional* on specific residue classes modulo the primorial should reveal that some classes follow Benford-like patterns while others follow anti-Benford patterns, averaging to near-uniformity in the aggregate.

**Experiment:**
1. Segment the Base-210 empirical data by residue class modulo 210
2. Compute the empirical leading-digit distribution within each residue class
3. Test whether within-class distributions show heterogeneous patterns (some Benford-like, some anti-Benford) that aggregate to near-uniformity
4. Verify whether the original model's assumption of homogeneous Benford convergence is violated

---

## Summary Table

| Hypothesis | Core Claim | Key Prediction | Testable Metric |
|------------|------------|----------------|-----------------|
| H1: Overcorrection | Coprime weighting too strong | Optimal α < 1 | KL vs. α curve |
| H2: Base-scaling | Wrong logarithm base | ln-based model fits better | KL comparison |
| H3: Uniformity override | Uniform is correct baseline | Small ε perturbation model | ε estimate significance |
| H4: Subset normalization | Wrong normalization set | Restricted-residue model wins | KL comparison |
| H5: Oscillatory phase | Finite-sample oscillation | Heterogeneous within-class patterns | χ² across residue classes |