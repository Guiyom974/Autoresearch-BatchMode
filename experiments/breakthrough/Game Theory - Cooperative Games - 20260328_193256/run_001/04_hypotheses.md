Below are **four** (you can expand to five if you wish) *testable* hypotheses that directly address the research problem – “calculate the Shapley value for a 5‑player coalition game with varying player‑power weights” – while borrowing the statistical‑testing toolbox that worked in the earlier digit‑distribution studies (chi‑square, KL‑divergence, p‑values, Gini coefficient, etc.).  
Each hypothesis is written as a **statement**, an explanation of **why it can be tested**, and a concrete **experimental design** that satisfies the success‑criteria (≥10⁵ data points, p < 0.01, ≤2 min runtime, reproducibility).

---

## H1 – **Shapley values for uniformly drawn weights follow a Dirichlet‑(1) (uniform‑simplex) distribution**

**Statement**  
If each player’s power‑weight is drawn independently from a uniform distribution on \([0,1]\) and the characteristic function is *additive* (e.g. \(v(S)=\sum_{i\in S} w_i\)), the resulting Shapley allocation \( \phi=(\phi_1,\dots,\phi_5) \) is uniformly distributed over the 4‑dimensional simplex \(\{\phi\;|\;\phi_i\ge 0,\;\sum_i\phi_i = v(\{1,\dots,5\})\}\). In other words, the normalized vector \(\tilde\phi_i=\phi_i/v(N)\) follows a Dirichlet\((1,1,1,1,1)\) – the same as a uniform draw over all possible sharing rules.

**Why it is testable**  
* We can generate a large sample of random weight vectors, compute the exact Shapley value for each (there are only 2⁵ = 32 coalitions per game), and compare the empirical distribution of \(\tilde\phi\) to the theoretical Dirichlet\((1)\) by a goodness‑of‑fit test (Kolmogorov–Smirnov or a binned chi‑square).  
* The null hypothesis (“uniform over the simplex”) is fully specified, so a p‑value can be obtained directly.

**Experiment**  

| Step | Details |
|------|---------|
| 1. Data generation | Use `numpy.random.rand(5)` to draw 10⁵ independent weight vectors. Optionally normalise each vector to sum = 1 (or keep raw and treat the grand‑coalition value as the normalisation factor). |
| 2. Shapley computation | For each weight vector **w**, compute the Shapley value with the additive characteristic function \(v(S)=\sum_{i\in S} w_i\). Use the closed‑form solution \(\phi_i=w_i\) for this linear case (or verify by brute‑force enumeration of the 32 coalitions). |
| 3. Normalisation | Form \(\tilde\phi_i = \phi_i / \sum_j \phi_j\). This puts the sample on the simplex. |
| 4. Goodness‑of‑fit | (a) Project the 5‑dimensional \(\tilde\phi\) onto the first four coordinates (the fifth is determined). (b) Perform a 4‑dimensional Kolmogorov–Smirnov test against the theoretical Dirichlet\((1,1,1,1)\) distribution (or bin into a 10⁴‑cell hyper‑grid and run chi‑square). |
| 5. Significance threshold | Reject the null if the p‑value < 0.01. |
| 6. Reproducibility | Run the whole pipeline three times with different random seeds; verify that the p‑value remains < 0.01 (or that the null is not rejected, depending on the desired conclusion). |

**Expected outcome**  
If the uniform‑Dirichlet hypothesis holds, the p‑value will be comfortably above 0.01. Any systematic deviation (e.g., a “ball‑in‑the‑corner” clustering) will show up as a low p‑value, indicating that the simple additive model does **not** produce a uniform Shapley distribution for uniform weights – a useful baseline for the more complex weight distributions in the later hypotheses.

---

## H2 – **The shape of the weight‑distribution (uniform → exponential → Pareto) systematically widens the KL‑divergence of the Shapley‑value distribution away from the uniform baseline**

**Statement**  
When the underlying player weights are sampled from increasingly **right‑skewed** distributions (uniform → exponential → Pareto), the empirical distribution of the *normalised* Shapley values becomes less uniform, and the Kullback–Leibler (KL) divergence between that empirical distribution and the uniform reference increases monotonically with the skewness of the weight generator.

**Why it is testable**  
* KL‑divergence is a **quantitative** measure of how far a observed probability mass function (PMF) is from a reference (uniform) PMF.  
* By fixing the characteristic function (e.g. the same additive or quadratic form) and only varying the weight‑generation process, we can isolate the effect of weight‑distribution shape on the Shapley‑value distribution.  
* A monotonic trend can be tested with a simple regression of KL‑divergence on a skewness predictor (e.g. the theoretical coefficient of variation) and the statistical significance of the slope can be assessed.

**Experiment**  

