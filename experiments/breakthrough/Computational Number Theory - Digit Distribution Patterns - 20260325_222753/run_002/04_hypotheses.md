

# Testable Hypotheses for Prime Digit Distribution Research

Based on the research problem and search context, I propose the following five testable hypotheses:

---

## Hypothesis 1: Base-Specific Benford's Law Deviation

### 1. The Hypothesis Statement
The leading digits of prime numbers will show **greater conformance to Benford's Law in Base-2** compared to Base-10 and Base-16 representations, with Base-16 showing intermediate deviation and Base-10 showing the largest deviation when analyzed at N = 10^7.

### 2. Why It's Testable
This hypothesis generates specific, measurable predictions about relative Kullback-Leibler (KL) divergence values across bases. KL divergence provides a continuous measure of distance between observed and theoretical distributions, allowing direct statistical comparison. The hypothesis is falsifiable because if Base-10 shows *better* conformance than Base-2, the hypothesis would be rejected.

### 3. Experiment to Test It
1. Generate all prime numbers up to N = 10^7 using a sieve algorithm
2. Convert each prime to Base-2, Base-10, and Base-16 string representations
3. Extract the leading (first) digit from each prime in each base
4. Calculate empirical frequency distributions P_obs(d) for digits 1-9 in Base-10 and corresponding digit ranges for Base-2 (digit 1 only) and Base-16 (digits 1-15)
5. Compute theoretical Benford's Law probabilities P_Benford(d) = log₁₀(1 + 1/d)
6. Calculate KL divergence: D_KL(P_obs || P_Benford) for each base
7. Compare the three KL divergence values to test the hypothesis's ordering prediction

---

## Hypothesis 2: Terminal Digit Uniformity After Filtering

### 1. The Hypothesis Statement
After explicitly filtering out trivially impossible terminal digits, the **remaining allowed terminal digits of prime numbers will exhibit a statistically uniform distribution** across Base-2, Base-10, and Base-16 at the N = 10^7 sample size.

### 2. Why It's Testable
This hypothesis can be tested using chi-squared goodness-of-fit tests, comparing observed terminal digit frequencies against expected uniform frequencies under the null hypothesis. The hypothesis makes a directional prediction (uniformity) that can be confirmed or rejected with quantifiable p-values. The explicit filtering constraint (e.g., removing 0, 2, 4, 5, 6, 8 for Base-10) is mathematically necessary and empirically verifiable.

### 3. Experiment to Test It
1. Generate primes up to N = 10^7
2. For each base:
   - **Base-10:** Filter to only allow terminal digits {1, 3, 7, 9}
   - **Base-16:** Filter to only allow terminal digits {1, 3, 5, 7, 9, 11, 13, 15} (odd, non-multiples of 8)
   - **Base-2:** Filter to only allow terminal digit 1 (all primes > 2 are odd)
3. Count frequency of each allowed terminal digit
4. Compute expected frequency under uniform distribution: E = (total filtered primes) / (number of allowed digits)
5. Calculate chi-squared statistic: χ² = Σ[(O - E)²/E]
6. Compare to critical value at α = 0.05 with (k-1) degrees of freedom (k = number of allowed digits)
7. Report p-values and determine whether to reject the uniformity null hypothesis

---

## Hypothesis 3: Sub-Terminal Digit Non-Uniformity

### 1. The Hypothesis Statement
The **second-to-last (sub-terminal) digits of prime numbers will show statistically significant deviations from uniform distribution** in at least one of the three bases (Base-2, Base-10, or Base-16) when tested using chi-squared analysis at N = 10^7.

### 2. Why It's Testable
Unlike terminal digits (which have known divisibility constraints), sub-terminal digits have no obvious mathematical restriction, making any detected non-uniformity genuinely interesting. The chi-squared test provides a standard statistical framework for detecting departures from uniformity, with clear acceptance/rejection criteria based on p-values.

