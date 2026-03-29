

# Testable Hypotheses for Digit Patterns in Prime Numbers

Based on the research problem and the stochastic modeling approaches suggested by the search results, I propose the following five hypotheses for investigation.

---

## Hypothesis 1: Non-Uniform Digit Transition Bias Within Prime Numbers (Base-10)

**1. Hypothesis Statement:**
The adjacent-digit transition probability matrix for prime numbers in Base-10 differs significantly from the transition matrix of randomly generated odd numbers not divisible by 2 or 5. Specifically, certain digit pairs (e.g., "77" or "33") will occur with frequencies that deviate beyond chance from the uniform baseline expectation.

**2. Why It's Testable:**
This hypothesis is directly testable through computational extraction of digit pairs from prime strings, construction of empirical transition matrices, and statistical comparison against a well-defined null model (random odd numbers with the same digit-generating process). The baseline is quantifiable, and deviations can be measured using standard divergence metrics (e.g., chi-square statistic, Kullback-Leibler divergence).

**3. Experiment to Test It:**
- **Step 1:** Generate all primes up to 10⁷ using the Sieve of Eratosthenes (or optimized variant). Convert each prime to its Base-10 string representation.
- **Step 2:** For each prime with ≥ 2 digits, extract all consecutive digit pairs (sliding window of size 2). Aggregate counts into a 10×10 transition matrix *Mₚ* where *Mₚ[i][j]* = frequency of digit *i* followed by digit *j*.
- **Step 3:** Generate a baseline dataset of random odd numbers in the same range, excluding multiples of 5, and construct a transition matrix *Mᵣ* using the same procedure.
- **Step 4:** Compute chi-square goodness-of-fit statistic comparing *Mₚ* against *Mᵣ*, or compute KL divergence *D_KL(Mₚ || Mᵣ)*.
- **Step 5:** Reject the null hypothesis if *p* < 0.01.

---

## Hypothesis 2: Terminal Digit Dependency Between Consecutive Primes

**1. Hypothesis Statement:**
The last digit of a prime number *p* influences the probability distribution of the last digit of the subsequent prime *p'*, beyond what would be expected if terminal digits were independently distributed. This constitutes a localized "memory" effect in the prime sequence.

**2. Why It's Testable:**
We can enumerate consecutive prime pairs, record their terminal digits (which are restricted to {1, 3, 7, 9} for primes > 10), and construct a 4×4 contingency table of transitions. The independence null hypothesis is straightforward to specify: if terminal digits were independent, *P(last_digit(p') = j | last_digit(p) = i) = P(last_digit(p') = j)* for all *i, j*. This can be tested with Pearson's chi-square test for contingency tables.

**3. Experiment to Test It:**
- **Step 1:** Generate consecutive primes up to 10⁷. For each pair (*pₙ*, *pₙ₊₁*), record the pair of terminal digits (*dₙ*, *dₙ₊₁*) where each *d* ∈ {1, 3, 7, 9}.
- **Step 2:** Build a 4×4 observed frequency matrix *O* where *O[i][j]* counts how often digit *i* is followed by digit *j*.
- **Step 3:** Compute expected frequencies *E[i][j]* under the independence assumption: *E[i][j] = (row_total[i] × col_total[j]) / grand_total*.
- **Step 4:** Compute the chi-square statistic: *χ² = Σ (O[i][j] - E[i][j])² / E[i][j]* with 9 degrees of freedom.
- **Step 5:** If *p* < 0.01, reject independence and conclude terminal digit dependency exists.

---

## Hypothesis 3: Middle Digit Non-Uniformity in Hexadecimal (Base-16) Representation

**1. Hypothesis Statement:**
When prime numbers up to 10⁷ are expressed in Base-16 (hexadecimal), certain hex digits are significantly over- or under-represented in the *middle* digit positions (excluding the most significant and least significant digits), compared to the uniform distribution expected from random integers.

**2. Why It's Testable:**
Middle-digit positions are not constrained by divisibility rules or the fact that primes > 2 are odd. Thus, any non-uniformity in these positions would indicate structure intrinsic to the primes' arithmetic properties. We can count digit frequencies at each middle position and compare against the uniform expectation (1/16 per hex digit) using chi-square tests. The hypothesis focuses on the middle to avoid edge effects from the distribution of leading/trailing digits.

**3. Experiment to Test It:**
- **Step 1:** Generate primes up to 10⁷. Convert each prime to its hexadecimal string representation. For each hex string with length ≥ 3, extract digits at all middle positions (positions 1 to *n*-2 in 0-indexed terms).
- **Step 2:** Aggregate counts across all primes and all middle positions, producing a frequency vector *F[0..15]* where *F[d]* = count of digit *d* appearing in middle positions.
- **Step 3:** Define the null model: under uniformity, expected count for each digit is *E[d] = total_middle_digits / 16*.
- **Step 4:** Compute *χ² = Σ (F[d] - E[d])² / E[d]* with 15 degrees of freedom.
- **Step 5:** Visualize deviations using a bar chart of normalized residuals (*(F[d] - E[d]) / √E[d]*). Report which hex digits deviate most and whether the overall test is significant at *p* < 0.01.

