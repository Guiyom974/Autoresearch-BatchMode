# AutoResearch Code Quality Improvements

## Error Analysis Summary
**Total failed experiments:** 228 out of 722 (31.6%)

### Error Breakdown

#### 1. **Syntax Errors (11 occurrences)** — CRITICAL
- Unterminated f-strings
- Unterminated triple-quoted strings
- Missing indentation after control structures
- Missing colons in function/class definitions
- Unbalanced brackets/parens

**Root Cause**: Generated code is truncated or malformed before execution.

**Current Safeguards** (experiment.py):
- `_is_truncated()` checks for incomplete syntax ✓
- Pre-execution AST parse check ✓
- Retry on truncation with Gemini ✓

**Improvements Needed**:
- Stricter validation before running (check for unmatched quotes more carefully)
- Add explicit code length validation before execution
- Add a "code fitness" score that checks: completeness, imports, main block

#### 2. **ValueError (16 occurrences)** — HIGH PRIORITY
- `ValueError: For each axis slice, the sum of observed frequencies must match expected`
- `ValueError: high is out of bounds for int32`
- Precision/range mismatches in scipy operations

**Root Cause**: Generated code makes invalid assumptions about data dimensions or parameter ranges.

**Improvements Needed**:
- Add validation in code generation prompt to check data shapes
- Add dtype handling in code generation (ensure int64, not int32)
- Add boundary checking before scipy operations
- Validate that random ranges are within int32 bounds

#### 3. **AttributeError (11 occurrences)** — HIGH PRIORITY
- `AttributeError: 'NoneType' object has no attribute 'log'`
- `AttributeError: 'int' object has no attribute 'sqrt'` (using Decimal without proper import)
- scipy API changes (removed functions like `scipy.special.li`)

**Root Cause**: 
- Missing imports or incorrect type handling
- Generated code assumes scipy functions exist (API deprecated)

**Improvements Needed**:
- Validate scipy version compatibility
- Add explicit type checking before method calls
- Add fallback implementations for deprecated scipy functions
- Include scipy API compatibility check in code generation prompt

#### 4. **TypeError (9 occurrences)** — MEDIUM PRIORITY
- Array indexing with non-integer scalar
- Format string on None
- Type mismatches in operations

**Root Cause**: Type assumptions not validated before operations.

**Improvements Needed**:
- Add type assertions before indexing operations
- Add None checks before formatting
- Improve code generation prompts to be more explicit about types

#### 5. **ImportError (5+ occurrences)** — HIGH PRIORITY
- `scipy.special.li` not available
- `scipy.special.log10` not available  
- `scipy.signal.cwt` not available
- `np.fromstring` deprecated (removed in 1.24+)

**Root Cause**: Code generation assumes functions exist; scipy API has changed.

**Improvements Needed**:
- Add scipy version check and compatibility mappings
- Include in code gen prompt: list of ACTUAL available scipy functions
- Add fallback implementations for common deprecated functions
- Test against installed scipy/numpy versions at startup

#### 6. **UnicodeEncodeError** — MEDIUM PRIORITY
- `'charmap' codec can't encode character` on Windows

**Current Safeguard**:
- PYTHONIOENCODING=utf-8 and PYTHONUTF8=1 environment vars set ✓
- sys.stdout.reconfigure() in code template ✓

**Still Occurring**: Some edge cases slip through.

**Improvements Needed**:
- Add explicit error handler wrapping to sys.stdout in code template
- Use `encoding='utf-8', errors='replace'` for all print operations

#### 7. **Silent Crashes** — CRITICAL
- Code runs but produces zero output
- Likely early import errors or unhandled exceptions before first print

**Current Safeguard**:
- Detects silent crashes and skips retry (returns clean error) ✓

**Improvements Needed**:
- Add a startup print in generated code: `print("START", flush=True)` at very beginning
- Wrap entire execution in try-except with stderr output
- Add explicit exception handler for common import errors

#### 8. **Empty Output** — MEDIUM PRIORITY
- Code runs but produces no visible results
- Often from timeout or incomplete iterations

**Root Cause**: Algorithm too complex for available runtime.

**Improvements Needed**:
- Add execution time budget checks
- Reduce iteration limits in initial generation
- Add progress indicators to detect hangs

---

## Recommended Code Changes

### experiment.py

1. **Enhance `_code_prompt()` to include:**
   - Explicit scipy/numpy version checks
   - List of ALLOWED scipy.special functions (not deprecated)
   - Stricter dtype requirements (force int64, float64)
   - Explicit type assertions in code template
   - Progress output markers

2. **Enhance `_is_truncated()` to check for:**
   - Mismatched quotes/triple quotes
   - Unclosed f-strings
   - Missing code after certain keywords

3. **Enhance `run_code()` to:**
   - Add startup marker print
   - Wrap execution in exception handler
   - Check for import errors specifically
   - Validate code length before execution

### researcher.py

1. **Update `_code_prompt()` to:**
   - Include specific scipy function compatibility checks
   - Add version checks at start of generated code
   - Provide fallback implementations for common deprecated functions

### llm.py (if exists)

1. **Add scipy compatibility layer:**
   - Map deprecated functions to modern equivalents
   - Document which functions are safe to use

---

## Implementation Priority

**Phase 1 (CRITICAL - Fix 60% of failures):**
- Fix syntax errors with stricter validation
- Fix ImportError by testing scipy version and adding compatibility checks
- Fix silent crashes with startup markers and exception wrapping

**Phase 2 (HIGH - Fix 25% of failures):**
- Fix ValueError by adding data validation and dtype enforcement
- Fix AttributeError by adding type checking before method calls
- Fix UnicodeEncodeError with better encoding handling

**Phase 3 (MEDIUM):**
- Optimize runtime to prevent timeouts
- Add progress indicators
- Improve algorithm suggestions in code generation

---

## Testing Strategy

After implementing fixes:
1. Re-run a sample of 20 failed experiments
2. Check that failure rate drops to <15%
3. Analyze remaining failures for patterns
4. Create regression test suite from common failure cases
