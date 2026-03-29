# Research Problem: Ecology - Climate Feedback

## Objective
Investigate the role of variable, gradient-dependent, and extreme horizontal heat transport coefficients in a 2D latitudinal Energy Balance Model (EBM). Previous experiments revealed that introducing a static, baseline horizontal heat transport ($D=0.15$) successfully resolved computational instabilities (NaNs) but failed to alter global climate sensitivity or ice extent compared to a zero-transport model. Both configurations yielded identical global mean temperatures and ice edges, remaining completely insensitive to polar boundary conditions. This research aims to determine if non-linear, temperature-gradient-dependent, or highly amplified heat transport parameters can break this rigid insensitivity and trigger dynamic spatial climate sensitivities.

## Research Questions
1. At what critical threshold of horizontal heat transport ($D$) does the global climate sensitivity and ice edge extent significantly diverge from the baseline zero-transport model?
2. How does implementing a dynamic, temperature-gradient-dependent heat transport formulation (where transport scales with $\nabla T$) alter the stability and strength of the ice-albedo feedback loop?
3. Can extreme or variable heat transport regimes successfully propagate localized polar boundary changes (e.g., polar albedo variations) to lower latitudes, thereby altering the global mean temperature?

## Methodology
1. **Parameter Sweeping**: Execute high-resolution parameter sweeps of the static heat transport coefficient across a logarithmic scale (e.g., $D = 0.01$ to $D = 100$) to identify bifurcation points or regime shifts in climate sensitivity.
2. **Dynamic Transport Implementation**: Modify the 2D EBM's diffusion term to represent non-linear meridional transport, calculating heat flow as a function of the local latitudinal temperature gradient rather than a constant background diffusion.
3. **Boundary Condition Re-testing**: Subject the new high-$D$ and dynamic-$D$ models to the previously tested polar albedo variations (0.40, 0.55, 0.70) to test if spatial coupling can now transmit polar forcing globally.
4. **Statistical Evaluation**: Quantify the variance in mean final temperature, ice-edge latitude shifts, and climate sensitivity ($K/(W/m^2)$) across the new parameter regimes.

## Success Criteria
1. Identification of a specific parameter regime or threshold where horizontal heat transport demonstrably changes the global mean temperature or ice extent by at least 1.0 K or 5 degrees latitude.
2. Successful implementation and simulation of gradient-dependent heat transport without reintroducing computational NaNs.
3. Generation of a phase space map detailing under what transport conditions the model becomes sensitive to localized polar albedo adjustments.

## Constraints
1. The research must remain strictly within the 2D latitudinal Energy Balance Model (EBM) framework.
2. Baseline solar irradiance and background greenhouse forcing must remain constant to strictly isolate the effects of horizontal heat transport.
3. The model must preserve the spatial resolution (latitudinal gradient) introduced in the previous iteration while ensuring mathematical stability at extreme parameter values.