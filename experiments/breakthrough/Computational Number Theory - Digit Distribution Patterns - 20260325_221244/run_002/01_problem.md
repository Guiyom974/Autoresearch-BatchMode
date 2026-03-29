# Research Problem: Incremental Analysis of Base-10 Digit Transition Probabilities in Prime Numbers

## Objective
To computationally investigate sequential digit dependencies in prime numbers by isolating the analysis to Base-10 adjacent digit transition probabilities. Because previous generalized multi-base attempts proved too computationally broad and prone to execution failure, this iteration scopes the research down to a focused, incremental baseline study. The goal is to rigorously map the $10 \times 10$ Markov transition matrix for adjacent digits in Base-10 primes and determine if localized biases exist when compared to a control group of non-prime integers with identical terminal digit constraints.

## Research Questions
1. **Empirical Transition Matrix:** What is the exact probability matrix for adjacent digit transitions (e.g., the likelihood of a "3" being immediately followed by a "7") in Base-10 primes up to $10^8$?
2. **Statistical Deviation:** How does the transition matrix for prime numbers differ significantly from the expected uniform distribution of a control set (composite odd numbers not ending in 5)?
3. **Positional Variance:** Do transition probabilities remain stable regardless of the digits' absolute magnitude positions (e.g., leading digits vs. internal digits)?

## Methodology
1. **Incremental Generation:** Implement a highly optimized, single-purpose segmented sieve to generate primes up to a strict limit of $10^8$. 
2. **Control Group Formulation:** Generate a control dataset of random integers within the same range that share the trivial properties of primes (ending only in 1, 3, 7, or 9).
3. **Transition Counting:** Parse the integers as strings and tally all adjacent left-to-right digit pairs ($d_i, d_{i+1}$) to construct a $10 \times 10$ transition frequency matrix for both datasets.
4. **Statistical Testing:** Apply a Chi-square test of independence to compare the prime transition matrix against the control matrix, isolating any statistically significant deviations ($\alpha = 0.01$).

## Success Criteria
- Successful, error-free execution of the computational pipeline on the restricted Base-10 dataset.
- Generation of a complete $10 \times 10$ transition probability matrix for primes up to $10^8$.
- A conclusive statistical determination (p-values) regarding whether adjacent digit transitions in primes deviate from the control group.

## Constraints
- **Scope Restriction:** Do not compute Base-2, Base-16, or any other bases in this iteration. Focus entirely on Base-10 to validate the core methodology.
- **Data Limits:** Cap the maximum prime generation at $10^8$ to ensure rapid testing and prevent memory overloads or timeout errors.
- **Algorithmic Simplicity:** Avoid complex multi-step string manipulations; use efficient mathematical digit extraction where possible to maintain script stability.