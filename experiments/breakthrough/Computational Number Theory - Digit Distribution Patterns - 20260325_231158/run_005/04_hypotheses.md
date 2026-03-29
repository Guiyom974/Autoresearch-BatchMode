

# Testable Hypotheses: Prefix N-Gram Biases in High-Order Primorial Bases

---

## Hypothesis 1: Non-Uniform Leading Digit Distribution in High-Order Primorial Bases

**1. Hypothesis Statement:**
Prime numbers represented in Base-210 and Base-2310 exhibit statistically significant deviations from uniform distributions in their leading 1-digit, 2-digit, and 3-digit prefixes, as measured by Chi-Squared goodness-of-fit tests (p < 0.01).

**2. Why It's Testable:**
This hypothesis makes a specific, quantitative prediction: the observed frequency distribution of leading digit sequences will deviate from the expected uniform distribution by more than chance alone. The prediction is falsifiable because we can compute the exact probability distribution expected under the null hypothesis of uniformity, count the actual observed frequencies, and calculate a test statistic. The large sample size (primes up to 10-50 million) ensures sufficient statistical power to detect medium-sized effects.

**3. Experiment Design:**
- Generate a dataset of primes up to 50 million using a segmented sieve algorithm
- Convert each prime to both Base-210 and Base-2310 representations
- For each base, extract the leading k digits where k ∈ {1, 2, 3}
- Count the frequency of each valid leading sequence
- Compute expected frequencies assuming uniform distribution
- Apply Chi-Squared goodness-of-fit test and record p-values
- Reject the null hypothesis if p < 0.01 for at least one prefix length in either base

---

## Hypothesis 2: Terminal-Prefix Mutual Information Dependency

**1. Hypothesis Statement:**
In Base-210 and Base-2310, the mutual information between the leading digit (prefix) and the terminal digit (last digit) of prime numbers will be significantly greater than zero, indicating measurable long-range positional dependency induced by the terminal digit constraint.

**2. Why It's Testable:**
Mutual Information (MI) is a non-negative information-theoretic measure where MI = 0 if and only if two random variables are statistically independent. We can empirically estimate the joint probability distribution P(prefix, terminal) and marginal distributions P(prefix) and P(terminal) from the data, then compute MI = Σ P(prefix, terminal) × log[P(prefix, terminal) / (P(prefix) × P(terminal))]. If the constraint on terminal digits creates exploitable structure linking to leading digits, MI will be positive and significantly different from bootstrapped MI values computed on shuffled data.

**3. Experiment Design:**
- Convert primes to Base-210 and Base-2310
- For each prime, record a tuple: (leading_digit, terminal_digit)
- Construct a contingency table of joint frequencies
- Compute empirical mutual information using the contingency table
- Generate a null distribution by: (a) shuffling terminal digits independently, (b) computing MI for 1,000 shuffled versions
- Calculate the z-score: (observed_MI - mean_shuffled_MI) / std_shuffled_MI
- Reject independence if z-score > 2.58 (one-tailed test, α = 0.01)

---

## Hypothesis 3: Monotonic Scaling of Prefix Bias with Primorial Order

**1. Hypothesis Statement:**
The magnitude of prefix n-gram bias, as quantified by normalized Chi-Squared statistics (χ²/n) or effect size measures, increases monotonically as the primorial base order increases from Base-30 through Base-210 to Base-2310. That is: Bias(Base-30) < Bias(Base-210) < Bias(Base-2310).

