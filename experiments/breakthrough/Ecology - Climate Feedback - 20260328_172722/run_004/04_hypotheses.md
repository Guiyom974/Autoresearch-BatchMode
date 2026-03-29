**Hypotheses – Multi‑dimensional Energy‑Balance Model (EBM) for Climate‑Feedback Research**  
*(All hypotheses are designed to be tested with the upgraded 2‑D latitudinal EBM described in the methodology. They build directly on the three prior findings: (i) the isolated albedo‑feedback exponent ≈ 2.3, (ii) the failure of a 1‑D albedo‑cloud coupling that produced NaNs, and (iii) the complete insensitivity of the 1‑D model to any boundary condition.)*  

---

## 1.  Horizontal heat transport introduces spatially **variable** climate sensitivity that depends on polar boundary conditions  

**Hypothesis statement**  
When a diffusion term for latitudinal heat transport is added, the 2‑D EBM will no longer produce the uniform temperature, albedo and ice‑cover fields observed in the 1‑D version. Instead, the model will generate distinct latitudinal gradients that respond systematically to changes in polar‑boundary parameters (e.g., imposed sea‑surface temperature, snow‑albedo, or cloud‑cover at the poles).

**Why it is testable**  
The hypothesis makes a clear, quantitative prediction: the **spatial variance** (or the inter‑quartile range) of temperature and ice‑fraction across latitude should increase from near‑zero (as in the 1‑D run) to a statistically significant value when horizontal diffusion is present. This can be measured with standard statistical tests (e.g., Levene’s test, ANOVA on latitude bands).

**Experiment that would test it**  
1. **Baseline 1‑D run** – replicate the earlier 1‑D EBM (no diffusion) and record the latitude‑resolved temperature \(T_i\) and ice‑fraction \(f_i\) for each latitude band \(i\). Confirm that the variance \(\sigma^2_{T,1D}\approx0\) and \(\sigma^2_{f,1D}\approx0\).  
2. **2‑D run** – enable the diffusion term (diffusivity \(D\) set to a physically plausible value, e.g. \(D=0.5\ \text{W m}^{-2}\,\text{K}^{-1}\) per degree latitude). Keep all other parameters identical to the 1‑D case.  
3. **Boundary‑condition perturbation series** – repeat the 2‑D run with a set of polar‑boundary changes:  
   * **Case A:** Increase the polar surface albedo by 0.1 (e.g., from 0.3 to 0.4).  
   * **Case B:** Raise the polar sea‑surface temperature (SST) by 2 K.  
   * **Case C:** Increase polar cloud‑cover fraction by 10 %.  
4. **Statistical comparison** – for each case compute the spatial variance \(\sigma^2_{T,2D}\) and \(\sigma^2_{f,2D}\). Use a two‑sample \(t\)‑test (or a non‑parametric Mann‑Whitney U) to test the null hypothesis \(\sigma^2_{T,2D}=0\). Reject the null (and accept H1) if any perturbation yields \(\sigma^2_{T,2D}>0\) at the 5 % significance level.  

*Expected outcome*: The 2‑D model will exhibit finite, latitude‑dependent structures that change systematically with the imposed polar boundary conditions, whereas the 1‑D model remains flat.

---

## 2.  There exists a **critical latitudinal‑heat‑diffusivity** (\(D_{\text{crit}}\)) that separates a globally ice‑stable regime from a regime of complete polar‑ice loss (a climate tipping point)  

**Hypothesis statement**  
By varying the diffusion coefficient \(D\) that governs meridional heat transport, the 2‑D EBM will display a bifurcation: for \(D<D_{\text{crit}}\) the global ice cover remains essentially permanent (stable ice‑line close to the poles), whereas for \(D>D_{\text{crit}}\) the ice‑line retreats equatorward dramatically, culminating in an ice‑free planet under the same solar forcing.

**Why it is testable**  
The statement predicts a sharp, identifiable transition in a continuous control parameter. In dynamical‑systems terms, it is a classic saddle‑node bifurcation that can be detected by a systematic parameter sweep and by computing the location of the ice‑edge latitude \(\phi_{\text{ice}}\) as a function of \(D\). The transition can be quantified with measures such as the derivative \(d\phi_{\text{ice}}/dD\) or by fitting a logistic curve and locating its inflection point.

