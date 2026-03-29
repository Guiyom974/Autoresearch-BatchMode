# Research Problem: Highly Optimized Bounded Detection of Modulo 210 Prime Race Crossovers

## Objective
Following the computational limits encountered in previous open-ended and moderately bounded searches, this iteration drastically tightens the scope to ensure successful execution. The objective is to empirically evaluate the prime race between the quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) modulo 210, strictly bounding the search space to $x \le 10^6$ using a highly optimized, memory-efficient prime counting method. 

## Research Questions
1. Does the first crossover point (where $\pi(x; 210, 1) > \pi(x; 210, 11)$) occur within the strictly bounded range $x \le 10^6$?
2. What is the maximum lead achieved by the quadratic non-residue class ($a=11$) over the residue class ($a=1$) within this interval?
3. How does the magnitude of the bias $\pi(x; 210, 11) - \pi(x; 210, 1)$ behave as $x$ approaches $10^6$?

## Methodology
1. **Targeted Sieve**: Implement a highly optimized Sieve of Eratosthenes strictly capped at $N = 10^6$.
2. **Selective Counting**: Instead of tracking all 48 coprime residue classes, only track the prime counts for $a=1$ and $a=11$ modulo 210.
3. **Difference Tracking**: Compute the running difference $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ at each prime $p \le 10^6$.
4. **Crossover Logging**: Record the exact prime values $x$ where $\Delta(x)$ changes sign.

## Success Criteria
1. Successful execution of the counting algorithm up to $x = 10^6$ without memory or timeout errors.
2. A definitive boolean answer on whether a crossover exists below $10^6$.
3. A logged maximum lead value for the non-residue class over the residue class.

## Constraints
1. **Search Bound**: The search limit must be strictly hardcoded to $x = 10^6$. No dynamic expansion of the search space is allowed.
2. **Memory Efficiency**: The algorithm must discard primes once they are tallied to prevent memory overflow, storing only the running totals and crossover indices.
3. **Residue Restriction**: Computation must be strictly limited to the classes $a=1$ and $a=11$ modulo 210.