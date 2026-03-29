# Research Problem: Baseline Empirical Validation of Logarithmic Density in Modulo 210 Prime Races

## Objective
To establish a verified, mathematically robust baseline for calculating the logarithmic density of the prime race modulo 210. Following previous execution failures, we must strip away premature algorithmic optimizations and perform a highly controlled "dry-run" of the theoretical framework. We will compute the logarithmic measure for the race between a quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) up to a strict micro-bound of $x = 10^6$. This ensures the core mathematical logic and discrete-sum approximations are fundamentally sound before scaling to higher bounds or $2310$.

## Research Questions
1. What is the empirical logarithmic density of the set of $x \leq 10^6$ for which $\pi(x; 210, 11) > \pi(x; 210, 1)$?
2. How closely does a simplified, unoptimized discrete-sum approximation of the logarithmic measure align with the qualitative predictions of the Rubinstein-Sarnak framework at this micro-bound?
3. At what threshold $x \leq 10^6$ does the Chebyshev bias first strongly manifest in the logarithmic density calculation?

## Methodology
1. **Prime Generation:** Implement a standard, unoptimized Sieve of Eratosthenes up to $x = 10^6$.
2. **Residue Tracking:** Tally primes strictly in the coprime residue classes $a=11 \pmod{210}$ and $a=1 \pmod{210}$. 
3. **Difference Array:** Construct an array representing the difference $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ for each integer $x$ up to $10^6$.
4. **Logarithmic Measure:** Calculate the logarithmic density using the discrete sum $\frac{1}{\log X} \sum_{x \leq X, \Delta(x) > 0} \frac{1}{x}$, evaluated at $X = 10^6$.
5. **Validation:** Compare the resulting density against the expected $>0.50$ theoretical threshold for Chebyshev's bias.

## Success Criteria
- Successful, error-free generation of the difference array $\Delta(x)$ up to $10^6$.
- Output of a definitive empirical logarithmic density value for the $a=11$ vs $a=1$ race.
- Confirmation that the foundational mathematical logic correctly identifies and quantifies the bias without reliance on complex, error-prone algorithmic optimizations.

## Constraints
- **Bound Limit:** Computations must strictly not exceed $x = 10^6$ to ensure rapid verification of the foundational logic.
- **Class Restriction:** Only analyze the race between $a=11$ and $a=1$ modulo 210.
- **Simplicity:** Avoid advanced algorithmic optimizations, memory-mapping, or parallelization. The focus is exclusively on theoretical accuracy and establishing a functional scientific baseline.