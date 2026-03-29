Based on the research problem and the constraints provided, here are four testable hypotheses. These hypotheses translate the research questions into specific, falsifiable predictions that your methodology is designed to evaluate.

### Hypothesis 1: Absence of Crossover within the Bounded Limit
*   **Hypothesis Statement:** The prime race difference function $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ will remain strictly positive for all $x$ in the interval $[1, 10^6]$. In other words, no crossover point exists where the residue class $a=1$ overtakes the non-residue class $a=11$ within this bound.
*   **Why it is testable:** This is a binary proposition. The experiment will either identify a value $x \le 10^6$ where $\Delta(x) \le 0$ (falsifying the hypothesis), or it will reach $10^6$ without ever recording a sign change (supporting the hypothesis).
*   **Experiment:** Run the optimized Sieve of Eratosthenes up to $10^6$. Track the running count of primes congruent to 1 and 11 mod 210. If the counter for $a=11$ is always greater than or equal to the counter for $a=1$ at every prime step, the hypothesis holds.

### Hypothesis 2: Non-Monotonicity of the Bias
*   **Hypothesis Statement:** The magnitude of the bias $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ will exhibit non-monotonic fluctuations rather than a steady, linear growth or decline as $x$ approaches $10^6$.
*   **Why it is testable:** This hypothesis predicts the *behavior* of the data rather than just the final result. It posits that the "race" is erratic. It is testable by calculating the first derivative of the difference function (the change in $\Delta$ at each prime step) and observing if it changes sign frequently.
*   **Experiment:** During the sieve process, record the value of $\Delta(x)$ at every prime $p \le 10^6$. Plot these points. If the slope of the line connecting $\Delta(p_n)$ and $\Delta(p_{n+1})$ alternates between positive and negative values (indicating the lead of one class over the other is not constant), the hypothesis is supported.

### Hypothesis 3: Bounded Maximum Lead
*   **Hypothesis Statement:** The maximum lead achieved by the quadratic non-residue class ($a=11$) over the residue class ($a=1$) will not exceed a threshold value $K = \sqrt{10^6} \cdot \log(10^6)$ (or a similar heuristic bound derived from the Prime Number Theorem for arithmetic progressions).
*   **Why it is testable:** This is a quantitative prediction. It establishes a specific numerical upper limit on the "lead" that the non-residue class can maintain.
*   **Experiment:** Monitor the variable `max_lead` throughout the algorithm. Each time a prime is processed, if $\Delta(x) > \text{current\_max\_lead}$, update the variable. At the end of the simulation, compare the final `max_lead` to the predicted threshold $K$. If the final lead is less than or equal to $K$, the hypothesis is supported.

### Hypothesis 4: Correlation with Density Fluctuations
*   **Hypothesis Statement:** Local increases in the density of primes (clusters of primes) will coincide with temporary expansions of the lead of the non-residue class ($a=11$) over the residue class ($a=1$).
*   **Why it is testable:** This hypothesis tests the relationship between local prime density and the "prime race" bias. It can be tested by correlating the *gap* between consecutive primes with the *change* in the bias $\Delta(x)$.
*   **Experiment:** Modify the algorithm to calculate the gap between consecutive primes ($g_n = p_{n+1} - p_n$). For every $x$, compare $g_n$ with the change in $\Delta(x)$. If instances of small gaps (high density) correlate with a positive change in the bias (the non-residue class pulling further ahead), the hypothesis is supported.