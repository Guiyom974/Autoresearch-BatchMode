# Research Problem: Extended Prime Pattern Analysis via Robust Computational Pipelines

## Objective
Computationally investigate prime gaps and residue-class clustering for extended ranges (up to 10^7) using a robust, self-validating execution harness. The goal is to discover non-obvious mathematical structures—specifically through high-order residue analysis and multi-layer spatial visualizations—while ensuring flawless automated execution and reproducibility.

## Research Questions
1. **Extended Prime Gaps Analysis**: How do the statistical distributions and clustering behaviors of differences between consecutive primes scale when the computational range is extended to 10^7? 
2. **High-Order Residue Class Clustering**: Do primes exhibit statistically significant clustering or avoidance in specific residue classes modulo larger primorials (e.g., 210, 2310)? 
3. **Multi-layer Spatial Patterns**: What novel structural insights emerge when primes are mapped using advanced geometric representations, such as multi-layer Ulam spirals?
4. **Computational Robustness**: How can a self-validating Python test harness effectively guarantee data generation and analysis without file-path or execution errors within a strict runtime limit?

## Methodology
- **Robust Infrastructure**: Implement a self-contained test harness with absolute file path handling, environment validation, and robust logging to capture and prevent runtime errors (e.g., `FileNotFoundError`).
- **Data Generation**: Generate primes up to 10^7 using an optimized Sieve of Eratosthenes, ensuring generation completes efficiently within the runtime constraints.
- **Statistical Analysis**: Perform clustering and gap analysis using empirical distributions, calculating means, standard deviations, and percentiles.
- **Visualization**: Create advanced plots, including multi-layer Ulam spirals and high-resolution gap distributions.
- **Artifact Management**: Embed plot images as base64 directly in the results or ensure precise, verified local artifact saving for reproducibility.
- **Hypothesis Testing**: Test clustering and gap hypotheses with quantitative metrics (p-values, correlation coefficients, effect sizes).

## Success Criteria
A breakthrough is achieved when a **non-trivial, computationally verified** pattern is discovered that meets ALL of these criteria:

1. **Reproducible**: The execution pipeline runs flawlessly without missing file errors, and the pattern holds across multiple prime ranges (e.g., up to 10^6 and 10^7).
2. **Non-obvious**: The pattern goes beyond introductory textbook facts (e.g., beyond basic 6k±1 observations).
3. **Quantifiable**: The finding is measured with clear numerical metrics (e.g., specific variance in residue class bins).
4. **Actionable**: The discovery provides a clear direction for further mathematical research or algorithmic optimization.

## Constraints
- All computation must be done in Python.
- No external data downloads (must generate/compute everything locally).
- Experiments must complete within 2 minutes of runtime.
- Code must be entirely self-contained, handling its own file creation, execution, and cleanup without special dependencies.
- All intermediate findings, logs, and visualizations must be successfully saved and validated as artifacts.