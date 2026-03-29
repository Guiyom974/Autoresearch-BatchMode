**Research Context**  
The LDAB calibration for primorial index \(k=16\) collapses from the expected ≈ 256 bits of empirical precision to only 10 bits, while adjacent indices (k = 15, 17) remain stable at 256 bits. Prior work identified:  

* overflow‑detection failures at high \(k\) (run 035),  
* a later overflow threshold at \(k=132\) where \(\log P_k\) exceeds the double‑precision range (run 036), and  
* premature overflow at small \(k\) caused by unguarded gamma evaluations (run 037).  

The \(k=16\) anomaly is highly localized and coincides with the moment the primorial’s size (\(\log_2 P_{16}\approx64.82\)) first surpasses a 64‑bit word boundary. The hypotheses below are designed to isolate whether the collapse stems from (i) a 64‑bit integer overflow/truncation in an intermediate arithmetic step, (ii) a numerical instability such as catastrophic cancellation, or (iii) a bug in the arbitrary‑precision library’s conversion or exponentiation routines. Each hypothesis is testable with the proposed bit‑level tracing, exact‑arithmetic cross‑validation, and boundary‑testing experiments.

---

## Hypothesis 1 – **Integer‑overflow in the intermediate binomial/factorial term**

**1. Hypothesis statement**  
The 10‑bit precision collapse at \(k=16\) is caused by an intermediate factorial or binomial‑coefficient calculation that exceeds the 64‑bit word size before being reduced. The arbitrary‑precision library stores this intermediate result as a 64‑bit unsigned integer (or truncates it to 64 bits), wrapping the value to a small number that propagates through the rest of the LDAB evaluation, destroying precision.

**2. Why it’s testable**  
*The hypothesis makes a concrete, falsifiable prediction*: at some step in the \(k=16\) run, an intermediate integer will exceed \(2^{64}-1\). If we can observe such an overflow and reproduce the 10‑bit result by forcing 64‑bit arithmetic at that step, the hypothesis is confirmed; otherwise it is refuted.

**3. Experiment that would test it**  

| Step | Procedure |
|------|------------|
| **A. Bit‑level tracing** | Insert instrumentation (e.g., logging of all intermediate integer multiplications/divisions) in the LDAB code for \(k=16\). Record the exact magnitude of every intermediate factorial, binomial coefficient, and product of primes. Flag any value > \(2^{64}-1\). |
| **B. Boundary‑forcing test** | Modify the code so that *only* the flagged operation (or all integer ops) are forced to use 64‑bit unsigned arithmetic (i.e., wrap on overflow). Re‑run the calibration for \(k=16\) and compare the final empirical precision. If the 10‑bit collapse reproduces, the hypothesis is supported. |
| **C. Exact‑arithmetic cross‑validation** | Re‑compute the same binomial/factorial term with an exact rational library (SymPy, mpmath’s `Integer` type) and verify that the true value indeed exceeds \(2^{64}\). A divergence between the exact value and the library’s internal representation will pinpoint the overflow source. |

If the collapse is reproduced only when the intermediate exceeds 64 bits, we have isolated the overflow as the root cause. If no overflow is observed, we move to the next hypothesis.

---

## Hypothesis 2 – **Catastrophic cancellation in the log‑density difference**

**1. Hypothesis statement**  
The LDAB log‑density term for \(k=16\) is computed as the difference of two large numbers (e.g., \(\log\Gamma(P_{16})\) and \(\log\Gamma(P_{16}-1)\)) that are within a factor of \(2^{10}\) of each other. The subtraction cancels most of the significant bits, leaving only ~10 bits of accurate information in the final result.

**2. Why it’s testable**  
If cancellation is the culprit, the *relative magnitude* of the two terms will be extremely close, and the true result will have far fewer than 256 bits of accuracy when computed with standard floating‑point arithmetic. By performing the same subtraction in arbitrary‑precision rational arithmetic we can confirm whether the true result indeed has low relative precision, and whether the floating‑point implementation loses the expected bits.

**3. Experiment that would test it**  

| Step | Procedure |
|------|------------|
| **A. Exact‑arithmetic subtraction** | Using SymPy (or an equivalent exact‑arithmetic system), compute the two logarithmic terms exactly as rational logarithms, then perform the subtraction with unlimited precision (e.g., 2000 bits). Determine the *exact* bit‑accuracy of the difference by comparing it to a reference value computed with even higher precision. |
| **B. Magnitude analysis** | Compute the ratio of the two terms (or their exponential representations) for \(k=16\). If the ratio is within \(2^{10}\) of 1, catastrophic cancellation is inevitable in binary floating‑point. |
| **C. Floating‑point comparison** | Run the LDAB calibration for \(k=16\) in the original library, then recompute the *same* subtraction using a high‑precision floating‑point type (e.g., 512‑bit MPFR) and compare the number of correct bits. If the MPFR result also shows a drop to ~10 bits, cancellation is confirmed. |
| **D. Algorithmic remedy** | Implement an alternative formula for the log‑density that avoids direct subtraction (e.g., use `log Gamma` directly, or apply the log‑difference identity \(\log a - \log b = \log(a/b)\) before exponentiation). Test whether this avoids the precision loss. |

