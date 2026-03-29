
**Hypotheses –  Rigorous error analysis & boundary‑effect mitigation for the primorial‑gap variance ratio \(R(k)\) up to \(k=8\)**  

Below are **five** mutually‑complementary, **testable** hypotheses that build directly on the prior LDAB‑calibration and Wasserstein‑distance results.  Each is accompanied by (i) the exact statement, (ii) why the claim can be falsified, and (iii) the concrete numerical experiment that would supply the data to evaluate it.

---

## Hypothesis 1 – *Boundary truncation is the dominant source of the observed \(R(8)\) acceleration*

**Statement**  
The increase of the empirical variance‑to‑mean² ratio \(R(8)\) above the simple logarithmic‑correction prediction is **not a genuine mathematical deviation** but is **primarily caused by truncation artefacts at the ends of the primorial interval \([0,P_{8}]\)**.

**Why it is testable**  
If the acceleration disappears once all gaps that intersect the interval boundaries are *strictly* excluded (or correctly weighted), the hypothesis predicts a **significant drop** in the measured \(R(8)\).  Conversely, if the acceleration persists after boundary cleaning, the hypothesis is refuted.

**Experiment**  

| Step | Description |
|------|--------------|
| 1. | Re‑implement the primary gap‑generation pipeline with *strict* boundary handling: only gaps whose both endpoints lie in \([2,P_{k}]\) are retained; partial gaps at the leftmost or rightmost residue classes are discarded (or weighted by the exact fraction of the interval they occupy). |
| 2. | Generate the full gap list for \(k=8\) under this strict rule, compute \(R_{\text{strict}}(8)\). |
| 3. | **Control set**: recompute \(R_{\text{lenient}}(8)\) using the original “lenient” pipeline that tolerates boundary‑spanning gaps (the method that produced the anomalous acceleration). |
| 4. | Apply **bootstrap resampling** (10 000 replicates) on each of the two gap lists, obtain the 99 % confidence interval (CI) for each \(R\). |
| 5. | **Decision rule**: If the lower bound of the 99 % CI for \(R_{\text{strict}}(8)\) lies **below** the upper bound of the CI for the theoretical logarithmic prediction, the hypothesis is supported; otherwise it is rejected. |

*Outcome*: The experiment directly quantifies how much of the observed acceleration can be attributed to truncation.

---

## Hypothesis 2 – *After proper boundary cleaning, a statistically significant residual deviation of \(R(8)\) from the simple logarithmic model will remain*

**Statement**  
Even after eliminating boundary artefacts (as per Hypothesis 1), the corrected \(R(8)\) will **still lie outside the 99 % CI of the simple logarithmic‑correction model**, indicating a genuine mathematical signal (e.g., a higher‑order power‑law correction).

**Why it is testable**  
If the corrected ratio falls inside the CI, the simple model would be sufficient and no further structure would be needed.  The hypothesis predicts an **out‑of‑CI residual**, which can be tested by standard confidence‑interval logic.

**Experiment**  

| Step | Description |
|------|--------------|
| 1. | Use the *strictly* cleaned dataset from Hypothesis 1 to compute the **empirical mean** \(\mu_{8}\) and **empirical variance** \(\sigma^{2}_{8}\) of primorial gaps for \(k=8\). |
| 2. | Evaluate the simple logarithmic‑correction prediction \(R_{\log}(8)=\frac{\sigma^{2}}{\mu^{2}}\) (theoretical expression derived from the asymptotic model). |
| 3. | Generate **10 000 bootstrap replicates** of the cleaned gap list, recompute \(R\) for each replicate, and construct the 99 % CI. |
| 4. | **Decision rule**: If \(R_{\log}(8)\) lies **outside** the 99 % CI of the bootstrap distribution, the hypothesis is supported. |

*Outcome*: Confirmation or refutation of a genuine mathematical anomaly after boundary effects are removed.

---

## Hypothesis 3 – *An independent segmented‑sieve implementation will reproduce the same \(R(k)\) values (within statistical error), ruling out algorithmic bias*

**Statement**  
The primary gap‑generation pipeline suffers **no systematic algorithmic bias** that could inflate \(R(k)\).  An entirely different prime‑generation method (segmented sieve with isolated boundary tracking) will yield **statistically indistinguishable** estimates for \(R(6),R(7),R(8)\).

**Why it is testable**  
If the two methods disagree beyond the expected bootstrap uncertainties, a bias is present; agreement confirms pipeline fidelity.

**Experiment**  

| Step | Description |
|------|--------------|
| 1. | Build a **segmented sieve** that explicitly marks the exact start and end positions of each residue class modulo \(P_{k}\) inside \([0,P_{k}]\).  From this, extract the same gap list as the primary method but **without any implicit boundary handling**. |
| 2. | Compute \(R_{\text{seg}}(k)\) for \(k=6,7,8\). |
| 3. | For each \(k\), compute the **difference** \(\Delta_{k}=R_{\text{primary}}(k)-R_{\text{seg}}(k)\). |
| 4. | Estimate the **standard error** of each \(R\) via bootstrap on the primary dataset (from Hypothesis 1). |
| 5. | **Decision rule**: If \(|\Delta_{k}| \le 2.58\,\text{SE}_{k}\) (the 99 % two‑sided Z‑value) for all three \(k\), algorithmic bias is ruled out; otherwise the hypothesis is refuted. |

