

**Research‑wide context** –  
The problem asks us to (i) validate the LDAB (Logarithmic‑Density‑Adjusted Benford) model for bases other than 210, (ii) strengthen it with higher‑order prime‑number‑theorem (PNT) corrections, (iii) track the Chebyshev‑bias (NR‑QR) race beyond the 210‑ and 2310‑moduli, (iv) check that the multi‑GPU infrastructure scales cleanly to ≥ 8 devices, and (v) verify that the distributed summation can deliver at least seven‑digit numerical precision at \(N=10^{12}\).

Below are **four** tightly focused, **testable** hypotheses that together cover every success‑criterion. (A fifth optional hypothesis is offered at the end.)

---

## Hypothesis 1 – LDAB Generalisation to a Larger Primorial Base  

### 1. Statement  
*Unmodified LDAB (the model that uses the simple \(1/\ln x\) PNT term) will **fail** to describe the leading‑digit distribution of primes when the digit‑construction base is the primorial \(2310 = 2\cdot3\cdot5\cdot7\cdot11\).*  

Specifically, the KL‑divergence between the empirical leading‑digit frequencies (computed from a full enumeration up to \(N=10^{9}\)) and the LDAB prediction will be **\(>5\times10^{-2}\)**, whereas a **base‑specific geometric correction** that accounts for the non‑uniform spacing of digit intervals in base 2310 will bring the KL‑divergence **below \(10^{-3}\)**.

### 2. Why it is testable  
*Data*: We can generate the complete list of primes up to \(10^{9}\) in base 2310 using the already‑validated segmented‑sieve code on the 4‑GPU cluster.  
*Metric*: KL‑divergence is a well‑defined, non‑negative information‑theoretic distance; it can be computed to machine precision with double‑precision arithmetic.  
*Control*: The same code base (just changing the base parameter) yields both the “unmodified” and the “corrected” predictions, so the test is deterministic and repeatable.

### 3. Experiment that would test it  
1. **Sieve** all primes ≤ \(10^{9}\) **in base 2310** on the distributed GPU farm (≈ 389 chunks).  
2. **Tabulate** the leading‑digit counts for the primes in this base.  
3. **Compute** the LDAB prediction  
   \[
   P_{LDAB}(d)=\frac{\displaystyle\int_{d}^{\,d+1}\frac{1}{\ln t}\,dt}
                    {\displaystyle\int_{1}^{B}\frac{1}{\ln t}\,dt},
   \qquad B=2310,
   \]  
   and the **geometric‑corrected** version that replaces the uniform digit‑interval width by the actual interval lengths in base 2310 (the correction factor \(g(b)=\frac{\text{actual digit width}}{\text{uniform width}}\) is pre‑computed once).  
4. **Calculate** the KL‑divergence \(D_{\mathrm{KL}}(P_{\text{obs}}\|P_{\text{LDAB}})\) for both versions.  
5. **Statistical test**: Bootstrap the prime list (or use a χ² goodness‑of‑fit) to obtain a p‑value for the “unmodified” failure and confirm that the corrected version passes the \(<10^{-3}\) threshold.

---

## Hypothesis 2 – Higher‑Order PNT Corrections to LDAB  

### 1. Statement  
*Replacing the first‑order PNT term \(1/\ln x\) in the LDAB model with the logarithmic integral \(\operatorname{Li}(x)\) (augmented by the first 10 non‑trivial zeros of ζ) will reduce the KL‑divergence by **at least one order of magnitude** (factor ≥ 10) at both \(N=10^{10}\) and \(N=10^{12}\).*

### 2. Why it is testable  
*Feasibility*: The values of \(\operatorname{Li}(x)\) and the explicit zero‑sum  
\[
R(x)=\sum_{\rho}\frac{x^{\rho}}{\rho}
\]  
are computable to arbitrary precision using known tables of the first few ζ‑zeros; they can be added directly into the integrand of the LDAB formula.  
*Metric*: The KL‑divergence before and after the correction can be measured with the same prime‑count data, so the improvement is directly observable.  
*Scale*: The hypothesis makes a quantitative prediction (“factor ≥ 10”) that can be falsified if the measured reduction is smaller.

### 3. Experiment that would test it  
1. **Run the distributed sieve** up to \(10^{10}\) and \(10^{12}\) (the latter may need the full 8‑GPU cluster and possibly a few weeks of wall‑time; the experiment is designed to be feasible within the existing resource plan).  
2. **For each prime \(p\)**, compute the corrected density  
   \[
   \rho_{\text{corr}}(p)=\frac{1}{\ln p}\Bigl[1+\frac{1}{\ln p}+\frac{2\,\Re\,R(p)}{\ln p}\Bigr],
   \]  
   where the factor in brackets comes from the asymptotic expansion \(\operatorname{Li}(x)=x/\ln x\bigl(1+O(1/\ln x)\bigr)\) and the explicit zero‑term.  
