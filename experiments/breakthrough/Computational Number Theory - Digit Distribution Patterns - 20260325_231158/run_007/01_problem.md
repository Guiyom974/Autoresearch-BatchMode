# Research Problem: Developing a Primorial-Adjusted Benford Null Model for Leading Digit Distributions in Prime Numbers

## Objective
Following the experimental finding that leading digits of primes up to $10^8$ in Base-210 deviate substantially from Benford's Law (KL divergence = 0.636), it is clear that primorial base structures introduce significant systematic artifacts independent of standard logarithmic scaling. The objective of this phase is to develop and validate a corrected "primorial-adjusted Benford" null model. By mathematically incorporating the known density of coprimes relative to the primorial base into the standard logarithmic baseline, we aim to determine whether the observed deviations vanish under this refined theoretical model or if deeper structural anomalies persist.

## Research Questions
1. **Mathematical Formulation:** How can the generalized Benford's Law for Base-$N$ be formally adjusted to weight digit probabilities based on their coprimality with $N$, specifically when $N$ is a high-order primorial (e.g., 30, 210, 2310)?
2. **Model Validation:** When testing primes up to $10^8$ in Base-210, does the residual KL divergence between the empirical leading-digit distribution and the new primorial-adjusted Benford model approach zero, or does a statistically significant residual remain?
3. **Residual Decomposition:** If residual divergence persists under the adjusted model, which specific leading digits (e.g., the dominant '1') drive these deviations, and do they correlate with deeper modular properties of the primorial?

## Methodology
1. **Theoretical Derivation:** Construct a modified probability mass function (PMF) that combines the standard Base-$N$ Benford probability $P(d) = \log_N(1 + 1/d)$ with a coprime filter function that zeroes out or down-weights digits sharing prime factors with the primorial base, re-normalizing the distribution appropriately.
2. **Data Generation:** Generate the sequence of prime numbers up to $10^8$. 
3. **Base Conversion & Extraction:** Convert the generated primes into Base-30 and Base-210, extracting the leading significant digit for each.
4. **Statistical Analysis:** Compute the KL divergence and perform Goodness-of-Fit tests comparing the empirical leading digit frequencies against:
   - The Uniform distribution (baseline check)
   - The standard Base-$N$ Benford distribution
   - The newly derived primorial-adjusted Benford distribution
5. **Per-Digit Residual Analysis:** Calculate and plot the per-digit error residuals between the empirical data and the adjusted model to identify any localized anomalies.

## Success Criteria
- Successful mathematical derivation of a normalized "primorial-adjusted Benford" probability distribution.
- A measurable, substantial reduction in KL divergence when evaluating the empirical prime data against the adjusted model compared to the standard Benford model (ideally reducing the previous 0.636 divergence to near zero).
- Clear identification and isolation of any remaining digit-specific biases that cannot be explained by either logarithmic scaling or basic coprimality to the base.

## Constraints
- The research must remain strictly focused on the digit structures of prime numbers in primorial bases.
- Computational limits restrict prime generation to an upper bound of $10^8$; algorithms must be optimized to handle base conversions (e.g., Base-210) efficiently at this scale.
- The analysis applies specifically to the *leading* digits to properly isolate logarithmic scaling effects from trailing-digit coprime restrictions.