# Research Problem: Recalibration of RMT Covariance Models for Chebyshev Bias Variance Estimation

## Objective
To identify the source of the massive structural discrepancy (empirically observed at a 28,268% relative error) in the Random Matrix Theory (RMT) covariance predictions for Chebyshev bias, and to develop an augmented, mathematically rigorous variance estimation model. Given that the RMT-corrected detection test performed well (Mahalanobis distance error of 9.28%) despite the variance scaling failure, the objective is to isolate and correct the scaling factor in the theoretical RMT model without breaking the underlying distributional geometry.

## Research Questions
1. **Variance Underestimation:** Why does the standard RMT covariance prediction drastically underestimate the empirical variance of the Chebyshev bias (predicting ~1.39 vs. empirical ~394.3) for highly composite moduli like 210?
2. **L-Function Dependencies:** Are there low-lying zeros of specific Dirichlet $L$-functions for mod 210 that contribute non-trivially to the covariance matrix, violating the baseline RMT assumption of independent zero spectra?
3. **Model Augmentation:** Can an empirically adjusted RMT model—incorporating explicit, low-level zero contributions via a truncated Explicit Formula—correctly estimate the variance scale?

## Methodology
1. **Explicit Zero Computation:** Shift away from purely asymptotic RMT limits. Compute the first 1,000 non-trivial zeros for the Dirichlet $L$-functions associated with characters mod 210.
2. **Cross-Correlation Analysis:** Evaluate the cross-correlations between specific competing prime classes (e.g., Non-Residues vs. Quadratic Residues) using the explicit zeros, specifically looking for constructive interference that the asymptotic RMT model smooths out.
3. **Model Formulation:** Formulate a "Hybrid RMT-Explicit" covariance matrix that uses standard RMT for high-lying zeros but exact analytic formulas for the low-lying zeros. 
4. **Empirical Validation:** Test the revised variance predictions against existing empirical prime counts up to $x = 10^9$, using the same chunked, multi-GPU architecture from previous iterations to ensure consistent data ingestion.

## Success Criteria
1. **Variance Error Reduction:** Reduce the relative error between the theoretical variance prediction and empirical variance from >28,000% to within ±10%.
2. **Mahalanobis Stability:** Maintain or improve the Mahalanobis distance accuracy of the RMT-Corrected Detection Test (must remain within ±10% relative error).
3. **Log-Log Growth Fit:** With the corrected variance scaling, the log-log growth of the bias magnitude must achieve an $R^2 > 0.90$ (improving upon the previous $R^2 = 0.623$).

## Constraints
1. **Domain Strictness:** The investigation must remain completely within the context of Chebyshev bias for primorial moduli (mod 210, 2310). Do not expand into general prime gaps or unrelated number theory domains.
2. **Computational Limits:** Validation must be restricted to $x \le 10^9$ to allow direct 1-to-1 comparison with the previous iteration's empirical data.
3. **Algorithmic Consistency:** Do not alter the base prime-counting or multi-GPU chunking logic; the failure is strictly theoretical/mathematical in the covariance model, not in the computational prime generation.