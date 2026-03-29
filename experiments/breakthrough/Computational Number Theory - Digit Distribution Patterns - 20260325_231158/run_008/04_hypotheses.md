

# Testable Hypotheses for Primorial-Adjusted Benford Model Validation

---

## Hypothesis 1: Primorial-Adjusted Model Reduces KL Divergence

### 1. Hypothesis Statement
The primorial-adjusted Benford model will produce a significantly lower Kullback-Leibler (KL) divergence when compared to empirical prime leading digit distributions in Base-210 than the naive Benford model, reducing the observed KL divergence from 0.636 toward a value consistent with random statistical fluctuation (< 0.05).

### 2. Why It's Testable
- KL divergence is a directly computable metric that quantifies the difference between two probability distributions
- We can compute both the naive and adjusted KL divergences using the same empirical data
- Statistical significance can be assessed by comparing KL values against null distributions generated via bootstrapping or Monte Carlo simulation
- The hypothesis is falsifiable: if KL divergence remains > 0.1, the hypothesis is rejected

### 3. Experiment Design
```
Experiment Protocol:
1. Generate all primes ≤ 10^8 using Sieve of Eratosthenes (optimized)
2. Convert each prime to Base-210 representation
3. Extract leading digits, confirming all fall within 48 coprime set
4. Compute empirical distribution P_emp(d) for each coprime digit
5. Calculate KL(P_emp || P_naive) and KL(P_emp || P_adjusted)
6. Generate 1000 bootstrap samples to establish null distribution
7. Perform paired t-test comparing the two KL divergences
8. Reject if adjusted KL is not significantly lower (p < 0.05)
```

---

## Hypothesis 2: Residual Anomalies Persist in Specific Digits

### 1. Hypothesis Statement
After applying the primorial adjustment, at least 3 of the 48 coprime leading digits in Base-210 will exhibit statistically significant residual deviations (|residual| > 1.96σ) from the theoretical primorial-adjusted Benford distribution when tested against primes up to 10^8.

### 2. Why It's Testable
- The research explicitly identifies localized bias as a concern
- Residual analysis is a standard statistical procedure
- Confidence intervals can be computed for each digit's expected frequency under the null model
- The threshold (3 digits) provides a clear rejection criterion based on binomial expectations under null hypothesis

### 3. Experiment Design
```
Experiment Protocol:
1. Compute expected probabilities P_adj(d) for each of 48 coprime digits
2. For each digit d, calculate:
   - Expected count: E[d] = n × P_adj(d)
   - Observed count: O[d]
   - Residual: R[d] = (O[d] - E[d]) / √E[d]
   - Standardized residual: Z[d] = R[d] × √(1 - P_adj(d))
3. Identify digits where |Z[d]| > 1.96 (95% CI) or |Z[d]| > 2.58 (99% CI)
4. Count persistent anomalies across 10 independent subsamples
5. Apply Bonferroni correction for multiple comparisons
6. Document which specific digits (e.g., 11, 13, 17) show systematic bias
```

---

## Hypothesis 3: Asymptotic Convergence to Primorial-Adjusted Model

### 1. Hypothesis Statement
The KL divergence between the empirical leading digit distribution of primes and the primorial-adjusted Benford model will decrease monotonically as the upper bound increases from 10^6 to 10^8, demonstrating asymptotic convergence at a rate consistent with O(1/log N).

### 2. Why It's Testable
- We can compute empirical distributions at multiple thresholds (10^6, 5×10^6, 10^7, 5×10^7, 10^8)
- Convergence rate can be quantified by regressing KL divergence against log(N)
- The hypothesis is directional (monotonic decrease) and falsifiable
- Sample size increases with bound, reducing variance in estimates

