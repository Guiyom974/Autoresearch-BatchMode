# Research Problem: Robust Computational Extraction and Analysis of 1st- and 2nd-Order Markovian Dependencies in Internal Digits of Base-10 Primes

## Objective
To systematically compute and statistically validate 1st-order and 2nd-order Markovian transition probabilities of internal digit sequences in Base-10 prime numbers. Since previous computational iterations failed to execute properly, this phase focuses on ensuring a scientifically rigorous, computationally stable extraction of transition matrices. The goal is to isolate internal digit sequences (pairs and triplets) from known boundary constraints (e.g., the last digit of primes) and determine if their sequential dependencies deviate from a uniform random distribution.

## Research Questions
1. **1st-Order Internal Dependencies:** What is the empirical 1st-order transition probability matrix for internal digits of Base-10 primes up to $10^8$, and does it show statistically significant deviations from a uniform distribution (excluding the final digit)?
2. **2nd-Order Internal Dependencies:** Do sequences of three internal digits (2nd-order transitions) exhibit localized clustering or avoidance patterns that cannot be explained by 1st-order probabilities?
3. **Scale Invariance:** Do the observed transition probabilities remain stable as the magnitude of the prime numbers increases across different logarithmic buckets (e.g., $10^6$ vs $10^8$)?

## Methodology
1. **Data Generation:** Generate a comprehensive dataset of all prime numbers up to a specified threshold (e.g., $10^8$) using an optimized Sieve of Eratosthenes.
2. **Data Sanitization:** Strip the first and last digits from each prime in the dataset to strictly isolate internal digits, removing trivial boundary biases (such as the inability of primes to end in 2, 4, 5, 6, 8, or 0).
3. **Matrix Computation:** Construct precise 1st-order ($10 \times 10$) and 2nd-order ($100 \times 10$) transition probability matrices based on the sanitized internal digit sequences.
4. **Statistical Testing:** Apply Chi-square goodness-of-fit tests to compare the empirical transition matrices against an expected uniform distribution matrix.
5. **Validation:** Implement robust error-handling and logging in the computational pipeline to ensure uninterrupted execution and reliable data extraction.

## Success Criteria
1. **Computational Stability:** Successful, uninterrupted execution of the digit-extraction and matrix-computation algorithms over the target prime dataset.
2. **Matrix Generation:** The successful generation of complete, empirical 1st-order and 2nd-order transition probability matrices for internal prime digits.
3. **Statistical Clarity:** A definitive statistical conclusion (via p-values) indicating whether internal digit transitions in Base-10 primes exhibit non-uniform Markovian dependencies.

## Constraints
1. **Domain Adherence:** The research must strictly remain within the analysis of digit distributions and sequence structures of prime numbers.
2. **Boundary Exclusion:** The analysis must strictly exclude the final digit of the prime numbers to prevent known trivial biases from skewing the transition matrices.
3. **Computational Efficiency:** The algorithms must be highly optimized to handle millions of primes without memory overflow or execution timeouts.