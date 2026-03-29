

Based on the research problem and search context, here are 4 testable hypotheses. Each includes the hypothesis statement, why it is testable, and an experiment to test it.

---

### Hypothesis 1: Mathematical Derivation of Primorial-Adjusted Benford Distribution
**Statement:** The leading digit probability \( P(d) \) for a primorial base \( N = \prod_{i=1}^k p_i \) (where \( p_i \) are the first \( k \) primes) follows a modified Benford distribution that incorporates the asymptotic density of numbers coprime to \( N \). Specifically,  
\[
P(d) = \frac{\log_N\left(1 + \frac{1}{d}\right) \cdot \mathbf{1}_{\gcd(d, N)=1}}{\sum_{j=1}^{N-1} \log_N\left(1 + \frac{1}{j}\right) \cdot \mathbf{1}_{\gcd(j, N)=1}},
\]  
where the indicator function \( \mathbf{1}_{\gcd(d,N)=1} \) zeroes out digits sharing prime factors with \( N \), and the denominator normalizes the sum to 1.

**Why it is testable:**  
The formula is explicit and calculable for any primorial base. We can compute the theoretical probabilities for base 30 and base 210 and compare them to empirical distributions from prime data.

**Experiment to test it:**  
1. Generate primes up to \( 10^8 \).  
2. Convert each prime to base 30 and base 210, extract the leading digit.  
3. Compute the empirical probability distribution of leading digits.  
4. Compute the primorial-adjusted Benford probabilities using the formula above.  
5. Compare empirical and theoretical distributions using KL divergence and chi-square goodness-of-fit tests.  
6. If the KL divergence is significantly lower than against standard Benford (e.g., below 0.1), the hypothesis is supported.

---

### Hypothesis 2: Reduction of KL Divergence Against Primorial-Adjusted Model
**Statement:** The KL divergence between the empirical leading digit distribution of primes up to \( 10^8 \) in base 210 and the primorial-adjusted Benford model will be substantially lower than the KL divergence against standard Benford's law (0.636), ideally approaching zero.

**Why it is testable:**  
KL divergence is a measurable statistic that quantifies the difference between two distributions. We can compute it directly from the empirical data and the two theoretical models.

**Experiment to test it:**  
1. As in Hypothesis 1, generate primes up to \( 10^8 \), convert to base 210, extract leading digits.  
2. Compute empirical probabilities \( P_{\text{emp}}(d) \) for \( d=1,\dots,9 \).  
3. Compute standard Benford probabilities \( P_{\text{Benford}}(d) = \log_{210}(1 + 1/d) \).  
4. Compute primorial-adjusted Benford probabilities \( P_{\text{adj}}(d) \) using the formula from Hypothesis 1.  
5. Calculate \( D_{\text{KL}}(P_{\text{emp}} \| P_{\text{Benford}}) \) and \( D_{\text{KL}}(P_{\text{emp}} \| P_{\text{adj}}) \).  
6. Compare the two divergences. If the adjusted divergence is much smaller (e.g., by at least 50%), the hypothesis is supported.

---

### Hypothesis 3: Digit-Specific Residual Biases Persist After Adjustment
**Statement:** Even after adjusting for coprimality, the residual KL divergence (if any) will be driven by specific leading digits (e.g., digit 1) that exhibit systematic over- or under-representation relative to the primorial-adjusted model. These residuals will correlate with deeper modular properties, such as the distribution of primes in residue classes modulo higher powers of the primorial's prime factors.

**Why it is testable:**  
We can compute per-digit residuals (e.g., \( P_{\text{emp}}(d) - P_{\text{adj}}(d) \)) and test for statistical significance using confidence intervals or bootstrap methods. Correlation with modular properties can be tested by analyzing primes in different residue classes.

**Experiment to test it:**  
1. Using the same data as in Hypothesis 1, compute per-digit residuals \( r_d = P_{\text{emp}}(d) - P_{\text{adj}}(d) \).  
2. Perform a chi-square test or binomial confidence interval for each digit to determine if any residual is statistically significant (e.g., p < 0.05).  
3. If residuals are significant for specific digits, analyze whether they correlate with properties such as the density of primes in residue classes modulo \( p^2 \) or other modular conditions related to the primorial's prime factors.  
4. If such correlations exist, the hypothesis is supported.

---

### Hypothesis 4: Cross-Base Consistency of the Primorial-Adjusted Model
**Statement:** The primorial-adjusted Benford model will yield consistent reductions in KL divergence across different primorial bases (e.g., base 30, 210, and 2310), indicating that the correction for coprimality is a universal feature of primorial bases rather than an artifact of a specific base.

**Why it is testable:**  
We can repeat the KL divergence analysis for multiple primorial bases and compare the reductions.

**Experiment to test it:**  
1. Generate primes up to \( 10^8 \).  
2. For each base \( N = 30, 210, 2310 \) (as computational limits allow), convert primes to base \( N \), extract leading digits.  
3. For each base, compute empirical leading digit probabilities.  
4. For each base, compute both standard Benford and primorial-adjusted Benford probabilities.  
5. Calculate KL divergences for both models in each base.  
6. Compare the reductions across bases. If all bases show substantial reduction (e.g., >50% decrease from standard Benford divergence), the hypothesis is supported.

---

### Hypothesis 5: Asymptotic Convergence to the Primorial-Adjusted Model
**Statement:** As the upper bound on primes increases (e.g., from \( 10^7 \) to \( 10^8 \) to \( 10^9 \) if feasible), the empirical leading digit distribution in base 210 will converge to the primorial-adjusted Benford distribution, with the residual KL divergence decreasing toward zero. This convergence will be faster than convergence to standard Benford's law.

**Why it is testable:**  
We can compute KL divergences for multiple upper bounds and observe whether they decrease toward the adjusted model.

**Experiment to test it:**  
1. Generate primes up to multiple upper bounds \( M = 10^6, 10^7, 10^8 \) (and beyond if computationally feasible).  
2. For each \( M \), convert primes to base 210, extract leading digits, compute empirical probabilities.  
3. For each \( M \), compute KL divergence against standard Benford and against the primorial-adjusted model.  
4. Plot the divergences as functions of \( M \). If both decrease but the adjusted divergence decreases faster and approaches zero, the hypothesis is supported.

---

These hypotheses address the core objectives: deriving a corrected model, validating it against data, identifying residual anomalies, and testing generalizability and asymptotic behavior.