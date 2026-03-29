# Research Problem: Bounded Empirical Detection of the First Modulo 210 Crossover

## Objective
Following the computational failure of the previous open-ended search, we must drastically tighten our scope to ensure successful execution while preserving the scientific core of the inquiry. The revised objective is to empirically locate the exact first sign change (crossover point) in the prime race between the quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) modulo 210, strictly bounding the search space to $x \le 10^7$. This avoids the overhead of asymptotic density calculations and focuses purely on exact prime counting within a feasible computational window.

## Research Questions
1. At what exact integer $x \le 10^7$ does the prime count $\pi(x; 210, 1)$ exceed $\pi(x; 210, 11)$ for the first time?
2. What is the maximum lead achieved by the theoretically favored class ($a=11$) prior to this first crossover point?
3. If no crossover exists below $10^7$, what is the asymptotic trajectory of the difference $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ within this interval?

## Methodology
1. **Prime Generation:** Utilize an optimized Sieve of Eratosthenes to generate all prime numbers strictly up to $x = 10^7$. 
2. **Residue Classification:** Filter the generated primes into two specific buckets: those congruent to $1 \pmod{210}$ and those congruent to $11 \pmod{210}$.
3. **Step-by-Step Tallying:** Iterate through the primes in ascending order, maintaining a running tally of $\pi(x; 210, 1)$ and $\pi(x; 210, 11)$.
4. **Crossover Detection:** At each prime step, compute the difference. Record the first instance where the tally for $a=1$ strictly exceeds the tally for $a=11$.

## Success Criteria
- The successful execution of the prime sieve up to $10^7$.
- The exact integer value $x$ of the first crossover point is identified and documented.
- If no crossover occurs before $10^7$, a plot or summary statistics of the difference $\Delta(x)$ up to the bound is provided.

## Constraints
- **Search Bound:** The algorithm must halt at $x = 10^7$ to ensure computational tractability.
- **Simplification:** No logarithmic density, weighted integrations, or Rubinstein-Sarnak analytical formulas will be computed in this iteration. Focus solely on the empirical step-function $\pi(x)$.
- **Scope limitation:** Only the residue classes $a=1$ and $a=11$ modulo 210 are to be tracked. All other 46 coprime classes are to be ignored for this run.