**Hypotheses – “Re‑evaluating Primorial Gap‑Variance Scaling”**  

Below are three **core** hypotheses (H1–H3) that attack the three research questions directly, plus two supplementary hypotheses (H4–H5) that address the observed low‑k artefacts and the need for arbitrary‑precision arithmetic.  All of them are phrased so that a concrete computational experiment can **reject** or **accept** them.

---

### H1 – True asymptotic scaling is a *power‑log* law, not a simple power law  

**Statement**  
For primorials with \(k\ge 8\) (i.e. \(P_{8}=9699690\) and larger) the gap‑variance grows as  

\[
\boxed{\;\operatorname{Var}(P_k)=A\;(\log P_k)^{\alpha}\;(\log\log P_k)^{\beta}\;},
\qquad A>0,\;\alpha\approx1.3\!-\!1.5,\;\beta\neq0 .
\]

**Why it is testable**  
The model contains two free exponents (\(\alpha,\beta\)) that can be estimated by non‑linear regression on the extended data set \((k=2,\dots,10)\).  If a pure power law (\(\beta=0\)) fits the data significantly worse (higher AIC/BIC, lower \(R^{2}\)), the hypothesis is supported.

**Experiment**  

1. **Exact computation** – Use an optimized sieving routine (or a segment‑wise “sliding‑window” sieve) to obtain the *full* list of coprime gaps for each \(P_k\) up to \(k=10\).  Compute the variance with arbitrary‑precision arithmetic (e.g. MPFR with ≥ 256‑bit mantissa).  
2. **Fitting** – Apply weighted non‑linear least‑squares (or Bayesian information‑theoretic model selection) to the paired values \((\log P_k,\log\log P_k,\operatorname{Var}(P_k))\).  Compare the pure‑power fit \((\beta=0)\) with the power‑log fit (both estimated simultaneously).  
3. **Diagnostics** – Examine residuals, test for homoscedasticity, and compute AIC/BIC.  The hypothesis is accepted if the power‑log model has \(\Delta\text{AIC}>5\) and yields \(R^{2}>0.99\) while the pure‑power model fails the latter.

---

### H2 – Gap‑length distribution converges to a **geometric** (or exponential) form whose mean scales as \((\log P_k)^{\gamma}\)

**Statement**  
As the primorial index \(k\) grows, the empirical histogram of *coprime* gap lengths \(g\) approaches a geometric distribution  

\[
\Pr\{g=m\}\;=\;(1-p_k)\,p_k^{\,m-1},\qquad m=1,2,\dots,
\]

with mean  

\[
\mu_k=\frac{1}{1-p_k}\;\sim\;C\;(\log P_k)^{\gamma},\qquad C>0,\;\gamma\approx1.2\!-\!1.4 .
\]

Because for a geometric law \(\operatorname{Var}(g)=\mu_k(\mu_k-1)\approx\mu_k^{2}\) for large \(\mu_k\), this predicts  

\[
\operatorname{Var}(P_k)\;\approx\;\bigl[C(\log P_k)^{\gamma}\bigr]^{2}.
\]

**Why it is testable**  
We can directly measure the *shape* of the empirical gap distribution for each \(k\) and test whether it is consistent with a geometric law (or, equivalently, an exponential law for the inter‑arrival times).  A Kolmogorov–Smirnov (KS) test will reject the hypothesis if the fitted geometric model is incompatible.

**Experiment**  

1. **Data collection** – For each \(P_k\) (up to \(k=10\)) store the full list of gap lengths (or a stratified random sample if memory becomes an issue).  
2. **Fit a geometric model** – Estimate \(p_k\) by maximum likelihood (\(\hat p_k=1/\bar g\)).  Perform a KS test of the empirical CDF against the theoretical geometric CDF.  Record the p‑value.  
3. **Scaling of \(\mu_k\)** – Plot \(\log\mu_k\) versus \(\log\log P_k\).  Regress \(\log\mu_k\) on \(\log\log P_k\) to obtain \(\gamma\).  Check whether the resulting \(\mu_k^{2}\) matches \(\operatorname{Var}(P_k)\) within the uncertainties (i.e. a linear regression of \(\operatorname{Var}(P_k)\) on \(\mu_k^{2}\) with intercept consistent with zero).  

If the KS test yields p‑values > 0.05 for **all** \(k\ge 8\) and the scaling exponent \(\gamma\) lies in the predicted range, H2 is confirmed.

---

### H3 – Variance is governed by the **second‑moment of prime‑reciprocal squares** multiplied by a power of \(\log P_k\)

**Statement**  
A probabilistic “random‑gap” model in which each integer \(n\) is declared a “gap‑endpoint” with probability proportional to the product of the densities of residues coprime to \(P_k\) leads to  

\[
\boxed{\;\operatorname{Var}(P_k)\;\asymp\;\Bigl(\sum_{p\mid P_k}\frac{1}{p^{2}}\Bigr)\;(\log P_k)^{\alpha}\;},
\]

where the sum \(\sum_{p\mid P_k}1/p^{2}\) is a measure of the “sparsity” of allowable residues.  For large \(k\) this sum approaches a constant (≈ 0.4522…) because the product \(\prod_{p\le P_k}(1-1/p^{2})\) converges, so the dominant growth comes from the \((\log P_k)^{\alpha}\) factor—consistent with H1.