**Experiment that would test it**  
1. **Parameter sweep** – run the 2‑D EBM for a range of diffusivity values from \(D=0.0\) (no transport) up to \(D=3.0\ \text{W m}^{-2}\,\text{K}^{-1}\) in steps of 0.1 (or finer near the suspected threshold). For each \(D\) record the **global mean ice‑fraction** \(\bar{f}_{\text{ice}}\) and the **poleward ice‑edge latitude** \(\phi_{\text{ice}}\).  
2. **Identify the threshold** – plot \(\bar{f}_{\text{ice}}\) vs. \(D\) and \(\phi_{\text{ice}}\) vs. \(D\). Locate the point where \(\bar{f}_{\text{ice}}\) drops below, say, 5 % of its maximum value; define this \(D\) as \(D_{\text{crit}}\). Perform a **bifurcation analysis** (e.g., compute the Jacobian of the discretized system and look for the eigenvalue crossing zero).  
3. **Sensitivity analysis** – repeat the sweep under a modest increase in solar constant (+1 %) and under a 10 % increase in atmospheric CO₂ (using the prescribed radiative‑forcing parameter). Determine whether \(D_{\text{crit}}\) shifts, thereby testing the robustness of the tipping point.  

*Expected outcome*: A clear nonlinear drop in \(\bar{f}_{\text{ice}}\) (or a rapid equatorward shift of \(\phi_{\text{ice}}\)) will be observed at a specific \(D\) value, confirming the existence of a diffusion‑controlled tipping point.

---

## 3.  The **latitude‑specific albedo‑feedback exponent** deviates from the 1‑D benchmark (≈ 2.3) in regions where cloud feedback is active, leading to a spatially heterogeneous feedback strength  

**Hypothesis statement**  
When cloud cover is allowed to vary with latitude in the 2‑D model, the local power‑law relationship between temperature anomaly \(\Delta T(\phi)\) and the change in absorbed solar radiation (i.e., the feedback exponent) will differ from the globally averaged value of 2.3. In particular, latitudes with strong low‑level cloud formation will exhibit a **lower effective exponent** (because clouds offset part of the albedo warming), while cloud‑free polar latitudes will retain an exponent close to 2.3.

**Why it is testable**  
The hypothesis makes a quantitative, spatially explicit prediction that can be tested by fitting a power‑law \(\Delta R_{\text{abs}}(\phi)=k(\phi)\,\Delta T(\phi)^{\alpha(\phi)}\) to model output from each latitude band. The fitted \(\alpha(\phi)\) can be compared across bands using a confidence‑interval test; a difference of > 0.2 units (larger than the Monte‑Carlo uncertainty) would constitute evidence for the hypothesis.

**Experiment that would test it**  
1. **Implement a simple cloud‑feedback scheme** – for each latitude band, define a latitude‑dependent cloud‑cover fraction \(c(\phi)\) that is a function of local temperature (e.g., \(c(\phi)=c_{\max}\tanh[\beta(T(\phi)-T_0)]\)). The scheme should increase high‑latitude cloudiness slightly with warming (a weak positive cloud‑feedback) while decreasing tropical cloudiness (a negative feedback).  
2. **Run a series of 2‑D simulations** – apply a suite of uniform radiative forcings (e.g., +1, +2, +3 % solar constant; +10, +20, +30 % CO₂) to generate a range of global mean temperature anomalies \(\Delta \bar{T}\).  
3. **Extract latitude‑resolved quantities** – for each latitude band compute the local temperature anomaly \(\Delta T(\phi)\) and the corresponding change in absorbed solar radiation \(\Delta R_{\text{abs}}(\phi)\). Perform a log‑log linear regression for each band to estimate \(\alpha(\phi)\) and \(k(\phi)\).  
4. **Statistical comparison** – plot \(\alpha(\phi)\) versus latitude; test whether the mean \(\alpha\) in the high‑latitude, high‑cloud band differs from the low‑latitude, low‑cloud band at the 95 % confidence level. Also compare the latitude‑averaged \(\alpha\) to the previously measured 1‑D value (≈ 2.3).  

*Expected outcome*: \(\alpha(\phi)\) will be ≈ 2.3 in polar, cloud‑poor regions and will be noticeably smaller (e.g., 1.7–2.0) in latitudes where the cloud feedback is strong, confirming spatial heterogeneity of the feedback exponent.

---

## 4.  Coupling ice‑albedo and cloud feedbacks in a **2‑D framework** yields **localized stabilization** that prevents the global NaN‑failure observed in the 1‑D runs, and produces **regional tipping points** rather than a single global transition  

