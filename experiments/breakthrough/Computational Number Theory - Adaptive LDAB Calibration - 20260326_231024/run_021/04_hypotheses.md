**Hypotheses for the “\(R(k)=1\) invariance” of primorial gap distributions**  
*(All experiments must use arbitrary‑precision integer or rational arithmetic – no floating‑point approximations.)*

---

### Hypothesis 1 – *Exact variance‑to‑mean identity*  

**Statement.**  
For every primorial index \(k\ge 1\) the gaps between consecutive integers coprime to the \(k^{\text{th}}\) primorial \(P_k\) (taken cyclically, i.e. the last gap closes the circle) satisfy  

\[
R(k)\;:=\;\frac{\operatorname{Var}(\text{gaps})}{\operatorname{Mean}(\text{gaps})}=1
\]

as an **exact rational number**.

**Why it is testable.**  
The reduced residue system modulo \(P_k\) can be enumerated completely, the list of gaps \(\{g_i\}\) is finite (size \(\phi(P_k)\)), and both the sum \(\sum g_i\) and the sum of squares \(\sum g_i^{2}\) are integers.  With arbitrary‑precision integers we can compute the mean \(\mu =\frac{\sum g_i}{\phi(P_k)}\) and the variance \(\sigma^{2}= \frac{\sum g_i^{2}}{\phi(P_k)}-\mu^{2}\) as exact fractions.  It is then a simple rational‑equality check whether \(\sigma^{2}/\mu = 1\).

**Experiment.**  
1. Generate the reduced residue set \(\{a_1<a_2<\dots<a_{\phi(P_k)}\}\) modulo \(P_k\).  
2. Form the gap list \(g_i = a_{i+1}-a_i\) for \(i=1,\dots,\phi(P_k)-1\) and the wrap‑around gap \(g_{\phi(P_k)} = P_k + a_1 - a_{\phi(P_k)}\).  
3. Using Python’s `int` (or any big‑integer library) compute  

   \[
   S_1=\sum_{i=1}^{\phi(P_k)} g_i,\qquad 
   S_2=\sum_{i=1}^{\phi(P_k)} g_i^{2}.
   \]  

4. Form the exact mean \(\mu = S_1/\phi(P_k)\) and variance \(\sigma^{2}=S_2/\phi(P_k)-\mu^{2}\).  
5. Reduce the fraction \(\sigma^{2}/\mu\) and test `numerator == denominator`.  
6. Repeat for \(k=1\) up to the largest \(k\) that is still computationally feasible (e.g. \(k=15\) or beyond if the enumeration of \(P_{15}\approx 6\times10^{17}\) can be handled with segmented residue generation).  

*Decision rule:* If the equality holds for every \(k\) tested, the hypothesis is supported; a single counter‑example (ratio ≠ 1) disproves it.

---

### Hypothesis 2 – *Closed‑form algebraic identity for \(\sum g_i^{2}\)*  

**Statement.**  
For the full‑period gap set defined above the following exact identity holds:

\[
\sum_{i=1}^{\phi(P_k)} g_i^{2}= \frac{P_k^{\,2}}{\phi(P_k)} \;+\; P_k .
\tag{1}
\]

Because \(\sum g_i = P_k\) (the total length of the cycle), equation (1) is equivalent to the variance‑to‑mean ratio being 1.

**Why it is testable.**  
Both sides of (1) are integers (the right‑hand side is an integer because \(\phi(P_k)\) divides \(P_k\)).  Direct computation of the left‑hand side for a given \(k\) yields an integer that can be compared to the right‑hand side using exact arithmetic.

**Experiment.**  
1. Compute \(P_k\) and \(\phi(P_k)\) exactly (they are products of the first \(k\) primes).  
2. Enumerate the gaps as in Hypothesis 1 and obtain \(S_2=\sum g_i^{2}\).  
3. Evaluate the right‑hand side \(RHS = P_k^{2}/\phi(P_k) + P_k\) using integer division (the division is exact).  
4. Test `S2 == RHS` for each \(k\).  

*Decision rule:* If (1) is satisfied for all tested \(k\), we have a proven combinatorial identity that explains the \(R(k)=1\) invariance.

---

### Hypothesis 3 – *Higher‑order moments converge to the Poisson limit*  

**Statement.**  
As \(k\) grows, the **skewness** \(\gamma_1\) and **excess kurtosis** \(\gamma_2\) of the primorial gap distribution approach the values of a Poisson random variable with the same mean \(\mu_k = P_k/\phi(P_k)\):

\[
\gamma_{1}(k)\;\xrightarrow[k\to\infty]{}\;\frac{1}{\sqrt{\mu_k}},\qquad
\gamma_{2}(k)\;\xrightarrow[k\to\infty]{}\;\frac{1}{\mu_k}.
\]

Thus the full gap distribution becomes asymptotically Poisson, not just the first two moments.

**Why it is testable.**  
All central moments up to the fourth can be expressed as exact rational numbers from the integer sums \(S_j=\sum g_i^{\,j}\) (\(j=1,2,3,4\)).  Computing them and forming the standardized moments yields rational numbers that can be compared to the Poisson predictions.

**Experiment.**  
1. For each \(k\) compute the exact moments:  

   \[
   \mu =\frac{S_1}{\phi},\qquad 
   \mu_2 =\frac{S_2}{\phi}-\mu^{2},\qquad
   \mu_3 =\frac{S_3}{\phi}-3\mu\frac{S_2}{\phi}+2\mu^{3},
   \]
   \[
   \mu_4 =\frac{S_4}{\phi}-4\mu\frac{S_3}{\phi}+6\mu^{2}\frac{S_2}{\phi}-3\mu^{4}.
   \]  