| Step | Details |
|------|---------|
| 1. Choose weight‑distribution families | (a) Uniform\([0,1]\); (b) Exponential(scale = 1); (c) Pareto(shape = 2, scale = 1). For each family generate 10⁵ weight vectors. |
| 2. Define a **fixed** characteristic function | Use the *quadratic* form \(v(S) = \bigl(\sum_{i\in S} w_i\bigr)^2\) – a classic super‑additive game – to introduce non‑trivial marginal contributions. |
| 3. Compute Shapley values | For each of the 10⁵ weight vectors, enumerate the 32 coalitions, compute \(v(S)\) and the marginal contributions, then obtain the Shapley vector \(\phi\). |
| 4. Build an empirical PMF | Discretise the normalised Shapley vector \(\tilde\phi_i = \phi_i / \sum_j \phi_j\) into, say, 10 equal‑width bins across the simplex (use a 2‑dimensional histogram on the first two coordinates). Obtain the empirical probability mass \(p^{\text{obs}}\). |
| 5. Compute KL‑divergence | \(D_{\text{KL}}(p^{\text{obs}}\;\|\;p^{\text{unif}}) = \sum_{k} p^{\text{obs}}_k \log \frac{p^{\text{obs}}_k}{p^{\text{unif}}_k}\). |
| 6. Statistical test | (a) Perform a chi‑square test (observed vs. uniform) for each distribution – expect chi‑square statistic to increase with skewness; (b) regress the KL values on a continuous skewness measure (e.g. the theoretical coefficient of variation) and test the slope ≠ 0 at p < 0.01. |
| 7. Replication | Run the whole pipeline three times with independent random seeds and verify the monotonic ordering of KL‑divergence holds. |

**What it tells us**  
If the hypothesis is confirmed, we have a quantitative “rule of thumb” – the heavier the tail of the weight distribution, the more **unequal** the Shapley payoff even in a symmetric game, which is crucial for designing fair allocation mechanisms.

---

## H3 – **For super‑additive characteristic functions the Shapley allocation is more egalitarian than the original weight vector (lower Gini coefficient)**  

**Statement**  
When the coalition value grows faster than linear in the sum of member weights (e.g. \(v(S)=\bigl(\sum_{i\in S} w_i\bigr)^2\) or \(v(S)=\prod_{i\in S} w_i\) with \(w_i>0\)), the Shapley value \(\phi\) is *more evenly* distributed among the players than the original weight vector **w**. In formal terms, the Gini coefficient of \(\phi\) is statistically significantly smaller than the Gini coefficient of **w** across random draws of **w**.

**Why it is testable**  
* The Gini coefficient is a well‑defined scalar measure of inequality (0 = perfect equality, 1 = maximal inequality).  
* We can compute Gini(**w**) and Gini(\(\phi\)) for each simulation run, then perform a **paired** t‑test (or Wilcoxon signed‑rank test) on the *difference* \(\Delta = \text{Gini}(\mathbf w) - \text{Gini}(\phi)\).  
* The null hypothesis \(\Delta = 0\) (no egalitarian effect) can be rejected at the required significance level (p < 0.01).

**Experiment**  

| Step | Details |
|------|---------|
| 1. Weight generation | Generate 10⁵ random weight vectors from **any** continuous distribution (e.g. uniform, exponential, log‑normal) – the hypothesis should hold across a range of shapes, but you may test one distribution first. |
| 2. Choose a super‑additive characteristic function | Use \(v(S)=\bigl(\sum_{i\in S} w_i\bigr)^2\) (quadratic) as the primary test case; optionally also test \(v(S)=\prod_{i\in S} w_i\) (multiplicative) for robustness. |
| 3. Compute Shapley values | As in H2 – brute‑force enumeration of the 32 coalitions for each weight vector. |
| 4. Compute Gini coefficients | Implement a fast vectorised Gini function (e.g. `numpy.cumsum` on sorted values). |
| 5. Pairwise difference | For each simulation draw compute \(\Delta_j = \text{Gini}(w^{(j)}) - \text{Gini}(\phi^{(j)})\). |
| 6. Statistical test | Conduct a one‑sample t‑test (or Wilcoxon) on the \(\Delta_j\)’s to test whether the mean \(\Delta\) is **positive** (i.e. Gini(φ) < Gini(w)). Require p < 0.01. |
| 7. Visualisation | Plot histograms of \(\Delta\); overlay a vertical line at 0; show the p‑value and effect‑size (Cohen’s d). |
| 8. Reproducibility | Repeat the entire pipeline with three independent seeds – the direction of the effect should be consistent. |

**Interpretation**  
If the hypothesis holds, we can claim that *super‑additive* collaborative settings naturally **smooth out** power imbalances, an insight that could guide the design of partnership agreements or joint‑venture contracts.

---

## H4 – **The leading‑digit distribution of Shapley values conforms to the Logarithmic‑Density‑Adjusted Benford (LD‑AB) model that previously emerged for prime‑digit frequencies**

