# Research Problem: Robust Path Component Validation and Native TemporaryDirectory Anchoring in Isolated Prime Generation

## Objective
Develop and validate a fully resilient path management architecture by abandoning custom path string manipulation in favor of Python's native `TemporaryDirectory` as an immutable anchor, coupled with strict part-based path validation. Following the failure of the previous iteration—where string-based pre-push normalization failed to detect duplicated directory components (resulting in `FileNotFoundError`s)—this phase focuses on analyzing the sequence of path parts (`pathlib.Path.parts`). The goal is to explicitly resolve candidate paths using `pathlib.Path.resolve(strict=False)`, compare their parts against the immutable root, and proactively reject any path containing repeating components before execution, ensuring completely safe directory transitions.

## Research Questions
1. **Part-Based Validation Efficacy**: How effectively does a strict pre-push validation step—which explicitly compares `pathlib.Path.parts` to detect repeating components—prevent the path duplication errors missed by previous string-based normalization?
2. **Native Anchoring**: To what extent does utilizing Python's built-in `TemporaryDirectory` as the sole immutable anchor simplify state tracking and eliminate accidental base path duplication during context manager transitions?
3. **Simulated Failure Resilience**: Can automated tests that deliberately introduce duplicated components in nested directory creation verify the robust interception of malformed paths before any `os.chdir` operation occurs?
4. **Pipeline Execution**: Can the isolated prime generation pipeline operate flawlessly within this natively anchored environment, successfully writing artifacts and passing all post-push assertions?

## Methodology
- **Native TemporaryDirectory Anchoring**: Replace custom ephemeral workspace managers with Python's built-in `tempfile.TemporaryDirectory`. Use its `.path` attribute as the absolute, immutable anchor for all operations.
- **Part-Based Path Normalization**: Implement a validation function that resolves every candidate path using `pathlib.Path.resolve(strict=False)`. Iterate through `pathlib.Path.parts` to explicitly verify that no directory component from the relative path repeats or duplicates the root's components.
- **Simulated Failure Injection**: Embed automated unit tests that deliberately construct malformed paths with duplicated components (e.g., nesting the run folder inside itself) to prove the validation logic correctly raises exceptions *before* directory transitions.
- **Post-Push Assertions**: Enforce post-push checks verifying that the current working directory exactly matches `anchor / unique_run_id` and that no component of the relative path appears elsewhere in the absolute path.

## Success Criteria
A breakthrough is achieved when the infrastructure proves **completely reliable and verified**, meeting ALL of these criteria:

1. **Zero Pipeline Exceptions**: The isolated prime generation pipeline runs from start to finish without a single `FileNotFoundError` or OS exception, successfully avoiding any duplicated directory components.
2. **Verified Part-Level Integrity**: Automated assertions confirm that no component in the sequence of path parts is illegally duplicated during execution.
3. **Successful Failure Interception**: Simulated failure tests correctly and safely reject deliberately malformed paths with duplicated components before any state changes occur.
4. **Verified Artifact Creation**: Explicit `pathlib` programmatic checks successfully confirm the creation and non-zero size of the generated prime data CSV file in the natively anchored ephemeral environment before cleanup.

## Constraints
- All computation must be done in Python.
- No external data downloads (must generate/compute everything locally).
- Experiments must complete within 2 minutes of runtime.
- Code must be entirely self-contained, handling its own temporary environment creation, execution, and cleanup without special dependencies.
- All intermediate findings and logs must be successfully managed within the new ephemeral directory structure.