### 3. Experiment Design
```
Experiment Protocol:
1. Generate primes at thresholds: N = [10^6, 2×10^6, 5×10^6, 10^7, 2×10^7, 5×10^7, 10^8]
2. At each threshold:
   - Extract leading digits in Base-210
   - Compute empirical distribution P_emp(N, d)
   - Calculate KL(P_emp(N) || P_adj)
3. Plot KL divergence vs. log(N)
4. Fit regression: KL(N) = a + b/log(N) + ε
5. Test H0: b ≥ 0 vs. H1: b < 0 (one-sided t-test)
6. Compare convergence rate to theoretical prediction
7. Optional: Test if naive Benford model shows worse convergence
```

---

## Hypothesis 4: Digit "1" Specifically Conforms to Theoretical Prediction

### 1. Hypothesis Statement
The leading digit d=1 will appear at a frequency of 0.4675 ± 0.005 (1σ) in the empirical distribution of primes up to 10^8 in Base-210, which is significantly higher than the naive Benford prediction for d=1 (~0.301) and explains a substantial portion of the original KL divergence.

### 2. Why It's Testable
- The theoretical value (0.4675) is explicitly specified in the problem
- We can directly count occurrences of leading digit "1" and compute observed proportion
- Standard error can be computed as √(p(1-p)/n)
- Hypothesis is directional and falsifiable

### 3. Experiment Design
```
Experiment Protocol:
1. Generate all primes ≤ 10^8
2. Convert to Base-210, count leading digit = 1
3. Compute observed proportion: p̂ = count(1) / total_primes
4. Calculate standard error: SE = √(0.4675 × 0.5325 / n)
5. Compute z-statistic: z = (p̂ - 0.4675) / SE
6. Test H0: p̂ = 0.301 (naive Benford) vs. H1: p̂ ≠ 0.301
7. Test H0: p̂ = 0.4675 vs. H1: p̂ ≠ 0.4675
8. Calculate proportion of KL divergence explained by d=1 alone:
   KL_1 ≈ P_emp(1) × ln(P_emp(1)/0.4675)
```

---

## Hypothesis 5: Chi-Squared Test Fails to Reject Primorial-Adjusted Model

### 1. Hypothesis Statement
The Chi-squared goodness-of-fit test will fail to reject the primorial-adjusted Benford model at the α = 0.05 significance level when applied to prime leading digits in Base-210 up to 10^8, yielding p-value > 0.05, whereas the naive Benford model will be decisively rejected (p-value < 10^-6).

### 2. Why It's Testable
- Chi-squared test is a standard goodness-of-fit procedure
- Degrees of freedom = 48 - 1 = 47 (after parameter estimation)
- Clear binary outcome: reject or fail to reject
- Comparison between models is straightforward

### 3. Experiment Design
```
Experiment Protocol:
1. Compute observed frequencies O[i] for i = 1 to 48 coprime digits
2. Compute expected frequencies E_naive[i] = n × P_naive(i)
3. Compute expected frequencies E_adj[i] = n × P_adj(i)
4. Calculate Chi-squared statistic for naive model:
   χ²_naive = Σ (O[i] - E_naive[i])² / E_naive[i]
5. Calculate Chi-squared statistic for adjusted model:
   χ²_adj = Σ (O[i] - E_adj[i])² / E_adj[i]
6. Compare p-values from χ² distribution with df=47
7. Perform power analysis to ensure n=10^8 provides adequate power
   (power > 0.80 for detecting effect size ω = 0.1)
8. Document whether adjusted model passes goodness-of-fit threshold
```

---

## Summary Table

| Hypothesis | Primary Metric | Null Hypothesis | Test Statistic |
|------------|----------------|-----------------|----------------|
| H1: KL Reduction | KL divergence | ΔKL ≤ 0 | Paired t-test |
| H2: Residual Anomalies | |Z| values | # anomalies ≥ 3 |
| H3: Convergence | KL(N) vs. log(N) | b ≥ 0 | One-sided regression |
| H4: Digit "1" Value | Proportion of d=1 | p̂ ≠ 0.4675 | z-test |
| H5: Chi-Squared Pass | p-value | p ≤ 0.05 | χ² test |

These hypotheses collectively provide comprehensive coverage of the research questions while maintaining testability, falsifiability, and clear experimental protocols.