**Why it is testable**  
The term \(\sum_{p\mid P_k}1/p^{2}\) can be computed exactly for each primorial, and its numerical value is independent of the gap‑variance calculation.  One can therefore test whether a linear relationship (on a log‑log scale) exists between \(\operatorname{Var}(P_k)\) and the product \(\bigl(\sum 1/p^{2}\bigr)(\log P_k)^{\alpha}\).

**Experiment**  

1. **Compute the sum** – For each \(k\) evaluate \(S_k=\sum_{p\mid P_k}1/p^{2}\) using the known list of the first \(k\) primes.  
2. **Multivariate regression** – Fit the model  

   \[
   \log\operatorname{Var}(P_k)=\log A+\alpha\log\log P_k+\log S_k+\varepsilon_k
   \]

   by ordinary least squares (or weighted LS).  
3. **Validate** – Examine the residuals \(\varepsilon_k\); they should be centred, homoscedastic, and show no systematic trend with \(k\).  Additionally, the fitted \(\alpha\) should be compatible with the exponent obtained in H1 (e.g. \(\alpha\approx1.3\!-\!1.5\)).  

If the regression yields a high \(R^{2}\) (> 0.98) and the coefficient of \(\log S_k\) is not significantly different from 1, H3 is supported.

---

### H4 – The original 1.168‑exponent fit is a **low‑k bias artefact** that disappears for \(k\ge 8\)

**Statement**  
The failure of the 1.168 power law stems from the fact that the data for \(k\le7\) are dominated by finite‑size effects.  Introducing a bias‑correction term proportional to \(1/k\) yields a model  

\[
\operatorname{Var}(P_k)=A'(\log P_k)^{1.168}\!\left(1+\frac{B'}{k}\right)
\]

which collapses onto the extended data for \(k\ge8\) and predicts the same asymptotic behaviour as H1 (i.e. the correction vanishes as \(k\) grows).

**Why it is testable**  
We can statistically test whether the residuals from the 1.168 model are systematically larger for small \(k\) and whether adding a \(1/k\) term significantly improves the fit (lower AIC, higher \(R^{2}\), and a non‑zero coefficient \(B'\)).

**Experiment**  

1. **Residual analysis** – Compute the residuals \(r_k=\operatorname{Var}_{\text{obs}}(P_k)-\operatorname{Var}_{\text{1.168}}(P_k)\) for \(k=2,\dots,10\).  
2. **Chow‑type structural‑break test** – Split the series at \(k=8\) and test whether the regression coefficients before and after the break are equal (F‑test).  
3. **Augmented model** – Fit the bias‑corrected model using non‑linear least squares and compare its AIC/BIC with the pure 1.168 model.  

If the break test rejects the null of a single regime (p < 0.05) and the augmented model reduces AIC by > 5, H4 is confirmed.

---

### H5 – Fixed‑precision arithmetic **underestimates** variance for \(k>9\); arbitrary‑precision reveals the continued rise predicted by H1

**Statement**  
The apparent “plateau” of \(\operatorname{Var}(P_k)\) observed in double‑precision experiments for \(k\ge 10\) is an artifact of floating‑point underflow/overflow.  Re‑computing with *arbitrary‑precision* libraries (MPFR, Python’s `decimal`, or GNU GMP) will show that the variance continues to grow according to the power‑log law of H1.

**Why it is testable**  
We can run the *same* algorithm twice: once with IEEE‑754 double precision and once with a high‑precision format (≥ 256‑bit mantissa).  The two results should agree for small \(k\) (where rounding errors are negligible) but diverge for large \(k\); a paired comparison (e.g., a Wilcoxon signed‑rank test) will detect the systematic bias.

**Experiment**  

1. **Implement dual‑precision variance** – Write a sieve that returns the full list of gaps and computes the variance; compile two versions: one using `double`, the other using `mpfr_t` with 256‑bit precision.  
2. **Run on the same primorials** – For \(k=2,\dots,10\) compute \(\operatorname{Var}_{\text{double}}\) and \(\operatorname{Var}_{\text{high}}\).  
3. **Statistical test** – Compute the differences \(d_k=\operatorname{Var}_{\text{high}}-\operatorname{Var}_{\text{double}}\).  Test whether the median of \(d_k\) is significantly > 0 (one‑sample Wilcoxon).  Also plot \(d_k\) vs. \(k\) to see if the divergence grows with \(k\).  

If the high‑precision values keep rising while the double‑precision values level off, H5 is verified and validates the need for arbitrary‑precision in the extended regime.

---

## How the Hypotheses Interlock

| Hypothesis | Addresses Research Question | Primary Evidence |
|------------|-----------------------------|------------------|
| **H1** | (1) True asymptotic scaling | Exact variance data + non‑linear regression |
| **H2** | (2) Distributional link | Gap‑histogram fitting (KS test) |
| **H3** | (2) Theoretical derivation of scaling | Sum of prime‑reciprocal squares vs. variance |
| **H4** | (3) Why 1.168 failed | Residual & structural‑break analysis |
| **H5** | (1) Computational limitation | Dual‑precision comparison |

Together they provide a **complete test‑plan**:  
1. **Collect** exact variance data (H1‑H3) using arbitrary‑precision (H5).  
2. **Fit** the power‑log model (H1) and compare with the distributional prediction (H2) and the prime‑reciprocal‑square model (H3).  
3. **Explain** the low‑k breakdown (H4) and **confirm** the need for high‑precision arithmetic (H5).  

A successful validation of all five will give a **rigorous, empirically grounded, theoretically motivated scaling law** for primorial gap variances, superseding the invalidated 1.168 exponent.