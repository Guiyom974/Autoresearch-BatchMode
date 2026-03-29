# Research Problem: Strict Path Normalization and Ephemeral Single-Level Workspaces in Isolated Prime Generation

## Objective
Develop and validate a foolproof path management architecture by abandoning local nested directories in favor of OS-level ephemeral workspaces (e.g., `/tmp/run_XYZ`) and implementing strict pre-push path normalization. Following the failure of the previous iteration—where `FileNotFoundError`s still occurred due to the base experiment directory appearing twice in the constructed absolute path—this phase focuses on actively detecting and preventing duplicated path components. The goal is to enforce a pre-push validation step that resolves candidate paths against an immutable root and guarantees string-level uniqueness of path components, ensuring completely safe directory transitions.

## Research Questions
1. **Pre-Push Normalization Efficacy**: How effectively does a strict pre-push normalization step—which explicitly checks the resolved candidate path string for repeated directory components—prevent the path duplication errors seen in previous iterations?
2. **OS-Level Ephemeral Workspaces**: To what extent does utilizing a truly flat, OS-assigned temporary directory (e.g., via Python's `tempfile`) eliminate the risk of accidental path concatenation compared to nesting run folders inside local project directories?
3. **String-Level Validation**: What combinations of automated assertions (e.g., checking that the CWD string is exactly the immutable anchor plus a single, unique sub-path) are required after each context manager push/pop to guarantee path integrity?
4. **Pipeline Simulation**: Can the isolated prime generation pipeline operate flawlessly within an externally rooted ephemeral directory, successfully writing artifacts and restoring the original execution context upon completion?

## Methodology
- **Pre-Push Path Normalization**: Implement a strict validation function within the context manager that resolves every candidate path. Before applying any directory change, this function must verify that the path is a direct child of the intended root and contains no duplicated sequence of directory names.
- **Single Flat Subdirectory per Run**: Redesign the temporary directory layout to completely avoid nesting within the current working directory. Utilize standard libraries (like `tempfile.TemporaryDirectory`) to create a single flat workspace rooted in the OS temporary folder.
- **Automated CWD Integrity Checks**: Embed unit tests that fire immediately after each push and pop operation. These tests will assert that the string representation of the current working directory does not contain overlapping base paths.
- **Minimal Isolated Execution**: Continue to isolate the prime-generation algorithm (Sieve of Eratosthenes up to 10^5) to test this new, strictly normalized I/O architecture without the noise of advanced statistical modules.

## Success Criteria
A breakthrough is achieved when the infrastructure proves **completely reliable and verified**, meeting ALL of these criteria:

1. **Zero Path Exceptions**: The isolated pipeline runs from start to finish without a single `FileNotFoundError` or OS exception, successfully avoiding any duplicated directory components.
2. **Verified String-Level Integrity**: Automated assertions confirm that no component or base path sequence appears more than once in the full path strings used during execution.
3. **Verified Stack Restoration**: The context manager's logs and assertions prove that the working directory is flawlessly tracked and restored to the exact absolute starting path of the initial immutable root.
4. **Verified Artifact Creation**: Explicit `pathlib` programmatic checks successfully confirm the creation and non-zero size of the generated prime data CSV file in the OS-level ephemeral environment before cleanup.

## Constraints
- All computation must be done in Python.
- No external data downloads (must generate/compute everything locally).
- Experiments must complete within 2 minutes of runtime.
- Code must be entirely self-contained, handling its own temporary environment creation, execution, and cleanup without special dependencies.
- All intermediate findings and logs must be successfully managed within the new ephemeral directory structure.