*Outcome*: Provides a *cross‑validation* checkpoint for the entire computational pipeline.

---

## Hypothesis 4 – *Finite‑sample error follows a predictable scaling law, measurable by subsampling the gap list*

**Statement**  
The **systematic error** on the variance‑to‑mean² ratio for a given \(k\) decays as a power of the number of observed gaps \(N\) (e.g., \(\propto N^{-\beta}\)).  This scaling can be recovered experimentally and can be **modelled quantitatively** to extrapolate the true asymptotic \(R(k)\).

**Why it is testable**  
If we plot the estimated error (e.g., \(|R(N)-R_{\text{true}}|\)) against \(N\) on log‑log axes, the hypothesis predicts a **straight line** with slope \(-\beta\).  Deviation from linearity falsifies the simple scaling model.

**Experiment**  

| Step | Description |
|------|--------------|
| 1. | From the full strict‑boundary dataset for \(k=8\), generate **sub‑samples** of increasing size: e.g., keep the first \(N=10^{3},10^{4},10^{5},\dots\) gaps (preserving order to mimic early‑stage sampling). |
| 2. | For each sub‑sample compute \(R(N)\) and the **bootstrap standard error** \(\text{SE}(N)\) (via 2 000 replicates). |
| 3. | Fit the model \(\text{SE}(N)=C\,N^{-\beta}\) (or the analogous model for the bias \(|R(N)-R_{\text{full}}|\)) using nonlinear least squares. |
| 4. | **Decision rule**: If the fitted exponent \(\beta\) is significantly non‑zero (p < 0.01) and the residuals are randomly distributed, the scaling law is supported; otherwise the hypothesis is rejected. |

*Outcome*: Gives a *quantitative error model* that can later be used to correct raw measurements for any finite‑size bias.

---

## Hypothesis 5 – *Wasserstein distance with non‑uniform weighting detects boundary artefacts earlier than KL divergence, enabling pre‑emptive correction at \(k=6\)*

**Statement**  
The **1‑dimensional Wasserstein distance** (earth‑mover distance) computed on the gap‑size distribution, with **non‑uniform residue‑class weighting** (as suggested by the prior “Wasserstein + non‑uniform weighting” finding), is **more sensitive** to boundary truncation than the KL divergence used earlier.  Consequently, it will flag a significant artefact already at \(k=6\), whereas KL divergence only shows a problem at larger \(k\).

**Why it is testable**  
If the Wasserstein distance **significantly larger** for the lenient‑boundary dataset at \(k=6\) while the KL divergence remains below its detection threshold, the hypothesis is upheld.  A simultaneous rise in both metrics would suggest equal sensitivity, falsifying the claim of superior sensitivity.

**Experiment**  

| Step | Description |
|------|--------------|
| 1. | Using the *strict* and *lenient* gap lists for each \(k=6,7,8\) (from Hypothesis 1), compute: <br> • **KL divergence** \(D_{\text{KL}}(P_{\text{lenient}}\|P_{\text{strict}})\) (histogram‑based, 50 bins). <br> • **Wasserstein distance** \(W_{1}(P_{\text{lenient}},P_{\text{strict}})\) with residue‑class weights proportional to the inverse of the primorial modulus (non‑uniform weighting). |
| 2. | **Control**: For each metric, generate **null distributions** by bootstrapping 5 000 times on the *strict* dataset (i.e., compare strict vs. a random sub‑sample of itself) to obtain 99 % significance thresholds. |
| 3. | **Decision rule**: If \(W_{1}\) exceeds its 99 % threshold **at \(k=6\)** while \(D_{\text{KL}}\) does **not**, the hypothesis is supported.  If both exceed thresholds at the same \(k\) or neither does, the hypothesis is refuted. |

*Outcome*: Provides a *diagnostic tool* that can catch boundary problems earlier, allowing corrective calibration before they corrupt higher‑order statistics such as \(R(k)\).

---

### How the Five Hypotheses Interlock

| # | Focus | Leverages Prior Work | Provides |
|---|-------|----------------------|----------|
| 1 | **Root‑cause test** – boundary truncation → observed \(R(8)\) excess | Dynamic LDAB calibration results on base‑210 show that boundary artefacts can be removed by careful handling | Direct evidence that truncation explains the anomaly |
| 2 | **Genuine‑signal test** – residual after cleaning | Same as H1, but asks whether any true deviation remains | Decides whether higher‑order corrections are needed |
| 3 | **Pipeline‑bias test** – algorithmic independence | Builds on the “cross‑validation” need expressed in the problem statement | Guarantees that results are not an artifact of a single code path |
| 4 | **Error‑model test** – systematic scaling with sample size | Extends the previous observation that KL/Wasserstein distances behave predictably with scale | Enables extrapolation to the true asymptotic value and informs future data‑collection strategies |
| 5 | **Diagnostic‑tool test** – sensitivity of divergence metrics | Directly follows the prior finding that Wasserstein distance is “more stable” and “more robust” than KL for multi‑scale LDAB | Supplies an early‑warning system for boundary problems, saving computational cost for higher \(k\) |

Together, they constitute a **comprehensive, falsifiable research agenda** that (i) isolates the source of the anomaly, (ii) validates whether any genuine mathematical signal survives, (iii) confirms the reliability of the computational pipeline, (iv) quantifies finite‑sample biases, and (v) equips the team with a superior diagnostic metric for future extensions to \(k\ge 9\).