**Hypothesis statement**  
The NaN collapse seen in the 1‑D coupled albedo‑cloud experiment was a consequence of an unstable feedback loop that lacked spatial averaging. Adding meridional heat diffusion will damp the runaway loop, yielding numerically stable solutions. Moreover, the stable 2‑D system will exhibit *multiple* local tipping points—e.g., an Arctic ice‑loss threshold and an Antarctic ice‑loss threshold—that are geographically separated rather than a single global bifurcation.

**Why it is testable**  
The hypothesis predicts both **numerical stability** (no NaNs) and **bifurcation structure** (multiple thresholds). Stability can be verified directly by running the coupled model for a wide range of time steps and observing whether the integration remains finite. The presence of separate thresholds can be detected by performing a sweep of a global forcing parameter (e.g., solar constant) and tracking both \(\phi_{\text{ice,Arctic}}(F)\) and \(\phi_{\text{ice,Antarctic}}(F)\); a clear separation of the two transition points indicates independent regional tipping points.

**Experiment that would test it**  
1. **Re‑implement the coupled albedo‑cloud scheme** in the 2‑D model, using the same temperature‑dependent cloud‑cover function introduced in H3, but now allowing the surface albedo to depend on local ice presence (binary ice‑albedo switch).  
2. **Integration‑stability test** – run the coupled model with three different explicit time steps (Δt = 1 h, 0.5 h, 0.1 h) and two implicit solvers (forward Euler, Crank‑Nicolson). Record whether any simulation produces NaN values in temperature, albedo, or cloud variables after 10 yr of integration.  
3. **Forcing‑threshold sweep** – start from a baseline solar constant \(S_0\) and increase it in increments of 0.5 % up to +5 %. For each forcing level, record the equilibrium ice‑edge latitudes for the Arctic (\(\phi_{\text{A}}\)) and Antarctic (\(\phi_{\text{AA}}\)). Identify the forcing level at which each pole loses > 50 % of its initial ice area; define these as the regional tipping points \(F_{\text{A}}^*\) and \(F_{\text{AA}}^*\).  
4. **Comparison** – test whether \(F_{\text{A}}^*\) and \(F_{\text{AA}}^*\) are statistically different (e.g., via bootstrap confidence intervals). If they differ by > 0.5 % of the solar constant, the hypothesis of independent regional tipping points is supported.  

*Expected outcome*: The 2‑D coupled model will converge to stable, finite solutions for all tested time steps, and the Arctic and Antarctic ice edges will undergo abrupt transitions at distinct forcing levels, confirming the emergence of multiple regional tipping points.

---

## 5.  The **hemispheric asymmetry** in the model’s response to polar‑albedo perturbations is governed by the **initial ice‑distribution and continental configuration**, leading to a larger temperature sensitivity in the hemisphere with more ocean‑covered polar cap  

**Hypothesis statement**  
When identical albedo perturbations are applied to the Arctic and Antarctic (e.g., a 0.1 increase in surface albedo at the pole), the resulting change in global mean temperature (\(\Delta T_{\text{global}}\)) and the shift in the ice line will be **significantly larger in the Arctic** because the Arctic is ocean‑dominated and has a lower initial albedo than the Antarctic (which is land‑dominated). This asymmetry will be amplified by the latitudinal heat‑transport term.

**Why it is testable**  
The hypothesis predicts a measurable difference in the climate‑sensitivity metric \(\Delta T_{\text{global}}\) (or in \(\Delta\phi_{\text{ice}}\)) between the two polar regions when identical perturbations are imposed. The test requires a paired experimental design: apply the same perturbation to both poles, then compare the responses using a paired \(t\)‑test (or a non‑parametric Wilcoxon signed‑rank test). The hypothesis also implies that the asymmetry will grow as the diffusion coefficient \(D\) increases, because stronger meridional transport will transport the extra heat from the perturbed pole toward the equator, thereby amplifying the temperature signal.

**Experiment that would test it**  
1. **Initialize two 2‑D runs** – one with the Arctic having an ocean‑filled polar cap (standard configuration) and the Antarctic having a land‑filled polar cap (or vice‑versa). Use the same baseline parameters (solar constant, CO₂, cloud scheme) for both runs.  
2. **Apply identical polar‑albedo perturbations** – increase the polar surface albedo by 0.1 in **both** the Arctic and the Antarctic (in separate runs, and then simultaneously).  
3. **Record the response** – after the model reaches a new steady state (or after a fixed integration period of 50 yr), compute:  
   * \(\Delta T_{\text{global}}\) (global mean temperature change).  
   * \(\Delta \phi_{\text{A}}\) (Arctic ice‑edge shift in degrees latitude).  
   * \(\Delta \phi_{\text{AA}}\) (Antarctic ice‑edge shift).  
