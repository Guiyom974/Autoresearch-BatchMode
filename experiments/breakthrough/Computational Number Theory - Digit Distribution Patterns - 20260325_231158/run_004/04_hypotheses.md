

# Testable Hypotheses for Positional N-Gram Biases in Prime Number Digit Distributions

Based on the research problem and search context, I propose the following 5 testable hypotheses that address the core research questions while being grounded in the described methodology.

---

## Hypothesis 1: Structural Primorial Advantage

**Statement:** Primorial bases (Base-6, Base-30) will exhibit significantly higher KL divergence in prefix n-gram distributions compared to power-of-two bases of equivalent or greater magnitude (Base-8, Base-32), indicating that structural properties of bases introduce stronger prime/composite digit biases than base size alone.

**Why it's testable:**
This hypothesis generates a clear, directional prediction that can be directly measured using the described methodology. By computing KL divergence values for prefix n-grams across Base-6, Base-8, Base-30, and Base-32, we can compare whether the primorial bases produce divergence values that exceed those of the power-of-two bases, regardless of base magnitude ordering.

**Experiment design:**
1. Generate all primes and a representative composite sample up to N = 1,000,000
2. Convert both sets to Base-6, Base-8, Base-30, and Base-32
3. Extract 2-gram and 3-gram prefix sequences from each representation
4. Apply Laplace smoothing (α = 1) to all probability distributions
5. Compute KL(Prime || Composite) divergence for each base and n-gram length
6. Statistically compare divergence values using paired t-tests or Mann-Whitney U tests to determine if primorial bases consistently outperform power-of-two bases in divergence magnitude

---

## Hypothesis 2: Positional Decay of Information Content

**Statement:** The KL divergence between prime and composite n-gram distributions will exhibit a significant decay curve as the n-gram window progresses from prefix (most significant digits) through internal positions to suffix (least significant digits), reflecting decreasing information content about primality in less significant digit positions.

**Why it's testable:**
This hypothesis proposes a quantitative relationship between digit position and divergence magnitude. The methodology explicitly defines extraction procedures for prefix, internal, and suffix n-grams, enabling systematic comparison across positional categories. The decay pattern can be tested by comparing mean KL divergence values across these three positional categories.

**Experiment design:**
1. Implement the three positional n-gram extraction methods: prefix (first n digits), internal (sliding window excluding first/last n positions), and suffix (last n digits)
2. For each base (Base-6, Base-8, Base-30, Base-32), compute KL divergence for each positional category
3. Perform one-way ANOVA or Kruskal-Wallis tests to determine if positional category significantly affects divergence magnitude
4. If significant, apply post-hoc pairwise comparisons to quantify the decay rate between prefix-internal, internal-suffix, and prefix-suffix pairs
5. Fit exponential or logarithmic decay models to characterize the rate of information loss across positions

---

## Hypothesis 3: Non-Trivial Suffix Divergence in Composite Bases

**Statement:** After mathematically accounting for and removing trivial divisibility-rule constraints (e.g., eliminating even digits and 5-ending digits in Base-10), the suffix n-gram KL divergence of primes in highly composite bases (Base-30) will remain significantly positive, indicating the existence of non-obvious sequential dependencies in prime endings beyond basic divisibility rules.

**Why it's testable:**
This hypothesis addresses the constraint to avoid triviality by proposing that meaningful divergence persists even after filtering obvious patterns. By explicitly modeling and removing digit categories that violate primality (e.g., digits divisible by base factors), we can test whether residual divergence exists in the remaining suffix patterns.

**Experiment design:**
1. For each base, identify digit values that are trivially incompatible with primality (e.g., in Base-30, any digit divisible by 2, 3, or 5)
2. Filter composite n-grams containing these trivially-excluded digits from both prime and composite distributions
3. Recompute suffix n-gram distributions for both sets using only "potentially prime" suffixes
4. Apply Laplace smoothing to the filtered distributions
5. Compute KL divergence on the filtered distributions
6. Compare the filtered divergence to the unfiltered divergence to quantify the proportion of divergence attributable to non-trivial patterns

---

## Hypothesis 4: Magnitude-Driven Scaling in Power-of-Two Bases

**Statement:** Among power-of-two bases (Base-8, Base-16, Base-32), the KL divergence for prefix n-grams will scale approximately linearly or log-linearly with the logarithm of base magnitude, supporting a pure magnitude-driven hypothesis where larger bases encode more discriminative information about primality in their most significant digits.

**Why it's testable:**
This hypothesis generates a quantitative prediction about the relationship between base size and divergence magnitude specifically for power-of-two bases. By testing multiple bases in this family, we can determine whether divergence increases monotonically with base magnitude in a predictable mathematical relationship.

**Experiment design:**
1. Extend the base set to include Base-2, Base-4, Base-8, Base-16, and Base-32 (or a subset within computational limits)
2. Compute prefix n-gram KL divergence for each base at consistent n-gram lengths (n=2, n=3)
3. Plot KL divergence against log₂(base) or base magnitude
4. Fit linear regression and log-linear regression models to the data
5. Calculate R² values to determine which scaling model best explains the relationship
6. Compare the fitted models against the primorial base data to determine if primorial bases deviate systematically from the power-of-two scaling law

---

## Hypothesis 5: Internal Digit Convergence Hypothesis

**Statement:** Internal n-gram distributions (non-prefix, non-suffix positions) will show minimal KL divergence between primes and composites, approaching zero as the internal position index increases, indicating that intermediate digits behave nearly randomly with respect to primality classification.

**Why it's testable:**
This hypothesis makes a directional prediction about internal positions having low divergence that can be empirically tested. The methodology explicitly defines internal n-gram extraction using sliding windows, enabling systematic testing of how divergence changes as we move away from the most and least significant digit positions.

**Experiment design:**
1. For each base, define internal position indices (P = 2, 3, 4, ... up to the maximum internal position)
2. Extract n-grams anchored at each internal position for both prime and composite sets
3. Compute KL divergence for each internal position separately
4. Create a position-divergence plot showing divergence magnitude as a function of internal position index
5. Perform statistical tests (t-test or bootstrap confidence intervals) to determine whether internal divergence values are significantly different from zero
6. Apply curve fitting to determine if internal divergence follows a predictable decay function (exponential, inverse, logarithmic) toward the baseline

---

## Summary Table

| Hypothesis | Independent Variable | Dependent Variable | Predicted Direction |
|------------|---------------------|---------------------|---------------------|
| 1: Structural Primorial | Base type (primorial vs. power-of-2) | KL divergence (prefix) | Primorial > Power-of-2 |
| 2: Positional Decay | N-gram position (prefix → suffix) | KL divergence | Decreasing |
| 3: Non-Trivial Suffix | Filtering of trivial patterns | KL divergence (suffix) | Remaining divergence > 0 |
| 4: Magnitude Scaling | Base magnitude (power-of-2 family) | KL divergence (prefix) | Positive correlation |
| 5: Internal Convergence | Internal position index | KL divergence | Approaching zero |

These hypotheses collectively address the three core research questions while generating specific, falsifiable predictions that can be tested using the described experimental methodology.