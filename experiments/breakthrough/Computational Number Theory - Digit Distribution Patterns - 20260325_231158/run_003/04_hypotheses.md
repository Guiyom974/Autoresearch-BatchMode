

# Testable Hypotheses for Positional N-Gram Patterns and Inter-Prime Gap Digit Sequences

Based on the research problem and search context, I propose the following five testable hypotheses:

---

## Hypothesis 1: Inter-Prime Gap N-grams Show Greater KL Divergence from Composite Gaps in Base-16 than in Base-10

### 1. Hypothesis Statement
The digit n-gram distributions of inter-prime gaps in Base-16 will exhibit a larger KL divergence from composite gap n-grams compared to the same comparison in Base-10, with the Base-16 divergence exceeding 0.05 while Base-10 divergence remains below this threshold.

### 2. Why It's Testable
This hypothesis is testable because:
- Both Base-10 and Base-16 representations can be directly computed from the same set of prime gaps
- KL divergence is a well-defined, symmetric statistical measure that can be computed for discrete distributions
- The hypothesis makes a specific directional prediction (Base-16 > Base-10) that can be falsified
- The magnitude threshold (0.05) provides an objective criterion for success

### 3. Experiment Design
1. Generate primes up to N = 10^7 and compute all inter-prime gaps
2. Generate a matched control set of pseudo-random odd composite numbers with similar distribution properties
3. Convert both prime gaps and composite gaps to Base-10 and Base-16 string representations
4. Extract n-grams of length 2 and 3 from each representation
5. Compute KL divergence between prime gap n-gram distributions and composite gap n-gram distributions for both bases
6. Compare the resulting KL divergence values with statistical significance testing (bootstrap confidence intervals)

---

## Hypothesis 2: Prefix N-grams of Prime Numbers Exhibit Statistically Distinct Biases from Internal N-grams After Benford's Law Normalization

