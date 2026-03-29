Based on the research problem provided, here are four testable hypotheses designed to validate the Rubinstein-Sarnak predictions regarding Chebyshev bias at primorial moduli.

---

### Hypothesis 1: The "Non-Residue Advantage" (Dirichlet Character Prediction)
**Hypothesis Statement:**
The logarithmic density of prime counts in quadratic non-residue (NR) classes modulo 210 will be strictly greater than 0.5 when raced against quadratic residue (QR) classes. Specifically, the sign of the sum of the non-principal real Dirichlet characters for a residue class $a$ correctly predicts its winning frequency against a QR class.

**Why it’s testable:**
This hypothesis operationalizes the Rubinstein-Sarnak theory into a binary outcome. It can be tested by calculating the Jacobi symbol for every coprime residue class mod 210 to classify them as QR or NR, then empirically measuring the "win rate" (the percentage of the interval $[2, x]$ where $\pi(x; 210, a_{NR}) > \pi(x; 210, a_{QR})$).

**Experimental Test:**
1. Generate primes up to $10^9$ using a segmented sieve.
2. For every coprime residue class $a \in \{1, \dots, 209\}$, compute the Jacobi symbol $\left(\frac{a}{210}\right)$.
3. Perform pairwise "races" between a selection of NR classes and QR classes.
4. Calculate the logarithmic density $\delta(a, b) = \lim_{x \to \infty} \frac{1}{\log x} \sum_{p \le x, \pi(p;q,a) > \pi(p;q,b)} \frac{1}{p}$ and verify if $\delta > 0.5$ for NR classes.

---

### Hypothesis 2: Scaling of Bias Magnitude
**Hypothesis Statement:**
The normalized bias, defined as $\Delta(x) = \frac{\pi(x; 210, a_{NR}) - \pi(x; 210, a_{QR})}{\sqrt{x}/\log x}$, does not remain constant but grows proportionally to $\log(\log x)$ as $x$ increases from $10^6$ to $10^9$.

**Why it’s testable:**
This is a quantitative prediction about the rate of divergence. By measuring the bias at logarithmic intervals (e.g., $10^6, 10^7, 10^8, 10^9$), we can perform a linear regression on the normalized bias against $\log(\log x)$ to determine if the slope is positive and consistent with theoretical predictions.

**Experimental Test:**
1. Identify the specific residue classes $a_{NR}$ and $a_{QR}$ that exhibit the most extreme bias at mod 210.
2. Track the difference in prime counts for these classes at powers of 10.
3. Compute the normalized difference $\Delta(x)$ at each step.
4. Plot $\Delta(x)$ versus $\log(\log x)$ and perform a least-squares fit to check for a linear relationship.

---

### Hypothesis 3: Cross-Primorial Structural Consistency
**Hypothesis Statement:**
The ranking of residue classes by prime count density is preserved across different primorial moduli. Specifically, a residue class $a$ that acts as a "winner" (NR) mod 210 will also act as a "winner" mod 2310, provided the classes are consistent with the same underlying quadratic character.

**Why it’s testable:**
This tests the universality of the bias. If the bias were an artifact of the specific modulus (210), the ordering would be stochastic or unrelated to the modulus 2310. By mapping the residue classes mod 210 to their corresponding "families" mod 2310, we can statistically correlate the rankings.

**Experimental Test:**
1. Determine the "winningest" residue classes mod 210.
2. Determine the "winningest" residue classes mod 2310.
3. Map the mod 210 residue classes to their corresponding residue classes mod 2310 (e.g., $a \pmod{210}$ corresponds to $a \pmod{2310}$ and $a+210 \pmod{2310}$, etc.).
4. Calculate the Spearman rank correlation coefficient between the prime count density of the mod 210 classes and the aggregated density of their "descendant" classes mod 2310.

---

### Hypothesis 4: The "Artifact Nullification" (Filter Validity)
**Hypothesis Statement:**
After applying the coprime filter ($\gcd(a, q) = 1$), the residue class $a=5 \pmod{210}$ will contain exactly one prime ($p=5$) and will show no statistically significant bias compared to other coprime classes; its observed frequency will be near zero for all $x \ge 5$.

**Why it’s testable:**
This is a control hypothesis to validate the methodology. It ensures that the previous error (interpreting non-coprime classes as having bias) is fully corrected.

**Experimental Test:**
1. Run the sieve and specifically flag the count of primes in the $a=5 \pmod{210}$ bucket.
2. Compare the count of this bucket against the expected count for any other coprime residue class (e.g., $a=11 \pmod{210}$).
3. A Chi-squared test should yield a massive discrepancy (p-value $\approx 0$) for the $a=5$ bucket, confirming it is an outlier that must be excluded from the "true" Chebyshev bias analysis.