### 3. Experiment to Test It
1. Generate primes up to N = 10^7
2. For each base, extract the second-to-last digit from each prime's representation
3. For each base, compile frequency counts of all possible sub-terminal digits:
   - **Base-10:** digits 0-9
   - **Base-16:** digits 0-15
   - **Base-2:** digit 0 or 1 (second-to-last bit)
4. Perform chi-squared goodness-of-fit test against uniform distribution
5. Apply Bonferroni correction or separate analysis for multiple comparisons across bases
6. Report which bases show significant deviation (p < 0.05) and the direction of deviation

---

## Hypothesis 4: Scale-Dependent Benford's Law Convergence

### 1. The Hypothesis Statement
The **Kullback-Leibler divergence between prime leading digit distributions and Benford's Law will decrease significantly** as the sample size increases from N = 10⁵ to N = 10⁶ to N = 10⁷, indicating convergence toward Benford's Law with larger prime samples.

### 2. Why It's Testable
This hypothesis predicts a specific trend (decreasing KL divergence with increasing N) that can be empirically measured at discrete sample sizes. The hypothesis is testable because we can computationally generate primes at multiple scales and measure the divergence at each scale. If divergence *increases* or remains constant, the hypothesis is falsified.

### 3. Experiment to Test It
1. Generate primes at three thresholds: N₁ = 10⁵, N₂ = 10⁶, N₃ = 10⁷
2. For each threshold, extract leading digits of primes in Base-10 (as the canonical representation)
3. Calculate empirical distribution and KL divergence from Benford's Law at each threshold
4. Perform regression or trend analysis on KL divergence as a function of log(N)
5. Test whether the trend coefficient is significantly negative
6. Additionally, examine whether the chi-squared p-value for Benford conformance increases across thresholds

---

## Hypothesis 5: Base-Specific Terminal Digit Bias Magnitude

### 1. The Hypothesis Statement
The **magnitude of chi-squared test statistics for terminal digit non-uniformity will differ significantly across bases**, with Base-2 showing the largest standardized deviation from uniformity and Base-16 showing the smallest, when testing primes up to N = 10⁷.

### 2. Why It's Testable
This hypothesis generates a testable prediction about the *relative* size of test statistics across bases, not just their statistical significance. By using standardized effect sizes (e.g., Cramér's V or normalized chi-squared), we can make fair comparisons across bases with different numbers of allowed digits. The hypothesis is falsifiable if Base-16 shows larger standardized deviation than Base-2.

### 3. Experiment to Test It
1. Generate primes up to N = 10⁷
2. For each base, identify allowed terminal digits and count frequencies
3. Calculate raw chi-squared statistic for each base: χ²_base
4. Calculate degrees of freedom for each base: df_base = (allowed digits - 1)
5. Compute standardized effect size using Cramér's V: V = √(χ²/(N × min(k-1, m-1))) where k and m are table dimensions
6. Alternatively, compute normalized chi-squared: χ²_norm = χ²/df to account for different numbers of categories
7. Compare standardized statistics across bases and test whether the ordering matches the hypothesis prediction

---

## Summary Table

| Hypothesis | Focus | Key Comparison | Statistical Method |
|------------|-------|----------------|-------------------|
| H1 | Benford's Law across bases | KL divergence: Base-2 < Base-16 < Base-10 | KL divergence |
| H2 | Terminal digit uniformity | Observed vs. uniform frequencies | Chi-squared GOF |
| H3 | Sub-terminal non-uniformity | Second-to-last digit frequencies | Chi-squared GOF |
| H4 | Scale convergence | KL divergence across N = 10⁵, 10⁶, 10⁷ | Trend/regression analysis |
| H5 | Terminal bias magnitude | Standardized χ² across bases | Cramér's V or normalized χ² |

These hypotheses are designed to be mutually complementary, collectively addressing all three research questions while providing multiple angles of evidence for or against the underlying theoretical expectations.