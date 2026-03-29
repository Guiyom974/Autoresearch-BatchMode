# Research Problem: Establishing a Robust Temporary-File Pipeline for Prime Pattern Analysis

## Objective
Develop and validate a robust, error-free computational pipeline for prime pattern analysis using temporary directories and strict path resolution. Before exploring extended prime ranges, this phase focuses on performing a minimal sanity-check experiment (primes up to 10^5) to verify end-to-end execution, artifact generation, and statistical computation without encountering OS-level or file-path errors.

## Research Questions
1. **Pipeline Robustness**: How can Python's `tempfile` and `pathlib` modules be utilized to create a self-validating execution harness that guarantees zero `FileNotFoundError` occurrences during automated runs?
2. **Artifact Lifecycle Management**: What is the most reliable method for generating, validating, and extracting visualization and data artifacts from a temporary execution environment before cleanup?
3. **Baseline Statistical Validation**: When generating primes up to 10^5, do the baseline gap statistics and basic residue-class distributions correctly match known mathematical expectations, confirming the analytical engine's accuracy?
4. **Execution Efficiency**: Can the end-to-end process—environment setup, prime generation, basic statistical analysis, plotting, and teardown—execute reliably well within the strict 2-minute limit?

## Methodology
- **Infrastructure Overhaul**: Restructure the test harness to exclusively use Python's `tempfile.TemporaryDirectory()`. Implement strict absolute-path resolution using `pathlib` and verify file existence prior to any subprocess execution.
- **Error Handling**: Add comprehensive `try/except` blocks around all file I/O and OS-level operations to gracefully capture, log, and report failures rather than crashing.
- **Minimal Sanity-Check Data**: Generate primes up to a reduced range of 10^5 using a standard Sieve of Eratosthenes to minimize computational load while testing the pipeline.
- **Basic Analysis & Visualization**: Compute fundamental prime gap statistics (mean, max, basic frequencies) and generate a simple histogram to test the artifact saving mechanism.
- **Verification Step**: Programmatically assert the existence and non-zero size of all generated output files (logs, CSVs, PNGs) before the temporary directory is cleaned up.

## Success Criteria
A breakthrough is achieved when the infrastructure proves **completely reliable and verified**, meeting ALL of these criteria:

1. **Flawless Execution**: The pipeline runs from start to finish without a single `FileNotFoundError` or unhandled OS exception.
2. **Verified Artifacts**: The test harness successfully proves the creation of valid data and image files within the temporary directory and safely copies them to a persistent location (or embeds them as base64).
3. **Accurate Baseline Data**: The prime generation and basic gap statistics for primes up to 10^5 are computed correctly, providing a solid foundation for future scaling.
4. **Actionable Foundation**: The validated harness requires no further structural changes to safely scale the prime generation limit up to 10^7 in subsequent experiments.

## Constraints
- All computation must be done in Python.
- No external data downloads (must generate/compute everything locally).
- Experiments must complete within 2 minutes of runtime.
- Code must be entirely self-contained, handling its own temporary environment creation, execution, and cleanup without special dependencies.
- All intermediate findings, logs, and visualizations must be successfully managed within the temporary directory structure.