3. **Aggregate** these densities over the appropriate digit intervals to obtain the corrected leading‑digit probabilities \(P_{\text{corr}}(d)\).  
4. **Compute KL‑divergence** for the original LDAB (\(P_{\text{old}}\)) and for the corrected model (\(P_{\text{corr}}\)) against the empirical frequencies.  
5. **Compare** the two divergences; the hypothesis is supported if  
   \[
   \frac{D_{\mathrm{KL}}(P_{\text{obs}}\|P_{\text{old}})}{D_{\mathrm{KL}}(P_{\text{obs}}\|P_{\text{corr}})}\ge 10.
   \]

---

## Hypothesis 3 – Chebyshev Bias (NR‑QR Race) Extends to Mod 30030  

### 1. Statement  
*The normalized difference*  

\[
\Delta_{30030}(x)=\frac{\#\{p\le x : p\equiv a\!\!\pmod{30030}\}-\#\{p\le x : p\equiv b\!\!\pmod{30030}\}}
{\displaystyle\frac{x}{\log x}}
\]  

*for any fixed quadratic‑non‑residue (NR) class \(a\) and quadratic‑residue (QR) class \(b\) will satisfy*  

\[
\Delta_{30030}(x)=C_{30030}\,\log\log x\;+\;o(\log\log x)
\]  

*for all \(x\) up to \(10^{9}\), where the constant \(C_{30030}>0\) is **statistically distinguishable from zero** (p < 0.01) and **scales roughly with the number of distinct prime factors** (i.e., \(C_{30030}\approx 6\,C_{210}\) reflecting the six primes in the modulus).*

### 2. Why it is testable  
*Theory*: The Rubinstein‑Sarnak framework predicts \(\Delta_{q}(x)\sim \名家(C_{q})\log\log x\) for any fixed modulus \(q\) under GRH. The hypothesis makes a concrete quantitative prediction that can be verified by a direct count.  
*Data*: The segmented sieve already produces all primes up to \(10^{9}\) for any modulus; we only need to tabulate the counts per residue class.  
*Statistical test*: Regression of \(\Delta_{30030}(x)\) against \(\log\log x\) yields a slope; its standard error can be used to compute a p‑value.

### 3. Experiment that would test it  
1. **Generate prime tables** for all residues modulo 30030 up to \(10^{9}\) using the GPU‑sieve (≈ 3 × 10⁷ primes).  
2. **Select a representative pair** (NR, QR) of residue classes (e.g., the classes that are quadratic non‑residues/residues for each of the six prime factors).  
3. **Compute** the cumulative counts \(N_{\text{NR}}(x)\) and \(N_{\text{QR}}(x)\) at a dense grid of \(x\) values (e.g., every \(10^{6}\) up to \(10^{9}\)).  
4. **Form** \(\Delta_{30030}(x)=\bigl(N_{\text{NR}}(x)-N_{\text{QR}}(x)\bigr)/\bigl(x/\ln x\bigr)\).  
5. **Fit** the linear model \(\Delta_{30030}(x)=C_{30030}\,\log\log x\) via ordinary least squares; obtain the estimate \(\hat C_{30030}\) and its standard error.  
6. **Test** the null hypothesis \(C_{30030}=0\) (t‑test) and confirm that the p‑value < 0.01.  
7. **Compare** \(\hat C_{30030}\) to the empirically measured constant for modulus 210 (previously reported ≈ 0.278) to see if the ratio is ≈ 6, as predicted.

---

## Hypothesis 4 – Linear Scaling Efficiency of ≥ 8 GPUs  

### 1. Statement  
*When the LDAB evaluation workload (the same 389 independent prime‑digit chunks) is distributed over **8 GPUs**, the parallel efficiency*  

\[
E_{8}=\frac{T_{1}}{8\,T_{8}}
\]  

*will stay **above 0.85** (i.e., ≥ 85 % of ideal linear speed‑up), with inter‑GPU communication overhead **≤ 10 %** of the total wall‑clock time. Moreover, weak‑scaling (problem size ∝ GPU count) will retain a **≥ 15‑percentage‑point advantage** over strong‑scaling (fixed total size) in overall throughput.*

### 2. Why it is testable  
*Measurables*: Wall‑clock times \(T_{1}\) (single‑GPU baseline), \(T_{4}\) (current 4‑GPU run), \(T_{8}\) (new 8‑GPU run) are directly recorded by the GPU‑scheduler. Communication time is logged separately.  
*Metrics*: Efficiency and overhead fractions are arithmetic combinations of those times; they do not rely on any modelling assumptions.  
*Reproducibility*: The same workload (identical chunk seeds) can be rerun on any compatible 8‑GPU node, so the test can be repeated across hardware generations.

### 3. Experiment that would test it  
1. **Baseline**: Run the full 389‑chunk LDAB evaluation on a **single GPU** and record total runtime \(T_{1}\).  
2. **Strong scaling – 4 GPUs**: Run the same workload on the existing 4‑GPU node, record \(T_{4}\).  
3. **Strong scaling – 8 GPUs**: Port the chunk distribution to an 8‑GPU machine (or emulate with two 4‑GPU nodes via NVLink‑connected bridges), run the identical workload, record \(T_{8}\).  
4. **Weak scaling – 8 GPUs**: Increase the total number of chunks to 2 × 389 (≈ 778) – i.e., problem size scales with GPU count – and run on 8 GPUs, recording runtime \(T_{8}^{\text{weak}}\).  
5. **Compute** efficiency:  
   \[
   E_{8}= \frac{T_{1}}{8\,T_{8}},\qquad 
   \text{overhead}_{\text{comm}} = \frac{T_{\text{comm}}}{T_{8}} .
   \]  
6. **Compare** the weak‑scaling throughput (chunks per second) to the strong‑scaling throughput to verify the ≥ 15 pp advantage.

---

## Hypothesis 5 (Optional) – Numerical Precision Floor of Distributed Hierarchical Summation  

### 1. Statement  
*At the largest scale \(N=10^{12}\), the distributed hierarchical summation carried out in **double‑precision (FP64)** will produce a KL‑divergence value that **differs from the high‑precision CPU reference (Kahan/Neumaier summation) by less than \(10^{-7}\)** (i.e., ≥ 7 significant decimal places). In contrast, the same algorithm using **single‑precision (FP32)** will have an error bounded by \(10^{-4}\).*

### 2. Why it is testable  
*Reference*: A single‑threaded, arbitrary‑precision (or at least 80‑bit) Kahan/Neumaier accumulation of the same prime‑digit counts yields a “ground‑truth” KL‑divergence.  
*Comparison*: The distributed FP64 result can be subtracted from the reference to obtain an absolute error; the same is done for FP32. Both errors are direct numbers that either satisfy or violate the stated bounds.  

### 3. Experiment that would test it  
1. **CPU baseline**: Implement the full LDAB evaluation for \(N=10^{12}\) on a single high‑core‑count CPU node using **Kahan (or Neumaier) compensated summation**; compute the KL‑divergence \(D_{\text{CPU}}\).  
2. **GPU FP64 run**: Execute the identical LDAB evaluation on the 8‑GPU cluster with **distributed hierarchical summation** in FP64; collect the partial sums and combine them with the same hierarchical tree (but still in FP64); compute \(D_{\text{GPU,FP64}}\).  
3. **GPU FP32 run**: Repeat step 2 but with **FP32** arithmetic throughout the hierarchical reduction; compute \(D_{\text{GPU,FP32}}\).  
4. **Error metrics**:  
   \[
   \epsilon_{\text{FP64}}=|D_{\text{CPU}}-D_{\text{GPU,FP64}}|,\qquad
   \epsilon_{\text{FP32}}=|D_{\text{CPU}}-D_{\text{GPU,FP32}}|.
   \]  
   Verify \(\epsilon_{\text{FP64}}<10^{-7}\) and \(\epsilon_{\text{FP32}}<10^{-4}\).

---

### How These Hypotheses Together Cover the Success Criteria  

| Success Criterion | Corresponding Hypothesis |
|-------------------|---------------------------|
| **LDAB Generalisation** (KL < 10⁻³ for at least one new primorial base) | Hypothesis 1 – shows the need for a base‑specific correction and provides a measurable threshold. |
| **Higher‑Order Improvement** (measurably lower KL with Li(x) / ζ‑zeros) | Hypothesis 2 – quantifies the factor‑10 gain. |
| **Chebyshev Extension** (log log x scaling for mod 30030, p < 0.01) | Hypothesis 3 – directly tests the Rubinstein‑Sarnak prediction at a new primorial. |
| **GPU Scaling Robustness** (≥ 85 % efficiency at 8 GPUs, < 10 % comm.) | Hypothesis 4 – supplies the empirical scaling data. |
| **Precision Floor** (≥ 7 dp at \(N=10^{12}\)) | Hypothesis 5 – validates numerical fidelity of the distributed summation. |

Each hypothesis is **operationally defined**, **falsifiable**, and **amenable to the computational infrastructure** already described in the problem statement. The experiments are concrete “run‑and‑measure” procedures that can be scheduled within the planned multi‑GPU campaign.