

# Testable Hypotheses for Higher-Order N-Gram Digit Sequencing in Prime Numbers

Based on the research problem and search context, I propose the following five testable hypotheses:

---

## Hypothesis 1: Internal N-Gram Frequency Deviation

**Statement:** The frequency distributions of 3-grams and 4-grams extracted from the internal digits of prime numbers will deviate significantly from those of matched composite control numbers in both Base-10 and Base-2, with effect sizes measurable via KL divergence exceeding 0.01.

**Why It's Testable:**
- This hypothesis generates specific, quantifiable predictions about measurable distributions
- KL divergence provides a continuous metric that can be compared against a defined threshold
- The comparison between primes and composites controls for general numerical properties
- Statistical significance can be evaluated using chi-square tests with Bonferroni correction

**Experiment Design:**
1. Generate 1 million prime numbers and 1 million composite controls matched by magnitude (1–10⁷)
2. Convert all numbers to both Base-10 and Base-2 representations
3. Strip terminal digits from each representation
4. Extract all overlapping 3-grams and 4-grams from internal digits
5. Compute frequency distributions for each group
6. Calculate KL divergence (primes vs. composites) for each base and n-gram length
7. Perform chi-square goodness-of-fit tests with α = 0.01
8. Generate comparative heatmaps showing over/under-represented sequences

---

## Hypothesis 2: Base-2 Amplified Bias Hypothesis

**Statement:** Base-2 representation of primes will exhibit statistically larger internal n-gram biases (higher KL divergence values and more significant chi-square statistics) compared to Base-10 representation, due to the deterministic bit-flipping constraints imposed by primality at binary boundaries.

**Why It's Testable:**
- This hypothesis makes a directional prediction (Base-2 > Base-10) that can be directly tested
- Both bases can be analyzed using identical methodology, enabling within-experiment comparison
- Effect size can be quantified as the ratio of KL divergences between bases
- The mechanistic rationale (bit-flipping constraints) provides a falsifiable causal explanation

**Experiment Design:**
1. Implement parallel extraction pipelines for Base-10 and Base-2 representations
2. Process identical prime and composite datasets through both pipelines
3. Compute KL divergence values for each base at n = 3, 4, and 5
4. Apply paired statistical tests (Wilcoxon signed-rank) to compare base-specific deviations
5. Visualize the base differential using paired bar charts or violin plots
6. Conduct subgroup analysis examining whether the bias concentrates in specific bit positions (LSB vs. MSB regions)

---

## Hypothesis 3: Suppressed Specific Sequence Hypothesis

**Statement:** Certain specific n-gram sequences—particularly those containing consecutive zeros in Base-2 or repeated even digits in Base-10—will appear at statistically suppressed rates (observed frequency < 75% of expected) within the internal digits of large primes compared to composite controls.

**Why It's Testable:**
- This hypothesis identifies particular sequences for targeted testing, not just overall distribution testing
- Suppression can be measured as a ratio of observed-to-expected frequencies
- The 75% threshold provides a clear binary decision criterion
- Multiple candidate sequences can be tested simultaneously with multiple comparisons correction

**Experiment Design:**
1. Define candidate suppressed sequences based on preliminary exploratory analysis:
   - Base-2: "000", "00100", "1111" patterns
   - Base-10: "00", "222", "666" (local digit constraints)
2. Count occurrences of each candidate sequence in prime and composite datasets
3. Compute observed-to-expected ratios for each sequence
4. Apply Benjamini-Hochberg correction for multiple comparisons
5. Flag sequences with corrected p-values < 0.01 and ratios < 0.75 as suppressed
6. Validate suppressed sequences by testing on held-out data (primes 10⁷–10⁸)

---

## Hypothesis 4: Magnitude-Dependent Bias Escalation Hypothesis

**Statement:** The magnitude of internal n-gram biases (measured by KL divergence from composite distributions) will increase monotonically as a function of prime magnitude, indicating that structural constraints accumulate over larger digit sequences.

**Why It's Testable:**
- This hypothesis predicts a specific functional relationship (monotonic increase) that can be empirically verified
- Magnitude brackets provide natural experimental conditions for comparison
- Linear regression or Spearman correlation can quantify the trend
- The prediction is falsifiable: if bias decreases or remains constant, the hypothesis is rejected

**Experiment Design:**
1. Stratify prime/composite datasets into magnitude brackets: 10⁴–10⁵, 10⁵–10⁶, 10⁶–10⁷
2. Compute n-gram distributions (3-grams and 4-grams) within each bracket
3. Calculate KL divergence for each bracket independently
4. Fit linear regression models: KL_divergence ~ log(magnitude)
5. Test for significant positive slope (β > 0) using t-tests
6. Verify monotonicity using Jonckheere-Terpstra trend test
7. Generate log-scale scatter plots with regression lines

---

## Hypothesis 5: N-Gram Order Complexity Threshold Hypothesis

**Statement:** Internal n-gram bias effects will exhibit a non-linear threshold behavior, being statistically detectable at n = 3 and n = 4 but becoming attenuated or undetectable at n = 5 due to the exponential reduction in sample size per unique sequence at higher orders.

**Why It's Testable:**
- This hypothesis makes a specific prediction about the n-gram length parameter
- The threshold effect can be directly measured by comparing effect sizes across n = 3, 4, 5
- Sample size requirements at each order can be calculated a priori
- The hypothesis is falsifiable: if biases persist at n = 5, the threshold prediction fails

**Experiment Design:**
1. Calculate required sample sizes for adequate power at each n-gram level (using pilot data)
2. Generate sufficient prime/composite data to achieve power > 0.80 for detecting medium effect sizes (Cohen's d = 0.3)
3. Extract n-grams for n = 3, 4, and 5 from internal digits
4. Compute chi-square statistics and effect sizes (Cramér's V) at each level
5. Compare effect sizes using repeated-measures ANOVA or Friedman tests
6. Identify threshold n where effect size drops below detection limit
7. Bootstrap confidence intervals around threshold estimate

---

## Summary Table

| Hypothesis | Independent Variable | Dependent Variable | Comparison Condition |
|------------|---------------------|-------------------|---------------------|
| H1 | Prime vs. Composite | N-gram distribution (KL div.) | Internal digits only |
| H2 | Numerical base (2 vs. 10) | Bias magnitude | Same prime dataset |
| H3 | Sequence type | Suppression ratio | vs. expected frequency |
| H4 | Prime magnitude | KL divergence | Across bracket ranges |
| H5 | N-gram order (3, 4, 5) | Effect size | Within same dataset |