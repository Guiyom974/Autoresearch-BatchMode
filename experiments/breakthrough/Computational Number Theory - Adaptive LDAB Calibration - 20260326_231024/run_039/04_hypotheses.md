**Research Hypotheses – Advanced Asymptotic Expansions & Analytic Continuation for LDAB Combinatorics**  

Below are **five concrete, testable hypotheses** that extend the prior “guarded log‑gamma” work (run 032) and the overflow‑detection study (run 027/028).  Each hypothesis is stated, justified as **empirically testable**, and accompanied by a concrete experimental plan that uses the same primorial‑gap data set and the same high‑precision “ground‑truth” pipeline (mpmath at ≥ 100‑digit precision) already employed in the earlier investigations.

---

## 1.  *Nemes’ expansion reaches the required 10⁻⁷ relative error for LDAB log‑Gamma terms up to the 10‑th primorial.*

**Hypothesis statement**  
Using a truncated Nemes asymptotic series ( log Γ(z) ≈ (z‑½)log z – z + ½log(2π) + 1/(12z) – 1/(360z³) + …)  with 5–6 terms) will compute the LDAB log‑Gamma components for all arguments ≤ P₁₀ (= 6 469 693 230) with a **relative error < 10⁻⁷**, safely beyond the current “k > 5” breakdown point.

**Why it is testable**  
*Ground‑truth* values for the exact log‑Gamma are already available from mpmath (≥ 100 decimal places).  The Nemes approximation is a deterministic closed‑form expression; we can directly compare its numeric output to the ground‑truth for any supplied argument.

**Experiment**  

| Step | Detail |
|------|--------|
| **a. Test matrix** | For each primorial order *k* = 1,…,10 generate 200 random integer arguments *z* in the range **[1, P_k]** that appear in LDAB binomial terms (e.g., *z* = P_k, P_k/2, P_k‑10). |
| **b. Exact reference** | Compute `logGamma_exact = mp.mpf(loggamma(z))` with 100‑digit precision. |
| **c. Nemes approximation** | Implement Nemes up to the term *1/(960960 z⁷)* (six terms) and evaluate `logGamma_approx`. |
| **d. Error metric** | `relErr = |exp(logGamma_approx) – exp(logGamma_exact)| / |exp(logGamma_exact)|`.  Record the maximum rel. error across all *z* for each *k*. |
| **e. Pass criterion** | “Pass” if **max relErr < 1 × 10⁻⁷** for every *k* ≤ 10. |

If the hypothesis holds, the LDAB pipeline can replace the failing guarded‑Stirling approach for the full target range.  If it fails for a particular *k*, the experiment will identify the smallest *k* where additional Nemes terms become necessary.

---

## 2.  *Analytic continuation via the Gamma reflection formula resolves the negative‑argument singularities that crash the LDAB binomial evaluator.*

**Hypothesis statement**  
When the LDAB model requires a binomial coefficient \(\binom{n}{k}\) with **negative integer *n* (e.g., *n* = −8)**, applying the analytic continuation identity  

\[
\binom{n}{k}=(-1)^{k}\,\binom{k-n-1}{k},
\]

followed by the Nemes expansion for the resulting **positive arguments**, will yield a finite, numerically stable value whose **relative error stays ≤ 10⁻⁷** relative to the mathematically defined analytic continuation (as given by mpmath’s `gamma` with complex arguments).

**Why it is testable**  
The right‑hand side of the identity always involves positive integers, which are safe for Nemes.  The left‑hand side is undefined in the naïve integer‑factorial definition, but mpmath can evaluate the Gamma function for negative arguments via its analytic continuation, providing a *gold‑standard* value.

**Experiment**  

| Step | Detail |
|------|--------|
| **a. Negative‑argument set** | Collect all *n* < 0 that appear in the LDAB binomial terms for *k* = 1,…,10 (e.g., *n* = −1, −2, …, −20). |
| **b. Gold‑standard** | Compute `binom_gold = mp.gamma(n+1) / (mp.gamma(k+1) * mp.gamma(n-k+1))` using mpmath’s Gamma with *complex* precision (≥ 80 digits). |
| **c. Continuation method** | For each pair (*n*, k*) compute `binom_cont = ((-1)**k) * binom(k-n-1, k)` where the inner binomial uses Nemes‑expanded log‑Gamma (as in Hypothesis 1). |
| **d. Error metric** | `relErr = |binom_cont – binom_gold| / |binom_gold|`. |
| **e. Pass criterion** | Pass if **max relErr < 1 × 10⁻⁷** for every negative *n* in the test set. |

