# Research Problem: Resolving the Goodness-of-Fit Paradox in Chebyshev Bias Modulo 210

## Objective
To resolve the methodological contradiction where empirical prime counts exhibit clear Chebyshev bias (favoring Non-Residues over Quadratic Residues modulo 210), yet standard chi-square Goodness-of-Fit tests yield a perfect uniform fit ($p=1.0$). The goal is to develop an advanced statistical variance model that properly accounts for the logarithmic density and inter-class correlations dictated by Dirichlet L-function zeros, replacing the flawed naive statistical framework.

## Research Questions
1. What specific mathematical or statistical artifact causes the standard chi-square test to produce a $p$-value of 1.0 when evaluating prime distributions modulo 210, despite the presence of a known theoretical and empirical bias?
2. How can we formulate a variance-covariance matrix that accurately captures the mutual dependence and correlation between Quadratic Residue (QR) and Non-Residue (NR) classes?
3. What is the appropriate Goodness-of-Fit metric to detect deviations governed by logarithmic density (as per the Rubinstein-Sarnak framework) rather than standard natural density?

## Methodology
1. **Artifact Diagnosis:** Mathematically deconstruct the standard chi-square calculation from the previous iteration to isolate the cause of the $p=1.0$ anomaly (e.g., assessing whether the variance of $\pi(x; q, a)$ is fundamentally mischaracterized by the Poisson/multinomial assumptions of standard chi-square).
2. **Variance Re-estimation:** Construct a new statistical test where the expected variance is derived from explicit formulas over the zeros of Dirichlet L-functions, accounting for the true asymptotic variance of primes in arithmetic progressions.
3. **Logarithmic Measure Implementation:** Shift the evaluation framework from natural counting $\pi(x)$ to logarithmic density $\delta(x) = \sum_{p \le x} \frac{1}{p}$ or $\frac{1}{\log p}$ to appropriately weight the early-term biases.
4. **Empirical Validation:** Apply the corrected statistical test to primes up to $X = 5,000,000$ modulo 210, verifying that the new $p$-value correctly rejects the strictly uniform null hypothesis in favor of the biased model.

## Success Criteria
1. Mathematical identification and explanation of why the naive uniform model yielded $p=1.0$.
2. Formulation of a corrected test statistic that successfully detects the NR > QR bias with statistical significance ($p < 0.05$) at $X = 5,000,000$.
3. Demonstration that the new variance model aligns with the $\log\log x$ scaling predicted by Rubinstein and Sarnak.

## Constraints
1. The research must remain strictly within the domain of prime distributions in primorial bases ($q=210$ and $q=2310$).
2. The statistical corrections must be theoretically grounded in analytic number theory (Dirichlet characters and L-functions), avoiding arbitrary scaling factors or ad-hoc adjustments to the variance.