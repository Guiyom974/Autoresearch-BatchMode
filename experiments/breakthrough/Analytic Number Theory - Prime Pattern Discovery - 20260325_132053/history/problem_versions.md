
## Iteration 1 [ORIGINAL]
Timestamp: 2026-03-25T13:20:53.231991

# Research Problem: Prime Number Patterns

## Objective
Computationally investigate patterns in prime numbers that reveal non-obvious
mathematical structure, with the goal of discovering novel or underexplored insights
that could inspire further mathematical investigation.

## Research Questions
1. **Prime Gaps Analysis**: What statistical patterns exist in the differences between consecutive primes? Are there predictable distributions or clustering?

2. **Residue Class Clustering**: Do primes cluster preferentially in specific residue classes modulo small integers (like 6, 30, 210)? What does this reveal about prime structure?

3. **Spatial Patterns**: What visual patterns emerge when primes are plotted using special coordinate systems like Ulam spirals, polar coordinates, or other geometric representations?

4. **Primality Patterns**: Can computational methods detect subtle patterns in near-prime numbers or semiprimes that reveal underlying structure?

5. **Sieve Optimization**: Are there novel approaches to generating or detecting primes more efficiently than classical methods?

## Methodology
- Generate primes up to 10^6 using the Sieve of Eratosthenes for computational efficiency
- Perform statistical analysis on prime distributions (means, standard deviations, percentiles)
- Conduct hypothesis testing using empirical methods
- Create visualizations of discovered patterns (Ulam spiral, gap distributions, etc.)
- Embed plot images as base64 in results for reproducibility
- Test each hypothesis with quantitative metrics (p-values, correlation coefficients, effect sizes)

## Success Criteria
A breakthrough is achieved when a **non-trivial, computationally verified** pattern is discovered that meets ALL of these criteria:

1. **Reproducible**: The pattern holds across multiple prime ranges (e.g., primes up to 10^5, 10^6)
2. **Non-obvious**: The pattern is not commonly discussed in introductory number theory textbooks
3. **Quantifiable**: The finding can be measured with clear numerical metrics
4. **Actionable**: The discovery could inspire a direction for further mathematical research or computational investigation

## Constraints
- All computation must be done in Python
- No external data downloads (must generate/compute everything locally)
- Experiments must complete within 2 minutes of runtime
- Code must be self-contained and runnable without special dependencies
- All intermediate findings and visualizations must be saved as artifacts

## Prior Knowledge
- Primes are distributed according to the Prime Number Theorem
- Prime gaps grow roughly logarithmically
- Primes (except 2 and 3) are always of the form 6k±1
- Many well-known patterns exist: Mersenne primes, twin primes, etc.

## Constraints on Investigation
- Focus on patterns that could be novel or underexplored, not just verification of well-known results
- Avoid trivial observations (e.g., "all odd primes are odd")
- Prioritize patterns with potential deeper mathematical significance


---

## Iteration 2 [REFORMULATED]
Timestamp: 2026-03-25T13:24:37.365416

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

---

## Iteration 3 [REFORMULATED]
Timestamp: 2026-03-25T13:28:50.457577

# Research Problem: High-Scale Statistical Detection of Primorial Chebyshev Biases

## Objective
Computationally isolate and quantify systematic Chebyshev-like biases in prime distributions modulo large primorials (e.g., $P_4 = 210$, $P_5 = 2310$, $P_6 = 30030$) over massively expanded search spaces ($N = 10^{10}$). Building upon previous findings where subtle deviations were indistinguishable from noise, this iteration aims to apply rigorous statistical significance testing and high-performance segmented sieving to confirm and measure true deviations from equidistribution among coprime residue classes.

## Research Questions
1. **Bias Scaling and Significance**: How do the magnitudes of Chebyshev biases scale across varying primorial moduli when analyzed up to $10^{10}$, and are these deviations statistically significant ($p < 0.01$) when evaluated using log-likelihood ratio tests?
2. **Dirichlet Character Influence**: Can the observed systematic biases be explicitly mapped to the presence of specific Dirichlet characters modulo $P_k$, particularly distinguishing between quadratic residues and non-residues?
3. **Prime Race Dynamics at Scale**: In the extended range up to $10^{10}$, do certain "prime races" (e.g., $a$ vs. $b \pmod{P_k}$) exhibit extreme asymmetry, and what is the logarithmic density of the regions where the dominant class leads?

## Methodology
1. **High-Performance Generation**: Implement a highly optimized, memory-efficient segmented Sieve of Eratosthenes to generate and process primes up to $N = 10^{10}$ without exhausting system memory.
2. **Residue Tracking**: Continuously track cumulative prime counts for all $\phi(P_k)$ coprime residue classes modulo 210, 2310, and 30030.
3. **Statistical Analysis**: Apply rigorous statistical tests (Log-Likelihood Ratio tests, Chi-square tests adjusted for prime number theorem expectations) to the final distributions to compute p-values and confidence intervals.
4. **Race Simulation**: Track the leader of specific targeted prime races (e.g., the classes that showed maximum variance in smaller samples) at discrete intervals to calculate the logarithmic density of the leader's dominance.

## Success Criteria
1. **Computational Scale**: Successful, memory-safe generation and analysis of primes up to $10^{10}$ within a reasonable computational timeframe.
2. **Statistical Rigor**: Quantitative determination of p-values for equidistribution deviations, clearly distinguishing true mathematical bias from stochastic noise.
3. **Insight Generation**: Identification of at least one statistically significant ($p < 0.01$) bias or prime race dominance modulo a large primorial, supported by logarithmic density metrics.

## Constraints
1. **Memory Management**: The algorithm must use chunked/segmented processing; storing all primes up to $10^{10}$ in active memory is prohibited.
2. **Domain Adherence**: The analysis must remain strictly focused on the distribution of primes modulo primorials and Chebyshev's bias extensions, without drifting into unrelated number theory domains.
3. **Statistical Validity**: Claims of bias must be backed by established statistical tests rather than raw numerical differences.

---
