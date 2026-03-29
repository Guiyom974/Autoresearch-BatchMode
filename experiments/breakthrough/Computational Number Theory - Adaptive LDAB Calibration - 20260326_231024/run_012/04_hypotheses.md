**Hypothesis 1 – Asymptotic “log‑correction” law for the variance‑to‑mean² ratio**  

**Statement**  
The variance‑to‑mean² ratio for the reduced‑residue gap distribution,
\[
R(k)\;=\;\frac{\operatorname{Var}_{k}}{\mu_{k}^{2}},
\]
tends to the Poisson‑type ceiling \(1/3\) from below and does so with a
logarithmic correction
\[
R(k)=\frac13-\frac{C}{\log P_{k}}+o\!\Bigl(\frac1{\log P_{k}}\Bigr),
\qquad C>0 .
\]

**Why it is testable**  
The ratio can be computed exactly for the already‑enumerated cases
\(k=3,\dots ,7\).  Fitting the single unknown constant \(C\) to those
five data points yields a concrete, quantitative prediction for
\(R(8)\) and \(R(9)\).  The hypothesis is falsifiable: if the observed
ratio at \(k=8\) or \(k=9\) lies outside the 5 % prediction interval,
the form of the law must be revised.

**Experiment**  

1. **Fit the model** – Using the exact \(\mu_{k}\) and \(\operatorname{Var}_{k}\)
   for \(k=3,\dots ,7\) (already available), perform a ordinary‑least‑squares
   fit of the linear relation
   \[
   \Bigl(\frac13-R(k)\Bigr)\log P_{k}=C+o(1)
   \]
   to estimate \(\hat C\) and its standard error.  
2. **Predict** – Compute the predicted ratio \(\hat R(8)\) and
   \(\hat R(9)\) together with a 5 % confidence band.  
3. **Validate** – For \(k=8\) (and, if computational budget permits,
   \(k=9\)) generate the reduced‑residue set modulo \(P_{8}=9\,699\,690\)
   with a segmented sieve, count all consecutive gaps, evaluate
   \(\mu_{8},\operatorname{Var}_{8}\) using arbitrary‑precision arithmetic,
   form \(R(8)\), and compare it with \(\hat R(8)\).  Success is declared
   if the observed value falls inside the confidence band (or within
   5 % relative error).

---

**Hypothesis 2 – Exact inclusion‑exclusion formula for the variance**  

**Statement**  
For a primorial \(P_{k}=p_{1}p_{2}\dots p_{k}\) the variance of the gap
distribution can be written as the finite alternating sum
\[
\operatorname{Var}_{k}
= \mu_{k}^{2}\;
   \Bigl[\,1
   -\sum_{i}\frac1{p_{i}}
   +\sum_{i<j}\frac1{p_{i}p_{j}}
   -\sum_{i<j<\ell}\frac1{p_{i}p_{j}p_{\ell}}
   +\cdots\Bigr].
\tag{1}
\]
The series terminates after \(2^{k}\) terms and converges rapidly; truncating
after the first‑order terms (\(|S|\le 1\)) already reproduces the empirical
variance to within 5 % for all \(k\ge3\).

**Why it is testable**  
Each term in (1) involves only the prime divisors of \(P_{k}\), all of which
are known.  One can evaluate the truncated sum (first order, second order,
…) exactly with rational arithmetic, then compare the resulting
variance estimate to the exact empirical variance obtained from the
enumerated gap lists.  The hypothesis is falsifiable: if the error of the
truncated formula exceeds the prescribed tolerance, the assumed functional
form is wrong.

**Experiment**  

1. **Compute the series** – For each \(k=3,\dots ,7\) generate the set of
   all subsets \(S\subseteq\{p_{1},\dots ,p_{k}\}\) up to \(|S|=2\) and
   evaluate the rational sum
   \[
   S_{k}^{(1)} = 1-\sum_{i}\frac1{p_{i}}+\sum_{i<j}\frac1{p_{i}p_{j}} .
   \]
2. **Compare with data** – Using the already‑computed \(\mu_{k}\) and
   \(\operatorname{Var}_{k}\), compute the relative error
   \(\bigl|\operatorname{Var}_{k}-\mu_{k}^{2}S_{k}^{(1)}\bigr|/
      \operatorname{Var}_{k}\).
   Verify that the error is < 5 % for every \(k\).  
3. **Higher‑order check** – Optionally add the third‑order term (\(|S|=3\))
   and confirm that the error shrinks further, providing evidence that
   the full inclusion‑exclusion series (1) is the correct model.

---

**Hypothesis 3 – Simplified product approximation for the suppression factor**  

**Statement**  
The leading behaviour of the variance‑to‑mean² ratio is captured by the
closed‑form product
\[
S_{k}\;=\;\prod_{p\mid P_{k}}\frac{1-\frac1p}{\,1-\frac{2}{p}\,}
\;=\;
\prod_{i=1}^{k}\frac{p_{i}-1}{p_{i}-2}.
\tag{2}
\]
Consequently,
\[
\frac{\operatorname{Var}_{k}}{\mu_{k}^{2}} \approx S_{k},
\qquad
\text{and } S_{k}\uparrow \frac13 \text{ monotonically as } k\to\infty .
\]

