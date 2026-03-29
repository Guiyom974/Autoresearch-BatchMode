Based on the research problem and the constraints provided, here are 4 testable hypotheses designed to explore deeper, non-obvious structures in prime number distribution.

### Hypothesis 1: Local Bias in Residue Class "Attraction"
**1. Hypothesis Statement:**
When analyzing consecutive prime pairs $(p_n, p_{n+1})$, the residue class of $p_{n+1} \pmod{30}$ is not uniformly distributed given the residue class of $p_n \pmod{30}$. Specifically, certain "transitions" between residues (e.g., $1 \to 7$ vs $1 \to 11$) occur with statistically significant higher frequency than expected under a random distribution model.

**2. Why it’s testable:**
This moves beyond the trivial observation that primes (except 2, 3, 5) avoid multiples of 2, 3, and 5. By mapping the transitions of primes modulo 30 (which has 8 coprime residue classes), we can construct a transition matrix. We can test if this matrix deviates from a uniform stochastic matrix using a Chi-squared goodness-of-fit test.

**3. Experiment:**
*   Generate all primes up to $10^6$.
*   Map each prime to its residue class mod 30 ($r \in \{1, 7, 11, 13, 17, 19, 23, 29\}$).
*   Count the frequency of all ordered pairs $(r_i, r_{i+1})$.
*   Calculate the expected frequency assuming independence and compare using a Chi-squared test to identify specific "attractor" or "repulsor" transitions.

---

### Hypothesis 2: Prime Gap Variance Scaling
**1. Hypothesis Statement:**
The variance of prime gaps $g_n = p_{n+1} - p_n$ within localized windows of size $K$ (e.g., $K=1000$ primes) scales predictably with the average gap size in that window, deviating from the global Poisson distribution model in a non-linear, power-law fashion.

**2. Why it’s testable:**
While the *global* distribution of prime gaps is well-studied (often approximated by an exponential distribution), the *local* variance is less explored. This hypothesis tests if the local "ruggedness" of the prime sequence changes as we move to higher integers, which could indicate localized clustering behavior that the Prime Number Theorem averages out.

**3. Experiment:**
*   Divide the sequence of primes into non-overlapping windows of size 1000.
*   For each window, calculate the mean gap $\mu$ and the variance $\sigma^2$.
*   Perform a regression analysis to determine if $\sigma^2 \propto \mu^\alpha$ for some exponent $\alpha$.
*   Quantify the deviation from the $\alpha=2$ behavior expected of a purely Poisson process.

---

### Hypothesis 3: Ulam Spiral Density Anomaly
**1. Hypothesis Statement:**
The density of primes on the diagonals of an Ulam Spiral is not solely determined by the quadratic polynomial $f(n) = 4n^2 + bn + c$, but is statistically correlated with the number of prime factors of the quadratic’s discriminant, suggesting an underlying "algebraic interference" pattern.

**2. Why it’s testable:**
Ulam spirals are often dismissed as visual artifacts, but they highlight polynomials that produce many primes (like Euler's $n^2 + n + 41$). This hypothesis attempts to quantify if the "primeness" of a diagonal relates to the arithmetic properties of the quadratic generating it, moving from visual observation to algebraic correlation.

**3. Experiment:**
*   Generate an Ulam spiral up to $10^6$.
*   Identify the top 10% of diagonals with the highest prime density.
*   Extract the quadratic coefficients $(a, b, c)$ for these diagonals.
*   Calculate the number of distinct prime factors of the discriminant $D = b^2 - 4ac$ for these diagonals vs. the bottom 10% of diagonals.
*   Use a T-test to see if high-density diagonals have significantly different discriminant factor counts.

---

### Hypothesis 4: Semiprime "Shadow" Correlation
**1. Hypothesis Statement:**
The distribution of semiprimes (numbers with exactly two prime factors) shows a detectable "shadow" effect relative to prime gaps; specifically, the density of semiprimes is statistically lower in the immediate interval preceding large prime gaps (gaps > $2\sigma$ of the mean gap).

**2. Why it’s testable:**
This investigates if the "scarcity" of primes (large gaps) is compensated for by a shift in the density of composite numbers, specifically semiprimes. It tests the hypothesis of "local arithmetic conservation," where the number of candidates for primality might be redistributed locally among near-primes.

**3. Experiment:**
*   Identify all "large gaps" (e.g., gaps > 2 standard deviations above the mean) in the range up to $10^6$.
*   Define a "pre-gap window" of size $W$ immediately preceding the start of a large gap.
*   Compare the density of semiprimes in these pre-gap windows to a control group of windows of the same size placed randomly in the sequence.
*   Use a Z-test to determine if the semiprime density in pre-gap windows is significantly different from the expected average density.