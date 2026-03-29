# Research Problem: Chebyshev Bias at Modulo 210 — Focused Quadratic Residue Analysis

## Objective
To rigorously quantify the Rubinstein-Sarnak Chebyshev bias strictly modulo the primorial $q=210$. Following the correction of the coprime filtering artifact, this iteration narrows the computational scope to guarantee successful execution. We will systematically compare the prime counting function $\pi(x; 210, a)$ for quadratic residues versus quadratic non-residues among the $\phi(210)=48$ valid coprime classes, up to a computationally safe bound.

## Research Questions
1. Among the 48 coprime residue classes modulo 210, which specific classes dominate the prime race up to $x = 10^7$?
2. When aggregating the prime counts, do quadratic non-residues modulo 210 collectively win the prime race against quadratic residues at a frequency consistent with the Rubinstein-Sarnak logarithmic density predictions?
3. What is the variance in the prime counts among the different quadratic non-residue classes themselves?

## Methodology
1. **Prime Generation & Filtering:** Generate all prime numbers up to a strict, computationally feasible limit of $x = 10^7$. 
2. **Coprime Verification:** Strictly filter the candidate residue classes $a$ such that $\gcd(a, 210) = 1$, yielding exactly 48 valid classes.
3. **Quadratic Classification:** Mathematically classify each of the 48 classes as either a quadratic residue or a quadratic non-residue modulo 210.
4. **Race Simulation:** Compute the running tally of primes in each class. Track the "leader" at each step and calculate the empirical density of the lead held by quadratic non-residues over residues.

## Success Criteria
1. Successful, uninterrupted execution of the prime race simulation up to $x = 10^7$ without computational timeouts.
2. An output matrix or summary detailing the leading percentages for all 48 coprime classes.
3. A clear, quantitative comparison showing the aggregate win rate of quadratic non-residues versus quadratic residues modulo 210.

## Constraints
1. **Domain Constraint:** Do not expand the scope to $q=2310$ or higher primorials in this iteration to ensure the script completes successfully and yields data.
2. **Algorithmic Constraint:** The algorithm must explicitly assert $\gcd(a, 210) = 1$ before counting any prime towards a residue class.
3. **Performance Constraint:** Memory and time limits must be respected; use efficient sieving and cumulative sum arrays rather than recalculating counts at each step.