2. Form skewness \(\gamma_1 = \mu_3/\sigma^{3}\) and excess kurtosis \(\gamma_2 = \mu_4/\sigma^{4}-3\) (with \(\sigma=\sqrt{\mu_2}\)).  
3. Compute the Poisson approximations \(\gamma_1^{\text{Pois}}=1/\sqrt{\mu}\) and \(\gamma_2^{\text{Pois}}=1/\mu\).  
4. For a sequence of increasing \(k\) (e.g. \(k=3,4,\dots,12\)), evaluate the absolute differences \(|\gamma_1-\gamma_1^{\text{Pois}}|\) and \(|\gamma_2-\gamma_2^{\text{Pois}}|\).  

*Decision rule:* If the differences trend monotonically toward zero (or fall below a pre‑specified ε), the hypothesis is supported.  Persistent non‑zero limits would indicate a different limiting distribution.

---

### Hypothesis 4 – *Boundary‑condition sensitivity: truncation destroys the invariance*  

**Statement.**  
If the gap sequence is **truncated** (i.e. the wrap‑around gap is omitted, so we only consider gaps from the first coprime up to the last coprime \(\le P_k\)), the variance‑to‑mean ratio drops below 1 for every \(k\):

\[
R_{\text{trunc}}(k) \;<\; 1 .
\]

Quantitatively, the deviation should be roughly \(\displaystyle \frac{P_k - a_{\phi(P_k)}}{P_k}\) (the relative size of the missing final segment).

**Why it is testable.**  
We can repeat the exact computation of Hypothesis 1 but deliberately exclude the final wrap‑around gap.  The resulting mean and variance are rational numbers that can be compared to the full‑period values.

**Experiment.**  
1. For each \(k\) generate the reduced residues and form the *truncated* gap list \(\{g_i^{\text{trunc}}\}_{i=1}^{\phi(P_k)-1}\) (no \(g_{\phi(P_k)}\)).  
2. Compute \(\mu_{\text{trunc}}= \frac{\sum_{i=1}^{\phi(P_k)-1} g_i^{\text{trunc}}}{\phi(P_k)-1}\) and \(\sigma^{2}_{\text{trunc}}\) analogously.  
3. Compute \(R_{\text{trunc}}= \sigma^{2}_{\text{trunc}}/\mu_{\text{trunc}}\).  
4. Compare to 1 (e.g. test `R_trunc < 1`).  

*Decision rule:* Observing \(R_{\text{trunc}}<1\) for all tested \(k\) would confirm that the previously identified truncation artifact is the sole source of the deviation from the exact identity.

---

### Hypothesis 5 – *Generalisation to any square‑free modulus*  

**Statement.**  
The exact invariance \(R(N)=1\) is **not** unique to primorials; it holds for *any* square‑free integer  

\[
N = \prod_{i=1}^{m} p_i \qquad (p_i\ \text{distinct primes}),
\]

when the gaps are taken over the full reduced‑residue cycle modulo \(N\).

**Why it is testable.**  
The same algorithm used for primorials works for any such \(N\).  By enumerating the reduced residues modulo \(N\) we can compute \(R(N)\) exactly and test the equality.

**Experiment.**  
1. Choose a list of square‑free \(N\) of increasing size, e.g.  

   \[
   N = 6,\; 30,\; 210,\; 2310,\; 30030,\; \dots
   \]  

   (the products of the first \(m\) primes, i.e. primorials, are a subset).  
2. For each \(N\) generate the reduced residue system, compute the gaps, and obtain \(R(N)=\sigma^{2}/\mu\) exactly as in Hypothesis 1.  
3. Test `R(N) == 1`.  

*Decision rule:* If the equality holds for every square‑free \(N\) examined, the result is a broader number‑theoretic identity; any failure would delimit the precise class of moduli for which the invariance holds.

---

## How these hypotheses build on the prior findings  

| Prior result | New hypothesis that builds on it |
|--------------|-----------------------------------|
| **Artifact‑free variance calculation** showed the variance‑to‑mean² ratio rising from 0.17 to 0.33 (i.e. mean growing faster than variance). | **Hypothesis 1** tests the *exact* ratio variance/mean = 1, which is equivalent to the observed growth because \(\frac{\operatorname{Var}}{\operatorname{Mean}} = \frac{\operatorname{Var}}{\operatorname{Mean}^2}\times\operatorname{Mean}\). |
| **Sub‑quadratic scaling model** predicted a deviation from simple log‑corrections. | **Hypothesis 2** provides a *closed‑form* identity that, if true, explains why the scaling is sub‑quadratic and pins down the exact coefficient. |
| **Higher‑order moments were not examined** in earlier runs. | **Hypothesis 3** directly addresses the unexplored higher‑order behavior, using the same exact arithmetic pipeline. |
| **Truncation artifact** was identified as the source of earlier non‑scaling. | **Hypothesis 4** systematically quantifies the effect of that artifact, showing that omitting the wrap‑around gap forces \(R(k)<1\). |
| **Generalisation was not explored** (only primorials were studied). | **Hypothesis 5** tests whether the identity is a special property of primorial bases or a more universal property of square‑free cycles. |

By testing these hypotheses with rigorous exact arithmetic we will either (i) prove the exact \(R(k)=1\) invariance and derive its algebraic source, or (ii) uncover the precise conditions under which the invariance breaks, thereby clarifying the role of boundary conditions and truncation that plagued earlier empirical models.