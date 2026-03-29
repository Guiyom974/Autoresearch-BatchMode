
## Iteration 1 [ORIGINAL]
Timestamp: 2026-03-25T15:11:12.944683

# Research Problem: Chebyshev Bias at Higher Primorials — Corrected & Extended

## Background
The previous experiment identified a statistically significant "excess" of primes in residue
class a=5 mod 210 (p=0.003). However, gcd(5, 210)=5 ≠ 1, meaning this class is NOT coprime
to 210 — the only prime in it is 5 itself. The finding was a code artifact from failing to
filter non-coprime residue classes.

This run corrects the filter and performs a rigorous, theoretically-grounded investigation of
**genuine Chebyshev bias** among the φ(210)=48 coprime residue classes modulo 210 and beyond.

## Objective
Verify and quantify the Rubinstein-Sarnak prediction for Chebyshev's bias at mod 210 and 2310:
non-residue quadratic residue classes should win prime races more than 50% of the time.
Find which specific coprime classes lead, measure the bias magnitude, and check whether the
magnitude scales with log(log(x)) as theory predicts.

## Research Questions

1. **Coprime Class Audit**: Among all φ(210)=48 coprime residue classes mod 210, which are
   quadratic residues (QR) and which are quadratic non-residues (NR)? Do the NR classes hold
   more primes as predicted by Chebyshev?

2. **Bias Magnitude & Scaling**: For the two extreme classes (most and fewest primes mod 210),
   how does the normalized difference (π(x;210,a_NR) − π(x;210,a_R)) / (x/log x) evolve as
   x grows from 10^6 to 10^9? Does it scale as C·log(log(x)) as Rubinstein-Sarnak predicts?

3. **Cross-Primorial Consistency**: Does the same qualitative Chebyshev structure appear at
   P₅=2310 (φ=480 coprime classes)? Are the winning classes consistent with their quadratic
   residue status in both moduli simultaneously?

4. **Logarithmic Density of Leaders**: For the top-3 competing coprime classes mod 210, compute
   the logarithmic density δ(a) = lim_{x→∞} (1/log x) ∑_{p≤x, π(p;q,a)>π(p;q,b)} 1/p.
   Does the NR class leader density exceed 0.5 as Chebyshev's bias predicts?

5. **Dirichlet Character Contribution**: For mod 210, identify which Dirichlet characters χ
   modulo 210 are real (χ² = χ₀). These are the ones responsible for Chebyshev bias. For each
   coprime residue class, compute the character sum ∑_χ real χ(a) and verify it predicts the
   observed bias direction.

## Methodology

1. **Corrected Sieve**: Implement a segmented Sieve of Eratosthenes. For each prime p, compute
   r = p mod q. Include only if gcd(r, q) == 1 (coprime filter). Verify: class a=5 mod 210
   should contain ONLY the prime 5 itself.

2. **Quadratic Residue Classification**: For each coprime residue a mod 210, determine whether
   a is a QR mod 210 using the Jacobi symbol (product of Legendre symbols mod 2, 3, 5, 7).
   Label classes as QR or NR.

3. **Statistical Test**: Apply a Chi-squared goodness-of-fit test to compare observed prime
   counts per coprime class against the expected 1/φ(q) uniform distribution. Report p-value
   and identify the most over- and under-represented coprime classes.

4. **Race Tracking**: Track cumulative counts π(x; 210, a) for the top-3 and bottom-3 coprime
   classes at intervals x = 10^k for k=5..9. Plot normalized lead δ(x,a,b) = (π(x;q,a) −
   π(x;q,b)) / √(x/log x) over x.

5. **L-Function Cross-Check**: Compute the real Dirichlet characters mod 210 analytically
   (there are 2^3 = 8 real characters, from the factorisation 210 = 2·3·5·7). For each
   coprime class a, evaluate ∑_{χ real, χ≠χ₀} χ(a). Theory predicts this sum is negative for
   QR classes (they lose) and positive for NR classes (they win).

## Success Criteria

