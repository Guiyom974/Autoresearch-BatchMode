

# Testable Hypotheses for Prime Digit Pattern Research

Based on the provided research problem and the landmark 2016 discovery by Lemke Oliver and Soundararajan regarding consecutive prime terminal digit repulsion, I propose the following five testable hypotheses:

---

## Hypothesis 1: Internal Digit Transition Bias Within Primes

### 1. Hypothesis Statement
The adjacent digit transition probabilities within a single prime number (e.g., examining positions 1→2, 2→3, etc.) are not uniformly distributed. Specifically, certain digit pairs (such as "11", "33", or "77") will be significantly *underrepresented* in the interior positions of primes compared to a uniform baseline, mirroring the terminal digit repulsion phenomenon observed in consecutive primes.

### 2. Why It's Testable
This hypothesis is testable because:
- We can construct a 10×10 transition matrix by examining every pair of adjacent digits within all primes up to 10⁷
- The uniform baseline expectation is computable: if digit *dᵢ* appears with probability *P(dᵢ)*, the expected probability of transition *dᵢ→dⱼ* is simply *P(dⱼ)* (independence assumption)
- We can apply a chi-square goodness-of-fit test comparing observed transition counts against expected counts under the uniform independence model
- The test is reproducible across different prime ranges (10⁶ vs 10⁷)

### 3. Experiment Design
```
Algorithm:
1. Generate all primes up to 10⁷ using Sieve of Eratosthenes
2. For each prime in base-10 representation:
   - Convert to string (e.g., 12347 → "12347")
   - Extract all adjacent digit pairs: ("12", "23", "34", "47")
   - Increment corresponding cell in a 10×10 transition counter matrix M
3. Compute row-normalized transition probability matrix T = M / row_sums(M)
4. Compute expected uniform matrix E where E[i,j] = P(digit j) = observed frequency of digit j
5. Perform chi-square test: Σ((M[i,j] - E[i,j])² / E[i,j])
6. Compare p-value against α = 0.01 threshold
7. Visualize via heatmap showing deviations (T - E)
```

---

## Hypothesis 2: Terminal Digit Influence Extends to Second-to-Last Position

### 1. Hypothesis Statement
The final digit of prime *pₙ* influences the probability distribution of the *second-to-last* digit of the *next* prime *pₙ₊₁*. That is, the tuple (last digit of *pₙ*, second-to-last digit of *pₙ₊₁*) exhibits non-uniform joint distribution—for example, a prime ending in 7 is less likely to be followed by a prime whose second-to-last digit is also 7, compared to the baseline.

### 2. Why It's Testable
This hypothesis is testable because:
- It generalizes the known 1D terminal digit repulsion to a 2D structure
- The sample space is finite: 4 possible terminal digits × 10 possible second-to-last digits = 40 observable classes
- Under the null hypothesis of independence, we can compute expected frequencies as P(last_digit = a) × P(second_to_last = b)
- The 10⁷ dataset provides sufficient samples (>664,579 primes) to detect medium effect sizes with power > 0.8

### 3. Experiment Design
```
Algorithm:
1. Generate primes up to 10⁷; store as list P = [p₁, p₂, ..., pₙ]
2. For each consecutive pair (pᵢ, pᵢ₊₁):
   - Extract last digit of pᵢ: d_last = pᵢ % 10
   - Extract second-to-last digit of pᵢ₊₁: d_snd_last = (pᵢ₊₁ // 10) % 10
   - Increment counter C[d_last][d_snd_last]
3. Compute expected matrix E[d_last][d_snd_last] = (count of primes ending in d_last / total) 
                                                  × (count of primes with given second-to-last digit / total)
                                                  × (total pairs)
4. Apply chi-square test with df = (4-1)(10-1) = 27 degrees of freedom
5. Identify specific significant cells via residual analysis (standardized residuals > 2)
```

---

## Hypothesis 3: Hexadecimal Digit Concentration in Prime Middle Positions

### 1. Hypothesis Statement
When primes are expressed in Base-16 (hexadecimal), certain hex digits (specifically 0x0, 0x1, 0xF) are overrepresented in the *middle third* of prime representations compared to their overall frequency, while other digits are underrepresented. This "central clustering" effect differs significantly from what is observed in randomly generated odd numbers filtered for primality constraints.

### 2. Why It's Testable
This hypothesis is testable because:
- We can systematically count hex digit occurrences by position (prefix, middle, suffix) across all primes
- The baseline expectation (null hypothesis) can be derived from digit frequencies in random odd numbers with the same filter (no even digits, no 5 or A in terminal position)
- Position-wise chi-square tests can isolate the middle-position effect from edge effects
- The phenomenon can be verified independently in base-10, base-16, and base-2 to test universality

