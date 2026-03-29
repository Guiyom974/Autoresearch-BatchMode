Based on the provided research problem and the principles of Chebyshev’s bias, here are four testable hypotheses designed to explore higher-order primorial residue distributions.

---

### Hypothesis 1: The "Non-Quadratic Residue" Bias
**Hypothesis Statement:** For any primorial modulus $P_k$ (where $k \ge 4$), prime numbers will exhibit a statistically significant preference for quadratic non-residue classes over quadratic residue classes modulo $P_k$ as $N \to 10^8$.

*   **Why it’s testable:** This hypothesis posits a structural rule (the quadratic nature of the residue) rather than just random fluctuation. By partitioning the coprime residue classes modulo $210$ and $2310$ into "quadratic residues" and "non-quadratic residues," we can calculate the cumulative count of primes in each group.
*   **Experimental Design:**
    1. For a modulus $M$ (e.g., 210), identify all coprime residues $r \in \{1, \dots, M\}$.
    2. Segregate these residues into two sets: those that are quadratic residues modulo $M$ and those that are not.
    3. Sum the prime counts for each set up to $N = 10^8$.
    4. Perform a paired t-test or sign test to determine if the "non-residue" group consistently maintains a higher prime count, checking for statistical significance ($p < 0.01$).

### Hypothesis 2: Persistent Asymmetry in "Prime Race" Lead-Changes
**Hypothesis Statement:** The frequency of "lead changes" (crossings) between competing coprime residue classes modulo $210$ decreases logarithmically as $N$ increases, indicating that the initial biases in higher-order primorials become "locked-in" rather than oscillating freely.

*   **Why it’s testable:** This measures the dynamic behavior of the race, not just the final tally. It tests the stability of the distribution. If the bias were purely random, crossings would occur with a predictable frequency related to the number of samples; if the bias is structural (as Chebyshev’s bias suggests), the frequency of crossings should diminish as the "leader" pulls away.
*   **Experimental Design:**
    1. Track the prime counts for two specific, competing residue classes $a$ and $b$ modulo $210$.
    2. Count the number of indices $n \le 10^8$ where the leader changes (i.e., $\pi(n; 210, a) > \pi(n; 210, b)$ flips to the inverse).
    3. Bin the data into intervals (e.g., $10^5$ range increments) and calculate the rate of crossing.
    4. Apply a regression analysis to determine if the crossing rate is decreasing as $N$ grows, testing the hypothesis of "lock-in" stability.

### Hypothesis 3: The "Primorial Density" Decay
**Hypothesis Statement:** The magnitude of the bias (the normalized difference between the most and least populated residue classes) modulo $P_k$ decreases as the order of the primorial $k$ increases, following a relationship proportional to $1/\phi(P_k)$.

*   **Why it’s testable:** This hypothesis relates the size of the modulus to the strength of the bias. It tests whether the "Chebyshev effect" dilutes as the number of available residue classes increases.
*   **Experimental Design:**
    1. Calculate the maximum bias $B_k = \max| \pi(N; P_k, a) - \frac{\pi(N)}{ \phi(P_k)} |$ for $P_4=210$ and $P_5=2310$ at $N=10^8$.
    2. Normalize these bias values by the total count of primes up to $N$.
    3. Compare the normalized bias ratios for $P_4$ and $P_5$.
    4. Determine if the ratio $B_5/B_4$ aligns with the ratio $\phi(210)/\phi(2310)$, indicating that the bias is inversely proportional to the number of coprime classes.

### Hypothesis 4: Correlation with the Liouville Function
**Hypothesis Statement:** The fluctuations in the prime race (the "lead") between two coprime residue classes modulo $210$ are positively correlated with the partial sums of the Liouville function $\lambda(n)$ evaluated only at integers congruent to those residues.

*   **Why it’s testable:** This hypothesis connects the empirical observation of "prime races" to deeper analytic number theory (the distribution of zeros of the Riemann zeta function, which is linked to the Liouville function). It is testable by correlating the "lead" status of a residue with the local density of primes as predicted by the Liouville function.
*   **Experimental Design:**
    1. Define two residue classes $a$ and $b$ mod $210$.
    2. Compute the "Lead Score" (1 if $a$ leads, -1 if $b$ leads) at intervals up to $10^8$.
    3. Compute the local sum of the Liouville function $\sum \lambda(n)$ for $n \equiv a \pmod{210}$ and $n \equiv b \pmod{210}$.
    4. Calculate the Pearson correlation coefficient between the Lead Score and the difference in Liouville sums to see if the "race" follows the analytic predictions of the zeta function.