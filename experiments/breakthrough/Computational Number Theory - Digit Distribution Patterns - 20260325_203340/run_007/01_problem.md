# Research Problem: Empirical Extraction and Statistical Analysis of 1st- and 2nd-Order Markovian Digit Transitions in Base-10 Primes

## Objective
To successfully compute and statistically analyze the 1st- and 2nd-order Markovian transition probabilities for internal digit sequences of Base-10 prime numbers. Building upon the foundational hypothesis of sequential digit dependencies, this iteration focuses on executing the mathematical extraction over a specific, large range of primes (e.g., $10^6$ to $10^8$) to rigorously test for statistically significant deviations from a uniform random distribution, avoiding edge-case biases.

## Research Questions
1. What are the exact 1st-order ($10 \times 10$) and 2nd-order ($100 \times 10$) digit transition probability matrices for the internal digits of Base-10 primes in the range $[10^6, 10^8]$?
2. When subjected to Chi-square goodness-of-fit tests, do these empirical transition matrices exhibit statistically significant deviations from the null hypothesis (which posits that internal digit transitions are uniformly distributed)?
3. Are there specific digit pairs or triplets (e.g., "3" followed by "7") that occur with anomalous frequency compared to non-prime integers in the same range?

## Methodology
1. **Prime Generation:** Utilize an efficient sieve algorithm to generate all prime numbers within the targeted range of $10^6$ to $10^8$.
2. **Data Sanitization:** For each prime, isolate the *internal* digits by stripping the most significant digit (to avoid Benford's Law biases) and the least significant digit (to avoid the well-known exclusion of even numbers and 5).
3. **Matrix Construction:** 
   - Construct a 1st-order transition matrix tracking the frequency of digit $d_{i+1}$ given $d_i$.
   - Construct a 2nd-order transition matrix tracking the frequency of digit $d_{i+2}$ given the sequence $(d_i, d_{i+1})$.
4. **Statistical Testing:** Compare the resulting matrices against a control set of composite numbers in the same range. Calculate Chi-square statistics and p-values to determine if the prime digit transitions deviate from expected uniform randomness.

## Success Criteria
1. The successful generation and population of both 1st- and 2nd-order Markovian transition matrices for the specified prime range.
2. The calculation of clear statistical metrics (Chi-square values, p-values) that quantify the deviation of prime internal digit sequences from uniform randomness.
3. Identification of at least three specific digit transitions (if any exist) that show the highest divergence from expected probabilities.

## Constraints
1. The analysis must strictly focus on Base-10 representations.
2. The first and last digits of every prime must be strictly excluded from the transition counts to prevent known trivial biases from skewing the Markovian analysis.
3. The computational approach must focus entirely on the mathematical and statistical extraction, assuming a clean, syntactically valid execution environment.