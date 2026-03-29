

# Testable Hypotheses for Digit Sequencing and Base-N Distribution Patterns in Prime Numbers

Based on the research problem and search context, I propose the following 5 testable hypotheses:

---

## Hypothesis 1: Internal Digit Transition Bias Beyond Terminal Digits

**Statement:** Within the internal digits of prime numbers (excluding the terminal digit), certain adjacent digit pairs occur at frequencies significantly different from the expected uniform distribution.

**Why it's testable:** This hypothesis can be directly tested by constructing a transition matrix from adjacent digit pairs within the body of prime numbers and comparing it against a chi-square goodness-of-fit test with the uniform expectation (each of 100 possible pairs having 1% probability).

**Experiment:**
1. Generate primes up to 10⁷ using Sieve of Eratosthenes
2. For each prime, extract all adjacent digit pairs from positions 1 through n-1 (excluding terminal digit at position n)
3. Aggregate counts across all primes to build a 10×10 transition matrix
4. Perform chi-square test comparing observed frequencies against uniform baseline
5. Use permutation tests to verify significance (p < 0.01 threshold)

---

## Hypothesis 2: Last-Digit Repulsion Effect is Base-Dependent

**Statement:** The "modular repulsion" effect (consecutive primes avoiding the same terminal digit) is not uniform across number bases—certain bases will exhibit stronger or weaker repulsion than Base-10.

**Why it's testable:** This hypothesis is testable by computing the empirical transition probabilities of terminal digits across different bases and testing whether the deviation from uniform distribution (25% for same-digit pairs) varies systematically with base.

**Experiment:**
1. Generate primes up to 10⁷
2. Convert each prime to Base-2, Base-10, and Base-16 representations
3. For each base, construct a 2×2 terminal digit transition matrix (where terminal digits are defined by the base's digit set)
4. Compute the "same-terminal" probability for consecutive primes in each base
5. Perform pairwise statistical comparisons across bases to determine if repulsion strength differs significantly

---

## Hypothesis 3: Prime Memory Decays Exponentially Within Fixed Prime Intervals

**Statement:** The dependency between consecutive primes' last digits follows an exponential decay model, with the repulsion effect becoming negligible after approximately d prime gaps (where d ≈ 10 for Base-10, based on prior work by Lemke Oliver & Soundararajan).

**Why it's testable:** This hypothesis can be tested by measuring the conditional probability of same-last-digit primes as a function of the gap distance between them and fitting an exponential decay model to the data.

**Experiment:**
1. Generate primes up to 10⁷ and record consecutive prime indices
2. For gap distances k = 1, 2, 3, ..., 20, compute P(same last digit | gap = k)
3. Fit model P(k) = 0.25 + (P₁ - 0.25) × e^(-λk) using nonlinear regression
4. Test whether λ > 0 (decay exists) and whether P₁ significantly differs from 0.25
5. Compare fitted decay rates across bases to test if the phenomenon is base-invariant

---

## Hypothesis 4: Middle Digits Exhibit Stronger Base-16 Bias Than Terminal Digits

**Statement:** When primes are expressed in Base-16, hex digits occurring in the middle positions (neither most nor least significant) show larger deviations from uniform distribution than terminal hex digits.

**Why it's testable:** This hypothesis is testable by comparing chi-square statistics for digit frequency distributions across different positional categories (first, middle, last hex digits) and testing for significant differences.

**Experiment:**
1. Generate primes up to 10⁷
2. Convert each to hexadecimal and categorize each digit by its position (first 20%, middle 60%, last 20%)
3. For each positional category, compute observed frequencies of hex digits 0x0 through 0xF
4. Calculate chi-square statistic for each category against uniform baseline
5. Use Levene's test or ANOVA to determine if variance across categories is significant

---

## Hypothesis 5: Digit Sum Distribution of Primes Converges to Normality More Slowly Than Random Odd Numbers

**Statement:** The sum of digits of prime numbers does not follow a normal distribution as quickly as expected by the Central Limit Theorem when compared to randomly generated odd numbers with the same digit-length distribution.

**Why it's testable:** This hypothesis is testable by comparing the empirical distribution of digit sums for primes against both the theoretical normal distribution and the empirical distribution for random odd numbers, using Kolmogorov-Smirnov tests.

**Experiment:**
1. Generate primes up to 10⁷ and generate a comparable set of random odd numbers (filtered for primality condition only: odd and not divisible by 5)
2. Compute digit sum for each number in both datasets
3. Group by number of digits to control for length effects
4. For each digit-length group, perform Kolmogorov-Smirnov test comparing:
   - Primes vs. theoretical normal distribution
   - Primes vs. random odd numbers
5. Test whether primes consistently show larger KS distances, indicating slower convergence to normality

---

## Summary Table

| Hypothesis | Key Variable | Expected Outcome | Statistical Test |
|------------|--------------|------------------|------------------|
| H1 | Internal digit pairs | Non-uniform frequencies | Chi-square |
| H2 | Number base | Varying repulsion strength | Pairwise comparison |
| H3 | Gap distance (k) | Exponential decay of memory | Nonlinear regression |
| H4 | Digit position in Base-16 | Middle > terminal bias | ANOVA on chi-square stats |
| H5 | Digit sum | Slower CLT convergence | Kolmogorov-Smirnov |

These hypotheses extend beyond the known terminal-digit repulsion phenomenon to investigate internal structure, cross-base consistency, and distributional properties—fulfilling the "non-obvious patterns" requirement in the research objectives.