A successful test would demonstrate that the LDAB framework can survive the “negative‑argument” failures that previously forced early termination.

---

## 3.  *The combined error of the Nemes expansion and analytic continuation stays below 10⁻⁷ in the LDAB density‑correction factor \(c(t)\), preserving a KL‑divergence < 10⁻⁴.*

**Hypothesis statement**  
When the new approximations replace the exact Gamma evaluations inside the **LDAB correction factor**  

\[
c(t)=\frac{\displaystyle\prod_{i} \binom{n_i}{k_i}}{\displaystyle\prod_{j} \binom{m_j}{\ell_j}},
\]

the resulting **relative error on *c(t)*** is ≤ 10⁻⁷, and consequently the **KL divergence** between the exact LDAB density and the approximated one remains **< 10⁻⁴** for all primorial bases *k* ≤ 10.

**Why it is testable**  
Both the exact and approximate versions of *c(t)* can be computed for the same set of LDAB parameters; the KL divergence can be evaluated either analytically (by integrating the density ratio) or numerically by sampling the LDAB distribution (e.g., using the primorial‑gap histogram).  The tolerance (10⁻⁴) is the a‑priori design goal, so a direct measurement is feasible.

**Experiment**  

| Step | Detail |
|------|--------|
| **a. Parameter set** | Use the full set of LDAB calibration parameters (the *n_i*, *k_i*, *m_j*, *ℓ_j*) that arise for *k* = 1,…,10. |
| **b. Exact *c(t)*** | Compute `c_exact` with full mpmath Gamma (≥ 100 digits). |
| **c. Approx. *c(t)*** | Compute `c_approx` by feeding the Nemes‑expansion log‑Gamma (Hypothesis 1) and the continuation binomial (Hypothesis 2) into the same formula. |
| **d. Error on *c(t)*** | `relErr_c = |c_approx – c_exact| / |c_exact|`. |
| **e. KL divergence** | Build the exact LDAB probability mass function (PMF) \(p(t)=c_{\text{exact}}\cdot p_0(t)\) and the approximated PMF \(q(t)=c_{\text{approx}}\cdot p_0(t)\). Compute `KL = sum(p(t) * log(p(t)/q(t)))` over the support (primorial gaps). |
| **f. Pass criteria** | 1) **max relErr_c < 1 × 10⁻⁷**; 2) **max KL < 1 × 10⁻⁴**. |

If both hold, the new approximations satisfy the **model‑stability** requirement; if either fails, the experiment will pinpoint whether the culprit is the per‑term error (needing more Nemes terms) or a structural sensitivity of *c(t)* that requires a different combinatorial formulation.

---

## 4.  *The Nemes‑based log‑Gamma evaluator runs **≥ 10× faster** than an arbitrary‑precision Gamma call while retaining the 10⁻⁷ accuracy target.*

**Hypothesis statement**  
For the LDAB parameter range (arguments ≤ P₁₀), the **CPU time** required to evaluate the **Nemes approximation (≤ 6 terms)** is at least **one order of magnitude lower** than the time needed for a comparable‑accuracy evaluation with mpmath’s `gamma` function (using ≥ 50‑digit precision).

**Why it is testable**  
Both methods are deterministic algorithms that can be timed repeatedly.  The speedup factor is a direct numeric ratio, making the hypothesis falsifiable.

**Experiment**  

| Step | Detail |
|------|--------|
| **a. Benchmark harness** | Use Python’s `time.perf_counter()` inside a loop that evaluates **10 000** random log‑Gamma calls for each method. |
| **b. Exact method** | `logGamma_exact = mp.loggamma(z)` with `mp.dps = 50` (≈ 166 bits). |
| **c. Nemes method** | `logGamma_nemes = nemes_log_gamma(z, terms=6)`. |
| **d. Warm‑up & repeats** | Perform 1 000 warm‑up calls to prime caches, then record **5 × 10⁴** timings for each method, compute mean and standard deviation. |
| **e. Pass criterion** | **Speedup = t_exact / t_nemes ≥ 10** (i.e., Nemes ≤ 10 % of the time). |

The experiment also records **throughput** (calls / second) for a realistic **real‑time streaming scenario** (e.g., updating LDAB calibration after each new primorial‑gap observation).  A ≥ 10× speedup confirms that the new expansions meet the “real‑time adaptive” constraint.

---

## 5.  *The Nemes approximation retains ≤ 10⁻⁷ error up to the 12‑th primorial (P₁₂) but degrades beyond P₁₃, establishing an operational ceiling for pure asymptotic evaluation.*

