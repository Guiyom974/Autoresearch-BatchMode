

Below are **five concrete, testable hypotheses** that directly address the three research questions in the problem statement.  
Each hypothesis is written as a **formal H₀/H₁ pair**, the reason it can be tested with the data we can generate, and the exact computational experiment that would be used to accept or reject it.

---

## 1.  **H1 – Benford’s Law explains the bulk of the observed KL‑divergence**

| | |
|---|---|
|**H₀**|The leading‑digit distribution of Base‑210 primes is **exactly** the Base‑210 generalized Benford distribution ( P(d)=log₂₁₀(1+1/d) ). In other words, the KL‑divergence between the observed distribution and the Benford baseline is **zero** (or indistinguishable from zero after sampling error).|
|**H₁**|A non‑zero residual KL‑divergence remains after the Benford component is removed, indicating a *primorial‑specific* artifact beyond Benford’s Law.|

### Why it is testable
* We can **compute the exact Benford probabilities** for every digit 1–209 in base‑210.  
* From a generated list of primes (≥ 10⁸) we can count the empirical leading‑digit frequencies and compute the KL‑divergence to the Benford baseline, D_KL(obs ‖ Benford).  
* By bootstrapping the prime list (or using a Monte‑Carlo simulation of a Benford‑consistent sequence) we can obtain a sampling distribution of D_KL(obs ‖ Benford) and test whether it is significantly > 0.

### Experiment that would test it
1. **Prime generation** – Sieve all primes up to 10⁸ (or a larger bound if computationally feasible).  
2. **Base‑210 conversion** – For each prime p, write p in base 210 and extract the most‑significant digit d₁(p).  
3. **Observed frequency table** – Count N(d) = #{p ≤ 10⁸ : d₁(p)=d} for d = 1,…,209.  
4. **Benford reference** – Compute P_B(d)=log₂₁₀(1+1/d).  
5. **KL‑divergence** –  
   \[
   D_{\text{obs}} = D_{KL}\bigl(N/ \sum N \;||\; P_B\bigr)
   \]  
   (use natural‑log KL in base‑e, then convert to bits for readability).  
6. **Bootstrap confidence interval** – Resample 10 000 subsets of the prime list (each of size ≈ 0.8·10⁸) and recompute D_KL each time; the 2.5 %–97.5 % quantiles give a 95 % CI for D_KL(obs ‖ Benford).  
7. **Proportion explained** –  
   \[
   \text{% explained} = \frac{D_{KL}(\text{obs ‖ uniform}) - D_{KL}(\text{obs ‖ Benford})}{D_{KL}(\text{obs ‖ uniform})}\times100\%
   \]  
   where the uniform baseline is the 1/209 expectation.  

**Decision rule:** If the 95 % CI for D_KL(obs ‖ Benford) lies entirely below 0.001 (i.e., negligible), we **fail to reject H₀** and conclude that Benford accounts for > 90 % of the original 0.141 divergence. If the CI is markedly above zero, we accept H₁ and quantify the residual primorial bias.

---

## 2.  **H2 – Uniformity of the trailing (least‑significant) digit across the 48 coprime residues**

| | |
|---|---|
|**H₀**|Among primes > 210, the **trailing digit** (i.e., p mod 210) is uniformly distributed over the 48 residues that are coprime to 210. No residue is preferred.|
|**H₁**|At least one coprime residue occurs with a frequency that deviates significantly from the uniform expectation (indicating a primorial structural bias).|

### Why it is testable
* The set of admissible residues (ϕ(210)=48) is known and finite.  
* With ≥ 10⁸ primes the expected count per residue is > 2 × 10⁶, giving enough power to detect tiny deviations (effect sizes down to ≈ 0.2 %).  
* A classic **χ² goodness‑of‑fit** test (or a multinomial exact test) can be applied directly.

### Experiment that would test it
1. **Extract the L‑digit** – For each prime p>210, compute r(p)=p mod 210.  
2. **Filter to coprime residues** – Keep only those r(p) with gcd(r(p),210)=1 (48 classes).  
3. **Observed counts** – O₁,…,O₄₈.  
4. **Expected counts under H₀** – Because the total number of primes is N, the expected count for each residue is E=N/48. (If one wishes to incorporate the Prime Number Theorem weighting for the exact interval [2, X], a slightly more refined expected value E_i = N·π_i/π(210) can be used, where π_i is the proportion of integers ≤ X that are congruent to residue i.)  
5. **χ² statistic** –  
   \[
   χ² = \sum_{i=1}^{48}\frac{(O_i-E_i)^2}{E_i}
   \]  
   Under H₀ this follows a χ² distribution with 47 df.  
