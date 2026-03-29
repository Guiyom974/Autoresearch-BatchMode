# Research Problem: Markovian Digit Transition Probabilities and Sequential Biases in Base-10 and Base-16 Primes

## Objective
To computationally establish and rigorously quantify Markovian digit transition probabilities within prime numbers across Base-10 and Base-16 representations. The goal is to determine if the internal sequential structure of primes exhibits localized structural biases (e.g., the probability of a digit $d_i$ being followed by $d_{i+1}$) that statistically deviate from the expected uniform distribution, excluding known terminal digit constraints.

## Research Questions
1. **Digit Transition Matrices:** Does the $N \times N$ empirical transition probability matrix for adjacent digits in primes significantly deviate from the expected probabilities of a random sequence of odd integers?
2. **Base-Specific Artifacts:** Are sequential biases invariant across bases, or do specific dependencies emerge in Base-16 that are absent in Base-10?
3. **Scale Dependence:** Do these transition probability distributions change as the magnitude of the prime numbers increases (e.g., primes $< 10^6$ vs. primes between $10^8$ and $10^9$)?

## Methodology
1. **Prime Generation:** Implement a highly optimized segmented sieve to generate prime numbers up to $10^8$. 
2. **Base Conversion & Sequence Extraction:** Extract the internal digit sequences of the generated primes in both Base-10 and Base-16, strictly stripping the final digit to prevent known terminal biases (e.g., 2, 4, 5, 6, 8, 0 in Base-10).
3. **Transition Counting:** Construct empirical Markov transition matrices by counting occurrences of adjacent digit pairs $(d_i, d_{i+1})$.
4. **Statistical Testing:** Perform Chi-square goodness-of-fit tests and calculate Kullback-Leibler (KL) divergence comparing the empirical prime transition matrices against matrices generated from randomized non-prime odd numbers of the same magnitude.

## Success Criteria
1. Successful generation of complete transition matrices for internal digits of primes in Base-10 and Base-16 up to $10^8$.
2. Statistical validation (p-value $< 0.01$) indicating whether the transition probabilities of prime digits deviate from the baseline uniform distribution.
3. Generation of heatmaps visualizing the transition matrices and highlighting specific transition anomalies.

## Constraints
1. The analysis must exclude the least significant digit (LSD) of each prime to avoid trivial terminal biases.
2. The computational pipeline must execute efficiently, strictly adhering to memory limits and completing within standard execution time bounds.
3. The research must remain strictly focused on statistical and structural distributions, avoiding numerology or ungrounded pattern matching.