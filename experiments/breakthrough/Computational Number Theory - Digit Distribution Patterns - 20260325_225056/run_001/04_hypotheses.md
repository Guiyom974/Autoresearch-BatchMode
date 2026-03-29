

# Testable Hypotheses for Prime Number Digit Distribution Research

---

## Hypothesis 1: Within-Prime Adjacent Digit Transition Bias

**Statement:** The transition probabilities between adjacent digits *within* a single prime number (e.g., the probability that digit "7" is followed by digit "3" within the same prime's decimal representation) will deviate significantly from the uniform distribution expected in random odd numbers not divisible by 2 or 5.

**Why it's testable:**
- The methodology explicitly includes "Markov Chain Analysis" building a 10×10 transition matrix for adjacent digits within primes
- We can generate random odd numbers as a baseline comparison
- Chi-square tests can quantify deviation from uniform expectations

**Experiment:**
1. Generate primes up to 10⁷ using Sieve of Eratosthenes
2. For each prime, extract all consecutive digit pairs (e.g., for p=1373: pairs are (1,3), (3,7), (7,3))
3. Build an empirical transition matrix counting all observed digit pair frequencies
4. Generate equivalent number of random odd numbers (not divisible by 2 or 5) and build their transition matrix
5. Perform χ² test comparing observed vs. expected uniform counts
6. Visualize deviations as a heatmap

---

## Hypothesis 2: Middle Digit Non-Uniformity in Hexadecimal Representation

**Statement:** When prime numbers are expressed in Base-16, certain hex digits (0-9, A-F) are over- or under-represented in *non-terminal positions* (i.e., excluding the final digit) compared to a uniform baseline derived from random odd numbers of similar magnitude.

**Why it's testable:**
- The research explicitly mentions sampling up to x = 10⁷ in Base-16
- Terminal digits are constrained by modular arithmetic, but middle digits should be "free"
- We can isolate the middle position analysis using string slicing

**Experiment:**
1. Generate primes up to 10⁷
2. Convert each prime to hexadecimal string representation
3. For primes with length ≥ 3 digits, extract all "middle" digits (positions 1 to length-2)
4. Count frequency of each hex digit (0-F) across all middle positions
5. Compute expected frequencies assuming uniform distribution
6. Apply χ² goodness-of-fit test
7. Control for length bias by stratifying analysis by prime magnitude (10⁴, 10⁵, 10⁶, 10⁷)

---

## Hypothesis 3: Cross-Base Correlated Biases in Terminal Digits

**Statement:** The terminal digit bias observed between consecutive primes in Base-10 (where primes "hate" to repeat final digits) will exhibit *different structural patterns* when analyzed in Base-16, indicating that the bias is not merely an artifact of digit representation but reflects deeper properties of prime gap distributions.

**Why it's testable:**
- The search results confirm the Base-10 anti-repetition bias is well-documented
- The problem explicitly asks for cross-base analysis
- Comparing the same phenomenon across bases can reveal representation-independent properties

**Experiment:**
1. Generate primes up to 10⁷
2. For each prime pair (pₙ, pₙ₊₁), record terminal digits in both Base-10 and Base-16
3. Build 4×4 transition matrices for Base-10 and 16×16 matrices for Base-16
4. Compare transition probability matrices using a distance metric (e.g., Frobenius norm)
5. Test whether the Base-16 "anti-repetition" effect is stronger, weaker, or qualitatively different from Base-10
6. Run permutation tests to assess statistical significance of cross-base differences

---

## Hypothesis 4: Digit Sum Distribution Acceleration Toward Normality

**Statement:** The sum of digits of prime numbers (in Base-10) converges to a normal distribution *faster* than predicted by standard central limit theorem asymptotics, with statistically detectable deviations from normality at sample sizes as small as n = 10⁴.

**Why it's testable:**
- The research problem explicitly asks about "digit sum biases" and convergence rates
- Digit sums of uniformly distributed random numbers in [1, N] follow predictable distributions
- We can test for normality using Shapiro-Wilk or Anderson-Darling tests at multiple sample sizes

**Experiment:**
1. Generate primes up to 10⁷
2. For each prime, compute its digit sum (e.g., 1373 → 1+3+7+3 = 14)
3. Create samples of digit sums at increasing sample sizes (10³, 10⁴, 10⁵, 10⁶, 10⁷)
4. For each sample, compute mean, variance, skewness, and kurtosis
5. Compare against theoretical moments for uniform random numbers of similar magnitude
6. Apply Shapiro-Wilk normality tests and compare p-values across sample sizes
7. Quantify convergence rate and identify at what scale size deviations disappear

---

## Hypothesis 5: Position-Dependent Digit Preference in Prime Representations

**Statement:** In Base-10 prime representations, certain digits exhibit statistically significant position-dependent preferences (e.g., digit "0" appears less frequently in the second-to-last position than expected, while digit "9" appears more frequently in leading positions).

**Why it's testable:**
- This extends beyond simple terminal digit analysis to positional preferences
- The effect can be isolated by conditioning on digit position
- Multiple comparison corrections (Bonferroni, FDR) can control for false positives

**Experiment:**
1. Generate primes up to 10⁷
2. For each prime converted to string, record the position of each digit (0-indexed from left)
3. Bin primes by total digit length (1-digit, 2-digit, 3-digit, etc.)
4. For each position index j, construct contingency tables of observed digit frequencies
5. Compute expected frequencies under independence assumption
6. Apply χ² tests with Bonferroni correction for multiple comparisons
7. Identify specific position-digit pairs with significant deviations (p < 0.01 after correction)

---

## Summary Table

| Hypothesis | Key Variable | Baseline Comparison | Statistical Test | Expected Outcome |
|------------|--------------|---------------------|------------------|------------------|
| H1 | Within-prime digit transitions | Random odd numbers | χ² test | Non-uniform transition matrix |
| H2 | Middle hex digits | Uniform distribution | χ² goodness-of-fit | Over/under-represented hex digits |
| H3 | Cross-base terminal digits | Base-10 bias strength | Permutation test | Different bias patterns in Base-16 |
| H4 | Digit sums | Normal distribution | Shapiro-Wilk test | Accelerated convergence |
| H5 | Position-digit interactions | Independence model | χ² with corrections | Position-dependent digit preferences |