1. **Artifact Confirmed**: Explicitly show that a=5 mod 210 contains ≤1 prime (the prime 5
   itself) and produces no statistically meaningful count signal.

2. **Bias Confirmed**: At least one pair of coprime classes (NR vs QR mod 210) shows a
   statistically significant race lead (NR winning >50% of the time by logarithmic density)
   consistent with the Chebyshev prediction.

3. **Scaling Verified**: The normalized bias (π_NR − π_QR)/√(x/log x) grows with log(log(x))
   over at least 3 orders of magnitude of x.

4. **Cross-Primorial**: The same NR→QR ordering is reproduced at mod 2310, confirming the
   structure is intrinsic to prime distribution, not a mod-210-specific artifact.

5. **Character Sum Match**: The sign of the Dirichlet character sum for each class correctly
   predicts the observed bias direction for ≥90% of coprime classes mod 210.

## Prior Knowledge to Incorporate
- Rubinstein-Sarnak (1994): proved logarithmic density exists for prime races assuming GRH +
  Grand Simplicity Hypothesis; non-residues win with density > 0.5
- Dirichlet's theorem: primes equidistribute among coprime residue classes asymptotically
- Chebyshev bias magnitude: O(log log x) correction to the equidistribution, not O(1)
- Devin (2017): proved Chebyshev bias distributions exist WITHOUT assuming GRH (weaker bounds)

## Constraints
- All code in Python, stdlib + numpy + matplotlib only
- No downloading data — all primes generated locally
- Must explicitly verify coprimality filter before any statistical test
- Runtime ≤ 3 minutes (use segmented sieve for memory efficiency)
- Experiments must clearly distinguish: (a) theoretical prediction, (b) observed result,
  (c) whether they agree


---

## Iteration 2 [REFORMULATED]
Timestamp: 2026-03-25T15:45:44.498439

# Research Problem: Chebyshev Bias at Modulo 210 — Focused Quadratic Residue Analysis

## Objective
To rigorously quantify the Rubinstein-Sarnak Chebyshev bias strictly modulo the primorial $q=210$. Following the correction of the coprime filtering artifact, this iteration narrows the computational scope to guarantee successful execution. We will systematically compare the prime counting function $\pi(x; 210, a)$ for quadratic residues versus quadratic non-residues among the $\phi(210)=48$ valid coprime classes, up to a computationally safe bound.

## Research Questions
1. Among the 48 coprime residue classes modulo 210, which specific classes dominate the prime race up to $x = 10^7$?
2. When aggregating the prime counts, do quadratic non-residues modulo 210 collectively win the prime race against quadratic residues at a frequency consistent with the Rubinstein-Sarnak logarithmic density predictions?
3. What is the variance in the prime counts among the different quadratic non-residue classes themselves?

## Methodology
1. **Prime Generation & Filtering:** Generate all prime numbers up to a strict, computationally feasible limit of $x = 10^7$. 
2. **Coprime Verification:** Strictly filter the candidate residue classes $a$ such that $\gcd(a, 210) = 1$, yielding exactly 48 valid classes.
3. **Quadratic Classification:** Mathematically classify each of the 48 classes as either a quadratic residue or a quadratic non-residue modulo 210.
4. **Race Simulation:** Compute the running tally of primes in each class. Track the "leader" at each step and calculate the empirical density of the lead held by quadratic non-residues over residues.

## Success Criteria
1. Successful, uninterrupted execution of the prime race simulation up to $x = 10^7$ without computational timeouts.
2. An output matrix or summary detailing the leading percentages for all 48 coprime classes.
3. A clear, quantitative comparison showing the aggregate win rate of quadratic non-residues versus quadratic residues modulo 210.

## Constraints
1. **Domain Constraint:** Do not expand the scope to $q=2310$ or higher primorials in this iteration to ensure the script completes successfully and yields data.
2. **Algorithmic Constraint:** The algorithm must explicitly assert $\gcd(a, 210) = 1$ before counting any prime towards a residue class.
3. **Performance Constraint:** Memory and time limits must be respected; use efficient sieving and cumulative sum arrays rather than recalculating counts at each step.

---

