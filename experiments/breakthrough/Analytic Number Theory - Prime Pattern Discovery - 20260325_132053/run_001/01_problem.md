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
