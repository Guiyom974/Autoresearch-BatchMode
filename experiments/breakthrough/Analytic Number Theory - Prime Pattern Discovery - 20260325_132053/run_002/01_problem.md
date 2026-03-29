# Research Problem: Higher-Order Primorial Residue Biases in Primes

## Objective
Computationally investigate higher-order modular clustering of prime numbers by analyzing distributions modulo large primorials (e.g., 210, 2310). The goal is to detect subtle, persistent deviations from expected equidistribution across coprime residue classes (extensions of Chebyshev's bias) in expanded search spaces up to $10^8$.

## Research Questions
1. **Primorial Equidistribution Deviations**: How do prime frequencies deviate from uniform equidistribution across the $\phi(P_k)$ coprime residue classes modulo the $k$-th primorials ($P_4=210$, $P_5=2310$, $P_6=30030$)?
2. **Persistent Bias Detection**: Are there statistically significant, persistent biases favoring specific higher-order residue classes as the search space expands, and do these biases fluctuate or stabilize as $N \to 10^8$?
3. **Prime Race Dynamics**: How do the cumulative counts of primes in competing residue classes ("prime races") behave for these larger moduli compared to classic small-moduli races (like mod 3 or mod 4)?

## Methodology
1. **Data Generation**: Utilize an efficient Sieve of Eratosthenes to generate and store all prime numbers up to $10^8$.
2. **Residue Mapping**: For each prime, compute its residue class modulo $P_4$ (210) and $P_5$ (2310). Filter out primes that divide the modulus.
3. **Statistical Analysis**: Apply goodness-of-fit tests (e.g., Chi-square, Kolmogorov-Smirnov) to compare the observed frequencies of primes in each coprime residue class against the expected uniform distribution ($1/\phi(P_k)$).
4. **Cumulative Tracking**: Plot the normalized differences in prime counts between the most and least populated residue classes as a function of $N$ (up to $10^8$) to visualize the "prime race" and identify structural asymmetries.

## Success Criteria
1. **Significant Deviation**: Identification of at least one coprime residue class modulo 210 or 2310 that exhibits a persistent, statistically significant deviation ($p < 0.01$) from the expected uniform distribution across the evaluated range.
2. **Reproducible Metrics**: Generation of a clear statistical summary detailing the variance, mean bias, and crossing frequencies (how often the "lead" changes in the prime race) for the analyzed moduli.
3. **Actionable Visualizations**: Production of cumulative bias plots that clearly demonstrate the divergence or convergence of prime counts in specific higher-order residue classes.

## Constraints
1. **Computational Limits**: The search space is capped at $N = 10^8$ to ensure memory and processing time remain manageable while providing a sufficiently large dataset for statistical power.
2. **Moduli Restriction**: The analysis must strictly focus on primorial moduli (product of the first $k$ primes) to analyze fundamental structural properties, avoiding arbitrary or highly composite numbers that lack the same theoretical grounding.
3. **Domain Focus**: The research must remain strictly analytical and mathematical; cryptographic applications or factoring algorithms are out of scope.