### 3. Experiment Design
```
Algorithm:
1. Generate all primes up to 10⁷
2. For each prime, compute hex representation (without "0x" prefix):
   - Identify total length L
   - Define middle region as positions [L//3, 2L//3)
   - Count digit occurrences in: prefix (pos < L//3), middle (L//3 ≤ pos < 2L//3), suffix (pos ≥ 2L//3)
3. Aggregate counts into 16-digit × 3-position contingency table
4. For baseline: generate equal-sized set of random odd numbers (not divisible by 2 or 5); compute same table
5. Perform chi-square test: H₀ = digit × position distribution is same as random baseline
6. Apply post-hoc standardized residual analysis to identify specific digit-position deviations
```

---

## Hypothesis 4: Digit Sum Distribution Deviation from Normal Approximation

### 1. Hypothesis Statement
The distribution of digit sums for primes converges to a normal distribution *more slowly* than predicted by classical limit theorems for sums of non-identically distributed random variables. Specifically, the kurtosis of the prime digit sum distribution remains significantly positive (leptokurtic) at sample sizes of 10⁷, indicating persistent digit-sum clustering beyond what random odd number controls exhibit.

### 2. Why It's Testable
This hypothesis is testable because:
- We can compute the empirical digit sum distribution for primes and measure kurtosis/excess kurtosis
- The null hypothesis (Lindeberg-Feller CLT applies) predicts excess kurtosis → 0 as n → ∞
- We can compare observed excess kurtosis against the sampling distribution under the null
- This provides a quantitative measure of "clustering speed" that can be compared across bases

### 3. Experiment Design
```
Algorithm:
1. Generate primes up to 10⁷; compute digit_sum(p) for each
2. Compute empirical statistics:
   - Mean μ = E[digit_sum]
   - Variance σ² = Var[digit_sum)
   - Skewness γ₁
   - Excess Kurtosis γ₂ = (μ₄/σ⁴) - 3
3. Generate matched control set: random odd numbers (not divisible by 2 or 5) up to 10⁷
4. Compute same statistics for control set
5. Test H₀: γ₂(primes) = γ₂(control) vs H₁: γ₂(primes) ≠ γ₂(control)
   - Use bootstrap standard errors or asymptotic normality of kurtosis estimator
6. Repeat analysis for base-16 digit sums to test base-independence
```

---

## Hypothesis 5: Asymmetric Cross-Base Transition Consistency

### 1. Hypothesis Statement
The digit transition bias observed in base-10 primes is *directionally consistent* across bases but *asymmetric in magnitude*. If digit pair "ab" is underrepresented in base-10 primes, the corresponding pair in base-16 (e.g., 0xAB) will also be underrepresented, but the degree of underrepresentation may differ significantly. The ratio of observed-to-expected frequencies is correlated across bases, but the correlation coefficient is less than 1.

### 2. Why It's Testable
This hypothesis is testable because:
- We can independently compute transition matrices for base-10 and base-16
- Each matrix cell represents an observed-to-expected ratio (O/E)
- We can compute Pearson correlation ρ between the O/E vectors across bases
- Under the null (biases are base-specific artifacts), ρ should not significantly differ from 0
- Under the alternative (biases reflect true prime structure), ρ should be significantly positive but < 1

### 3. Experiment Design
```
Algorithm:
1. Generate all primes up to 10⁷
2. For base-10:
   - Build 10×10 transition matrix M₁₀
   - Compute expected matrix E₁₀ under uniform independence
   - Compute O/E ratio matrix R₁₀ = M₁₀ / E₁₀
3. For base-16:
   - Convert each prime to hex string
   - Build 16×16 transition matrix M₁₆
   - Compute expected E₁₆ and ratio R₁₆
4. Flatten both ratio matrices into vectors; compute Pearson correlation r(R₁₀, R₁₆)
5. Statistical test:
   - H₀: ρ = 0 (no cross-base consistency)
   - H₁: ρ > 0 (positive correlation)
   - Use Fisher's z-transformation for confidence interval
   - Test if ρ < 1 (asymmetry): compute 95% CI for ρ
6. Control experiment: repeat with random odd numbers; verify ρ is not significantly > 0
```

---

## Summary Table

| Hypothesis | Focus | Key Variables | Statistical Test |
|------------|-------|---------------|------------------|
| H1 | Internal digit transitions | Adjacent digit pairs within primes | Chi-square GOF |
| H2 | 2D terminal dependency | (last digit of pₙ, 2nd-last of pₙ₊₁) | Chi-square test |
| H3 | Hex middle-position clustering | Digit × Position contingency | Chi-square test |
| H4 | Digit sum kurtosis | Excess kurtosis γ₂ | Bootstrap/Asymptotic |
| H5 | Cross-base consistency | O/E ratios across bases | Pearson correlation |

Each hypothesis directly addresses the research problem's goal of discovering "unexpected localized biases in the digits of primes" while building upon the known terminal digit repulsion phenomenon discovered by Lemke Oliver and Soundararajan.