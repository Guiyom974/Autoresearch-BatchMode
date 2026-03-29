# Research Problem: Absolute Path Resolution and Explicit I/O Verification in Isolated Prime Generation

## Objective
Develop and validate a bulletproof file-handling mechanism for in-process prime pattern analysis by enforcing absolute path resolution and explicit I/O verification. Following the failure of the initial in-process migration due to persistent `FileNotFoundError` exceptions, this phase strips away visualization and complex statistical modules. The goal is to perform a minimal, isolated test (primes up to 10^5) within a temporary directory, strictly utilizing absolute paths and pre-write/post-write existence checks to guarantee reliable artifact generation before reintroducing complex analysis modules.

## Research Questions
1. **Absolute Path Reliability**: How does strictly enforcing absolute paths (`os.path.abspath`) for all file I/O operations within a temporary context manager eliminate the path-resolution failures observed in previous in-process iterations?
2. **Explicit I/O Verification**: What is the most effective logging and verification strategy (e.g., `os.path.isdir`, `os.path.exists`, `os.path.getsize`) to diagnose and prevent file write errors in real-time during execution?
3. **Isolated Pipeline Viability**: Can a stripped-down, isolated prime-generation function execute flawlessly within this strictly managed environment, proving the foundational I/O architecture is sound?
4. **Environment Context Management**: How can the execution environment safely alter and restore its working directory (`os.chdir`) during the temporary context lifecycle without breaking internal module imports?

## Methodology
- **Absolute Path Enforcement**: Refactor the test harness to compute and utilize absolute paths for all file operations (logs, data exports). Ensure the current working directory is explicitly set and verified before any imports or file writes occur.
- **Minimal Isolated Testing**: Temporarily remove the plotting and extended statistical computation modules. Focus solely on executing the prime-generation algorithm (Sieve of Eratosthenes up to 10^5) and writing the raw output to a CSV.
- **Explicit Checkpoints**: Insert explicit pre-write and post-write assertions (`os.path.exists`, file size checks) accompanied by detailed standard output logging for every artifact generation step.
- **Context Management**: Continue utilizing Python's `tempfile.TemporaryDirectory()`, but ensure the absolute path of this directory is actively passed to all file-writing functions rather than relying on relative working directory assumptions.

## Success Criteria
A breakthrough is achieved when the infrastructure proves **completely reliable and verified**, meeting ALL of these criteria:

1. **Zero Path Exceptions**: The isolated pipeline runs from start to finish without a single `FileNotFoundError`, OS exception, or path resolution failure.
2. **Verified Artifact Creation**: Explicit programmatic checks successfully confirm the creation and non-zero size of the generated prime data CSV file using absolute paths before the temporary directory is cleaned up.
3. **Accurate Baseline Data**: The prime generation function accurately computes the primes up to 10^5 and successfully writes them to disk.
4. **Actionable Foundation**: The absolute-path I/O framework is proven stable, providing a verified foundation to safely reintroduce visualization and advanced statistical modules in the next iteration.

## Constraints
- All computation must be done in Python.
- No external data downloads (must generate/compute everything locally).
- Experiments must complete within 2 minutes of runtime.
- Code must be entirely self-contained, handling its own temporary environment creation, execution, and cleanup without special dependencies.
- All intermediate findings and logs must be successfully managed within the temporary directory structure using absolute paths.