6. **Effect‑size** – Compute Cramér’s V = √(χ²/(N·min(48‑1, 209‑1))) and interpret it (V < 0.10 → negligible bias).  

**Decision rule:** If p‑value > 0.05 (after a Bonferroni correction for the 48 tests if a post‑hoc look at individual residues is performed) we **retain H₀**; otherwise we **reject** it and flag the offending residues.

---

## 3.  **H3 – Residual leading‑digit bias after removing Benford is non‑uniform across the 48 coprime residues**

| | |
|---|---|
|**H₀**|After subtracting the expected Benford contribution, the **residual leading‑digit frequencies** are the same for all 48 coprime residues (i.e., the residuals are random noise).|
|**H₁**|Some residues show a systematic excess or deficit of a particular leading digit, indicating a *primorial‑specific* leading‑digit structure.|

### Why it is testable
* We can **compute the expected Benford frequency for each digit within each residue class** by multiplying the overall Benford probability by the proportion of primes that fall in that residue.  
* The residual for digit d in residue r is:  
  \[
  R_{r,d}=O_{r,d} - E_{r,d}^{\text{Benford}}
  \]  
* Under H₀ the residuals should be centred at zero with a variance that can be estimated from the data (or from a bootstrap). A **multivariate χ² test** or a set of **binomial tests** with FDR correction can detect systematic deviations.

### Experiment that would test it
1. **Build a contingency table** – For each coprime residue r (48 rows) and each possible leading digit d (1–209 columns), count O_{r,d}.  
2. **Compute the Benford expectation per cell** –  
   \[
   E_{r,d}^{\text{Benford}} = N_r \times P_B(d)
   \]  
   where N_r is the total number of primes belonging to residue r.  
3. **Residual matrix** – R_{r,d}=O_{r,d}−E_{r,d}^{Benford}.  
4. **Global test** – Use a **χ² test of independence** on the contingency table after adjusting for Benford (i.e., compare the observed to the Benford‑adjusted expected). This yields a χ² with (48‑1)*(209‑1) df.  
5. **Post‑hoc cell‑wise tests** – For each (r,d) compute a standardized residual z_{r,d}=R_{r,d}/√E_{r,d}^{Benford}. Cells with |z|>3 (≈ p < 0.003) are flagged; apply **Benjamini–Hochberg FDR** to control the false‑discovery rate.  
6. **Interpretation** – If any cell survives the FDR threshold, we have evidence for H₁ (local primorial bias).  

**Decision rule:** Reject H₀ if the global χ² test yields p < 0.05 **or** if, after FDR correction, any cell shows a significant residual. Otherwise, H₀ is retained.

---

## 4.  **H4 – Secondary‑digit distribution deviates from both uniform and Benford expectations**

| | |
|---|---|
|**H₀**|The **second‑leading digit** (or any digit beyond the most‑significant one) of Base‑210 primes follows a **uniform** distribution across the 210 possible symbols (or, if we consider a generalized Benford for second digits, follows that model).|
|**H₁**|The secondary‑digit distribution is **neither uniform nor Benford‑derived**; it exhibits a pattern that cannot be explained by either model, pointing to a primorial‑specific structure.|

### Why it is testable
* For every prime we can extract the **second digit** (the digit immediately to the right of the most‑significant one).  
* The null distribution (uniform) is simply 1/210 for each symbol. A Benford‑type expectation for the second digit can be derived analytically (or approximated by simulation) under the assumption that numbers are uniformly distributed on a logarithmic scale.  
* We can compute KL‑divergence or a χ² statistic to compare observed to either null.

### Experiment that would test it
1. **Extract the second digit** – Write each prime in base 210, take the digit in position 2 (counting from the most‑significant side).  
2. **Frequency table** – Count O_s for s = 0,…,209 (210 symbols).  
3. **Uniform baseline** – E_s^{U}=N/210.  
4. **Benford‑type baseline** – Simulate a large set (e.g., 10⁷) of numbers that follow the logarithmic distribution in base 210, record their second‑digit frequencies, and use these as E_s^{B}. (Alternatively, analytically integrate the log‑density over the intervals that map to each second‑digit value.)  
5. **Test statistics** –  
   * χ²_U = Σ (O_s‑E_s^{U})² / E_s^{U} (df = 209)  
   * χ²_B = Σ (O_s‑E_s^{B})² / E_s^{B} (df = 209)  
   * KL_U = D_KL(O/N || uniform)  
   * KL_B = D_KL(O/N || Benford‑second)  
