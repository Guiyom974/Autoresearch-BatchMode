# Research Problem: Algorithmic Optimization and Micro-Bound Validation of Logarithmic Density Modulo 210

## Objective
To overcome the severe computational bottlenecks that prevented output generation in previous iterations by shifting focus to algorithmic efficiency. We will develop a highly optimized, discrete-sum approximation for calculating logarithmic density in the modulo 210 prime race ($a=11$ vs $a=1$). The strict objective is to validate this optimized counting methodology up to a micro-bound of $x = 10^6$, ensuring the script successfully executes and provides a baseline empirical measurement of the Rubinstein-Sarnak Chebyshev bias.

## Research Questions
1. How can the numerical integration of logarithmic density be algorithmically simplified (e.g., via discrete summation over prime gaps) to eliminate computational timeouts?
2. Using an optimized segmented sieve and discrete logarithmic density summation, what is the empirical bias of the quadratic non-residue class $a=11$ against the principal class $a=1$ modulo 210 up to $x = 10^6$?
3. Does the $a=11$ class establish an initial dominance at this micro-bound, consistent with the predicted Chebyshev bias for non-residue vs. residue classes?

## Methodology
1. **Algorithmic Refactoring**: Replace continuous numerical integration functions (which likely caused the previous timeouts/failures) with a discrete cumulative sum approximation: $\delta(S) \approx \frac{1}{\log x} \sum_{n \in S, n \le x} \frac{1}{n}$.
2. **Optimized Sieve**: Implement a fast, memory-efficient Sieve of Eratosthenes strictly capped at $x = 10^6$. 
3. **Array Vectorization**: Utilize vectorized operations (e.g., NumPy if available, or highly optimized native arrays) to filter primes into the $a=11$ and $a=1$ residue classes modulo 210.
4. **Race Evaluation**: Track the running difference $\pi(x; 210, 11) - \pi(x; 210, 1)$ at discrete intervals, updating the logarithmic density metric only when the leader changes or at fixed logarithmic checkpoints.

## Success Criteria
1. **Execution**: The experiment must successfully run to completion without timing out or failing silently.
2. **Performance**: The prime generation and density calculation up to $x = 10^6$ must execute in under 30 seconds.
3. **Scientific Output**: The successful calculation of a specific logarithmic density value for the $a=11$ vs $a=1$ race modulo 210, providing a verified baseline for future scaling.

## Constraints
1. **Maximum Bound**: The evaluation bound is strictly capped at $x = 10^6$. Do not attempt to scale higher until this micro-bound is validated.
2. **Scope**: Limit the analysis exclusively to the two-way race between $a=11$ and $a=1$ modulo 210. Do not evaluate other residue classes or primorials.
3. **Mathematical Simplification**: Avoid heavy symbolic math libraries or continuous integration functions; rely strictly on discrete array manipulation and basic arithmetic summation.