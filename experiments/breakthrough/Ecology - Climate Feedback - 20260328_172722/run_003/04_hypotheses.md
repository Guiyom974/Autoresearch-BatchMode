**Research context (quick reminder)**  
- Run 001 of the 1‑D EBM reproduced the theoretical ice‑albedo exponent (α≈2.3) for the *isolated* albedo‑feedback case.  
- Run 002 coupled the albedo and cloud modules and obtained **NaN** power‑law coefficients together with a modest ΔT (≈4 K) – i.e. the coupled system is currently **unstable/undefined** under the default settings.  
- The literature and previous sensitivity work show that (i) land‑albedo and solar‑multiplier are the biggest drivers of variance, (ii) clouds have a dual cooling/warming role, and (iii) the choice of boundary conditions and numerical time‑step can shift a model from a stable power‑law regime into a chaotic or non‑convergent regime.

Below are **five testable hypotheses** that directly extend the above findings.  Each hypothesis (①‑⑤) is stated, followed by why it can be tested and what numerical experiment is required.

---

## 1.  Cloud‑albedo magnitude controls the **effective** albedo‑feedback exponent (α)

**Hypothesis statement**  
Within the physically plausible cloud‑albedo range (0.30 ≤ A<sub>cloud</sub> ≤ 0.80), the power‑law exponent that describes the ice‑albedo feedback (α) will **decrease monotonically** as A<sub>cloud</sub> increases.  At very high A<sub>cloud</sub> (≈0.70‑0.80) the fit will become ill‑conditioned and α will be undefined (NaN).

**Why it is testable**  
α is a direct output of the existing power‑law fitting routine (bounded nonlinear least‑squares).  By running the coupled model over a **discrete grid of A<sub>cloud</sub>** values, we can record whether the fitting algorithm converges and, if it does, the estimated α.  A systematic trend (or its absence) can be quantified with a simple regression of α vs. A<sub>cloud</sub>.

**Experiment**  
1. Fix all other parameters at their baseline values (e.g., solar multiplier = 1.0, baseline temperature = 288 K, time‑step = 0.1 yr).  
2. Run the coupled 1‑D EBM for **A<sub>cloud</sub> = 0.30, 0.35, …, 0.80** (≈11 levels).  
3. For each run, extract the time‑series of global‑mean temperature (T) and ice‑extent (I).  
4. Fit the relation  ΔT ≈ k·(ΔI)<sup>α</sup> (bounded least‑squares) and record α, k, and the fit‑quality (R², residual‑variance).  
5. Test for a statistically significant trend (Spearman correlation, α vs A<sub>cloud</sub>) and identify the threshold A<sub>cloud</sub> where the fit becomes NaN.

---

## 2.  Temporal resolution (Δt) biases the estimated feedback strength

**Hypothesis statement**  
Using integration time‑steps larger than **≈0.5 yr** introduces numerical diffusion that **over‑estimates** the sensitivity metric d(dT)/d(ice) (the slope of the temperature‑ice relationship) and inflates its variance.  Sub‑annual steps (Δt ≤ 0.1 yr) yield unbiased estimates that reproduce the analytical α ≈ 2.3 when clouds are turned off.

**Why it is testable**  
The sensitivity metric is computed **post‑integration** from the same time‑series used for the power‑law fit.  By varying Δt while keeping the physical model identical, we can compare the resulting d(dT)/d(ice) values and test whether their means differ significantly (ANOVA or Kruskal–Wallis).

**Experiment**  
1. Disable cloud feedback (A<sub>cloud</sub> = 0) to recover the baseline α ≈ 2.3 (validated in Run 001).  
2. Run the model with **Δt = 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0 yr** (7 levels).  
3. Compute the **finite‑difference sensitivity**  d(dT)/d(ice)  from each run (central differences, using the same ice‑loss interval, e.g., 5 %–15 % loss).  
4. Perform a **statistical test** (t‑test or Wilcoxon) to detect a step‑size effect; also compute the coefficient of variation (CV) as a proxy for numerical noise.  
5. Plot sensitivity vs Δt and identify the **critical Δt** above which bias exceeds, say, 10 % of the reference value.

