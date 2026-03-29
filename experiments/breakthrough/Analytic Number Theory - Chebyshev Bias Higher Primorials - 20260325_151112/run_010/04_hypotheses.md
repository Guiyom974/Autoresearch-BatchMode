Based on the research problem and the provided context regarding Chebyshev’s bias, here are four testable hypotheses.

---

### Hypothesis 1: The Dominance Hypothesis
**1. Hypothesis Statement:**
The non-quadratic residue class ($a=11 \pmod{210}$) will maintain a majority lead over the quadratic residue class ($a=1 \pmod{210}$) for more than 90% of the integers $x$ in the range $2 \le x \le 10^5$.

**2. Why it is testable:**
This hypothesis provides a specific, quantifiable threshold (90%) against which the experimental data can be measured. It directly tests the core tenet of Chebyshev's bias—that non-residues tend to be "more frequent"—within the specified ultra-low bound.

**3. Experiment:**
During the sieve execution, maintain a counter for the number of times $\Delta(x) > 0$ versus the total number of primes encountered. At the conclusion of the $10^5$ limit, calculate the percentage of steps where the non-residue class held the lead.

---

### Hypothesis 2: The "Trivial Start" Lag Hypothesis
**1. Hypothesis Statement:**
The quadratic residue class ($a=1 \pmod{210}$) will hold the lead during the initial interval $x < 100$, before the non-quadratic residue class ($a=11 \pmod{210}$) establishes a sustained, irreversible lead.

**2. Why it is testable:**
This hypothesis tests the "onset" of the bias. It acknowledges that at very small values of $x$, the distribution is often erratic or dominated by small-number noise, allowing for the "trivial" residue to lead before the asymptotic bias of the non-residue takes over.

**3. Experiment:**
Monitor the sign of $\Delta(x)$ specifically for the first 100 integers. Record the exact value of $x$ (the "crossover point") where $\pi(x; 210, 11)$ first exceeds $\pi(x; 210, 1)$ and stays above it for the remainder of the dataset.

---

### Hypothesis 3: The Magnitude Asymmetry Hypothesis
**1. Hypothesis Statement:**
The maximum lead achieved by the non-quadratic residue class ($a=11$) will be at least twice as large as the maximum lead ever achieved by the quadratic residue class ($a=1$) within the search space $x \le 10^5$.

**2. Why it is testable:**
This measures the *severity* of the bias. Rather than just asking "who is winning," it asks "by how much." It tests the prediction that the bias isn't just a frequency preference, but a distinct statistical advantage in magnitude.

**3. Experiment:**
Maintain two running maximum variables: `max_lead_11` and `max_lead_1`. Whenever $\Delta(x) > 0$, update `max_lead_11` if the current $\Delta(x)$ is higher; whenever $\Delta(x) < 0$, update `max_lead_1` if the absolute value $|\Delta(x)|$ is higher. Compare these two variables at the end of the run.

---

### Hypothesis 4: The Monotonicity of Bias Growth
**1. Hypothesis Statement:**
The net difference $\Delta(x)$ will exhibit a non-decreasing trend in terms of its local maxima; that is, the global maximum lead of $a=11$ will occur in the latter half of the search space ($x > 50,000$) rather than the first half.

**2. Why it is testable:**
This hypothesis tests whether the bias is a stable, growing phenomenon that accumulates over time, or if it is merely a product of early-integer anomalies. If the bias is "real" in the Chebyshev sense, it should theoretically strengthen as $x$ increases.

**3. Experiment:**
Divide the dataset into two buckets: $x \in [0, 50,000]$ and $x \in [50,001, 100,000]$. Track the maximum observed $\Delta(x)$ for each bucket. If the maximum in the second bucket is greater than the maximum in the first, the hypothesis is supported.