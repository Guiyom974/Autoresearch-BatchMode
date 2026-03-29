# Research Problem: Two-Way Prime Race Modulo 210 — $\pi(x; 210, QNR)$ vs $\pi(x; 210, 1)$

## Objective
To bypass previous computational bottlenecks (which resulted in no output) by drastically tightening the scope of the investigation. Instead of calculating the prime counting function $\pi(x; 210, a)$ for all 48 coprime residue classes, this iteration will focus entirely on a single, targeted two-way "prime race." We will evaluate the Rubinstein-Sarnak Chebyshev bias by strictly comparing the principal quadratic residue class ($a=1$) against a single, verified quadratic non-residue (QNR) class (e.g., $a=11$) modulo the primorial $q=210$, up to a highly restricted and computationally safe bound.

## Research Questions
1. In a direct head-to-head comparison modulo 210, what percentage of the time does the quadratic non-residue class lead the quadratic residue class $a=1$ up to $x = 10^6$?
2. At what specific values of $x$ (if any within the bound) does the principal quadratic residue class ($a=1$) temporarily overcome the Chebyshev bias and take the lead?
3. What is the maximum magnitude of the difference $\Delta(x) = \pi(x; 210, QNR) - \pi(x; 210, 1)$ within this restricted search space?

## Methodology
1. **Parameter Selection:** Set the modulus to the primorial $q = 210$. 
2. **Class Isolation:** Select exactly two coprime residue classes for tracking: the principal quadratic residue $a_1 = 1$, and a known quadratic non-residue, such as $a_2 = 11$ (since $\gcd(11, 210) = 1$ and it is not a square modulo 210).
3. **Optimized Sieve:** Implement a standard Prime Sieve strictly capped at a low upper bound of $N = 1,000,000$ to guarantee execution completion.
4. **Delta Tracking:** Iterate through the generated primes, tallying counts for the two chosen classes only. Maintain a running difference $\Delta(x)$.
5. **Statistical Aggregation:** Calculate the exact proportion of integers $x \le 10^6$ for which $\Delta(x) > 0$.

## Success Criteria
1. The experiment successfully runs to completion and produces quantifiable output without timing out or exceeding memory limits.
2. A definitive percentage is calculated representing how often the chosen QNR class leads the QR class $a=1$ up to $10^6$.
3. Identification of the first few "axis crossings" (values of $x$ where the lead changes hands), if they exist within the bound.

## Constraints
1. **Strict Computational Limits:** The search bound must be hard-capped at $x = 10^6$. Do not attempt to scale higher until this baseline completes.
2. **Narrowed State Space:** Do not track or instantiate arrays for all 48 coprime classes. Memory and processing must be restricted to tracking only the two selected residue classes.
3. **Domain Strictness:** The investigation must remain exclusively focused on Chebyshev's bias modulo 210.