## Iteration 3 [REFORMULATED]
Timestamp: 2026-03-25T15:54:37.254274

# Research Problem: Two-Way Prime Race Modulo 210 — $\pi(x; 210, QNR)$ vs $\pi(x; 210, 1)$

## Objective
To bypass previous computational bottlenecks (which resulted in no output) by drastically tightening the scope of the investigation. Instead of calculating the prime counting function $\pi(x; 210, a)$ for all 48 coprime residue classes, this iteration will focus entirely on a single, targeted two-way "prime race." We will evaluate the Rubinstein-Sarnak Chebyshev bias by strictly comparing the principal quadratic residue class ($a=1$) against a single, verified quadratic non-residue (QNR) class (e.g., $a=11$) modulo the primorial $q=210$, up to a highly restricted and computationally safe bound.

## Research Questions
1. In a direct head-to-head comparison modulo 210, what percentage of the time does the quadratic non-residue class lead the quadratic residue class $a=1$ up to $x = 10^6$?
2. At what specific values of $x$ (if any within the bound) does the principal quadratic residue class ($a=1$) temporarily overcome the Chebyshev bias and take the lead?
3. What is the maximum magnitude of the difference $\Delta(x) = \pi(x; 210, QNR) - \pi(x; 210, 1)$ within this restricted search space?

## Methodology
1. **Parameter Selection:** Set the modulus to the primorial $q = 210$. 
2. **Class Isolation:** Select exactly two coprime residue classes for tracking: the principal quadratic residue $a_1 = 1$, and a known quadratic non-residue, such as $a_2 = 11$ (since $\gcd(11, 210) = 1$ and it is not a square modulo 210).
3. **Optimized Sieve:** Implement a standard Prime Sieve strictly capped at a low upper bound of $N = 1,000,000$ to guarantee execution completion.
4. **Delta Tracking:** Iterate through the generated primes, tallying counts for the two chosen classes only. Maintain a running difference $\Delta(x)$.
5. **Statistical Aggregation:** Calculate the exact proportion of integers $x \le 10^6$ for which $\Delta(x) > 0$.

## Success Criteria
1. The experiment successfully runs to completion and produces quantifiable output without timing out or exceeding memory limits.
2. A definitive percentage is calculated representing how often the chosen QNR class leads the QR class $a=1$ up to $10^6$.
3. Identification of the first few "axis crossings" (values of $x$ where the lead changes hands), if they exist within the bound.

## Constraints
1. **Strict Computational Limits:** The search bound must be hard-capped at $x = 10^6$. Do not attempt to scale higher until this baseline completes.
2. **Narrowed State Space:** Do not track or instantiate arrays for all 48 coprime classes. Memory and processing must be restricted to tracking only the two selected residue classes.
3. **Domain Strictness:** The investigation must remain exclusively focused on Chebyshev's bias modulo 210.

---

## Iteration 4 [REFORMULATED]
Timestamp: 2026-03-25T16:06:01.156390

# Research Problem: Low-Bound Empirical Verification of the Modulo 210 Prime Race ($a=11$ vs $a=1$)

## Objective
To bypass the severe computational bottlenecks encountered in previous iterations by drastically restricting the maximum evaluation bound. We will evaluate the Rubinstein-Sarnak Chebyshev bias prediction for a single, targeted two-way prime race modulo 210: the quadratic non-residue (QNR) class $a=11$ against the principal quadratic residue class $a=1$. The strict objective is to measure the logarithmic density of this specific race up to a hard-capped bound of $x = 10^7$, ensuring the computation completes and yields actionable baseline data.

## Research Questions
1. Does the QNR class $a=11$ maintain a strict dominance over the principal class $a=1$ modulo 210 for all primes up to $x = 10^7$?
2. If lead changes occur within this restricted bound, at what specific values of $x$ do they manifest?
3. What is the empirical logarithmic density of the set of $x \le 10^7$ for which $\pi(x; 210, 11) > \pi(x; 210, 1)$?

