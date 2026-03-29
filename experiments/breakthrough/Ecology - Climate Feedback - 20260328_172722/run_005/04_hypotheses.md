# Testable Hypotheses for 2D Latitudinal EBM with Variable Heat Transport

Based on the research problem and prior findings, I propose five hypotheses that build on previous experiments without duplicating them. These hypotheses address the core issue: the model's current insensitivity to heat transport parameters.

---

## Hypothesis 1: Critical Threshold Hypothesis

**Statement:** There exists a critical value of the static horizontal heat transport coefficient (D_crit) above which the 2D latitudinal EBM exhibits significant bifurcation in global mean temperature and ice-edge position relative to the zero-transport baseline.

**Why it's testable:**
- Parameter sweeps across a logarithmic D range (0.01 to 100) can systematically identify where temperature deviates by ≥1.0 K or ice edge shifts by ≥5° latitude from the zero-transport baseline.
- This is measurable via the proposed statistical evaluation framework.

**Experiment to test it:**
1. Execute high-resolution parameter sweeps using static D values: 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 25.0, 50.0, 100.0.
2. For each D value, record final global mean temperature and ice-edge latitude.
3. Compute the deviation from zero-transport baseline at each D.
4. Identify D_crit as the smallest D where deviation exceeds the 1.0 K / 5° threshold.

**Rationale:** Prior work showed D=0.15 produced no divergence. This hypothesis posits that stronger amplification (orders of magnitude higher) is required to overcome the model's rigidity.

---

## Hypothesis 2: Gradient-Dependent Transport Alters Ice-Albedo Feedback Stability

**Statement:** Implementing a dynamic, temperature-gradient-dependent heat transport formulation (D ∝ ∇T) will weaken the ice-albedo feedback loop's positive feedback strength, resulting in a measurable reduction of the effective albedo feedback exponent (α) compared to the confirmed 1D baseline of α ≈ 2.3.

**Why it's testable:**
- The gradient-dependent formulation introduces a negative feedback: stronger polar cooling increases ∇T, enhancing poleward heat transport, which moderates cooling.
- This is quantifiable by fitting the power-law relationship between ice loss and temperature change across multiple experiments.

**Experiment to test it:**
1. Modify the 2D EBM diffusion term to: D(x, t) = D_base × (1 + k|∇T|), where |∇T| is the latitudinal temperature gradient.
2. Run experiments with k values: 0.1, 0.5, 1.0, 2.0, 5.0.
3. For each k, simulate incremental ice loss scenarios (vary solar irradiance or CO₂).
4. Fit power-law exponent α to the temperature–ice-loss curve for each k.
5. Compare α values to the static-D baseline (α ≈ 2.3 from 1D experiments).

**Rationale:** Prior findings showed static D=0.15 didn't alter sensitivity. A gradient-dependent scheme introduces spatial coupling that may counteract the runaway albedo feedback mechanism.

---

## Hypothesis 3: Extreme Transport Coefficients Enable Pole-to-Equator Forcing Propagation

**Statement:** Under extreme static heat transport coefficients (D ≥ 50), localized polar boundary changes (albedo variations) will propagate to mid-latitudes and alter global mean temperature, breaking the zero-transport insensitivity observed at D=0.15.

**Why it's testable:**
- Prior experiments with D=0.15 showed no propagation of polar albedo changes.
- Testing with D ≥ 50 isolates the effect of transport magnitude on spatial coupling.
- Outcome is measurable as statistically significant variance in mid-latitude temperatures across albedo conditions.

**Experiment to test it:**
1. Set D = 50 and D = 100 (extreme values based on Hypothesis 1 thresholds).
2. Run the model with polar albedo values: 0.40, 0.55, 0.70 (matching prior boundary conditions).
3. Record latitudinal temperature profiles for each albedo case.
4. Perform ANOVA or variance analysis to test whether polar albedo changes produce statistically significant temperature shifts at latitudes < 60°.

