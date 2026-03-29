# Research Problem: Robust Statistical Extraction of 1st- and 2nd-Order Markovian Digit Transitions in Internal Base-10 Primes ($10^6$ to $10^8$)

## Objective
To successfully compute and rigorously quantify the 1st- and 2nd-order Markovian transition probabilities of internal digits within Base-10 primes in the range of $10^6$ to $10^8$. Following previous execution limitations, this iteration emphasizes a robust, error-free analytical pipeline to establish the definitive transition matrices. The primary goal is to determine if the internal digits of primes exhibit any localized "memory" or sequential dependencies that deviate from expected uniform randomness, isolating these effects from trivial boundary biases.

## Research Questions
1. **Empirical Transition Matrices:** What are the exact empirical 1st-order ($10 \times 10$) and 2nd-order ($100 \times 10$) transition probability matrices for internal digits (strictly excluding the first and last digits) of Base-10 primes between $10^6$ and $10^8$?
2. **Statistical Deviation:** Do these internal transition probabilities deviate significantly from a uniformly random distribution, and how do they compare against the transition matrices of composite numbers within the exact same numerical range?
3. **Localized Biases:** Are there specific digit pairs (e.g., "3 followed by 3") or triplets that occur with a statistically significant higher or lower frequency than predicted by standard uniform probability models?

## Methodology
1. **Data Generation:** Utilize an optimized Sieve of Eratosthenes to generate all prime numbers strictly within the $10^6$ to $10^8$ range.
2. **Data Sanitization:** Convert primes to strings and explicitly strip the most significant (first) and least significant (last) digits to eliminate well-known Base-10 boundary artifacts (e.g., primes cannot end in 0, 2, 4, 5, 6, 8).
3. **Markovian Analysis:** 
   - Tally 1st-order transitions ($P(D_i | D_{i-1})$) and 2nd-order transitions ($P(D_i | D_{i-1}, D_{i-2})$) across the sanitized internal digit sequences.
   - Compute the corresponding probability matrices.
4. **Statistical Testing:** Apply Chi-square tests of independence and calculate the Kullback-Leibler (KL) divergence to measure the distance between the observed prime digit transition distributions and a purely uniform null hypothesis.

## Success Criteria
1. Successful compilation of complete, mathematically sound 1st- and 2nd-order transition probability matrices for the specified range.
2. Generation of statistically rigorous p-values (via Chi-square analysis) determining whether internal prime digits exhibit non-random Markovian memory.
3. Clear visualization (e.g., heatmaps) of the transition matrices to highlight any identified localized biases.

## Constraints
1. The analysis must be strictly confined to Base-10 integers between $10^6$ and $10^8$.
2. The algorithm must strictly exclude the terminal digit of every prime to prevent the trivial $\{1, 3, 7, 9\}$ ending rule from skewing the transition probabilities. 
3. The computational pipeline must be scientifically verified for mathematical correctness prior to statistical extraction, ensuring no invalid data artifacts influence the matrices.