4. **Statistical analysis** – for the paired comparison (same model, same perturbation applied to each pole separately), test whether \(|\Delta \phi_{\text{A}}| > |\Delta \phi_{\text{AA}}|\) and whether \(\Delta T_{\text{global}}\) is larger when the perturbation is applied to the Arctic. Use a one‑sided paired \(t\)‑test (or bootstrap) with α = 0.05.  
5. **Sensitivity to diffusion** – repeat the entire experiment with a **high‑diffusivity** case (\(D = 1.5\ \text{W m}^{-2}\,\text{K}^{-1}\)) to see if the asymmetry grows.  

*Expected outcome*: The Arctic perturbation will produce a larger \(\Delta T_{\text{global}}\) and a larger equatorward ice‑edge shift than the Antarctic perturbation, especially at higher \(D\), confirming that hemispheric asymmetry is controlled by initial ice distribution and heat transport.

---

### How the Hypotheses Build on Prior Findings  

| Prior Finding | Direct Link to New Hypotheses |
|----------------|-------------------------------|
| **Albedo‑feedback exponent ≈ 2.3** (run 001) | **H3** uses this benchmark to test whether the exponent becomes latitude‑dependent when cloud feedback is added. |
| **Failed 1‑D albedo‑cloud coupling (NaNs)** (run 002) | **H4** specifically addresses why spatial coupling (horizontal diffusion) should resolve the instability and produce realistic regional tipping points. |
| **1‑D model showed no sensitivity to any boundary condition** (run 003) | **H1** directly tests whether the introduction of a diffusion term restores sensitivity; **H5** investigates whether the sensitivity differs between hemispheres. |
| **General need for spatial heterogeneity** (web‑search literature) | **H2** adds a quantitative diffusion threshold (tipping point) that is a classic prediction of multi‑dimensional EBMs; **H4** expands the cloud‑feedback analysis beyond the simple 1‑D treatment. |

---

#### Quick Summary of Each Hypothesis  

| # | Hypothesis (one‑sentence) | Key Test | Primary Variable(s) |
|---|---------------------------|----------|---------------------|
| 1 | Horizontal heat transport makes the 2‑D EBM sensitive to polar boundary conditions, producing non‑uniform latitudinal temperature/ice fields. | Compare spatial variance of temperature/ice between 1‑D and 2‑D runs under identical boundary‑condition changes. | \(\sigma^2_T, \sigma^2_f\) across latitude. |
| 2 | A critical meridional diffusivity \(D_{\text{crit}}\) separates a globally ice‑stable regime from an ice‑free regime. | Parameter sweep of \(D\) and locate abrupt loss of ice cover. | Global ice‑fraction \(\bar{f}_{\text{ice}}\) vs. \(D\). |
| 3 | The local albedo‑feedback exponent \(\alpha(\phi)\) varies with latitude, being lower where cloud feedback is strong. | Fit power‑law per latitude band and compare \(\alpha(\phi)\). | \(\alpha(\phi)\) and \(k(\phi)\). |
| 4 | Spatial coupling of ice‑albedo and cloud feedbacks yields numerically stable solutions and produces independent Arctic and Antarctic tipping points. | Check for NaN stability and identify separate forcing thresholds for each pole. | Presence of NaNs, \(F^*_{\text{A}}, F^*_{\text{AA}}\). |
| 5 | Arctic and Antarctic responses to identical albedo perturbations are asymmetric, with the ocean‑dominated Arctic showing larger temperature sensitivity. | Paired perturbation experiment, measure \(\Delta T_{\text{global}}\) and ice‑edge shifts for each pole. | \(\Delta T_{\text{global}}, \Delta \phi_{\text{A}}, \Delta \phi_{\text{AA}}\). |

These hypotheses together address the three core research questions: (i) how spatial dimensions affect boundary‑condition sensitivity, (ii) where and how tipping points arise in a multi‑dimensional EBM, and (iii) how the rate of meridional heat diffusion controls global ice stability. Each is formulated to be directly testable with the planned 2‑D EBM, staying within the idealized‑EBM framework and respecting the coarse latitudinal resolution (10–18 bands).