6. **Model selection** – Use a **likelihood‑ratio test** (or AIC/BIC) to decide whether the uniform or Benford‑second model provides a significantly better fit.  
7. **Effect size** – Compute Cramér’s V between the second digit and the coprime‑residue class; if V > 0.05, consider it a non‑trivial association.

**Decision rule:** If both χ²_U and χ²_B give p < 0.05 *and* the likelihood‑ratio test prefers a third “primorial” model (e.g., a mixture of residues), we accept H₁. Otherwise, H₀ (uniform or Benford) cannot be rejected.

---

## 5.  **H5 – After controlling for Benford, the residual effect size (Cramér’s V) for leading‑digit vs. coprime‑residue is negligible**

| | |
|---|---|
|**H₀**|When the leading‑digit distribution is **adjusted for Benford**, the association between the leading digit and the 48 coprime residues, as measured by **Cramér’s V**, is **zero** (or ≤ 0.05, a pre‑specified “negligible” threshold).|
|**H₁**|The association remains **positive and non‑trivial** (V > 0.05), indicating a residual primorial structure even after Benford is removed.|

### Why it is testable
* Cramér’s V is a symmetric measure of association for two categorical variables.  
* We can compute the **contingency table** “leading digit (209 categories) × coprime residue (48 categories)” and obtain V directly.  
* The **null distribution of V under independence** can be approximated by permuting the residue labels many times and recomputing V; this yields a p‑value for the observed V.

### Experiment that would test it
1. **Contingency table** – Same as in H3, but now we focus on the *overall* association, not individual cells.  
2. **Benford‑adjusted frequencies** – Replace each cell count O_{r,d} by O_{r,d}^{adj}=O_{r,d}‑E_{r,d}^{Benford} (or, equivalently, compute expected counts under independence *after* removing the Benford component).  
3. **Cramér’s V** –  
   \[
   V = \sqrt{\frac{\chi^2}{N \times \min(208,\,47)}}
   \]  
   where χ² is the usual Pearson chi‑square statistic on the adjusted table.  
4. **Permutation test** – Randomly shuffle the residue labels among primes 10 000 times, recompute V each time, and obtain the empirical distribution of V under the null of no association.  
5. **Confidence interval** – Bootstrap the prime list (or the residuals) to obtain a 95 % CI for V.  
6. **Decision rule** – If the 95 % CI lies entirely below 0.05 **and** the permutation p‑value > 0.05, we **retain H₀** (no meaningful primorial bias). If the CI exceeds 0.05 or the p‑value < 0.05, we **reject H₀** and claim a non‑negligible residual effect.

---

### How the five hypotheses together answer the overall research problem

| Hypothesis | What it tests | Key quantity obtained |
|------------|----------------|-----------------------|
| **H1** | Is Benford the dominant cause of the 0.141 KL‑divergence? | % of divergence explained by Benford |
| **H2** | Do the 48 admissible trailing digits behave uniformly? | χ², Cramér’s V for residue uniformity |
| **H3** | After Benford subtraction, are there residue‑specific leading‑digit biases? | Residual χ², FDR‑adjusted cell‑wise p‑values |
| **H4** | Does any secondary‑digit distribution betray a primorial pattern? | KL‑divergence to uniform & Benford, χ², model‑selection |
| **H5** | What is the net effect size of a residual primorial bias after Benford removal? | Cramér’s V with confidence interval & permutation p‑value |

By **accepting or rejecting** each of these statements with the rigorous experiments outlined above, we will be able to:

1. **Quantify** how much of the observed 0.141 KL‑divergence is Benford‑induced versus genuine primorial structure.  
2. **Map** the coprime‑residue behaviour of both leading and trailing digits, revealing any systematic artifacts intrinsic to Base‑210.  
3. **Provide** a clean effect‑size (Cramér’s V) that reflects the true magnitude of the primorial bias once Benford is mathematically subtracted.

All experiments stay strictly within **Base‑210**, use the same large prime dataset (≥ 10⁸), and rely on standard statistical tests that are well‑known to be robust to large sample sizes. The methodology is fully reproducible (a Python/NumPy/ MPMath script can be shared) and the results can be validated by cross‑checking with an independent prime generator (e.g., `primegen` or `pyprimes`).