## Methodology
1. **Targeted Prime Generation:** Utilize a highly optimized prime sieve strictly capped at $N = 10^7$. 
2. **Binary Class Filtering:** As primes are generated, filter and count *only* those that satisfy $p \equiv 1 \pmod{210}$ and $p \equiv 11 \pmod{210}$. Discard all other primes immediately to save memory.
3. **Cumulative Tallying:** Maintain a running tally of $\pi(x; 210, 11)$ and $\pi(x; 210, 1)$.
4. **Logarithmic Density Calculation:** At regular intervals (e.g., every $10^4$), compute the logarithmic weight $\frac{1}{x}$ to approximate the logarithmic density of the QNR lead.
5. **Lead Change Tracking:** Record the exact prime values where the lead transitions from one class to the other.

## Success Criteria
1. The experiment successfully completes without timing out or exhausting memory resources.
2. Output includes the total count of primes in both the $a=11$ and $a=1$ classes up to $10^7$.
3. Output provides a definitive list of the first $k$ lead changes (if any exist below $10^7$).
4. Output yields a calculated logarithmic density for this specific two-way race over the bounded interval.

## Constraints
1. **Hard Bound:** The maximum value for $x$ must absolutely not exceed $10^7$. 
2. **Strict Two-Class Limit:** The algorithm must only track counts for $a=1$ and $a=11$. Do not calculate or store data for the other 46 coprime residue classes.
3. **Empirical Only:** Do not attempt to compute Dirichlet L-functions, zeros, or theoretical Rubinstein-Sarnak distributions in this run; focus solely on the empirical prime counting function $\pi(x)$.

---

## Iteration 5 [REFORMULATED]
Timestamp: 2026-03-25T16:16:37.083232

# Research Problem: Algorithmic Optimization and Micro-Bound Validation of Logarithmic Density Modulo 210

## Objective
To overcome the severe computational bottlenecks that prevented output generation in previous iterations by shifting focus to algorithmic efficiency. We will develop a highly optimized, discrete-sum approximation for calculating logarithmic density in the modulo 210 prime race ($a=11$ vs $a=1$). The strict objective is to validate this optimized counting methodology up to a micro-bound of $x = 10^6$, ensuring the script successfully executes and provides a baseline empirical measurement of the Rubinstein-Sarnak Chebyshev bias.

## Research Questions
1. How can the numerical integration of logarithmic density be algorithmically simplified (e.g., via discrete summation over prime gaps) to eliminate computational timeouts?
2. Using an optimized segmented sieve and discrete logarithmic density summation, what is the empirical bias of the quadratic non-residue class $a=11$ against the principal class $a=1$ modulo 210 up to $x = 10^6$?
3. Does the $a=11$ class establish an initial dominance at this micro-bound, consistent with the predicted Chebyshev bias for non-residue vs. residue classes?

## Methodology
1. **Algorithmic Refactoring**: Replace continuous numerical integration functions (which likely caused the previous timeouts/failures) with a discrete cumulative sum approximation: $\delta(S) \approx \frac{1}{\log x} \sum_{n \in S, n \le x} \frac{1}{n}$.
2. **Optimized Sieve**: Implement a fast, memory-efficient Sieve of Eratosthenes strictly capped at $x = 10^6$. 
3. **Array Vectorization**: Utilize vectorized operations (e.g., NumPy if available, or highly optimized native arrays) to filter primes into the $a=11$ and $a=1$ residue classes modulo 210.
4. **Race Evaluation**: Track the running difference $\pi(x; 210, 11) - \pi(x; 210, 1)$ at discrete intervals, updating the logarithmic density metric only when the leader changes or at fixed logarithmic checkpoints.

## Success Criteria
1. **Execution**: The experiment must successfully run to completion without timing out or failing silently.
2. **Performance**: The prime generation and density calculation up to $x = 10^6$ must execute in under 30 seconds.
3. **Scientific Output**: The successful calculation of a specific logarithmic density value for the $a=11$ vs $a=1$ race modulo 210, providing a verified baseline for future scaling.

