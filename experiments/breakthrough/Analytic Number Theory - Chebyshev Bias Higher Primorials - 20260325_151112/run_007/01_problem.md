# Research Problem: Identifying the First Crossover Point in the Modulo 210 Prime Race

## Objective
Following the execution failure of the logarithmic density computation, we must drastically tighten the scope to ensure our foundational prime counting framework is functional. The revised objective is to isolate and verify the fundamental prime race mechanics by finding the very first sign change (crossover point) in the race between the quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) modulo 210. We will defer complex logarithmic integration until the basic crossover dynamics are empirically proven.

## Research Questions
1. At what exact integer $x$ does the prime count for the quadratic residue class $\pi(x; 210, 1)$ first equal or exceed the count for the non-residue class $\pi(x; 210, 11)$?
2. What is the maximum absolute lead (the Chebyshev bias "excess") achieved by the $a=11$ class prior to this initial crossover?
3. Does this first transition point occur within a heavily restricted micro-bound of $x \le 10^5$?

## Methodology
To prevent computational timeouts and memory exhaustion:
1. **Algorithmic Simplification:** Strip out all continuous logarithmic density integration logic. Revert to a strictly discrete natural counting function $\pi(x; q, a)$.
2. **Prime Generation:** Generate primes sequentially up to a reduced micro-bound of $x = 10^5$ using a highly optimized, standard sieve.
3. **State Tracking:** Maintain running tallies for $\pi(x; 210, 11)$ and $\pi(x; 210, 1)$. Compute the delta $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ at each prime step.
4. **Early Stopping:** The algorithm must immediately halt and record the exact prime $x$ and the preceding state the moment $\Delta(x) \le 0$ is achieved. 

## Success Criteria
- The successful execution of the counting script without failure.
- The identification of the exact prime $x$ representing the first crossover point, OR a definitive output proving that no crossover exists for $x \le 10^5$.
- A recorded integer tracking the maximum lead established by the $a=11$ class before the crossover (or up to the bound).

## Constraints
- **Domain Strictness:** Do NOT analyze any residue classes other than $a=11$ and $a=1$ modulo 210.
- **Metric Strictness:** Do NOT attempt to calculate logarithmic density. Use natural counting only.
- **Computational Limits:** Hard cap the search space at $x = 10^5$ to guarantee completion and validate the baseline script mechanics.