---

## 3.  A critical cloud‑cover‑fraction scaling factor (C<sub>crit</sub>) demarcates stable vs. unstable feedback regimes

**Hypothesis statement**  
When the cloud‑cover‑fraction scaling factor (C<sub>scale</sub>, which multiplies the baseline cloud‑cover fraction) exceeds a **model‑specific threshold** (C<sub>crit</sub> ≈ 1.5–2.0), the power‑law fitting routine will **fail to converge** (NaN α, k).  Below this threshold the fits converge and α follows the trend identified in Hypothesis 1.

**Why it is testable**  
Convergence of the fitting algorithm is a binary outcome (converged / NaN) that can be recorded for each simulation.  By sweeping C<sub>scale</sub> across a plausible range (0.5 – 3.0) and noting the convergence status, we can locate C<sub>crit</sub> with a simple **break‑point analysis** (e.g., binary‑search or change‑point detection).

**Experiment**  
1. Keep A<sub>cloud</sub> fixed at a mid‑range value (e.g., 0.55) that is known to give convergent fits for the default C<sub>scale</sub>.  
2. Run the coupled model for **C<sub>scale</sub> = 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0** (9 levels).  
3. For each run, attempt the bounded least‑squares power‑law fit and record **convergence flag** (yes/No) and, if successful, α and k.  
4. Fit a **logistic regression** (convergence ~ C<sub>scale</sub>) to estimate C<sub>crit</sub> (the point where probability of convergence drops below 50 %).  
5. Validate C<sub>crit</sub> by performing a finer sweep around the estimated value (step = 0.05) to confirm the break‑point.

---

## 4.  Cloud and ice‑albedo feedbacks interact synergistically, producing a **second‑order** contribution to temperature variance

**Hypothesis statement**  
In the coupled system, the **total‑order Sobol index** of the cloud‑cover‑fraction scaling (C<sub>scale</sub>) will be significantly larger than its **first‑order** index, indicating a strong **interaction effect** between clouds and ice albedo.  The sum of the first‑order indices of C<sub>scale</sub> and ice‑albedo parameters will account for **< 70 %** of the total output variance, with the remainder attributable to their interaction.

**Why it is testable**  
Sobol’s variance‑based sensitivity analysis provides **first‑order (S₁)** and **total‑order (Sₜ)** indices for each parameter.  If Sₜ > S₁, an interaction (synergy) is indicated.  The analysis can be performed with the same model code by generating the large sample of model runs required for the Sobol estimator (typically > 10⁴ runs).

**Experiment**  
1. Define the parameter sample space:  
   - A<sub>cloud</sub> ∈ [0.30, 0.80]  
   - C<sub>scale</sub> ∈ [0.5, 3.0]  
   - Ice‑albedo parameter (A<sub>ice</sub>) ∈ [0.50, 0.85] (or the solar‑multiplier)  
   - Baseline temperature (T<sub>0</sub>) ∈ [260, 300] K (if the analysis is expanded later).  
2. Generate a **Sobol‑sequence** sample of N = 10 000 parameter sets covering the 3‑dimensional space.  
3. Run the coupled 1‑D EBM for each set (the same integration Δt found in Hypothesis 2).  
4. Compute the **output variance** (ΔT) and evaluate S₁ and Sₜ for each factor using the Saltelli decomposition algorithm.  
5. Compare S₁ vs. Sₜ for C<sub>scale</sub> and A<sub>ice</sub>.  If Sₜ(C<sub>scale</sub>) – S₁(C<sub>scale</sub>) > 0.10, declare a synergistic interaction.

---

## 5.  Extreme cloud‑albedo values (> 0.75) cause a **non‑monotonic** temperature response to ice loss, revealing a reversal of the expected warming trend