## Constraints
1. **Maximum Bound**: The evaluation bound is strictly capped at $x = 10^6$. Do not attempt to scale higher until this micro-bound is validated.
2. **Scope**: Limit the analysis exclusively to the two-way race between $a=11$ and $a=1$ modulo 210. Do not evaluate other residue classes or primorials.
3. **Mathematical Simplification**: Avoid heavy symbolic math libraries or continuous integration functions; rely strictly on discrete array manipulation and basic arithmetic summation.

---

## Iteration 6 [REFORMULATED]
Timestamp: 2026-03-25T16:39:05.593943

# Research Problem: Baseline Empirical Validation of Logarithmic Density in Modulo 210 Prime Races

## Objective
To establish a verified, mathematically robust baseline for calculating the logarithmic density of the prime race modulo 210. Following previous execution failures, we must strip away premature algorithmic optimizations and perform a highly controlled "dry-run" of the theoretical framework. We will compute the logarithmic measure for the race between a quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) up to a strict micro-bound of $x = 10^6$. This ensures the core mathematical logic and discrete-sum approximations are fundamentally sound before scaling to higher bounds or $2310$.

## Research Questions
1. What is the empirical logarithmic density of the set of $x \leq 10^6$ for which $\pi(x; 210, 11) > \pi(x; 210, 1)$?
2. How closely does a simplified, unoptimized discrete-sum approximation of the logarithmic measure align with the qualitative predictions of the Rubinstein-Sarnak framework at this micro-bound?
3. At what threshold $x \leq 10^6$ does the Chebyshev bias first strongly manifest in the logarithmic density calculation?

## Methodology
1. **Prime Generation:** Implement a standard, unoptimized Sieve of Eratosthenes up to $x = 10^6$.
2. **Residue Tracking:** Tally primes strictly in the coprime residue classes $a=11 \pmod{210}$ and $a=1 \pmod{210}$. 
3. **Difference Array:** Construct an array representing the difference $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ for each integer $x$ up to $10^6$.
4. **Logarithmic Measure:** Calculate the logarithmic density using the discrete sum $\frac{1}{\log X} \sum_{x \leq X, \Delta(x) > 0} \frac{1}{x}$, evaluated at $X = 10^6$.
5. **Validation:** Compare the resulting density against the expected $>0.50$ theoretical threshold for Chebyshev's bias.

## Success Criteria
- Successful, error-free generation of the difference array $\Delta(x)$ up to $10^6$.
- Output of a definitive empirical logarithmic density value for the $a=11$ vs $a=1$ race.
- Confirmation that the foundational mathematical logic correctly identifies and quantifies the bias without reliance on complex, error-prone algorithmic optimizations.

## Constraints
- **Bound Limit:** Computations must strictly not exceed $x = 10^6$ to ensure rapid verification of the foundational logic.
- **Class Restriction:** Only analyze the race between $a=11$ and $a=1$ modulo 210.
- **Simplicity:** Avoid advanced algorithmic optimizations, memory-mapping, or parallelization. The focus is exclusively on theoretical accuracy and establishing a functional scientific baseline.

---

## Iteration 7 [REFORMULATED]
Timestamp: 2026-03-25T16:52:47.208017

# Research Problem: Identifying the First Crossover Point in the Modulo 210 Prime Race

## Objective
Following the execution failure of the logarithmic density computation, we must drastically tighten the scope to ensure our foundational prime counting framework is functional. The revised objective is to isolate and verify the fundamental prime race mechanics by finding the very first sign change (crossover point) in the race between the quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) modulo 210. We will defer complex logarithmic integration until the basic crossover dynamics are empirically proven.

## Research Questions
1. At what exact integer $x$ does the prime count for the quadratic residue class $\pi(x; 210, 1)$ first equal or exceed the count for the non-residue class $\pi(x; 210, 11)$?
2. What is the maximum absolute lead (the Chebyshev bias "excess") achieved by the $a=11$ class prior to this initial crossover?
3. Does this first transition point occur within a heavily restricted micro-bound of $x \le 10^5$?

