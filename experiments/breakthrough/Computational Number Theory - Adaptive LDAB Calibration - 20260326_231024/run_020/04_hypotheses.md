**Overall context**  
Prior experiments (run 004–006) showed that variance‑differentials collapse to zero for large primorials, that adaptive Wasserstein or hybrid weighting cannot suppress the variance, and that arbitrary‑precision arithmetic confirms the growth is real and not a computational artifact.  Those findings leave the *functional form* of the growth as the central open question.  The empirical fit for \(k\le 15\) yields a near‑perfect tie between a power‑law (\(R(k)\sim C\,k^{2.19}\)) and a logarithmic trend, but the data are too short to decide.  The four hypotheses below attack the problem from complementary analytic angles (random‑matrix/Cramér model, inclusion‑exclusion/Mertens, smooth‑number/Dickman, and spectral‑graph theory).  Each hypothesis is stated in a way that can be falsified with the existing data (or with a modest extra analytical derivation) and does **not** require new gap calculations for \(k>15\).

---

## Hypothesis 1 – **Pure power‑law scaling (random‑matrix/Cramér link)**  

**Statement**  
\[
R(k)\;\underset{k\to\infty}{\sim}\;C\,k^{\beta},\qquad\beta\approx 2.19 .
\]

**Why it is testable**  
* The exponent \(\beta\) can be derived analytically from Cramér’s random‑model for the primes (or from a Gaussian orthogonal‑ensemble picture of the coprime indicator).  The derivation yields a concrete predicted value for \(\beta\) (e.g. \(\beta=2\) plus a correction term that for the first 15 primorials gives ≈ 2.19).  
* The existing clean dataset for \(k=1\ldots15\) already contains the pairs \((k,R(k))\).  A standard nonlinear regression (or a log‑log linear fit) can estimate \(\beta\) and its uncertainty.

**Experiment**  
1. **Analytic part** – Using the Cramér random‑model, write the variance of the coprime‑indicator as  
   \[
   \operatorname{Var}[I_{P_k}]\;=\;\prod_{p\le p_k}(1-\tfrac1p)\Bigl[1-\prod_{p\le p_k}(1-\tfrac1p)\Bigr]
   \]
   and compare the resulting \(R(k)=\operatorname{Var}/\text{mean}\) to the random‑matrix prediction for the eigenvalue spread of the associated **circulant sieve matrix**.  This yields a theoretical \(\beta\).  
2. **Empirical part** – Fit the model \(R(k)=C k^{\beta}\) to the 15‑point empirical curve (e.g. by minimizing the summed‑squared‑log‑residuals).  Compute the 95 % confidence interval for \(\beta\).  If the interval contains the random‑matrix value, the hypothesis is supported; if it excludes it, the hypothesis is rejected.  

*Result expected*: If the fitted \(\beta\) is ≈ 2.19 and the residuals are randomly scattered, the power‑law hypothesis gains strong support.

---

## Hypothesis 2 – **Logarithmic scaling (inclusion‑exclusion + Mertens)**  

**Statement**  
\[
R(k)\;\sim\;A\,\log P_k\;+\;B,
\]
i.e. the variance‑to‑mean ratio grows linearly with the logarithm of the primorial (equivalently, with \(\log p_k\)).

**Why it is testable**  
* The product \(\prod_{p\le p_k}(1-1/p)\) is, by Mertens’ third theorem, \(\displaystyle \frac{e^{-\gamma}}{\log p_k}+o(1/\log p_k)\).  Treating the coprime indicator as an independent Bernoulli process with success probability \(p=\prod(1-1/p)\) gives a geometric gap distribution whose variance‑to‑mean ratio is \((1-p)/p\approx \frac{\log p_k}{e^{-\gamma}}-1\).  Hence a **logarithmic** term emerges naturally from elementary sieve theory.  
* The same dataset \((k,R(k))\) can be plotted against \(\log P_k\) and tested for linearity.

**Experiment**  
1. **Theoretical derivation** – Show that, under the independent‑Bernoulli approximation,  
   \[
   R(k)=\frac{1-p}{p}= \frac{e^{\gamma}\log p_k}{1+o(1)}-1,
   \]
   which is asymptotically linear in \(\log p_k\).  
2. **Empirical test** – Perform a linear regression \(R(k)=A\log P_k+B\) on the 15 points.  Compute AIC/BIC and compare with the power‑law fit of Hypothesis 1.  If the logarithmic model has a lower AIC (or if the residuals are smaller and show no systematic curvature), the hypothesis is favoured.

*Result expected*: If the linear relationship holds (R² > 0.99) and the intercept is close to \(-1\), the logarithmic scaling would be confirmed.

---

## Hypothesis 3 – **Stretched‑exponential scaling (smooth‑number/Dickman link)**  

**Statement**  
\[
R(k)\;\sim\;\exp\!\Bigl(c\,\bigl(\log P_k\bigr)^{\delta}\Bigr),\qquad 0<\delta<1 .
\]
The exponent \(\delta\) is set by the Dickman‑function tail of the distribution of numbers whose prime factors are all \(\le p_k\).

