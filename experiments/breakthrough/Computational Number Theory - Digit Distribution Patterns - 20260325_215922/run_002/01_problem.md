# Research Problem: Comparative Markovian Analysis of Adjacent Digit Transitions in Base-10 and Base-2 Prime Numbers

## Objective
To computationally investigate and quantify first-order sequential digit dependencies (Markov transition probabilities) within prime numbers, specifically comparing Base-10 and Base-2 representations. The goal is to determine if adjacent digit transitions in primes deviate from a purely uniform random distribution (after accounting for known trivial constraints, such as the final digit), thereby identifying localized structural biases in prime digit sequencing.

## Research Questions
1. **Base-10 Transition Probabilities:** Within the set of primes up to $10^8$, does the first-order transition probability matrix for adjacent digits (e.g., the likelihood of '3' being followed by '7') show statistically significant deviations from expected uniform frequencies?
2. **Base-2 Structural Biases:** When the exact same set of prime numbers is converted to Base-2, do binary adjacent digit transitions (0->0, 0->1, 1->0, 1->1) exhibit non-uniform clustering or oscillatory patterns?
3. **Cross-Base Invariants:** Are there any sequence dependency anomalies that persist across both Base-10 and Base-2 representations?

## Methodology
1. **Data Generation:** Utilize an efficient sieve algorithm (e.g., Sieve of Eratosthenes) to generate all prime numbers up to $10^8$. 
2. **Data Preprocessing:** Strip the final digit from the Base-10 representations and the final bit from the Base-2 representations to eliminate trivial constraints (e.g., Base-10 primes $>5$ must end in 1, 3, 7, or 9; Base-2 primes $>2$ must end in 1).
3. **Transition Matrix Construction:** Construct $10 \times 10$ transition matrices for Base-10 and $2 \times 2$ matrices for Base-2 by counting adjacent digit pairs moving left-to-right.
4. **Statistical Testing:** Perform Chi-Square Goodness-of-Fit tests on the transition matrices against a null hypothesis of uniformly distributed adjacent digits.

## Success Criteria
- Successful generation and population of transition matrices for both Base-10 and Base-2 primes without runtime errors.
- Identification of statistically significant deviations (p < 0.01) in specific digit-to-digit transitions, or rigorous confirmation of uniformity.
- Delivery of a clean, reproducible script that cleanly bypasses previous syntax and execution failures.

## Constraints
- **Algorithmic Efficiency:** The prime generation and matrix population must be optimized to run within standard memory limits (avoiding full string conversions of massive arrays simultaneously).
- **Domain Strictness:** The analysis must strictly remain on the structural distributions of digits within standard bases (Base-10 and Base-2), avoiding unrelated number theoretic properties.
- **Triviality Avoidance:** The algorithm must explicitly exclude the final digit/bit of each prime to prevent skewing the transition matrix with known, trivial prime ending rules.