## Methodology
To prevent computational timeouts and memory exhaustion:
1. **Algorithmic Simplification:** Strip out all continuous logarithmic density integration logic. Revert to a strictly discrete natural counting function $\pi(x; q, a)$.
2. **Prime Generation:** Generate primes sequentially up to a reduced micro-bound of $x = 10^5$ using a highly optimized, standard sieve.
3. **State Tracking:** Maintain running tallies for $\pi(x; 210, 11)$ and $\pi(x; 210, 1)$. Compute the delta $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ at each prime step.
4. **Early Stopping:** The algorithm must immediately halt and record the exact prime $x$ and the preceding state the moment $\Delta(x) \le 0$ is achieved. 

## Success Criteria
- The successful execution of the counting script without failure.
- The identification of the exact prime $x$ representing the first crossover point, OR a definitive output proving that no crossover exists for $x \le 10^5$.
- A recorded integer tracking the maximum lead established by the $a=11$ class before the crossover (or up to the bound).

## Constraints
- **Domain Strictness:** Do NOT analyze any residue classes other than $a=11$ and $a=1$ modulo 210.
- **Metric Strictness:** Do NOT attempt to calculate logarithmic density. Use natural counting only.
- **Computational Limits:** Hard cap the search space at $x = 10^5$ to guarantee completion and validate the baseline script mechanics.

---

## Iteration 8 [REFORMULATED]
Timestamp: 2026-03-25T17:00:36.331269

# Research Problem: Bounded Empirical Detection of the First Modulo 210 Crossover

## Objective
Following the computational failure of the previous open-ended search, we must drastically tighten our scope to ensure successful execution while preserving the scientific core of the inquiry. The revised objective is to empirically locate the exact first sign change (crossover point) in the prime race between the quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) modulo 210, strictly bounding the search space to $x \le 10^7$. This avoids the overhead of asymptotic density calculations and focuses purely on exact prime counting within a feasible computational window.

## Research Questions
1. At what exact integer $x \le 10^7$ does the prime count $\pi(x; 210, 1)$ exceed $\pi(x; 210, 11)$ for the first time?
2. What is the maximum lead achieved by the theoretically favored class ($a=11$) prior to this first crossover point?
3. If no crossover exists below $10^7$, what is the asymptotic trajectory of the difference $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ within this interval?

## Methodology
1. **Prime Generation:** Utilize an optimized Sieve of Eratosthenes to generate all prime numbers strictly up to $x = 10^7$. 
2. **Residue Classification:** Filter the generated primes into two specific buckets: those congruent to $1 \pmod{210}$ and those congruent to $11 \pmod{210}$.
3. **Step-by-Step Tallying:** Iterate through the primes in ascending order, maintaining a running tally of $\pi(x; 210, 1)$ and $\pi(x; 210, 11)$.
4. **Crossover Detection:** At each prime step, compute the difference. Record the first instance where the tally for $a=1$ strictly exceeds the tally for $a=11$.

## Success Criteria
- The successful execution of the prime sieve up to $10^7$.
- The exact integer value $x$ of the first crossover point is identified and documented.
- If no crossover occurs before $10^7$, a plot or summary statistics of the difference $\Delta(x)$ up to the bound is provided.

## Constraints
- **Search Bound:** The algorithm must halt at $x = 10^7$ to ensure computational tractability.
- **Simplification:** No logarithmic density, weighted integrations, or Rubinstein-Sarnak analytical formulas will be computed in this iteration. Focus solely on the empirical step-function $\pi(x)$.
- **Scope limitation:** Only the residue classes $a=1$ and $a=11$ modulo 210 are to be tracked. All other 46 coprime classes are to be ignored for this run.

---

## Iteration 9 [REFORMULATED]
Timestamp: 2026-03-25T17:08:48.333835

# Research Problem: Highly Optimized Bounded Detection of Modulo 210 Prime Race Crossovers

## Objective
Following the computational limits encountered in previous open-ended and moderately bounded searches, this iteration drastically tightens the scope to ensure successful execution. The objective is to empirically evaluate the prime race between the quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) modulo 210, strictly bounding the search space to $x \le 10^6$ using a highly optimized, memory-efficient prime counting method. 