**Hypothesis statement**  
When cloud albedo is pushed to the upper bound of the realistic range (A<sub>cloud</sub> > 0.75), the global‑mean temperature **first rises** with ice loss (as expected) but then **decreases** as ice loss continues, producing a **U‑shaped T vs. I curve**.  This reversal is caused by the dominant cooling effect of highly reflective clouds overwhelming the albedo warming once the ice‑induced solar absorption is saturated.

**Why it is testable**  
The model can be forced into this regime by simply setting A<sub>cloud</sub> to the extreme values and examining the **trajectory** of T versus I over the full simulation (from full ice cover to ice‑free conditions).  The presence of a turning point can be detected with a **quadratic or spline regression** on the T‑I pairs.

**Experiment**  
1. Run the coupled model for **A<sub>cloud</sub> = 0.76, 0.78, 0.80** (3 levels).  
2. Record the time‑series of **global temperature** (T) and **ice‑extent** (I) until a steady‑state or a pre‑specified long integration time (e.g., 10 kyr) is reached.  
3. Plot **T as a function of I** and fit a **second‑order polynomial** (T = a·I² + b·I + c).  A significantly negative quadratic coefficient (a < 0) indicates a U‑shape.  
4. Perform a **bootstrap test** (1 000 resamples) to assess the significance of a < 0.  
5. Compare the turning point (maximum T) across the three extreme A<sub>cloud</sub> values to quantify the sensitivity of the reversal threshold.

---

### How the hypotheses relate to the prior findings  

| Prior result | New hypothesis that builds on it |
|--------------|-----------------------------------|
| **Run 001** – isolated albedo feedback gave α ≈ 2.3. | **H1** asks whether adding clouds systematically **modifies** that exponent, and **H2** checks whether the numerical method used to obtain 2.3 is itself robust to time‑step choice. |
| **Run 002** – coupled albedo‑cloud runs gave **NaN** fits. | **H3** directly targets the *boundary* (C<sub>crit</sub>) where the NaN problem emerges, while **H1** explores the *parameter dimension* (A<sub>cloud</sub>) that controls convergence. |
| Literature – cloud feedbacks dominate model‑to‑model spread. | **H4** quantifies the *variance contribution* of clouds vs. ice‑albedo using Sobol indices, and **H5** examines an *extreme* cloud scenario that is rarely tested but could explain the NaN outcome. |

---

## Summary Table of Hypotheses

| # | Hypothesis (one‑sentence) | Key Variable(s) | Expected Observable | Test |
|---|---|---|---|---|
| **1** | Cloud albedo magnitude linearly reduces the effective albedo‑feedback exponent α. | A<sub>cloud</sub> | α (fitted) vs. A<sub>cloud</sub> | Parameter sweep + regression |
| **2** | Integration time‑step > 0.5 yr biases the sensitivity d(dT)/d(ice) upward. | Δt | d(dT)/d(ice) and its CV | Multi‑Δt runs + ANOVA |
| **3** | A critical cloud‑cover‑fraction scaling factor C<sub>crit</sub> separates convergent from NaN regimes. | C<sub>scale</sub> | Convergence flag (yes/No) | Binary sweep + logistic regression |
| **4** | Cloud‑cover‑fraction scaling interacts synergistically with ice‑albedo, producing a large second‑order Sobol term. | C<sub>scale</sub>, A<sub>ice</sub> | Sₜ – S₁ for C<sub>scale</sub> | Sobol variance‑based SA (≥10⁴ runs) |
| **5** | Extreme cloud albedo (> 0.75) yields a non‑monotonic (U‑shaped) T vs. I trajectory. | A<sub>cloud</sub> > 0.75 | Quadratic coefficient a < 0 | Extreme‑A<sub>cloud</sub> runs + spline/quadratic fit |

Each hypothesis is **operationally testable** with the existing 1‑D EBM framework, **respects the imposed constraints** (1‑D, bounded parameters, no new biogeochemical cycles), and **directly addresses** the three research questions about cloud‑parameter stability, power‑law regime transitions, and temporal‑resolution effects.  Once the experiments are performed, the resulting phase‑space map (stable vs. unstable regimes) will satisfy the success criteria of eliminating NaN estimates and quantifying the sensitivity of α to cloud processes.