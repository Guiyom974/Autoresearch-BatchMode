Based on the research problem provided, here are four testable hypotheses designed to validate the Rubinstein-Sarnak predictions regarding Chebyshev bias at higher primorial moduli.

### Hypothesis 1: The Non-Residue Dominance Hypothesis
**1. Statement:** For any modulus $q$ (where $q$ is a primorial like 210 or 2310), the logarithmic density of the prime race winning set for a quadratic non-residue (NR) class will be significantly greater than 0.5, while quadratic residue (QR) classes will exhibit a density significantly less than 0.5.

**2. Why it’s testable:** The Rubinstein-Sarnak theory explicitly predicts a logarithmic density $> 0.5$ for non-residue classes. By calculating the logarithmic density $\delta(a) = \lim_{x \to \infty} \frac{1}{\log x} \sum_{p \leq x, \pi(p;q,a) > \pi(p;q,b)} \frac{1}{p}$, we can quantitatively compare the win rates of NR vs. QR classes against the 0.5 null hypothesis.

**3. Experiment:**
*   Identify all QR and NR classes mod 210 using the Jacobi symbol.
*   For a set of prime races between a chosen NR class and a chosen QR class, track the cumulative prime counts $\pi(x; 210, a)$ as $x$ increases from $10^6$ to $10^9$.
*   Calculate the proportion of the logarithmic measure where $\pi(x; 210, NR) > \pi(x; 210, QR)$.
*   Statistical verification: Perform a one-sample t-test or binomial test to determine if the observed density deviates significantly from 0.5.

---

### Hypothesis 2: The Character Sum Predictor Hypothesis
**1. Statement:** The direction of the bias (which class "wins" the race) is strictly determined by the sum of real Dirichlet characters $\sum_{\chi \text{ real}, \chi \neq \chi_0} \chi(a)$. Classes with a lower (more negative) character sum will consistently lose prime races to classes with a higher (more positive) character sum.

**2. Why it’s testable:** This hypothesis connects abstract number theory (Dirichlet characters) to empirical data (prime counts). We can analytically calculate the character sum for every coprime residue class and then compare these sums to the empirical rankings derived from the sieve data.

**3. Experiment:**
*   Compute the 8 real Dirichlet characters mod 210.
*   For each coprime residue $a$, compute $S(a) = \sum_{\chi \text{ real}, \chi \neq \chi_0} \chi(a)$.
*   Rank all 48 coprime classes by their $S(a)$ value.
*   Compare this theoretical ranking to the empirical ranking of prime counts $\pi(x; 210, a)$ at $x=10^9$.
*   Success criterion: A high correlation (Spearman’s rank correlation coefficient $\rho > 0.85$) between the theoretical character sum and the empirical prime count.

---

### Hypothesis 3: The Log-Log Scaling Hypothesis
**1. Statement:** The normalized difference in prime counts between a winning NR class and a losing QR class, defined as $\Delta(x) = \frac{\pi(x; q, NR) - \pi(x; q, QR)}{\sqrt{x}/\log x}$, does not converge to zero but instead scales proportionally to $\log(\log x)$.

**2. Why it’s testable:** This hypothesis tests the "rate of growth" of the bias. If the bias were purely random, the normalized difference would fluctuate around zero with no trend. If Chebyshev bias holds, we should observe a clear, positive, non-linear growth trend as $x$ increases.

**3. Experiment:**
*   Select the most prominent NR class and the most prominent QR class mod 210.
*   Calculate the normalized difference $\Delta(x)$ at logarithmic intervals (e.g., $10^6, 10^{6.5}, 10^7, \dots, 10^9$).
*   Perform a linear regression of $\Delta(x)$ against $\log(\log x)$.
*   Success criterion: A statistically significant positive slope ($p < 0.05$) in the regression model, indicating that the bias magnitude increases as predicted by the Rubinstein-Sarnak framework.

---

### Hypothesis 4: The Primorial Invariance Hypothesis
**1. Statement:** The qualitative ranking of coprime residue classes based on prime density is invariant across different primorial moduli (210 vs. 2310). A class that is a "winner" mod 210 will remain a "winner" mod 2310 if it is a descendant of the same quadratic residue status.

**2. Why it’s testable:** This tests whether the Chebyshev bias is a local artifact of the chosen modulus or a structural feature of prime distribution. Since 2310 is a multiple of 210, we can map the classes and check for consistency.

**3. Experiment:**
*   Sieve for primes up to $10^9$ for both mod 210 and mod 2310.
*   For mod 210, identify the top 5 "winning" coprime classes.
*   Map these classes to their corresponding residue classes mod 2310 (e.g., if $a \equiv r \pmod{210}$, then $a$ is also $r \pmod{2310}$ or $r+210 \pmod{2310}$).
*   Calculate the prime counts for these classes mod 2310.
*   Success criterion: The Spearman correlation of the "winning" intensity between the mod 210 and mod 2310 datasets should be positive and statistically significant.