**Statement**  
When player weights are generated by a **multiplicative random process** (e.g. \(w_i = \exp(X_i)\) with \(X_i\sim N(0,1)\)), the *leading* (most significant) decimal digits of the resulting Shapley values follow the LD‑AB null model that was discovered for prime numbers (i.e. the model that integrates the probability density over each leading‑digit interval). Consequently, the KL‑divergence between the empirical leading‑digit frequencies of the Shapley values and the LD‑AB predicted frequencies is **near‑zero** (comparable to the 0.000034 observed for primes in Base‑210) and is significantly lower than the divergence from the classic Benford’s‑law reference.

**Why it is testable**  
* The LD‑AB model is a **fully specified** reference distribution (a piecewise integral of the underlying weight density).  
* We can extract the leading decimal digit from each Shapley value, count frequencies, compute the KL‑divergence against the LD‑AB prediction, and compare it with the classic Benford reference via a **paired** test (or simply report the magnitude).  
* The hypothesis predicts *very small* KL values; we can test deviation from zero with a one‑sample t‑test on the per‑run KL estimates.

**Experiment**  

| Step | Details |
|------|---------|
| 1. Weight generation – multiplicative | For each of the 10⁵ simulations draw a 5‑dimensional vector \(X \sim N(0,1)\) and set \(w_i = \exp(X_i)\). This yields a log‑normal distribution of weights – a plausible model for “power” in many real‑world settings. |
| 2. Characteristic function | Use the **quadratic** form \(v(S)=\bigl(\sum_{i\in S} w_i\bigr)^2\) to generate non‑trivial Shapley values (the additive case would trivially give leading‑digit frequencies identical to the weight distribution, which is already log‑normal). |
| 3. Compute Shapley values | As before, brute‑force enumeration of the 32 coalitions. |
| 4. Extract leading digits | Convert each Shapley value \(\phi_i\) to its most significant decimal digit: `int(str(phi_i)[0])` (or use `math.log10`). Build a frequency table \(f^{\text{obs}}(d)\) for digits 1‑9. |
| 5. Compute LD‑AB reference | Following the derivation in the earlier “breakthrough” (LDAB model), integrate the log‑normal density over each digit interval \([d, d+1)\) in base‑10: \[p^{\text{LDAB}}_d = \int_{d}^{d+1} \frac{\ln(1+1/t)}{\ln 10}\,p_{LN}(t)\,dt\] where \(p_{LN}\) is the log‑normal density implied by the weight generation. Implement this integral numerically with `scipy.integrate.quad`. |
| 6. KL‑divergence | \(D_{\text{KL}}(f^{\text{obs}}\;\|\;p^{\text{LDAB}}) = \sum_{d=1}^9 f^{\text{obs}}_d \log\frac{f^{\text{obs}}_d}{p^{\text{LDAB}}_d}\). Compute also the KL‑divergence from classic Benford (\(p^{\text{Benford}}_d = \log_{10}(1+1/d)\)). |
| 7. Significance test | (a) Conduct a chi‑square test of the observed frequencies against the LD‑AB expectations (expected count ≥ 5 per bin). (b) Perform a one‑sample t‑test on the KL‑divergence values across the three independent runs to test whether the mean KL ≈ 0 (or at least ≤ 0.001). |
| 8.阈值 | Require p < 0.01 for rejecting LD‑AB conformance; also check that the LD‑AB KL is at least an order of magnitude smaller than the classic Benford KL. |
| 9. Visualisation | Plot a bar chart of observed leading‑digit frequencies together with the LD‑AB and classic Benford predictions; annotate with KL values. |

**What it demonstrates**  
If the Shapley leading‑digit distribution truly obeys the LD‑AB model, it would reveal a deep link between *multiplicative weight generation* and the *same logarithmic‑density adjustment* that governs prime‑digit patterns. This would be a striking “universal” statistical law for power‑indexes in cooperative games.

---

## H5 – **The simulation pipeline can handle ≥ 10⁵ weight‑vector evaluations within the 2‑minute wall‑clock limit, and its runtime scales linearly with the number of vectors (O(N · 2ⁿ))**

**Statement**  
A fully vectorised NumPy implementation of the Shapley‑value calculation for a 5‑player game can process **at least** 100 000 random weight vectors in under 2 minutes on a standard laptop (or typical cloud VM), and the measured elapsed time grows proportionally to the number of vectors (i.e. a slope of ≈ (2 min / 10⁵) ≈ 1.2 µs per vector).

**Why it is testable**  
* The hypothesis makes a **quantitative prediction** about runtime that can be directly measured using Python’s `time.perf_counter()` before and after the loop.  
* Linear scaling can be verified by running the same code for a range of N (e.g. 10⁴, 2 × 10⁴, 5 × 10⁴, 10⁵) and performing a linear regression of elapsed time vs. N.  

