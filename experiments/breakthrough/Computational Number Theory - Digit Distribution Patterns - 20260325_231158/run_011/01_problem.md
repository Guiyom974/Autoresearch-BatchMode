# Research Problem: Logarithmic Density and Prime Gap Corrections for Leading Digit Distributions in Primorial Bases

## Objective
To develop and validate a new theoretical model for the leading digit distribution of prime numbers in Base-210. Given previous findings that standard Benford's Law yields a high KL divergence (~0.64) and that coprime filtering overcorrects the distribution (optimal $\alpha = 0.00$), this research phase will abandon coprime adjustments. Instead, the objective is to formulate a correction mechanism utilizing logarithmic density corrections (derived from the Prime Number Theorem) and explicit prime gap adjustments to accurately capture the non-uniform distribution of prime leading digits.

## Research Questions
1. **Benford Deviation Analysis:** Why does standard Benford's Law fail so significantly to model prime leading digits in Base-210 (yielding a KL divergence of ~0.64), and to what extent does the logarithmic thinning of primes across the vast numerical intervals of Base-210 explain this deviation?
2. **Logarithmic Density Correction:** How can the continuous probability density function of primes, approximated by $1/\ln(x)$ via the Prime Number Theorem, be integrated into a discrete Benford framework to predict leading digit frequencies accurately?
3. **Prime Gap Adjustments:** Does incorporating average prime gap scaling for specific leading digit intervals yield a mathematically robust model that achieves a lower KL divergence than pure logarithmic density corrections?

## Methodology
1. **Mathematical Formulation:** 
   - Derive a Logarithmic Density Adjusted Benford (LDAB) model. Instead of standard $\log_{210}(1 + 1/d)$, calculate the expected probability mass by integrating the prime density function $1/\ln(x)$ over the specific numerical ranges dictated by each leading digit $d \in [1, 209]$ in Base-210 across multiple magnitudes.
2. **Data Generation:** 
   - Computationally generate a robust dataset of prime numbers up to a sufficiently large magnitude (e.g., $10^8$ or $10^9$).
   - Convert these primes into Base-210 and extract the empirical frequency distribution of the leading digits.
3. **Statistical Evaluation:** 
   - Calculate the Kullback-Leibler (KL) divergence and perform Chi-square goodness-of-fit tests between the empirical Base-210 data and the predictions of the new LDAB model.
   - Benchmark these results against the previously established baseline of standard Benford's Law (KL ~0.64).

## Success Criteria
1. **Model Derivation:** Successful mathematical formalization of the LDAB model without reliance on the previously falsified coprime filtering mechanics.
2. **Error Reduction:** The newly proposed logarithmic/gap-adjusted model must achieve a KL divergence significantly lower than the 0.639560 baseline established by standard Benford's Law in Base-210.
3. **Explanatory Power:** The research must conclusively identify whether logarithmic thinning is the primary driver of the leading digit bias deviation in large primorial bases.

## Constraints
1. **Domain Restriction:** The investigation must strictly remain focused on leading digit distributions of primes within specific bases (specifically Base-210 for this phase to allow direct comparison with previous iterations). Do not investigate trailing digits or unrelated sequence patterns.
2. **Computational Limits:** The integration over numerical intervals for the LDAB model must be computationally tractable and scalable to the maximum prime bounds used in the empirical dataset.