**2. Why It's Testable:**
This is a directional prediction about the relationship between base complexity and bias magnitude. We can operationalize "bias magnitude" using standardized effect size statistics that are comparable across bases with different alphabet sizes (e.g., Cramér's V for chi-squared tests, or normalized MI). The monotonic ordering can be tested directly by computing these statistics for each base and verifying the inequality holds. The prediction is falsifiable if any reversal in the ordering is observed.

**3. Experiment Design:**
- Implement identical prime generation and conversion pipelines for Base-30, Base-210, and Base-2310
- For each base, extract leading 2-digit prefixes (to ensure sufficient sample per cell for valid chi-squared)
- Compute Chi-Squared statistics for each base
- Calculate Cramér's V = √(χ² / (n × min(r-1, c-1))) where r and c are the dimensions of the contingency table
- Compare Cramér's V values across bases
- Test for statistical significance of differences using bootstrap resampling (10,000 iterations) to generate confidence intervals for each V estimate
- Accept hypothesis if the 95% CI for V(Base-2310) does not overlap with V(Base-30) and the ordering is preserved

---

## Hypothesis 4: Primorial-Specific Versus Generic Base-Effect Distinction

**1. Hypothesis Statement:**
The observed prefix biases in Base-210 and Base-2310 will be significantly larger than those observed in power-of-two bases of comparable or larger alphabet size (Base-256, Base-512), demonstrating that the effect is uniquely attributable to the primorial structure rather than being a generic artifact of large base alphabets.

**2. Why It's Testable:**
This hypothesis makes a comparative prediction that allows us to control for confounding variables. Power-of-two bases (Base-256, Base-512) have large alphabets similar to primorial bases but lack the multiplicative prime structure. If the bias is caused specifically by the primorial construction (which restricts terminal digits to residues coprime to the base), we should observe it in Base-210/2310 but not in Base-256/512. This control condition directly tests the theoretical mechanism proposed in the research problem.

**3. Experiment Design:**
- Convert the same prime dataset to Base-210, Base-2310, Base-256, and Base-512
- For each base, extract leading 1-digit and 2-digit prefixes
- Perform Chi-Squared goodness-of-fit tests for each base/prefix-length combination
- Compute effect sizes (Cramér's V or Cohen's w) for all tests
- Conduct pairwise comparisons: 
  - V(Base-210) vs. V(Base-256)
  - V(Base-2310) vs. V(Base-512)
- Use Fisher's z-transformation to test for significant differences between effect sizes
- Hypothesis supported if both primorial bases show significantly larger effect sizes (p < 0.01) than their power-of-two counterparts

---

## Hypothesis 5: Information Theoretic Asymmetry in Digit-to-Digit Dependencies

**1. Hypothesis Statement:**
In high-order primorial bases, the conditional entropy H(terminal | prefix) will be lower than H(prefix | terminal), indicating that the leading digit carries more predictive information about the terminal digit than vice versa. This asymmetry arises because the primorial structure creates a constraint propagation from the most significant to least significant digit positions.

**2. Why It's Testable:**
Entropy and conditional entropy are well-defined information-theoretic quantities that can be estimated from empirical distributions. We can directly compute H(terminal | prefix) = -Σ P(prefix, terminal) × log[P(terminal | prefix)] and H(prefix | terminal) = -Σ P(prefix, terminal) × log[P(prefix | terminal)]. The asymmetry prediction can be tested by calculating both quantities and comparing them. The hypothesis is falsifiable if the observed asymmetry is in the opposite direction or not statistically distinguishable from zero.

**3. Experiment Design:**
- Convert primes to Base-210 and Base-2310
- Build the joint probability distribution P(prefix, terminal) from the data
- Compute the full entropy decomposition:
  - H(prefix, terminal) = -Σ P(joint) × log₂ P(joint)
  - H(prefix) = -Σ P(prefix) × log₂ P(prefix)
  - H(terminal) = -Σ P(terminal) × log₂ P(terminal)
  - H(terminal | prefix) = H(prefix, terminal) - H(prefix)
  - H(prefix | terminal) = H(prefix, terminal) - H(terminal)
- Calculate asymmetry index: D = H(prefix | terminal) - H(terminal | prefix)
- Generate null distribution for D via bootstrap: recompute D for 1,000 samples of equal size drawn with replacement
- Reject D = 0 if the observed D falls outside the 99% confidence interval of the bootstrap distribution
- Confirm direction: accept if D > 0 (prefix more informative about terminal than reverse)