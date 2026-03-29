# Research Problem: Simplified Absolute Path Stack and Flat Context Management in Isolated Prime Generation

## Objective
Develop and validate a robust, simplified path management architecture using a strict stack of absolute paths and flattened directory structures. Following the failure of the previous iteration—where `FileNotFoundError`s occurred due to duplicated directory components caused by deep nesting and faulty relative path concatenation—this phase focuses on entirely eliminating relative path appends. The goal is to enforce an absolute-path-only context manager, ensuring safe directory transitions and reliable artifact generation by restricting targets to direct, verified children of the immutable root (`Path(__file__).resolve().parent`).

## Research Questions
1. **Absolute Stack Reliability**: How does strictly enforcing a stack of pre-verified *absolute* paths within the context manager prevent the path duplication errors seen in previous iterations?
2. **Flattened Directory Architecture**: To what extent does flattening the temporary directory structure (avoiding deep nesting) reduce the risk of working-directory drift and resolution failures?
3. **Pre-I/O State Logging**: What combinations of inline automated assertions (`Path.exists()`, `Path.is_absolute()`) and context manager state logging are required to detect path drift before an OS-level exception is raised?
4. **Pipeline Simulation**: Can embedded unit tests successfully simulate the full pipeline in a flattened temporary directory, verifying that the context manager's stack push/pop operations yield the exact immutable anchor upon completion?

## Methodology
- **Simplified Absolute Pathing**: Refactor the file handling logic to strictly construct and use absolute paths. Any new path must be built directly from the immutable anchor (`Path(__file__).resolve().parent`) without appending intermediate relative components.
- **Absolute-Stack Context Management**: Redesign the multi-level context manager to maintain a clear stack of absolute paths. Instrument the manager with explicit logging of the current working directory at each push/pop operation to detect drift early.
- **Pre-I/O Verification**: Add comprehensive pre-I/O checks (e.g., `Path.exists()`, `Path.is_dir()`, `Path.is_absolute()`) immediately before every directory change or file open operation.
- **Minimal Isolated Execution**: Continue to isolate the prime-generation algorithm (Sieve of Eratosthenes up to 10^5) to test this new, flattened I/O architecture without the noise of advanced statistical modules.

## Success Criteria
A breakthrough is achieved when the infrastructure proves **completely reliable and verified**, meeting ALL of these criteria:

1. **Zero Path Exceptions**: The isolated pipeline runs from start to finish without a single `FileNotFoundError` or OS exception, successfully avoiding any duplicated directory components.
2. **Verified Stack Restoration**: The context manager's logs and automated assertions prove that the working directory is flawlessly tracked and restored to the exact absolute starting path.
3. **Validated Absolute Paths**: Automated pre-I/O assertions confirm that 100% of directory transitions use absolute paths and that the target directories exist prior to the switch.
4. **Verified Artifact Creation**: Explicit `pathlib` programmatic checks successfully confirm the creation and non-zero size of the generated prime data CSV file in the flattened temporary environment before cleanup.

## Constraints
- All computation must be done in Python.
- No external data downloads (must generate/compute everything locally).
- Experiments must complete within 2 minutes of runtime.
- Code must be entirely self-contained, handling its own temporary environment creation, execution, and cleanup without special dependencies.
- All intermediate findings and logs must be successfully managed within the temporary directory structure using absolute paths.