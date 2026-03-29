# Research Problem: Anchor-Based Path Construction and Multi-Level Context Management in Isolated Prime Generation

## Objective
Develop and validate a highly resilient, anchor-based file handling architecture using `Path(__file__).resolve()` as the immutable root for all path constructions, coupled with a multi-level directory context manager. Following the failure of the previous iteration—where `FileNotFoundError`s occurred due to deeply nested temporary paths and working directory drift—this phase focuses on decoupling path resolution from the current working directory entirely. The goal is to guarantee safe directory transitions across nested levels and ensure reliable artifact generation before reintroducing complex analysis modules.

## Research Questions
1. **Anchor-Based Reliability**: How does strictly anchoring all file operations to the resolved script location (`Path(__file__).resolve().parent`) eliminate the vulnerabilities associated with working-directory dependence?
2. **Multi-Level Context Tracking**: How can an enhanced context manager accurately track and restore the original working directory across multiple nesting levels and temporary directory switches?
3. **Pre-I/O Validation**: What inline automated assertions (e.g., verifying `Path.exists()` immediately before switching directories or opening files) are required to prevent deep-nesting resolution failures?
4. **Pipeline Simulation**: Can embedded unit tests successfully simulate the full pipeline in a temporary directory, verifying that every `Path.resolve()` call yields the correct absolute path?

## Methodology
- **Anchor-Based Pathing**: Refactor the test harness so that all relative paths are constructed strictly using the resolved base of the executing script (`Path(__file__).resolve().parent`) rather than relying on the current working directory.
- **Enhanced Context Management**: Upgrade the custom context manager to support multi-level nesting, capturing and restoring the working directory at each level using a stack-based approach, and explicitly checking that target directories exist before switching into them.
- **Automated Inline Testing**: Embed lightweight unit tests within the script that simulate the path resolution process, asserting that constructed paths point to the correct absolute locations and that generated artifacts are present and non-empty.
- **Minimal Isolated Execution**: Continue to isolate the prime-generation algorithm (Sieve of Eratosthenes up to 10^5) to test this new I/O architecture without the noise of plotting or advanced statistical modules.

## Success Criteria
A breakthrough is achieved when the infrastructure proves **completely reliable and verified**, meeting ALL of these criteria:

1. **Zero Path Exceptions**: The isolated pipeline runs from start to finish without a single `FileNotFoundError` or OS exception, successfully locating the script and resolving deeply nested directories.
2. **Verified Multi-Level Restoration**: The enhanced context manager successfully tracks, transitions, and flawlessly restores the working directory across all nested levels, even if simulated exceptions are thrown.
3. **Validated Absolute Paths**: Automated assertions confirm that all path resolutions correctly map to the intended absolute paths based on the script's anchor, independent of the current working directory.
4. **Verified Artifact Creation**: Explicit `pathlib` programmatic checks successfully confirm the creation and non-zero size of the generated prime data CSV file before the temporary environment is cleaned up.

## Constraints
- All computation must be done in Python.
- No external data downloads (must generate/compute everything locally).
- Experiments must complete within 2 minutes of runtime.
- Code must be entirely self-contained, handling its own temporary environment creation, execution, and cleanup without special dependencies.
- All intermediate findings and logs must be successfully managed within the temporary directory structure using absolute paths.