## Research Questions
1. Does the first crossover point (where $\pi(x; 210, 1) > \pi(x; 210, 11)$) occur within the strictly bounded range $x \le 10^6$?
2. What is the maximum lead achieved by the quadratic non-residue class ($a=11$) over the residue class ($a=1$) within this interval?
3. How does the magnitude of the bias $\pi(x; 210, 11) - \pi(x; 210, 1)$ behave as $x$ approaches $10^6$?

## Methodology
1. **Targeted Sieve**: Implement a highly optimized Sieve of Eratosthenes strictly capped at $N = 10^6$.
2. **Selective Counting**: Instead of tracking all 48 coprime residue classes, only track the prime counts for $a=1$ and $a=11$ modulo 210.
3. **Difference Tracking**: Compute the running difference $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ at each prime $p \le 10^6$.
4. **Crossover Logging**: Record the exact prime values $x$ where $\Delta(x)$ changes sign.

## Success Criteria
1. Successful execution of the counting algorithm up to $x = 10^6$ without memory or timeout errors.
2. A definitive boolean answer on whether a crossover exists below $10^6$.
3. A logged maximum lead value for the non-residue class over the residue class.

## Constraints
1. **Search Bound**: The search limit must be strictly hardcoded to $x = 10^6$. No dynamic expansion of the search space is allowed.
2. **Memory Efficiency**: The algorithm must discard primes once they are tallied to prevent memory overflow, storing only the running totals and crossover indices.
3. **Residue Restriction**: Computation must be strictly limited to the classes $a=1$ and $a=11$ modulo 210.

---

## Iteration 10 [REFORMULATED]
Timestamp: 2026-03-25T17:23:10.494962

# Research Problem: Ultra-Low Bounded Quantification of Initial Chebyshev Bias Modulo 210

## Objective
Following repeated computational timeouts in crossover detection, this iteration pivots from seeking race crossovers to quantifying the *initial accumulation of bias*. The objective is to empirically measure the onset and magnitude of Chebyshev's bias modulo 210 between the quadratic non-residue ($a=11$) and the trivial quadratic residue ($a=1$) within an ultra-tight, guaranteed-to-execute bound of $x \le 10^5$. 

## Research Questions
1. How rapidly does the prime-counting difference $\Delta(x) = \pi(x; 210, 11) - \pi(x; 210, 1)$ establish a positive trend in the early integers ($x \le 10^5$)?
2. What is the maximum and mean observed deviation $\Delta(x)$ within this restricted search space?
3. Does the quadratic residue class ($a=1$) ever take the lead in this initial microscopic range, or does the non-residue class assert dominance immediately?

## Methodology
1. **Ultra-Fast Sieving:** Implement a basic, highly optimized Sieve of Eratosthenes strictly hardcoded to a maximum limit of $N = 100,000$. 
2. **Residue Filtering:** As primes are generated, immediately classify them into buckets for $p \equiv 1 \pmod{210}$ and $p \equiv 11 \pmod{210}$.
3. **Step-wise Delta Tracking:** Maintain a running tally of $\pi(x; 210, 11)$ and $\pi(x; 210, 1)$. Compute the difference $\Delta(x)$ at each prime step.
4. **Statistical Aggregation:** Instead of storing large arrays of race history, calculate running statistics in memory (current lead, max lead for $a=11$, max lead for $a=1$, and proportion of $x$ where $a=11$ leads).

## Success Criteria
1. Complete, error-free execution of the prime sieve and residue counting up to $x = 10^5$.
2. Output of summary statistics detailing the exact prime counts for both residue classes at $x = 10^5$.
3. Clear quantification of the maximum lead achieved by either class in this range.

## Constraints
1. **Strict Upper Bound:** The search space must absolutely not exceed $x = 100,000$ to guarantee execution within environment limits.
2. **Memory Efficiency:** Do not store arrays of all primes or full race histories. Use running counters to track statistical metrics.
3. **Domain Strictness:** The analysis must remain entirely focused on the $a=1$ and $a=11$ modulo 210 coprime residue classes.

---
