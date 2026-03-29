
**Overview**

The earlier experimental series showed that *pure Python integer arithmetic* already avoids the floating‑point under‑flow that plagued the original float‑64 pipeline:

* gap counts and VMR for **k ≤ 5** are stable,  
* the variance‑to‑mean ratio scales roughly as **R(k) ∝ (log Pₖ)⁰·⁸⁰**, and  
* integer‑only code can compute the sum‑of‑squares for k = 5 without overflow.

The next step is to replace the integer “work‑around” with a **deliberately exact symbolic/arbitrary‑precision core** (e.g. rational factor‑caching, SymPy expressions, or GMP‑backed big‑int rationals).  
The five hypotheses below ask whether that exact core can (i) **match the known baselines exactly**, (ii) **run fast enough**, (iii) **fit in ordinary RAM**, (iv) **reproduce the observed scaling law**, and (v) **deliver a tangible speed‑up when intermediate results are reused**.

---

## Hypothesis 1 – Exactness (Zero‑Precision‑Loss)

**Statement**  
When the primorial‑gap pipeline is rebuilt with an exact symbolic/rational representation, the computed gap‑frequency tables and the resulting Variance‑to‑Mean Ratios (VMR) for **k ≤ 5** will agree with the mathematically proven baseline values with **0 % deviation**.

