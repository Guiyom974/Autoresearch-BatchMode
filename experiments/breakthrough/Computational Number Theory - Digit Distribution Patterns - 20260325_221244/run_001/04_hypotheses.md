

# Testable Hypotheses for Digit Sequencing and Base-N Distribution Patterns in Prime Numbers

Based on the research problem, I propose the following five testable hypotheses:

---

## Hypothesis 1: Adjacent Digit Transition Bias in Prime Numbers

### 1. Hypothesis Statement
The transition probability matrix for adjacent digits within prime numbers (Base-10) exhibits significant deviations from the transition matrix derived from randomly generated odd numbers (numbers not divisible by 2 or 5). Specifically, certain digit pairs (e.g., "33", "77", "99") will appear with frequencies that deviate by more than 2 standard errors from the baseline expectation.

### 2. Why It's Testable
This hypothesis is testable because:
- We can construct empirical 10×10 transition matrices from both primes and random odd numbers
- The null hypothesis (no difference) can be formally tested using chi-square goodness-of-fit or a chi-square test of independence
- Statistical significance can be quantified with p-values, allowing us to reject or fail to reject the null hypothesis at predetermined thresholds (p < 0.01)

### 3. Experiment Design
**Data Generation:**
- Generate all primes up to x = 10^7 using the Sieve of Eratosthenes
- Generate an equal-sized set of random odd numbers (non-divisible by 2 or 5) for baseline comparison

**Analysis Procedure:**
1. Convert each number to its Base-10 string representation
2. For each adjacent digit pair (d₁ → d₂), increment the corresponding cell in the transition matrix
3. Normalize rows to obtain empirical transition probabilities
4. Compute expected transition probabilities from the random odd number baseline
5. Calculate chi-square statistic: χ² = Σ[(observed - expected)² / expected]
6. Compare against critical value with 81 degrees of freedom (10×10 - 10 - 10 + 1)

**Success Criterion:** Reject the null hypothesis of uniform transitions with p < 0.01

---

## Hypothesis 2: Terminal Digit Dependency Between Consecutive Primes

### 1. Hypothesis Statement
The final digit of a prime p influences the probability distribution of the final digit of the next consecutive prime pₙ₊₁ in a non-uniform way. The 4×4 terminal digit transition matrix (for digits {1, 3, 7, 9}) will show significant deviations from the uniform distribution expected under the assumption that terminal digits are independent and identically distributed.

### 2. Why It's Testable
This hypothesis is testable because:
- We can directly observe and count all transitions between terminal digits of consecutive primes
- The expected distribution under the null hypothesis is simply uniform (each of 16 possible transitions has probability 1/16)
- Chi-square goodness-of-fit test provides a direct statistical comparison
- The experiment is computationally efficient using sequential prime generation

### 3. Experiment Design
**Data Generation:**
- Generate all primes up to x = 10^7
- Extract the final digit of each prime (restricted to {1, 3, 7, 9})

**Analysis Procedure:**
1. Create a 4×4 transition count matrix for terminal digit pairs (pₙ terminal → pₙ₊₁ terminal)
2. Calculate expected counts assuming uniform distribution: expected = total_transitions / 16
3. Compute chi-square statistic with 15 degrees of freedom
4. For significant results, identify specific transition anomalies (e.g., if primes ending in 9 are disproportionately followed by primes ending in 7)

**Control Baseline:**
- Compare results against a simulated baseline where terminal digits are randomly assigned according to the observed marginal distribution

**Success Criterion:** At least one terminal digit transition shows deviation significant at p < 0.01

---

## Hypothesis 3: Non-Uniform Middle Digit Distribution in Hexadecimal Representation

### 1. Hypothesis Statement
When prime numbers are expressed in Base-16 (hexadecimal), certain hex digits (0-9, A-F) are over- or under-represented in non-terminal positions compared to the uniform distribution expected from random odd numbers. This bias will be most pronounced in the middle digits of longer primes (≥4 hex digits).

### 2. Why It's Testable
This hypothesis is testable because:
- We can systematically extract all non-terminal hex digits from primes
- The expected distribution under the null hypothesis is uniform (1/16 for each hex digit)
- Chi-square goodness-of-fit test can detect deviations from uniformity
- We can stratify analysis by digit position (leading, middle, trailing non-terminal positions)

### 3. Experiment Design
**Data Generation:**
- Generate primes up to x = 10^7
- Convert each prime to hexadecimal string representation
- Extract non-terminal digit positions (excluding most significant and least significant hex digits)

**Analysis Procedure:**
1. Count occurrences of each hex digit in middle positions across all qualifying primes
2. Calculate expected counts assuming uniform distribution: expected = total_middle_digits / 16
3. Perform chi-square goodness-of-fit test (15 degrees of freedom)
4. Stratify analysis by prime size (group by hex digit length: 1-2, 3-4, 5+ digits)
5. Create heatmaps visualizing deviations from uniform distribution