Confirmation: if the exact arithmetic yields a result with full precision but the floating‑point subtraction yields only 10 bits, the hypothesis is validated.

---

## Hypothesis 3 – **Conversion bug at the 64‑bit integer‑to‑floating‑point boundary**

**1. Hypothesis statement**  
The arbitrary‑precision library’s routine that converts a high‑precision integer (the primorial \(P_{16}\) ≈ \(2^{64.82}\)) to a binary floating‑point value mis‑handles numbers just larger than \(2^{64}\). The conversion algorithm (often a “split‑and‑round” step) erroneously truncates the mantissa to ~10 bits, producing a floating‑point approximation that retains only 10 bits of the original integer’s value.

**2. Why it’s testable**  
The hypothesis makes a precise, library‑specific prediction: the conversion function will lose mantissa bits for any integer in the narrow range \((2^{64},\,2^{65})\). This can be tested in isolation by feeding the library a known integer in that range and examining the resulting floating‑point bit pattern.

**3. Experiment that would test it**  

| Step | Procedure |
|------|------------|
| **A. Minimal conversion test** | Write a small program that (i) constructs an arbitrary‑precision integer exactly equal to \(P_{16}\) (or a comparable number such as \(2^{64}+2^{10}\)), (ii) converts it to the library’s binary `float` type, and (iii) extracts the mantissa bits (e.g., by using `frexp` or comparing the float to neighboring floating‑point values). Compare the converted value to the true integer value to count how many bits are correct. |
| **B. Boundary sweep** | Perform the same conversion test for a sequence of integers: \(2^{63}\), \(2^{64}\), \(2^{64}+1\), …, \(2^{65}\). Plot the number of correct bits as a function of the integer’s bit‑length. A sudden drop to ~10 bits precisely at the transition from 64‑ to 65‑bit numbers would indicate a conversion bug. |
| **C. Library version comparison** | If the library offers multiple build configurations (e.g., with/without assembly optimizations), repeat the conversion test for each. A difference in behavior would pinpoint the bug to a specific code path. |
| **D. Cross‑library validation** | Convert the same integer using a second, independent arbitrary‑precision library (e.g., GMP’s `mpf` or MPFR) and verify that the conversion yields the full 64‑bit mantissa. Divergence would confirm the bug in the first library. |

If the conversion test shows a systematic loss of ≈ 54 bits (i.e., only 10 bits remain) for numbers just above \(2^{64}\), the hypothesis is confirmed.

---

## Hypothesis 4 – **Unguarded gamma evaluation returning a 64‑bit integer at \(k=16\)**

**1. Hypothesis statement**  
The LDAB calibration calls a gamma function for an argument that at \(k=16\) yields a value exactly representable as a 64‑bit integer. The library’s gamma implementation returns this as a native 64‑bit integer rather than an arbitrary‑precision object, causing subsequent arithmetic (e.g., multiplication or division) to be performed in 64‑bit mode and to overflow or truncate, which ultimately collapses the precision of the final density estimate to 10 bits.

**2. Why it’s testable**  
The hypothesis predicts that the gamma function will return a *machine‑integer* type (e.g., `uint64_t`) and that the result will be exactly a power‑of‑two or a small integer. By intercepting the gamma call and inspecting the returned type and value, we can determine whether the overflow originates there. Re‑running the calibration with a wrapper that forces the gamma result into arbitrary‑precision should restore the correct precision.

**3. Experiment that would test it**  

| Step | Procedure |
|------|------------|
| **A. Gamma call isolation** | Extract the specific gamma argument used in the LDAB formula for \(k=16\) (e.g., \(\Gamma(P_{16})\) or \(\Gamma(P_{16}+1)\)). Compute the gamma function using the same library and record the returned type (`int`, `uint64_t`, `mpz_t`, etc.) and value. |
| **B. Exact‑arithmetic gamma** | Compute the same gamma using a CAS (SymPy’s `gamma` with rational arguments) or an arbitrary‑precision library (mpmath’s `mp.gamma`) to obtain the exact integer (or arbitrary‑precision) value. Compare this to the library’s result. A mismatch (especially if the library returns a 64‑bit integer) points to the bug. |
| **C. Forced arbitrary‑precision wrapper** | Modify the LDAB code to wrap every gamma call with a cast to an arbitrary‑precision integer type (e.g., `mpz` in GMP). Re‑run the calibration for \(k=16\) and observe whether the empirical precision returns to ~256 bits. |
| **D. Regression test across k** | Apply the same wrapper for all k in [11, 17] and verify that the 10‑bit collapse disappears only at \(k=16\) while preserving performance elsewhere. |

