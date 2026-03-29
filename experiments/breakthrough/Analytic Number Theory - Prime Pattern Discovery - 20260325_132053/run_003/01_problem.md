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