# Research Problem: Ultra-Low Bounded Quantification of Initial Chebyshev Bias Modulo 210

## Objective
Following repeated computational timeouts in crossover detection, this iteration pivots from seeking race crossovers to quantifying the *initial accumulation of bias*. The objective is to empirically measure the onset and magnitude of Chebyshev's bias modulo 210 between the quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) within an ultra-tight, guaranteed-to-execute bound of $x \le 10^5$. 

## Research Questions
1. How rapidly does the prime-counting difference $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ establish a positive trend in the early integers ($x \le 10^5$)?
2. What is the maximum and mean observed deviation $\Delta(x)$ within this restricted search space?
3. Does the quadratic residue class ($a=1$) ever take the lead in this initial microscopic range, or does the non-residue class assert dominance immediately?

## Methodology
1. **Ultra-Fast Sieving:** Implement a basic, highly optimized Sieve of Eratosthenes strictly hardcoded to a maximum limit of $N = 100,000$. 
2. **Residue Filtering:** As primes are generated, immediately classify them into buckets for $p \equiv 1 \pmod{210}$ and $p \equiv 11 \pmod{210}$.
3. **Step-wise Delta Tracking:** Maintain a running tally of $\pi(x; 210, 11)$ and $\pi(x; 210, 1)$. Compute the difference $\Delta(x)$ at each prime step.
4. **Statistical Aggregation:** Instead of storing large arrays of race history, calculate running statistics in memory (current lead, max lead for $a=11$, max lead for $a=1$, and proportion of $x$ where $a=11$ leads).

## Success Criteria
1. Complete, error-free execution of the prime sieve and residue counting up to $x = 10^5$.
2. Output of summary statistics detailing the exact prime counts for both residue classes at $x = 10^5$.
3. Clear quantification of the maximum lead achieved by either class in this range.

## Constraints
1. **Strict Upper Bound:** The search space must absolutely not exceed $x = 100,000$ to guarantee execution within environment limits.
2. **Memory Efficiency:** Do not store arrays of all primes or full race histories. Use running counters to track statistical metrics.
3. **Domain Strictness:** The analysis must remain entirely focused on the $a=1$ and $a=11$ modulo 210 coprime residue classes.