

# Testable Hypotheses for Primorial-Adjusted Benford Model Validation

---

## Hypothesis 1: KL Divergence Superiority of Primorial-Adjusted Model

### 1. Hypothesis Statement
The Kullback-Leibler divergence between the empirical leading digit distribution of primes in Base-210 and the **primorial-adjusted Benford model** will be significantly smaller than the KL divergence measured against the **naive Benford model**.

### 2. Why It's Testable
This hypothesis is directly testable because:
- All components are quantifiable: empirical probabilities from data, theoretical probabilities from both models
- KL divergence has a well-defined formula: $D_{KL}(P_{emp} || P_{theoretical}) = \sum_{i=1}^{48} P_{emp}(i) \log\frac{P_{emp}(i)}{P_{theoretical}(i)}$
- Both distributions operate over the same support set (48 coprime digits)
- Statistical comparison via bootstrap confidence intervals can determine significance

### 3. Experiment to Test It
1. Generate primes up to 10^7, filter to p > 210
2. Convert each prime to Base-210, extract leading digit
3. Compute empirical probability distribution $P_{emp}$ for all 48 coprime digits
4. Calculate theoretical distributions: $P_{naive}$ (standard Benford) and $P_{primorial}$ (primorial-adjusted)
5. Compute KL divergence for both: $D_{naive} = D_{KL}(P_{emp} || P_{naive})$ and $D_{primorial} = D_{KL}(P_{emp} || P_{primorial})$
6. Compare $D_{primorial} < D_{naive}$ using paired bootstrap resampling (10,000 iterations) to generate 95% confidence intervals

---

## Hypothesis 2: Chi-Squared Goodness-of-Fit Enhancement

### 1. Hypothesis Statement
The chi-squared test statistic comparing empirical leading digit frequencies to the **primorial-adjusted Benford model** will yield a **smaller χ² value and higher p-value** compared to the uniform distribution model, indicating superior goodness-of-fit.

### 2. Why It's Testable
This hypothesis is testable because:
- Chi-squared test requires only observed counts and expected proportions under each model
- Null hypothesis structure allows direct comparison: $H_0$: "Data follows [model X]"
- Rejection/non-rejection decisions provide binary comparison framework
- Sample size (187,936 digits) provides sufficient degrees of freedom (47 df)

### 3. Experiment to Test It
1. Calculate observed frequencies $O_i$ for each of the 48 coprime digits
2. Calculate expected frequencies $E_i^{uniform} = N/48$ under uniform model
3. Calculate expected frequencies $E_i^{primorial} = N \times P_{primorial}(i)$ under primorial-adjusted model
4. Compute chi-squared statistics: $\chi^2_{uniform} = \sum\frac{(O_i - E_i^{uniform})^2}{E_i^{uniform}}$ and $\chi^2_{primorial}$
5. Perform chi-squared goodness-of-fit tests for each model
6. Compare p-values: $p_{primorial} > p_{uniform}$ with significance level α = 0.05

---

## Hypothesis 3: Deviation from Naive Benford's Law

### 1. Hypothesis Statement
The empirical leading digit distribution of primes in Base-210 will exhibit **statistically significant deviation** from naive Benford's law (p < 0.05 in chi-squared test), while conforming to the primorial-adjusted Benford model.

### 2. Why It's Testable
This hypothesis is testable because:
- Statistical hypothesis testing framework directly addresses "significant deviation"
- Both models can be tested against the same empirical data
- The comparison is directional: naive Benford should reject, primorial-adjusted should not
- The 48-digit support provides adequate power for detection

### 3. Experiment to Test It
1. Using the same dataset (primes up to 10^7, p > 210)
2. Compute $\chi^2_{naive}$ against naive Benford distribution
3. Compute $\chi^2_{primorial}$ against primorial-adjusted distribution
4. Determine critical values at α = 0.05 for 47 degrees of freedom (χ² ≈ 64.0)
5. Expected outcome: $\chi^2_{naive} > 64.0$ (reject naive Benford) while $\chi^2_{primorial} < 64.0$ (fail to reject primorial-adjusted)

---

## Hypothesis 4: Complete Coprime Digit Coverage

### 1. Hypothesis Statement
100% of the observed leading digits from the filtered prime dataset (p > 210) will fall exclusively within the **48-digit set coprime to 210**, confirming data integrity and the structural property of primorial-adjusted models.

### 2. Why It's Testable
This hypothesis is testable because:
- It's a binary outcome: every observed digit is either coprime to 210 or it isn't
- No statistical uncertainty exists; the result is deterministic given correct data processing
- Verification requires only cross-referencing extracted digits against the coprime set
- This serves as a necessary condition for model validity

### 3. Experiment to Test It
1. Generate complete list of integers 1-209 coprime to 210: {1, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 127, 131, 137, 139, 143, 149, 151, 157, 163, 167, 169, 173, 179, 181, 191, 193, 197, 199, 209}
2. Extract all leading digits from Base-210 representation of primes (p > 210)
3. Verify: $\forall$ leading digit $d$, $d \in$ coprime set
4. Report: count of non-coprime digits found (expected: 0)

---

## Hypothesis 5: Primorial Adjustment Exceeds Uniform Baseline

### 1. Hypothesis Statement
The **information-theoretic improvement** provided by the primorial-adjusted Benford model over the uniform distribution, measured as the reduction in KL divergence, will be **greater than 50%** compared to the improvement provided by naive Benford.

### 2. Why It's Testable
This hypothesis is testable because:
- Information loss relative to uniform can be directly computed: $D_{uniform} = D_{KL}(P_{emp} || U)$
- Improvement metric is well-defined: $\Delta_{naive} = D_{uniform} - D_{naive}$ and $\Delta_{primorial} = D_{uniform} - D_{primorial}$
- Percentage comparison provides a normalized metric independent of sample size
- Clear threshold (50%) allows definitive acceptance/rejection

### 3. Experiment to Test It
1. Compute $D_{uniform} = D_{KL}(P_{emp} || U_{48})$ where $U_{48}(i) = 1/48$ for all digits
2. Compute relative improvements: $\text{Improvement}_{naive} = 1 - \frac{D_{naive}}{D_{uniform}}$ and $\text{Improvement}_{primorial} = 1 - \frac{D_{primorial}}{D_{uniform}}$
3. Test: $\text{Improvement}_{primorial} > 0.5$ (primorial captures >50% of deviation from uniform)
4. Compare: $\text{Improvement}_{primorial} > \text{Improvement}_{naive}$ (primorial outperforms naive)

---

## Summary Table

| Hypothesis | Key Comparison | Statistical Test | Expected Outcome |
|------------|----------------|------------------|------------------|
| H1 | KL divergence rankings | Bootstrap CI | $D_{primorial} < D_{naive}$ |
| H2 | Chi-squared goodness-of-fit | χ² test, p-value comparison | $p_{primorial} > p_{uniform}$ |
| H3 | Model conformance | χ² test (47 df) | Reject naive, fail to reject primorial |
| H4 | Data integrity | Set membership verification | 100% coprime coverage |
| H5 | Relative improvement | KL-based percentage metrics | >50% improvement, primorial > naive |