**Rationale:** This directly addresses Research Question 3 by testing whether "extreme or variable heat transport regimes" can transmit polar forcing globally.

---

## Hypothesis 4: Non-Linear Transport Regimes Induce Regime Shifts via Saddle-Node Bifurcation

**Statement:** The transition from low-sensitivity to high-sensitivity climate states in the 2D latitudinal EBM occurs via a saddle-node bifurcation as D increases, characterized by the coexistence of multiple stable equilibria over a narrow D range.

**Why it's testable:**
- Bifurcation analysis is computationally tractable in 1D/2D EBMs.
- Hysteresis behavior (multiple equilibria) can be detected by sweeping D up and down and comparing final states.
- Phase space mapping will reveal whether the transition is continuous or discontinuous.

**Experiment to test it:**
1. For D values near the critical threshold (identified in Hypothesis 1), perform both forward and backward sweeps:
   - Forward: Start from zero-ice state, gradually increase D.
   - Backward: Start from full-ice state, gradually decrease D.
2. Record final ice-edge latitude and global temperature for each direction.
3. If hysteresis loops appear (different final states for same D depending on initial conditions), this confirms saddle-node bifurcation.
4. Generate a 2D phase diagram: D vs. ice extent, showing stable/unstable branches.

**Rationale:** This extends beyond identifying a threshold (Hypothesis 1) to characterizing the *nature* of the transition—a key theoretical insight for understanding climate tipping points.

---

## Hypothesis 5: Variable/Amplitude-Modulated Transport Disrupts Steady-State Insensitivity

**Statement:** Time-varying or spatially heterogeneous heat transport coefficients (e.g., sinusoidal modulation or latitude-dependent amplification) will produce measurable transient climate sensitivities that differ from both static high-D and zero-transport steady states, even when time-averaged transport is equivalent.

**Why it's testable:**
- A variable transport scheme introduces temporal dynamics absent in static models.
- Comparative experiments can isolate the effect of variability vs. magnitude.
- Model outputs (temperature variance, ice-edge oscillation amplitude) are directly measurable.

**Experiment to test it:**
1. Implement three transport formulations:
   - **Static high-D**: D(t) = 50 (constant)
   - **Sinusoidally varying**: D(t) = 50 × (1 + 0.5 × sin(ωt)), with ω = 0.01, 0.1, 1.0 yr⁻¹
   - **Latitude-dependent**: D(φ) = 50 × (1 + δ × |φ|/90°), with δ = 0.5, 1.0, 2.0
2. Run each formulation to steady state (or 10,000 model years).
3. Compare:
   - Final global mean temperature
   - Ice-edge stability (steady vs. oscillating)
   - Total variance in latitudinal temperature profiles
4. Test whether variability alone (without changing mean D) alters climate sensitivity.

**Rationale:** This hypothesis addresses the possibility that *dynamics* in transport—rather than just magnitude—may be required to break the model's insensitivity. It builds on the prior finding that static D=0.15 and D=0 both yielded identical results.

---

## Summary Table

| Hypothesis | Independent Variable | Dependent Variable | Expected Outcome |
|------------|---------------------|--------------------|------------------|
| 1 | Static D (0.01–100) | ΔT_global, Δice_lat | Critical threshold D_crit identified |
| 2 | Gradient-dependent D (k values) | Albedo feedback exponent α | Reduced α due to stabilizing transport |
| 3 | Extreme D (50, 100) + polar albedo | Latitudinal temperature propagation | Mid-latitude sensitivity to polar changes |
| 4 | Bidirectional D sweeps near D_crit | Ice extent (forward vs. backward) | Hysteresis confirming bifurcation |
| 5 | Variable D (temporal/spatial) | Transient sensitivity, variance | Time-varying transport breaks insensitivity |

These hypotheses collectively address all three research questions while building on prior findings (confirmed α ≈ 2.3, D=0.15 insensitivity) without duplicating previous experiments.