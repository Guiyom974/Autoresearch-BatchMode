Based on the research problem and prior findings, we propose the following four testable hypotheses. Each builds on existing work and addresses key uncertainties about primorial gap VMR behavior at \(k \ge 8\), overflow artifacts, and LDAB calibration.

---

### Hypothesis 1: The observed VMR collapse at \(k=8\) is a 64-bit overflow artifact, not a genuine mathematical boundary effect.

**Statement:**  
The previously observed drop in variance-to-mean ratio (VMR) to 1.65 at \(k=8\) is caused by integer overflow in the intermediate sum of squared gaps during 64-bit arithmetic. Using arbitrary-precision arithmetic will yield a VMR that continues the upward trend observed for \(k < 8\).

**Why it's testable:**  
This hypothesis is directly testable by comparing VMR calculations using standard 64-bit integers/floats versus arbitrary-precision arithmetic (e.g., GMP) for the same primorial gaps at \(k=8\) and \(k=9\). If the arbitrary-precision VMR is significantly higher and aligns with an extrapolated trend, it confirms overflow as the cause.

**Experiment:**  
1. Generate primorial gaps for \(k=6\) to \(k=9\) (primes up to at least \(p_{12}=37\)).  
2. Compute VMR using two parallel tracks:  
   - **Track A:** 64-bit integers/floats (standard double or 64-bit integer accumulation).  
   - **Track B:** Arbitrary-precision integers for sums and high-precision floats for final division.  
3. Log the exact values of sum of gaps, sum of squared gaps, and VMR from both tracks at each \(k\).  
4. Determine the first \(k\) where Track A and Track B diverge, and identify the specific intermediate step (gap accumulation, square accumulation, or variance derivation) where overflow occurs.

---

### Hypothesis 2: The corrected VMR from arbitrary-precision arithmetic follows an extended scaling law with higher-order terms.

**Statement:**  
For \(k \ge 8\), the VMR of primorial gaps scales as  
\[
\text{VMR}(k) = \frac{1}{3} - \frac{C}{\log P_k} + \frac{D}{\log^2 P_k} + \frac{E}{P_k^\alpha} + \text{higher-order terms},
\]  
where \(P_k\) is the \(k\)-th primorial, and \(C, D, E, \alpha\) are constants fitted from data. This form extends the simple log-correction model that fails at \(k=8\).

**Why it's testable:**  
We can test this by fitting the proposed functional form to arbitrary-precision VMR values for \(k=1\) to \(k=9\) and evaluating the goodness of fit. Statistical tests (e.g., residual analysis, AIC comparison) can determine if the higher-order terms significantly improve the model.

**Experiment:**  
1. Using arbitrary-precision arithmetic, compute exact VMR for \(k=1\) through \(k=9\).  
2. Perform nonlinear regression to estimate parameters \(C, D, E, \alpha\) for the extended model.  
3. Compare the fit to the simple model (without \(D\) and \(E\) terms) using a statistical criterion (e.g., \(R^2\), p-values for additional terms).  
4. Validate by predicting VMR for a larger \(k\) (if computationally feasible) and checking against empirical values.

---

### Hypothesis 3: Boundary truncation systematically suppresses the VMR at \(k=8\), and applying mitigation increases it.

**Statement:**  
The variance of primorial gaps is artificially reduced by boundary effects at the start and end of the sequence. Removing a fraction of gaps near the boundaries (e.g., first and last 10%) will yield a higher VMR that better reflects the intrinsic distribution.

**Why it's testable:**  
We can test this by computing VMR with and without boundary truncation for the same \(k=8\) and \(k=9\) data. If the truncated VMR is significantly higher and more stable across different truncation windows, it suggests bias correction is necessary.

**Experiment:**  
1. Using arbitrary-precision arithmetic, compute the full-sequence VMR for \(k=8\) and \(k=9\).  
2. Apply a truncation window: remove the first and last \(x\%\) of gaps, where \(x\) varies (e.g., 5%, 10%, 15%).  
3. Compute VMR for each truncated dataset.  
4. Compare truncated VMR values to the full-sequence VMR and assess convergence as \(x\) decreases.  
5. Use statistical tests (e.g., bootstrap confidence intervals) to determine if the difference is significant and if an optimal truncation point exists.

---

### Hypothesis 4: Corrected VMR values from arbitrary-precision arithmetic improve LDAB density estimation accuracy.

**Statement:**  
The adaptive LDAB model's calibration factor \(c(t)\) will be more accurate when derived from overflow-free VMR values, leading to better prediction of large-gap densities in real-time primorial sequences.

**Why it's testable:**  
We can test this by comparing LDAB density predictions using the old (64-bit) VMR and the new (arbitrary-precision) VMR against empirical gap densities from known primorial datasets.

**Experiment:**  
1. For a set of primorial bases (e.g., \(k=6\) to \(k=9\)), compute the LDAB density estimate using both the old VMR (from 64-bit calculations) and the corrected VMR (from arbitrary-precision).  
2. Evaluate each estimate against empirical gap densities obtained from exhaustive enumeration of gaps.  
3. Compute error metrics (e.g., mean absolute error, root mean square error) for both approaches.  
4. Perform a statistical test (e.g., paired t-test) to determine if the corrected VMR significantly reduces prediction error.

---

These hypotheses address the core objectives: isolating the overflow artifact, validating the true VMR trajectory, correcting for boundary bias, and improving LDAB calibration. They build on prior findings that highlighted the \(k=8\) anomaly, suggested higher-order corrections, and noted boundary truncation effects, while introducing novel, feasible experiments to resolve open questions.