**Hypothesis statement**  
For primorial orders **k = 11–15** (P₁₁ ≈ 2 × 10¹³, P₁₂ ≈ 6 × 10¹³, P₁₃ ≈ 2 × 10¹⁵, P₁₄ ≈ 6 × 10¹⁶, P₁₅ ≈ 2 × 10¹⁸), the Nemes expansion (with the same 6‑term truncation) will **maintain relative error < 10⁻⁷** for **k ≤ 12**, but the error will **exceed 10⁻⁷ for k ≥ 13**.  This defines the **maximal primorial index** beyond which the framework must fall back to arbitrary‑precision arithmetic or higher‑order corrections.

**Why it is testable**  
We can generate ground‑truth values for the larger primorials with mpmath (still feasible for k ≤ 15 using increased digit settings) and compare them to Nemes outputs exactly as in Hypothesis 1.

**Experiment**  

| Step | Detail |
|------|--------|
| **a. Extended test matrix** | For *k* = 11,…,15, draw 200 random arguments *z* in **[1, P_k]**. |
| **b. Exact reference** | Compute `logGamma_exact` with mpmath at **200‑digit precision** (to ensure no rounding contamination). |
| **c. Nemes approximation** | Evaluate `logGamma_approx` with the same 6‑term Nemes formula used in Hypothesis 1. |
| **d. Error tracking** | Compute `relErr` for each (*k*, *z*) pair and plot **max relErr vs k**. |
| **e. Threshold detection** | Identify the smallest *k* where **max relErr ≥ 1 × 10⁻⁷**.  This *k* becomes the empirical “ceiling”. |
| **f. Pass criterion** | Hypothesis is **supported** if **k ≤ 12** passes and **k ≥ 13** fails, confirming a concrete operational bound. |

If the hypothesis fails (e.g., Nemes stays accurate beyond P₁₃), the experiment still yields valuable data on the *robustness* of the approximation and may suggest that the LDAB framework can be extended further without fallback.

---

### How These Hypotheses Build on Prior Work  

| Prior Finding | New Hypothesis Built Upon It |
|---------------|------------------------------|
| **Overflow detection at k = 132** (run 027) showed that pure double‑precision fails early. | **Hypotheses 1 & 4** test higher‑order approximations that avoid overflow and meet speed requirements, directly addressing the overflow issue for the *target* range (k ≤ 10). |
| **Guarded log‑gamma (Stirling) only modest stabilization** (run 032) could not push past k = 5. | **Hypothesis 1** replaces the guarded Stirling with a *Nemes* series, expecting a ten‑fold improvement in accuracy. |
| **VMR behaviour (drops at k = 8, rises thereafter)** hinted at subtle numerical instabilities. | **Hypothesis 3** directly measures the impact of approximation error on the LDAB *correction factor* and the KL divergence, tying the VMR observations to model‑level stability. |
| **No prior work on negative‑argument handling**. | **Hypothesis 2** introduces analytic continuation for the previously untested “negative‑n” binomial terms, a necessary step for a fully general LDAB evaluator. |
| **No performance benchmarking against arbitrary‑precision libraries**. | **Hypothesis 4** provides concrete evidence that the new asymptotic methods preserve the real‑time constraint. |
| **Exploratory “larger‑k” VMR trend** suggested possible future instabilities. | **Hypothesis 5** empirically maps the *accuracy ceiling* of the asymptotic series, giving a data‑driven stopping rule for future extensions. |

---

## Summary of Expected Outcomes  

| Hypothesis | Primary Metric | Pass Criterion |
|------------|----------------|-----------------|
| 1 – Nemes accuracy | Max relative error of log‑Gamma | < 10⁻⁷ for k ≤ 10 |
| 2 – Analytic continuation | Relative error on negative‑argument binomials | < 10⁻⁷ |
| 3 – LDAB model stability | Relative error of *c(t)* and KL divergence | < 10⁻⁷ and < 10⁻⁴ |
| 4 – Real‑time speed | Speedup factor vs. arbitrary‑precision | ≥ 10× |
| 5 – Operational ceiling | Largest k with < 10⁻⁷ error | k ≤ 12 (≥ 13 fails) |

If **all five hypotheses hold**, the research will have demonstrated a **complete, error‑controlled, and computationally efficient** path to extend the LDAB calibration framework to the full primorial base range (up to P₁₀) and beyond, while respecting the strict KL‑divergence and real‑time constraints.  Any failure will pinpoint the exact bottleneck (accuracy, analytic continuation, error propagation, or speed) that must be addressed in subsequent development.