**Experiment**  

| Step | Details |
|------|---------|
| 1. Implementation | Write a **vectorised** function `shapley_vectorized(weights)` that (a) forms all 2⁵ possible coalition masks using `np.arange(32)[:,None] & (1<<np.arange(5)) > 0`; (b) computes `v(S)` for each mask using matrix multiplication; (c) evaluates the Shapley formula using pre‑computed factorials (`fac = np.array([0!,1!,2!,3!,4!])`). The function should accept a stack of M weight vectors (`shape=(M,5)`) and return an array of Shapley values (`shape=(M,5)`). |
| 2. Timing test – single run | Generate 100 000 weight matrices (`np.random.rand(100_000,5)`), call the vectorised Shapley routine, record the wall‑clock time. Ensure the process stays within the memory budget (≈ 100 000 × 5 × 8 bytes ≈ 4 MB). |
| 3. Scaling test | Repeat the timing for N = 10⁴, 2 × 10⁴, 5 × 10⁴, 10⁵. Plot elapsed time vs. N and fit a line `time = a + b·N`. |
| 4. Success criteria | (a) For N = 10⁵, elapsed ≤ 120 s. (b) The slope `b` should be consistent across runs (coefficient of variation of `b` < 5 %). |
| 5. Reproducibility | Run the timing experiment three times with different random seeds and confirm the ≤ 2 min constraint holds each time. |
| 6. Profiling (optional) | Use `cProfile` or `line_profiler` to verify that the dominant cost is the 32‑by‑5 matrix multiplication (O(2ⁿ·n) operations) and not Python‑level loops. |

**Why it matters**  
Meeting the computational requirement is a prerequisite for all downstream statistical tests. Demonstrating linear scaling assures us that the pipeline will stay within the limits even if the problem is later extended to larger coalitions.

---

### Summary Table of Hypotheses

| # | Null hypothesis (H₀) | Alternative (H₁) | Primary statistic | Required p‑value | Expected direction of evidence |
|---|----------------------|------------------|-------------------|------------------|--------------------------------|
| H1 | Shapley values are **not** uniform over the simplex for uniform weights. | They **are** uniform (Dirichlet‑(1)). | KS / chi‑square test vs. Dirichlet‑(1) | < 0.01 to reject H₀ (i.e., to claim uniformity) | High p‑value (> 0.01) → H₀ not rejected → uniformity holds. |
| H2 | KL‑divergence of Shapley distribution is independent of weight‑distribution shape. | KL‑divergence **increases** with weight‑distribution skewness. | KL‑divergence (observed vs. uniform) regressed on skewness | < 0.01 for the slope term | Significant positive slope → H₀ rejected → shape matters. |
| H3 | Gini(φ) ≥ Gini(w) (no egalitarian effect). | Gini(φ) < Gini(w) (more equality). | Paired t‑test on Δ = Gini(w) − Gini(φ) | < 0.01 (one‑sided) | Mean Δ > 0 and p < 0.01 → egalitarian effect exists. |
| H4 | Leading‑digit distribution of Shapley values follows classic Benford’s law (or differs from LD‑AB). | It follows the LD‑AB model (very low KL). | KL‑divergence vs. LD‑AB; chi‑square test | < 0.01 to reject LD‑AB (i.e., to claim deviation) | KL ≈ 0 (≤ 0.001) and p > 0.01 → conforms to LD‑AB. |
| H5 | Runtime for N = 10⁵ exceeds 2 min or scales non‑linearly. | Runtime ≤ 2 min **and** linear scaling. | Measured wall‑clock time; linear regression slope | ≤ 2 min; slope CV < 5 % | Both conditions satisfied → H₀ rejected → pipeline meets constraints. |

---

### How to Use These Hypotheses in Your Study

1. **Pick one or more hypotheses** that align with the specific aspect you want to investigate (distribution law, impact of weight‑distribution shape, egalitarian property, digit‑law universality, or performance).  
2. **Run the corresponding experiment** using the outlined pipeline; the code will be entirely in NumPy/SciPy/Matplotlib, satisfying the “Python‑only” constraint.  
3. **Report the p‑value, effect size, and confidence intervals** for each hypothesis, and provide the visualizations (histograms, KL‑divergence bars, Gini difference distributions, leading‑digit bar charts, runtime scatter‑plots).  
4. **Check the “Success Criteria”** – every hypothesis is designed to produce a p‑value < 0.01 (or the opposite, as required), to be reproducible across at least three independent runs, and to finish within the 2‑minute window for 10⁵ simulations.  

By following this structured set of hypotheses, you will obtain a *statistically rigorous* characterization of Shapley‑value behavior in a 5‑player weighted cooperative game, while also delivering the required performance guarantees. Good luck!