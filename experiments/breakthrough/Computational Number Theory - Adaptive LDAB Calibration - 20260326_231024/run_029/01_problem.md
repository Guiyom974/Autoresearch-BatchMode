# Research Problem: Resolving Numerical Overflow Artifacts in Primorial Gap Variance-to-Mean Ratios ($k \ge 8$)

## Objective
Recent computational iterations revealed a catastrophic and anomalous drop in the Variance-to-Mean Ratio (VMR) of primorial gaps exactly at $k=8$, where the VMR plummeted from over $1.4 \times 10^6$ (at $k=7$) to $1.65$. Given the magnitude of the variance at $k=7$ ($2.93 \times 10^{12}$), this sharp discontinuity strongly indicates a 64-bit integer overflow or floating-point truncation error rather than a genuine mathematical phenomenon. The objective of this research is to diagnose and correct these numerical limitations by implementing an arbitrary-precision computational pipeline, thereby recovering the true VMR values for $k \ge 8$ and accurately determining the asymptotic scaling exponent $\gamma$.

## Research Questions
1. **Numerical Diagnosis:** At what exact computation stage (e.g., sum of squared gaps, variance calculation) did standard data types (like 64-bit floats or integers) overflow or lose precision for $k=8$?
2. **Trajectory Recovery:** Once computed with arbitrary precision, does the VMR for $k \ge 8$ seamlessly continue the exponential trajectory observed for $k \le 7$?
3. **Asymptotic Scaling:** With corrected data for $k \ge 8$, what is the true scaling behavior of the VMR, and does the exponent $\gamma$ align with the previously hypothesized $\approx 0.633$ target?

## Methodology
1. **Artifact Isolation:** Analyze the existing code to identify the bounds of the data types used for calculating the mean and variance of gaps for $k=8$ (where the primorial is $9,699,690$).
2. **Arbitrary-Precision Implementation:** Refactor the gap generation and statistical calculation pipeline to strictly use arbitrary-precision arithmetic (e.g., Python's native large integers and the `decimal` module with high precision).
3. **Recalculation and Verification:** Recalculate the VMR for bases $k=1$ through $k=12$ using the new pipeline to ensure exact parity for $k \le 7$ and to generate corrected, monotonically increasing values for $k \ge 8$.
4. **Curve Fitting:** Re-apply power-law and exponential fits to the sanitized dataset to re-evaluate the stability of the scaling exponent across all $k$.

## Success Criteria
1. **Error Identification:** Explicit documentation of the numerical threshold that triggered the artifact at $k=8$.
2. **Monotonicity Restored:** The newly calculated VMR must demonstrate strict monotonic growth for $k \ge 8$, eliminating the artificial collapse.
3. **Model Fit:** Achieving a robust fit ($R^2 > 0.99$) for the VMR scaling across the entire range $k=1$ to $k=12$, providing a reliable empirical exponent $\gamma$.

## Constraints
1. **Performance Overhead:** Arbitrary-precision arithmetic is computationally expensive; calculations for $k \ge 10$ may require significant memory and processing time.
2. **Algorithmic Limits:** The research must focus purely on computational correction and empirical measurement; developing closed-form analytical bounds is deferred until the numerical foundation is completely stabilized.