**Why it is testable**  
*Exact* means that the output can be compared bit‑for‑bit with the known exact values (e.g., the exact gap counts for 2#, 3#, 5#, 7#, 11# are tabulated in OEIS A057809‑A057813). Any numeric difference, however tiny, will show up as a non‑zero absolute error.

**Experiment**  
1. Implement the exact‑arithmetic pipeline (rational primorial generation, gap enumeration, VMR aggregation) using either Python’s `fractions.Fraction` combined with `gmpy2` big ints, or SymPy’s `Integer`/ ` Rational` types.  
2. Run the pipeline for k = 1,…,5.  
3. For each k, compute:
   * the full list of gaps,
   * the empirical VMR,
   * the sum‑of‑squares of the gaps.  
4. Compare each value to the corresponding known exact value (or, where a proof‑derived formula exists, evaluate the formula with exact arithmetic).  
5. Report the maximum absolute deviation (expected ≤ 10⁻⁶ in the worst case because of integer division; ideally exactly 0).  

**Acceptance criterion** – No deviation greater than the smallest representable integer (i.e., the output is *identical* to the baseline.

---

## Hypothesis 2 – Computational Overhead (Time Budget)

**Statement**  
For primorials up to **k = 7**, the wall‑clock time of the exact‑symbolic pipeline will be **no more than twice (≤ 2×) the time of a stripped‑down GMP‑only integer implementation** for the same set of gap‑enumeration tasks.

**Why it is testable**  
Both the symbolic version and a “baseline” GMP version can be benchmarked on identical hardware. Because the two codes perform the *same* algorithmic steps, any difference in runtime can be attributed to the extra bookkeeping of symbolic objects.

**Experiment**  
1. Write two modules:
   * **GMP‑only**: uses `gmpy2.mpz` for primorial multiplication, stores gaps as plain integers.
   * **Exact‑symbolic**: uses `gmpy2.mpz` for the underlying integer arithmetic but wraps each primorial factor in a *rational* or *factor‑cache* object (e.g., a `namedtuple(prime, exponent)` that stays symbolic). Gap generation still yields plain integers but the intermediate primorial is kept symbolic.
2. Run a fixed benchmark suite (e.g., generate `pₖ#`, enumerate all gaps, compute VMR) for k = 1,…,7, recording wall‑clock time with `time.perf_counter()`.  
3. Repeat each run ≥ 10 times to obtain mean and standard deviation.  
4. Compute the **time‑ratio** (symbolic / GMP‑only).  
5. Test the hypothesis with a one‑sided t‑test (α = 0.05) that the ratio ≤ 2.

**Acceptance criterion** – The 95 % confidence upper bound of the ratio is ≤ 2 for every k ≤ 7.

---

## Hypothesis 3 – Memory Footprint (RAM Constraint)

**Statement**  
The peak RSS (resident‑set size) of the exact‑symbolic pipeline when processing the **full gap map for k = 7** will stay **below 16 GB**, comfortably fitting the nominal 16‑32 GB workstation limit.

**Why it is testable**  
Memory consumption can be measured directly with OS‑level tools (`/usr/bin/time -v`, `tracemalloc`, `memory_profiler`). The gap map for k = 7 is the largest data structure the pipeline will create, so its size dominates the footprint.

**Experiment**  
1. Instrument the pipeline with `tracemalloc` (or use `valgrind --tool=massif` for C‑level extensions).  
2. Execute the pipeline for k = 7, storing **all gaps** in a compact format (e.g., a list of Python `int` objects, or a NumPy array of `object` dtype if needed).  
3. Record the **peak memory** during the run.  
4. Repeat three times to capture variance.  

**Acceptance criterion** – The smallest observed peak memory among the three runs is ≤ 16 GB.

---

## Hypothesis 4 – Scaling Law Preservation (VMR Exponent)

**Statement**  
The VMR of primorial gaps computed with the exact‑symbolic framework for **k = 1…7** will continue to follow the power‑law **R(k) ∝ (log Pₖ)⁰·⁸⁰** observed earlier, confirming that the new exact arithmetic does **not introduce any hidden numerical noise** that would alter the scaling exponent.

**Why it is testable**  
If the exact implementation truly eliminates rounding, the empirical VMR values should be *identical* to those obtained with pure integer arithmetic (which already produced the 0.80 exponent). Deviation from that exponent would signal subtle truncation or algorithmic differences.

**Experiment**  
1. Using the exact‑symbolic pipeline, compute VMR(k) for k = 1,…,7.  
2. Fit a linear model to the log‑log data: `log VMR = α + β · log log Pₖ`.  
3. Obtain the estimate **β̂** and its 95 % confidence interval (CI).  
4. Perform a two‑sided hypothesis test:  
   * H₀: β = 0.80 (the previously reported exponent)  
   * H₁: β ≠ 0.80  

**Acceptance criterion** – The 95 % CI for β̂ contains 0.80, and the point estimate lies in the interval [0.75, 0.85] (a pre‑specified tolerance window).

---

## Hypothesis 5 – Incremental Re‑Use (Caching Benefit)

**Statement**  
By **caching the symbolic primorial factorisation** (i.e., the list of prime‑exponent pairs) and reusing it for subsequent gap‑query operations, the average query time for a random gap (e.g., “what is the 10⁶‑th gap after pₖ#?”) will be **at least 50 % lower** than the time required when the same query is answered by recomputing the primorial from scratch each time.

**Why it is testable**  
We can generate a suite of *random* gap‑position queries, run the pipeline twice: once with caching enabled (store the symbolic primorial), once with caching disabled (clear the cache before each query). By measuring the per‑query elapsed time we obtain paired observations that can be compared with a paired t‑test.

**Experiment**  
1. For each k = 4,…,7:
   * **Cached run**: compute `pₖ#` symbolically once, then answer 1 000 random queries “gap at position n” using the stored factorisation.
   * **Uncached run**: before each query, regenerate `pₖ#` from primes (simulating a fresh calculation).  
2. Record the per‑query wall‑clock time for both strategies.  
3. Compute the **speed‑up factor** = (mean uncached time) / (mean cached time).  
4. Apply a **paired t‑test** (or Wilcoxon signed‑rank test) to the 1 000 paired differences to test whether the median speed‑up ≥ 1.5 (i.e., ≥ 50 % reduction).  

**Acceptance criterion** – The lower bound of the 95 % CI for the speed‑up factor is ≥ 1.5 for all tested k.

---

### Summary of the Experimental Programme

| # | Hypothesis | Primary Metric | Measurement Tool | Accept Criterion |
|---|------------|----------------|------------------|-------------------|
| 1 | Exactness (zero deviation) | Absolute error vs. known baselines | Custom compare script | Max error = 0 |
| 2 | Time overhead ≤ 2× GMP | Wall‑clock ratio (symbolic / GMP) | `time.perf_counter` | 95 % CI ≤ 2 |
| 3 | Memory ≤ 16 GB for k = 7 | Peak RSS | `tracemalloc` / `massif` | Peak ≤ 16 GB |
| 4 | VMR scaling exponent ≈ 0.80 | Log‑log slope β̂ | Linear regression (statsmodels) | β̂ ∈ [0.75, 0.85] with CI covering 0.80 |
| 5 | Caching gives ≥ 50 % speed‑up | Speed‑up factor (cached vs. recompute) | Per‑query timing + paired t‑test | Lower 95 % CI ≥ 1.5 |

If all five hypotheses are confirmed, we will have **demonstrated** that the exact‑symbolic framework:

* reproduces the established exact results without any precision loss,  
* runs fast enough to be practical on commodity hardware,  
* fits comfortably within the memory envelope of a typical workstation,  
* preserves the discovered scaling law (important for future theoretical work), and  
* offers a tangible performance gain when intermediate symbolic objects are reused.

These outcomes will constitute a solid, verified foundation for the next phase—extending the validated core to **k ≥ 8** and eventually to the full‑scale primorial‑gap problem.