**Comparative Baseline:**
- Repeat the same analysis on randomly generated odd numbers of equivalent magnitude
- Subtract the random baseline from the prime distribution to isolate prime-specific biases

**Success Criterion:** Significant deviation (p < 0.01) in at least one hex digit position category

---

## Hypothesis 4: Accelerated Convergence of Digit Sum Distribution

### 1. Hypothesis Statement
The distribution of digit sums of prime numbers converges to a normal distribution faster than predicted by the classical Central Limit Theorem convergence rate for sums of independent, identically distributed random variables. Specifically, for primes up to 10^7, the standardized digit sum distribution will have kurtosis and skewness closer to zero than expected for samples of that size from random odd numbers.

### 2. Why It's Testable
This hypothesis is testable because:
- We can compute digit sums for all primes up to 10^7
- Standard statistical measures (mean, variance, skewness, kurtosis) can be calculated
- The null hypothesis assumes standard CLT convergence rates
- We can compare observed distributions to theoretical normal distributions using Kolmogorov-Smirnov tests

### 3. Experiment Design
**Data Generation:**
- Generate all primes up to x = 10^7
- Compute the digit sum for each prime

**Analysis Procedure:**
1. Calculate sample statistics: mean, standard deviation, skewness (γ₁), kurtosis (γ₂)
2. Perform Kolmogorov-Smirnov test comparing the empirical distribution to the theoretical normal distribution with matching mean and variance
3. Compute the KS statistic and compare against critical values
4. Repeat for random odd number baseline
5. Compare convergence rates: if primes show smaller KS statistics than random numbers of similar size, hypothesis is supported

**Statistical Comparison:**
- Calculate z-scores for skewness and kurtosis to determine if deviations from normality are statistically significant
- Compare the rate of convergence between primes and random odd numbers

**Success Criterion:** The digit sum distribution of primes shows closer convergence to normality than random odd numbers at the same sample size

---

## Hypothesis 5: Least Significant Bit Independence Violation in Binary Representation

### 1. Hypothesis Statement
The distribution of the least significant bit (LSB) in the binary representation of prime numbers is not purely determined by the constraint that all primes (except 2) are odd. Specifically, the proportion of primes whose binary representation ends in "...01" versus "...11" (i.e., the second LSB) shows unexpected bias related to the prime's magnitude or preceding bits.

### 2. Why It's Testable
This hypothesis is testable because:
- We can extract the second LSB for all odd primes (excluding 2)
- Under simple divisibility constraints, we expect approximately 50/50 distribution
- Chi-square test can detect significant deviations from the expected proportion
- We can analyze whether the bias correlates with prime magnitude

### 3. Experiment Design
**Data Generation:**
- Generate all odd primes up to x = 10^7
- Convert each prime to binary and extract the second least significant bit (bit position 1)

**Analysis Procedure:**
1. Count the number of primes where bit position 1 = 0 vs. bit position 1 = 1
2. Calculate expected proportion: 50% for each under the null hypothesis
3. Perform binomial test or chi-square goodness-of-fit
4. Stratify by prime magnitude (e.g., primes in ranges [3, 10⁴], [10⁴, 10⁵], [10⁵, 10⁶], [10⁶, 10⁷]) to detect magnitude-dependent patterns
5. Extend to analyze higher-order bit positions for more complex dependencies

**Extended Analysis:**
- Build transition probabilities between the last 2-3 bits of consecutive primes
- Test whether the binary suffix influences the binary suffix of the next prime

**Success Criterion:** Significant deviation from 50/50 distribution at p < 0.01 in at least one magnitude range

---

## Summary Table of Hypotheses

| Hypothesis | Key Variables | Statistical Test | Expected Outcome |
|------------|----------------|------------------|------------------|
| 1: Digit Transition Bias | Adjacent digit pairs in Base-10 | Chi-square test of independence | Non-uniform transition matrix |
| 2: Terminal Digit Dependency | Final digits of consecutive primes | Chi-square goodness-of-fit | Dependent terminal transitions |
| 3: Hex Middle Digit Bias | Hex digits in non-terminal positions | Chi-square goodness-of-fit | Non-uniform hex distribution |
| 4: Digit Sum Convergence | Sum of digits | Kolmogorov-Smirnov test | Faster CLT convergence |
| 5: LSB Independence | Second LSB in binary | Binomial/chi-square test | Deviation from 50/50 |

Each hypothesis addresses a distinct aspect of the research problem and can be tested within the computational constraints (2-3 minutes execution time) using the proposed methodology.