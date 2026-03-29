# Research Problem: Empirical Validation and Statistical Testing of the Primorial-Adjusted Benford Model in Base-210

## Objective
To rigorously validate the newly derived primorial-adjusted Benford null model by conducting statistical hypothesis testing against the empirical leading digit distributions of primes up to $10^8$ in Base-210. While the theoretical derivation successfully normalizes probabilities across the 48 coprime digits (with $d=1$ expected at 0.4675), this phase aims to quantify the exact goodness-of-fit. The ultimate goal is to determine whether this adjusted model fully resolves the previously observed massive deviation (KL divergence = 0.636) or if statistically significant residual anomalies persist.

## Research Questions
1. **Goodness-of-Fit:** How much does the primorial-adjusted Benford model reduce the Kullback-Leibler (KL) divergence and Chi-squared statistics compared to the naive Benford model when applied to primes up to $10^8$ in Base-210?
2. **Residual Anomalies:** After adjusting for the coprime restriction, do specific leading digits among the 48 valid candidates in Base-210 still exhibit statistically significant over- or under-representation? 
3. **Asymptotic Convergence:** Does the empirical leading digit distribution converge closer to the primorial-adjusted model as the prime search bound increases from $10^6$ to $10^8$?

## Methodology
1. **Data Generation:** Computationally generate all prime numbers up to $10^8$ using an optimized sieve.
2. **Base Conversion:** Convert the generated primes into Base-210 ($p_4\#$) representation and extract the leading digits.
3. **Empirical Distribution:** Tabulate the absolute and relative frequencies of the leading digits, ensuring that all observed digits fall within the set of 48 coprimes.
4. **Statistical Testing:** 
   - Compute the exact KL divergence between the empirical distribution and the theoretical primorial-adjusted Benford distribution.
   - Perform a Chi-squared goodness-of-fit test to assess statistical significance.
   - Calculate the residual differences (Empirical - Expected) for each of the 48 digits to identify localized biases.

## Success Criteria
- A fully computed statistical comparison clearly demonstrating the difference in fit (via KL divergence and p-values) between the naive Benford model and the primorial-adjusted model.
- A comprehensive residual analysis table for all 48 coprime digits in Base-210, identifying any digits that deviate beyond a 95% confidence interval from the new null model.
- Determination of whether the primorial-adjusted model is sufficient to explain the distribution, or if further adjustments (e.g., Chebyshev-type prime biases) are required.

## Constraints
- **Computational Scope:** Prime generation and base conversion should be strictly bounded to $10^8$ to ensure rapid iteration while providing a statistically robust sample size for the 48 degrees of freedom.
- **Domain Focus:** The analysis must remain strictly focused on leading digit distributions in primorial bases, specifically Base-210, avoiding tangential explorations into other bases or non-prime sequences.