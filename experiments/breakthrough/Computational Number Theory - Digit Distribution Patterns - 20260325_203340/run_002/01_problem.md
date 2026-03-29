# Research Problem: Markovian Digit Transition Probabilities in Base-2 and Base-10 Primes

## Objective
Establish a robust computational baseline to investigate Markovian transition probabilities of adjacent digits in prime numbers, focusing specifically on Base-10 and Base-2 representations. The goal is to rigorously quantify whether the sequence of digits within a prime number exhibits localized, non-trivial dependencies (e.g., predicting the next digit based on the current digit) that deviate from a purely random uniform distribution, ensuring a highly verified and systematic computational pipeline.

## Research Questions
1. **Base-10 Transition Biases:** Excluding the least significant digit (to avoid trivial divisibility rules), do the digit transition matrices $P(d_{i+1} | d_i)$ for primes exhibit statistically significant deviations from expected uniform distributions compared to composite numbers of the same magnitude?
2. **Base-2 Bit-Flipping Patterns:** In the binary representation of primes, are there unexpected localized biases in bit-sequence transitions (e.g., the probability of encountering "10" vs "11" after a "1"), and how do these scale as the magnitude of the prime increases?

## Methodology
1. **Data Generation:** Computationally generate all prime numbers up to $10^7$ using a highly verified, strictly validated sieve algorithm to ensure data integrity.
2. **Base Conversion & Truncation:** Convert the primes into Base-10 and Base-2 string representations. Truncate the final digit/bit to eliminate well-known trivial biases (e.g., Base-10 primes not ending in 2, 4, 5, 6, 8, 0; Base-2 primes always ending in 1).
3. **Transition Matrix Construction:** For each base, construct a Markov transition matrix mapping the frequency of digit $d_{i+1}$ immediately following digit $d_i$.
4. **Statistical Analysis:** Apply Chi-square goodness-of-fit tests to compare the empirical transition matrices of primes against randomly generated sequences and composite numbers.

## Success Criteria
1. Successful extraction and population of $10 \times 10$ (Base-10) and $2 \times 2$ (Base-2) empirical transition matrices without computational or parsing errors.
2. Identification of statistically significant deviations (p-value < 0.01) in specific digit transitions, or a rigorous mathematical confirmation of uniform randomness.
3. Clear visualizations (e.g., heatmaps) of the transition probability matrices.

## Constraints
1. The analysis must strictly exclude the least significant digit to prevent contamination from elementary divisibility rules.
2. The computational scope is limited to primes up to $10^7$ to ensure the analysis can be run quickly and reliably in a single execution environment.
3. The methodology must focus purely on adjacent pairwise dependencies (Markov order 1) before attempting higher-order sequential patterns.