### 1. Hypothesis Statement
When normalized for leading-digit distributions (Benford's Law), the n-gram frequency distributions of the first three digits (prefix) of prime numbers will differ significantly from the n-gram distributions of the middle three digits (internal), as measured by a KL divergence greater than 0.01 and chi-square p-value less than 0.01.

### 2. Why It's Testable
This hypothesis is testable because:
- The distinction between "prefix" and "internal" positions is well-defined operationally
- Benford's Law provides a known baseline for normalizing leading digit distributions
- Statistical tests (KL divergence, chi-square) can directly compare discrete distributions
- The hypothesis controls for an established phenomenon, isolating positional effects

### 3. Experiment Design
1. Generate primes up to N = 10^7 in Base-10 representation
2. Extract fixed-length n-grams (n=2,3) from:
   - The first three digit positions (prefix)
   - The middle three digit positions (internal)
3. Apply Benford's Law normalization to prefix n-grams
4. Compute KL divergence between normalized prefix distributions and internal n-gram distributions
5. Conduct chi-square goodness-of-fit tests to assess statistical significance
6. Repeat the analysis in Base-16 for comparative purposes

---

## Hypothesis 3: Specific Repeating N-gram Patterns Within Prime Gaps Occur at Frequencies Significantly Different from Composite Gaps

### 1. Hypothesis Statement
Certain repeating n-gram patterns within inter-prime gap sequences—specifically "00" and "FF" (hexadecimal) or "00" and "50" (decimal)—will appear at frequencies that deviate significantly from their expected frequencies in composite gap sequences, with standardized residuals exceeding ±2 in chi-square analysis.

### 2. Why It's Testable
This hypothesis is testable because:
- It identifies specific, observable patterns that can be counted directly
- Chi-square analysis with standardized residuals provides a clear statistical criterion
- The threshold (±2 standardized residual) is a conventional threshold for identifying outliers
- The comparison is against a well-defined control (composite gaps)

### 3. Experiment Design
1. Generate primes up to N = 10^7 and compute inter-prime gaps
2. Generate matched composite gap sequences
3. Convert all gaps to Base-10 and Base-16
4. Count occurrences of target n-grams ("00", "FF", "50") in each dataset
5. Calculate expected frequencies under the null hypothesis (composite distribution)
6. Compute chi-square standardized residuals for each pattern
7. Identify patterns with residuals exceeding ±2 as significant deviations

---

## Hypothesis 4: The Observed Deviation Between Prime and Composite Gap N-gram Distributions Will Scale Consistently Across Multiple Prime Ranges

### 1. Hypothesis Statement
The KL divergence between prime gap n-gram distributions and composite gap n-gram distributions will remain consistent (within 20% relative variation) when measured across distinct, contiguous subsets of the prime dataset—specifically in the ranges 10^5–10^6, 10^6–10^7, and 10^7–10^8 (if computationally feasible).

### 2. Why It's Testable
This hypothesis is testable because:
- The prime dataset can be divided into contiguous, non-overlapping ranges
- Consistency is objectively measurable through relative variation calculations
- The hypothesis addresses reproducibility, a key scientific criterion
- The specific ranges are computationally feasible with the proposed N = 10^7 limit

### 3. Experiment Design
1. Partition the generated prime dataset into contiguous ranges:
   - Range 1: 10^5 to 10^6
   - Range 2: 10^6 to 10^7
   - (Optional) Range 3: 10^7 to 10^8 if computational resources allow
2. For each range, compute inter-prime gaps
3. Generate matched composite gap sequences for each range
4. Extract n-grams (n=2,3) from gaps in each range
5. Compute KL divergence between prime and composite distributions for each range
6. Calculate the relative variation (standard deviation / mean) of KL divergence values across ranges
7. Accept hypothesis if relative variation is less than 20%

---

## Hypothesis 5: Base Conversion Artifacts Will Not Account for the Observed Prime Gap N-gram Biases

### 1. Hypothesis Statement
The statistically significant deviations observed in prime gap n-gram distributions (relative to composite gaps) will persist after filtering for trivial modular arithmetic constraints and base-specific artifacts, demonstrating that the biases are inherent to the prime distribution rather than induced by representation artifacts.

### 2. Why It's Testable
This hypothesis is testable because:
- It explicitly defines what must be filtered: modular constraints (e.g., primes ending in 2, 4, 5, 6, 8, 0 in Base-10) and base conversion artifacts
- The filtering criteria are clearly specified and implementable
- The persistence of deviation after filtering is a binary (yes/no) outcome
- This addresses the "non-trivial discovery" success criterion from the research problem

### 3. Experiment Design
1. After establishing significant KL divergence in Hypotheses 1-3, apply explicit filters:
   - Remove gaps where the last digit is constrained by modular arithmetic (e.g., gaps ending in even digits in Base-10 are impossible for odd prime gaps)
   - Remove n-grams containing digits that are artifacts of base conversion (e.g., leading zeros in Base-16 representations)
2. Recompute KL divergence and statistical significance after each filtering step
3. Document the reduction in sample size and divergence magnitude at each stage
4. Accept hypothesis only if KL divergence remains > 0.01 and p-value < 0.05 after all filters are applied
5. Conduct a sensitivity analysis to determine which constraints have the greatest impact on the results

---

## Summary Table

| Hypothesis | Primary Focus | Key Measure | Success Threshold |
|------------|---------------|-------------|-------------------|
| 1 | Base-16 vs Base-10 | KL divergence ratio | Base-16 > 0.05, Base-10 < 0.05 |
| 2 | Positional bias | KL divergence (prefix vs internal) | > 0.01, p < 0.01 |
| 3 | Specific patterns | Chi-square standardized residuals | > ±2 for target patterns |
| 4 | Reproducibility | Relative variation in KL divergence | < 20% across ranges |
| 5 | Non-triviality | KL divergence after filtering | > 0.01, p < 0.05 |

These hypotheses collectively address the three research questions while adhering to the computational constraints (n ≤ 4) and the domain-specific requirements outlined in the research problem.