# Research Problem: Algorithmic Validation and Robust Execution for Extracting Markovian Dependencies in Base-10 Prime Digits

## Objective
To successfully and rigorously compute the 1st- and 2nd-order Markovian transition probabilities for internal digit sequences of Base-10 prime numbers by developing a computationally robust and fault-tolerant algorithmic pipeline. Following previous execution failures, this iteration focuses on implementing rigorous validation, error handling, and logical logging to ensure the uninterrupted and accurate statistical extraction of digit dependencies, strictly isolating internal sequences from boundary constraints.

## Research Questions
1. **Algorithmic Robustness:** How can we structure the prime generation and digit-parsing algorithms with comprehensive error handling and logging to guarantee successful execution over large sets of primes (e.g., up to $10^7$)?
2. **Transition Probabilities:** Once a stable pipeline is established, what are the exact 1st-order (pair) and 2nd-order (triplet) Markovian transition probabilities for internal digits of Base-10 primes?
3. **Statistical Deviation:** Do the successfully extracted internal transition matrices exhibit statistically significant deviations from a uniform distribution when analyzed using chi-square tests?

## Methodology
1. **Pipeline Validation:** Develop a Python-based computational script with strict syntax validation and structural integrity checks to prevent pre-execution failures.
2. **Robust Execution Architecture:** Implement comprehensive `try-except` blocks, execution logging, and modular architecture to gracefully handle edge cases during prime generation and string manipulation.
3. **Prime Generation and Parsing:** Generate primes up to $10^7$ using a highly optimized Sieve of Eratosthenes. Convert primes to strings and strip the first and last digits to isolate internal sequences.
4. **Markovian Extraction:** Calculate the empirical frequencies of internal digit transitions ($d_i \to d_{i+1}$ and $d_i, d_{i+1} \to d_{i+2}$) and compile them into normalized transition probability matrices.
5. **Statistical Testing:** Apply Pearson's chi-square test to compare the observed transition matrices against the expected uniform distribution matrices.

## Success Criteria
1. **Execution Success:** The computational script runs to completion without syntax, runtime, or logical errors, successfully generating detailed execution logs.
2. **Data Extraction:** Complete 1st-order ($10 \times 10$) and 2nd-order ($100 \times 10$) Markovian transition matrices are successfully outputted for the internal digits of the target prime set.
3. **Statistical Output:** The experiment outputs valid p-values and chi-square statistics quantifying the deviation of internal prime digit transitions from true randomness.

## Constraints
1. **Domain Strictness:** The analysis must remain strictly focused on the digit sequences of prime numbers, avoiding any deviation into unrelated number theory or cryptography.
2. **Internal Digits Only:** The algorithm must explicitly exclude the first digit (which cannot be zero) and the last digit (which is restricted to 1, 3, 7, 9 in Base-10) to prevent trivial biases.
3. **Computational Efficiency:** The robust error-handling mechanisms must not introduce unacceptable computational overhead, allowing the analysis of primes up to $10^7$ within standard execution time limits.