---

## Hypothesis 4: Faster-Than-Normal Convergence of Digit Sum Distribution

**1. Hypothesis Statement:**
The distribution of digit sums for prime numbers converges to a Gaussian (normal) distribution more rapidly than predicted by standard central limit theorem (CLT) scaling as *O(1/√n)*, where *n* is the number of digits. Equivalently, the variance of the digit sum across primes of a given digit-length converges to the binomial variance faster than expected under independence assumptions.

**2. Why It's Testable:**
For a random variable consisting of *n* i.i.d. uniform digits (0-9), the digit sum has mean *μ = 9n/2* and variance *σ² = 9n/2*. The empirical mean and variance of digit sums for primes of length *n* can be computed and compared to these theoretical values. If convergence is faster, the observed variance will be significantly smaller than *σ²* for moderate *n*. This can be tested using a Z-test or Kolmogorov-Smirnov test against the normal CDF.

**3. Experiment to Test It:**
- **Step 1:** Generate primes and bin them by digit length (e.g., 5-digit primes, 6-digit primes, 7-digit primes).
- **Step 2:** For each bin, compute the empirical mean *μ̂* and variance *σ̂²* of digit sums.
- **Step 3:** Compute the theoretical variance for *n*-digit numbers: *σ²_theory = 9n/2*.
- **Step 4:** For each bin, compute a standardized deviation: *Z = (σ̂² - σ²_theory) / (SE(σ̂²))*, where the standard error is estimated via bootstrap or analytical formula for sample variance.
- **Step 5:** Test whether *Z* is significantly different from 0. Also, plot *|μ̂ - μ|* and *|σ̂² - σ²_theory|* as functions of digit length to assess convergence rate.

---

## Hypothesis 5: Persistent Markov Stationary Distribution in Digit Gaps (Cross-Base Validation)

**1. Hypothesis Statement:**
The Markov chain transition model constructed from within-prime digit transitions (Hypothesis 1) will exhibit a unique stationary distribution that is *robust across bases*: when the same analysis is performed on primes in Base-2 (binary) and Base-16, the normalized stationary distribution vectors will show correlated biases, suggesting a common underlying structure in prime digit sequences that transcends numerical representation.

**2. Why It's Testable:**
If digit transition matrices are ergodic (as noted in the search results for prime gaps), they possess a unique stationary distribution. We can compute this stationary distribution for each base, normalize it, and compare across bases. The hypothesis predicts that bases with different digit alphabets will nonetheless show correlated deviations from uniformity—e.g., if "3" is over-represented after "3" in Base-10, then the binary equivalent might show over-representation of certain bit patterns. Correlation coefficients between stationary distributions across bases can be computed and tested for significance.

**3. Experiment to Test It:**
- **Step 1:** Generate primes up to 10⁷. Convert each to binary and hexadecimal strings.
- **Step 2:** For each base representation (Base-2, Base-10, Base-16), build the transition matrix *M* as in Hypothesis 1.
- **Step 3:** Compute the stationary distribution *π* for each *M* by solving *π = πM* (or via iterative power method).
- **Step 4:** Normalize each *π* to sum to 1. For Base-2, the stationary distribution is over {0, 1}; for Base-10, over {0,...,9}; for Base-16, over {0,...,15}.
- **Step 5:** For cross-base comparison, embed all distributions into a common feature space (e.g., compute deviations from uniform: *δ[d] = π[d] - 1/|alphabet|*). Compute Pearson correlation between *δ* vectors across base pairs.
- **Step 6:** If correlations are significantly positive (e.g., *r* > 0.5, *p* < 0.01), conclude that biases are preserved across representations.

---

## Summary Table

| Hypothesis | Focus | Key Comparison | Statistical Test |
|------------|-------|----------------|------------------|
| 1 | Within-prime digit transitions | Primes vs. random odd numbers | Chi-square / KL divergence |
| 2 | Terminal digit dependency | Consecutive prime endings | Chi-square for contingency |
| 3 | Hex middle-digit uniformity | Middle digits vs. uniform | Chi-square goodness-of-fit |
| 4 | Digit sum convergence | Empirical vs. CLT-predicted variance | Z-test / K-S test |
| 5 | Cross-base stationary distributions | Stationary *π* across bases | Pearson correlation |

These hypotheses collectively address the research questions while providing clear, executable experimental designs that meet the success criteria (significant deviations at *p* < 0.01, reproducibility across dataset sizes, and robustness against baseline artifacts).