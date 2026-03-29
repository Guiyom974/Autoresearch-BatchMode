# Research Problem: Higher-Order (k-step) Markovian Dependencies and Sub-sequence Clustering in Internal Digits of Base-10 Primes

## Objective
To systematically compute and statistically validate higher-order ($k=2$ and $k=3$) Markovian transition probabilities of internal digit sequences in Base-10 prime numbers. Since previous attempts to construct 1st-order matrices were interrupted before yielding data, this iteration narrows the scientific focus to computationally robust, higher-order dependencies. The goal is to rigorously isolate internal digit sequences (triplets and pairs) from known terminal-digit biases and determine if long-range digit dependencies exist that would be obscured by simple adjacent-digit analysis.

## Research Questions
1. **Higher-Order Transitions:** Do sequences of three consecutive internal digits (e.g., the transition from "34" to "5") in Base-10 prime numbers exhibit statistically significant deviations from a uniform distribution expected in random odd numbers?
2. **Sub-sequence Clustering:** Are there specific internal digit pairs or triplets that appear with unexpectedly high or low frequencies in primes up to $10^8$, independent of the leading or terminal digits?
3. **Composite Baseline Comparison:** How do the $k$-step transition matrices of prime numbers differ from those of composite numbers of the same magnitude?

## Methodology
1. **Data Generation:** Computationally generate all prime numbers and a control set of randomly selected composite odd numbers up to $10^8$.
2. **Data Sanitization:** Strip the first digit and the last digit from all numbers in the dataset to strictly isolate the "internal core" digits, completely eliminating Benford's Law effects and terminal-digit biases (e.g., absence of 2, 4, 5, 6, 8, 0).
3. **Matrix Construction:** Construct 2nd-order ($100 \times 10$) and 3rd-order ($1000 \times 10$) transition probability matrices for the internal digits.
4. **Statistical Testing:** Apply Pearson's Chi-Square tests and Kullback-Leibler (KL) divergence to compare the empirical prime digit distributions against both the uniform theoretical distribution and the composite number control group.

## Success Criteria
- Successful construction of error-free 2nd and 3rd-order transition matrices for internal digits.
- Identification of at least one specific digit transition sequence where the prime distribution diverges from the composite/random distribution with a statistical significance of $p < 0.01$.
- Generation of a clear KL-divergence metric quantifying the exact information difference between prime internal digits and uniform randomness.

## Constraints
- **Domain Strictness:** The analysis must remain entirely focused on the digits of prime numbers. Do not expand into other number theory sequences (e.g., Fibonacci).
- **Exclusion of Trivia:** Leading digits and the final digit must be explicitly excluded from all transition calculations to prevent known biases from skewing the transition matrices.
- **Computational Tractability:** The algorithm must be optimized to handle matrices up to $10^8$ without memory overflow, ensuring clean execution.