# Research Problem: Statistical Baselines and Uniformity Testing in Base-N Prime Digit Distributions

## Objective
Establish rigorous statistical baselines for prime number digit distributions across multiple numerical bases (Base-2, Base-10, Base-16) before pursuing localized sequencing biases. The primary goal is to evaluate the applicability of Benford's Law to the leading digits of primes and to utilize Chi-squared uniformity tests to rigorously quantify known non-random patterns, such as terminal digit biases, providing a foundation for detecting truly novel deviations.

## Research Questions
1. **Benford's Law Applicability:** To what extent do the leading digits of prime numbers conform to Benford's Law as the sequence expands, and how does this conformity scale across Base-2, Base-10, and Base-16 representations?
2. **Terminal Digit Uniformity:** Excluding trivially restricted digits (e.g., evens and 5 in Base-10), do the allowed terminal digits of prime numbers exhibit a statistically significant deviation from a uniform distribution when analyzed using Chi-squared tests?
3. **Sub-Terminal Distributions:** Do the second-to-last digits of primes in various bases show any statistically significant deviations from a uniform distribution when subjected to Chi-squared testing?

## Methodology
1. **Prime Generation:** Computationally generate all prime numbers up to a robust upper bound (e.g., $N = 10^7$).
2. **Base Conversion:** Translate the generated prime sequence into Base-2, Base-10, and Base-16 string representations.
3. **Leading Digit Analysis:** Extract the first digit of each prime in each base and calculate the empirical frequency distribution. Compare these frequencies against the theoretical expectations of Benford's Law.
4. **Statistical Testing:** Extract the terminal and sub-terminal digits for each base. Filter out trivially impossible terminal digits (e.g., 0, 2, 4, 5, 6, 8 in Base-10). Apply Chi-squared goodness-of-fit tests to the remaining allowed digits to evaluate the null hypothesis of uniform distribution.

## Success Criteria
1. Successful generation of probability distribution tables for leading, sub-terminal, and terminal digits across the three specified bases.
2. Calculation of Chi-squared statistics and corresponding $p$-values for terminal and sub-terminal digit frequencies, definitively confirming or rejecting the uniform distribution hypothesis.
3. A quantitative measure of divergence (e.g., Kullback-Leibler divergence) between the observed leading digits and the theoretical Benford's Law distribution.

## Constraints
1. The analysis must explicitly filter out known trivial constraints (e.g., Base-10 primes greater than 5 can only end in 1, 3, 7, or 9) before conducting uniformity tests.
2. Computational limits should be restricted to $N = 10^7$ or a similarly manageable bound to ensure rapid iteration and statistical validity without requiring excessive memory.
3. Focus strictly on frequency analysis and baseline statistical tests; complex Markov chain or sequence-transition models are deferred until these baselines are established.