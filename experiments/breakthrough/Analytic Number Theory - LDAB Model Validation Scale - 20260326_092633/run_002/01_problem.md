# Research Problem: Robust Statistical Methodologies for Evaluating Chebyshev Bias in Primorial Bases

## Objective
Develop a mathematically rigorous statistical framework for evaluating Chebyshev Bias modulo 210 and 2310, focusing specifically on the precise formulation of expected frequencies. The goal is to establish accurate Goodness-of-Fit testing across all Quadratic Residue (QR) and Non-Residue (NR) classes, ensuring valid statistical comparisons even in sparse distributions at finite scales.

## Research Questions
1. How can the expected frequencies of primes in residue classes modulo 210 and 2310 be accurately modeled using the Prime Number Theorem for arithmetic progressions to prevent statistical anomalies (e.g., zero or near-zero expected counts) at $x \le 5,000,000$?
2. What normalization, thresholding, or class-grouping strategies are required to ensure robust Chi-Square statistics when tracking the NR−QR prime count differences?
3. Once expected frequencies are rigorously defined, does the statistically significant Chebyshev-type bias previously observed remain robust under strict Goodness-of-Fit validation?

## Methodology
1. **Expected Frequency Formulation:** Replace naive uniform distribution assumptions with precise expected frequency calculations based on $\pi(x; q, a) \sim \text{Li}(x)/\phi(q)$, ensuring exact sum-matching between observed and expected counts over the interval.
2. **Dynamic Thresholding:** Implement minimum-count thresholds (e.g., $E_i \ge 5$) for residue classes. If sparse classes at lower bounds fail this threshold, apply mathematically sound grouping strategies to preserve degrees of freedom while maintaining the NR vs. QR distinction.
3. **Statistical Validation:** Re-run the Goodness-of-Fit testing on the generated prime dataset ($x = 5,000,000$) using the corrected expected frequencies, calculating the $\chi^2$ statistic and $p$-values to evaluate the Rubinstein-Sarnak predictions.

## Success Criteria
1. Mathematical formulation of expected frequencies that strictly satisfies the constraints of Goodness-of-Fit testing (no negative, zero, or sub-threshold expected counts).
2. Successful completion of statistical divergence tests across the dataset without undefined mathematical operations.
3. Generation of a statistically sound confidence interval and $p$-value for the observed Chebyshev bias modulo 210 and 2310.

## Constraints
* The study must remain strictly focused on the primorial bases 210 and 2310.
* The analysis must maintain the distinction between Quadratic Residues and Non-Residues.
* Methodological improvements must be grounded in analytic number theory (e.g., Dirichlet's theorem on arithmetic progressions) rather than arbitrary statistical smoothing.