**Why it is testable**  
The right‑hand side of (2) depends only on the prime factors of the
primorial; it can be evaluated instantly for any \(k\).  One can compare
\(S_{k}\) directly with the empirical ratio \(R(k)\) for \(k=3,\dots ,7\)
and test whether the relative deviation tends to zero.  The hypothesis
predicts a monotone increase of \(R(k)\) and an asymptotic limit of
\(1/3\); both are falsifiable.

**Experiment**  

1. **Compute the product** – For each \(k=3,\dots ,7\) calculate
   \(S_{k}\) from (2) using arbitrary‑precision rational arithmetic.  
2. **Compute the empirical ratio** – From the exact gap lists obtain
   \(R(k)=\operatorname{Var}_{k}/\mu_{k}^{2}\).  
3. **Assess fit** – Form the relative error
   \(\epsilon_{k}=|R(k)-S_{k}|/R(k)\) and plot it against \(k\).  If
   \(\epsilon_{k}\) decreases with \(k\) and stays below, say, 10 % for
   all five values, the product form is supported.  
4. **Extrapolation test** – Using the observed trend, predict \(R(8)\)
   by \(S_{8}\) (or a slightly corrected version) and verify with the
   enumerated data for \(k=8\) (see Experiment for Hypothesis 1).

---

**Hypothesis 4 – Decay of higher‑order standardized moments**  

**Statement**  
The standardized skewness \(\gamma_{1,k}\) and excess kurtosis
\(\gamma_{2,k}\) of the gap distribution tend to zero as the primorial
grows, obeying the simple logarithmic decay laws
\[
\gamma_{1,k}= \frac{A}{\log P_{k}}+o\!\Bigl(\frac1{\log P_{k}}\Bigr),\qquad
\gamma_{2,k}= \frac{B}{\log P_{k}}+o\!\Bigl(\frac1{\log P_{k}}\Bigr),
\]
with constants \(A,B>0\).

**Why it is testable**  
Both \(\gamma_{1,k}\) and \(\gamma_{2,k}\) can be computed from the exact
gap lists already available for \(k=3,\dots ,7\).  Fitting the linear
relations \((\gamma_{1,k}\,\log P_{k})\) and \((\gamma_{2,k}\,\log P_{k})\)
to those five points yields estimates \(\hat A,\hat B\) and prediction
intervals for \(k=8,9\).  The hypothesis is falsifiable: if the observed
higher moments at \(k=8\) or \(k=9\) do not fall within the predicted
range, the decay law must be revised.

**Experiment**  

1. **Calculate moments** – For each \(k=3,\dots ,7\) compute the sample
   skewness \(\hat\gamma_{1,k}\) and excess kurtosis \(\hat\gamma_{2,k}\)
   of the empirical gap list (using formulas for raw, central, and
   standardized moments).  
2. **Fit decay constants** – Perform a linear regression of
   \(\hat\gamma_{1,k}\) versus \(1/\log P_{k}\) and of
   \(\hat\gamma_{2,k}\) versus \(1/\log P_{k}\) to obtain \(\hat A,\hat B\)
   and their standard errors.  
3. **Predict for larger \(k\)** – Use the fitted models to obtain
   predicted \(\gamma_{1,8},\gamma_{2,8}\) (and similarly for \(k=9\))
   with 95 % prediction intervals.  
4. **Validate** – Enumerate the reduced‑residue gaps for \(k=8\) (and
   \(k=9\) if feasible), compute the corresponding sample skewness and
   kurtosis, and check whether they lie inside the prediction bands.
   Agreement within the bands supports the logarithmic decay law; failure
   would necessitate an alternative functional form (e.g. a power law
   with exponent \(<1\)).

---

### How the hypotheses build on prior findings  

* **Failure of weighting schemes** (runs 004–006) showed that
  simple adaptive weighting cannot capture the structural suppression of
  variance.  Hypotheses 2 and 3 replace weighting by **exact
  inclusion‑exclusion** and by a **prime‑factor product**, respectively,
  directly exploiting the algebraic structure of the primorial modulus.

* **Floating‑point underflow** for large primorials signals the need for
  **arbitrary‑precision arithmetic**; all proposed experiments explicitly
  require high‑precision calculations, ensuring that the measured
  variance and moments are not contaminated by round‑off error.

* The **monotonic trend** of the variance‑to‑mean² ratio (0.173 → 0.333)
  motivates the **asymptotic law** in Hypothesis 1 and the **product
  approximation** in Hypothesis 3, both of which predict a smooth
  approach to the theoretical ceiling \(1/3\).

* By testing **higher‑order moments** (Hypothesis 4) we go beyond the
  first two moments that have been examined so far, providing a deeper
  check of the distributional shape and a more stringent validation of
  any theoretical model.  

Together, these four hypotheses form a coherent, testable programme:
they specify a concrete analytical form for the variance (H2/H3), a
quantitative scaling law (H1), and a structural explanation for why all
higher moments collapse (H4).  Each is falsifiable with the data that
will become available after the next round of exact enumerations for
\(k=8\) and, if feasible, \(k=9\).