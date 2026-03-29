# Research Problem: High-Resolution Analysis of 1st- and 2nd-Order Markovian Digit Transitions in Base-10 Primes ($10^6$ to $10^8$)

## Objective
To precisely quantify 1st- and 2nd-order Markovian transition probabilities within the internal digit sequences of Base-10 prime numbers in the range of $10^6$ to $10^8$. Moving past initial framework validation, this iteration focuses on deploying a robust, error-free computational pipeline to identify statistically significant localized biases or sequential dependencies. The primary goal is to determine if internal prime digits exhibit "memory" of preceding digits that deviates from a purely random uniform distribution, completely isolating these effects from known trivial rules.

## Research Questions
1. Do the internal 1st-order digit transition probabilities (e.g., $P(d_{i+1} | d_i)$) of primes in the $10^6$ to $10^8$ range differ with statistical significance from uniformly expected values?
2. Are there specific 2nd-order Markovian chains (e.g., $P(d_{i+2} | d_{i+1}, d_i)$) that exhibit anomalous suppression or enhancement in prime numbers compared to a control dataset of odd composite numbers of the same magnitude?
3. How does the transition probability matrix evolve as the magnitude of the primes increases across the specified range?

## Methodology
1. **Data Generation:** Utilize an optimized Sieve of Eratosthenes to generate a complete set of prime numbers strictly between $10^6$ and $10^8$. Generate a parallel control set of odd composite numbers in the same range.
2. **Digit Extraction & Truncation:** Convert the numbers to Base-10 strings. Strip the first digit (to avoid Benford's Law biases) and the final digit (to avoid trivial primality constraints like the absence of 2, 4, 5, 6, 8, 0) from all numbers.
3. **Markovian Matrix Construction:** Parse the remaining internal digit sequences to populate $10 \times 10$ matrices for 1st-order transitions and $100 \times 10$ matrices for 2nd-order transitions.
4. **Statistical Testing:** Perform Chi-square goodness-of-fit tests to compare the empirical prime transition matrices against the control matrices and a theoretical uniform distribution.

## Success Criteria
1. Uninterrupted, error-free computational extraction of the Markovian transition matrices for the specified range.
2. Generation of statistically rigorous p-values comparing the internal digit transitions of primes against the uniform and composite-number null hypotheses.
3. Identification of at least three specific digit transitions (if any exist) that show the highest divergence from expected random behavior.

## Constraints
1. The analysis must strictly ignore the trailing digit of all primes to prevent contamination from known Base-10 divisibility rules.
2. The analysis must strictly ignore the leading digit to prevent contamination from Benford's Law.
3. The computational pipeline must be structurally sound and strictly focused on data extraction without syntax interruptions.