**Why it is testable**  
* The probability that a random integer \(\le x\) has all prime factors \(\le y\) (with \(y=p_k\) and \(x=P_k\)) is given by the Dickman function \(\rho(u)\) with \(u=\frac{\log x}{\log y}\).  For large \(u\), \(\rho(u)=\exp\!\bigl[-u(\log u+O(1))\bigr]\).  Taking logarithms yields a **stretched exponential** in \(\log x\).  The same tail controls the decay of the density of \(p_k\)-smooth numbers, which directly influences the gap distribution.  
* One can fit the three‑parameter model \(R(k)=\exp[c(\log P_k)^{\delta}]\) to the data, treating \(c\) and \(\delta\) as unknowns.

**Experiment**  
1. **Analytic part** – Derive the leading‑order expression for the gap‑length tail from the Dickman function:  
   \[
   \Pr\{\text{gap}>g\}\approx \exp\!\Bigl[-\theta\,\bigl(\log g\bigr)^{\alpha}\Bigr]
   \]
   and translate this into the variance‑to‑mean ratio, obtaining the stretched‑exponential form above.  This yields a predicted \(\delta\) (e.g. \(\delta=1/2\) from the saddle‑point analysis).  
2. **Empirical part** – Use nonlinear least‑squares (or Bayesian information criterion) to fit the model to the 15 points.  Compare the fitted \(\delta\) to the theoretical value (≈ 0.5).  If they agree within error, the hypothesis is supported.

*Result expected*: If the fitted \(\delta\) is around 0.5 ± 0.1 and the residuals are smaller than those of the power‑law or logarithmic models, the stretched‑exponential hypothesis is favoured.

---

## Hypothesis 4 – **Spectral exponent (inclusion‑exclusion matrix eigenvalue)**  

**Statement**  
\[
\beta\;\approx\;\lambda_{\max}(M_k),
\]
where \(M_k\) is the \(k\times k\) inclusion‑exclusion matrix with entries  

\[
M_k(i,j)=
\begin{cases}
\displaystyle\frac{1}{p_i p_j}, & i\neq j,\\[4pt]
0, & i=j,
\end{cases}
\]

and \(\lambda_{\max}(M_k)\) is its largest eigenvalue.  As \(k\) grows, \(\lambda_{\max}(M_k)\) obeys a power law \(\lambda_{\max}(M_k)\sim C'\,k^{\beta}\) with the same exponent that governs \(R(k)\).

**Why it is testable**  
* The variance of the coprime count can be expressed (via the inclusion‑exclusion principle) as a quadratic form involving the matrix \(M_k\).  The leading term in that quadratic form is precisely \(\lambda_{\max}(M_k)\) multiplied by the mean squared amplitude, giving a direct proportionality \(R(k)\propto\lambda_{\max}(M_k)\).  Thus the scaling exponent of \(R(k)\) must coincide with the spectral exponent of \(M_k\).  
* For the 15 known primorials we can explicitly build \(M_k\) (the primes up to \(p_k\) are known) and compute its eigenvalues using standard linear‑algebra software; no new gap calculations are required.

**Experiment**  
1. **Matrix construction** – For each \(k=1,\ldots,15\) form the matrix \(M_k\) using the reciprocals of the first \(k\) primes (off‑diagonal) and zeros on the diagonal.  Compute \(\lambda_{\max}(M_k)\) (e.g. via Python’s `numpy.linalg.eigvalsh`).  
2. **Fitting** – Perform a power‑law fit \(\lambda_{\max}(M_k)=C'\,k^{\beta}\).  Compare the estimated \(\beta\) with the empirical exponent ≈ 2.19.  Additionally, plot \(R(k)\) versus \(\lambda_{\max}(M_k)\); a linear relationship (Pearson r > 0.99) would strongly support the hypothesis.  

*Result expected*: If \(\beta_{\text{eigen}}\) ≈ 2.19 (within the 95 % CI) and the scatter plot shows a clean proportionality, the spectral hypothesis would provide a mechanistic explanation for the observed exponent.

---

### How to use these hypotheses

| Hypothesis | Predicted functional form | Key theoretical basis | Primary test |
|------------|---------------------------|-----------------------|--------------|
| **1** | \(R(k)=C\,k^{\beta}\) (β≈2.19) | Cramér random‑model / random‑matrix eigenvalue distribution | Non‑linear regression on existing data; compare β with random‑matrix prediction |
| **2** | \(R(k)=A\log P_k+B\) | Inclusion‑exclusion + Mertens theorem (geometric gap model) | Linear regression of \(R(k)\) vs \(\log P_k\); compare AIC/BIC with Hypothesis 1 |
| **3** | \(R(k)=\exp[c(\log P_k)^{\delta}]\) (δ≈0.5) | Dickman‑function tail for smooth numbers | Nonlinear fit of stretched‑exponential; compare δ to theoretical value |
| **4** | \(R(k)\propto\lambda_{\max}(M_k)\) with \(\lambda_{\max}\sim C'k^{\beta}\) | Spectral analysis of inclusion‑exclusion matrix | Compute eigenvalues, fit power law, check proportionality to \(R(k)\) |

Each hypothesis is **falsifiable** with the current 15‑point dataset (or with a modest analytical derivation) and does **not** require gap computations beyond the existing ones.  By comparing the statistical evidence (goodness‑of‑fit, AIC, residuals) for the four competing functional forms we can determine which scaling class the primorial‑gap variance‑to‑mean ratio truly belongs to, thereby resolving the power‑law vs. logarithmic tie identified in the original empirical study.