If wrapping the gamma call restores full precision, the hypothesis is validated. If not, the problem lies elsewhere.

---

## Hypothesis 5 – **Exponentiation overflow/underflow in the log‑density term at the 64‑bit exponent boundary**

**1. Hypothesis statement**  
The LDAB log‑density term involves an exponential operation (e.g., \(\exp(\theta)\) or \(e^{\theta}\)) where the exponent \(\theta\) is proportional to \(\log P_{16}\) (≈ 64.82 bits). The library’s exponentiation routine uses a 64‑bit exponent field internally; when the true exponent exceeds this limit, the routine either overflows to a special value (inf) or underflows to zero, and subsequent logarithmic transformations reduce the result to a value with only ~10 bits of meaningful mantissa.

**2. Why it’s testable**  
If exponentiation is the bottleneck, feeding the routine a value just above the 64‑bit exponent threshold will produce a dramatically incorrect result. By testing the exponentiation routine in isolation and by deliberately scaling the exponent to stay within the 64‑bit limit, we can observe whether the precision loss disappears.

**3. Experiment that would test it**  

| Step | Procedure |
|------|------------|
| **A. Exponentiation boundary test** | Using the same arbitrary‑precision library, compute `exp(64.82*ln(2))` (i.e., the value that should equal \(P_{16}\)). Compare the result to the true primorial. Record the number of correct bits. Also test `exp(63*ln(2))` and `exp(65*ln(2))` to see where the accuracy breaks down. |
| **B. Restricted exponent width** | Modify the exponentiation routine to cap the exponent at 63 bits (i.e., enforce `if (exponent > 2^63) then clamp to 2^63`). Re‑run the LDAB calibration for \(k=16\) and check whether the 10‑bit collapse persists or disappears. |
| **C. Alternative exponentiation** | Replace the library’s `exp` with a user‑defined implementation that uses arbitrary‑precision arithmetic for the whole operation (e.g., MPFR’s `mpfr_exp` with precision set to 256 bits). Compare the resulting precision for \(k=16\). |
| **D. Log‑then‑exp analysis** | In the LDAB formula, identify the exact expression that is exponentiated. Compute it using symbolic differentiation or using log‑sum‑exp tricks to avoid large exponents. If the precision improves, the original exponentiation was the culprit. |

If the precision restores when using a higher‑precision exponentiation method, the hypothesis is confirmed.

---

### How These Hypotheses Address the Research Questions

| Hypothesis | Root‑cause focus | Direct test of word‑size boundary? | Algorithmic fix suggested? |
|------------|------------------|-----------------------------------|---------------------------|
| **H1** – Integer overflow in intermediate factorial/binomial | Yes – checks 64‑bit overflow of intermediate ints | Yes – forces 64‑bit arithmetic | Yes – use arbitrary‑precision ints for that step |
| **H2** – Catastrophic cancellation in log‑density difference | Yes – evaluates numerical stability of subtraction | Indirectly (size of terms near 2^64) | Yes – rewrite subtraction using log‑ratio |
| **H3** – Conversion bug at 64‑bit integer→float boundary | Yes – isolates library conversion bug | Directly – tests conversion at exact boundary | Yes – patch or bypass conversion |
| **H4** – Unguarded gamma returning 64‑bit integer | Yes – checks gamma implementation | Indirectly (gamma result near 2^64) | Yes – wrap gamma in arbitrary‑precision type |
| **H5** – Exponentiation overflow/underflow | Yes – tests exponentiation routine | Directly – tests exponent near 2^64 | Yes – replace with higher‑precision exp |

Each hypothesis is **mutually exclusive** (they invoke distinct mechanisms) but **not exhaustive**; additional subtle bugs (e.g., in rounding mode selection) could emerge. The experimental suite is designed to **逐层排除** (eliminate) each possibility until the precise computational origin is identified. Once the culprit is pinned down, the corresponding algorithmic correction (e.g., using arbitrary‑precision integers for intermediate factorials, rewriting the log‑difference, or patching the conversion routine) should restore the expected ~256‑bit precision for \(k=16\) and allow the linear scaling law to recover an \(R^{2}>0.90\).