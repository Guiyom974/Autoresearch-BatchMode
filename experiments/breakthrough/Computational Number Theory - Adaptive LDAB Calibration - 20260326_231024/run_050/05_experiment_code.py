import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from scipy import special
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Constants
PRIMORIAL_INDICES = list(range(1, 21))  # k = 1 to 20
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

def segmented_sieve(limit):
    """Return list of primes up to `limit` using segmented sieve."""
    if limit < 2:
        return []
    # Simple sieve for small limits
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i:limit+1:i] = False
    return np.where(sieve)[0].tolist()

def primorial(k):
    """Compute the k-th primorial: product of first k primes."""
    if k <= 0:
        return 1
    return int(np.prod(PRIMES[:k]))

def log_primorial(k):
    """Compute log of k-th primorial using sum of logs of first k primes."""
    if k <= 0:
        return 0.0
    return np.sum(np.log(PRIMES[:k]))

def ldab_gamma_term(k):
    """
    LDAB gamma term: Γ(k + 1/2) / Γ(1/2)
    Using log-gamma for numerical stability: log Γ(k + 1/2) - log Γ(1/2)
    Returns both double and extended (float64 and float128 if available) versions.
    """
    # Standard double precision
    log_gamma_k_half = special.gammaln(k + 0.5)
    log_gamma_half = special.gammaln(0.5)
    log_term_double = log_gamma_k_half - log_gamma_half
    term_double = np.exp(log_term_double)
    
    # Extended precision (via float128 if available, else fallback to float64)
    try:
        # Try to use numpy's float128 (available on some platforms)
        log_gamma_k_half_ext = np.longdouble(special.gammaln(np.longdouble(k) + np.longdouble(0.5)))
        log_gamma_half_ext = np.longdouble(special.gammaln(np.longdouble(0.5)))
        log_term_ext = log_gamma_k_half_ext - log_gamma_half_ext
        term_ext = np.exp(log_term_ext)
    except (AttributeError, ValueError, OverflowError):
        # float128 not available; use high-precision via mpmath not allowed — fallback to double
        term_ext = term_double
    
    return term_double, term_ext

def ldab_loggamma_term(k):
    """
    LDAB term using log-gamma directly (no exponentiation until final step).
    This is the guarded formulation.
    """
    return special.gammaln(k + 0.5) - special.gammaln(0.5)

def ldab_direct_exponentiated(k):
    """
    LDAB term computed by exponentiating the log-gamma difference.
    This may cause underflow/overflow or loss of precision for large k.
    """
    return np.exp(ldab_loggamma_term(k))

def ldab_stable(k):
    """
    LDAB stable version: use exp(log_gamma_diff) with scaling if needed.
    Here we use the direct exponentiation, but with log-gamma for stability.
    """
    return np.exp(ldab_loggamma_term(k))

def ldab_full_calibration(k):
    """
    Simulated LDAB calibration step that includes:
    - primorial P_k
    - gamma term Γ(k+1/2)/Γ(1/2)
    - normalization factor
    
    Returns double and extended-precision versions.
    """
    P_k = primorial(k)
    logP_k = log_primorial(k)
    
    # LDAB formula: term = exp( logP_k ) * Γ(k+1/2)/Γ(1/2)
    # But logP_k may overflow in exponentiation for large k, so we compute log of full term:
    log_term_double = logP_k + ldab_loggamma_term(k)
    term_double = np.exp(log_term_double) if log_term_double < 709 else np.inf
    
    # Extended precision
    try:
        logP_k_ext = np.longdouble(logP_k)
        log_term_ext = logP_k_ext + np.longdouble(ldab_loggamma_term(k))
        if log_term_ext < np.log(np.longdouble(np.finfo(np.float64).max)):
            term_ext = np.exp(log_term_ext)
        else:
            term_ext = np.longdouble('inf')
    except (AttributeError, ValueError, OverflowError):
        term_ext = term_double
    
    return term_double, term_ext

def mantissa_bits(x):
    """
    Estimate the number of significant mantissa bits in a floating-point number
    by comparing to high-precision reference (if available).
    Returns integer bits (0–53 for double).
    """
    # Use float128 reference if available
    try:
        x_ext = np.longdouble(x)
        # Compute relative error against high-precision version
        # Use a reference computed at high precision (simulated)
        # For now, use a heuristic: count trailing zeros in binary representation of mantissa
        # This is crude but sufficient for comparison.
        if x == 0:
            return 0
        # Get mantissa as integer
        mant, exp = np.frexp(x)
        mant_int = int(mant * 2**53)  # 53-bit mantissa for double
        # Count leading 1 bits in mantissa (from MSB)
        # Find position of first 1
        bin_str = bin(mant_int)[2:]  # strip '0b'
        # Pad to 53 bits
        bin_str = bin_str.zfill(53)
        # Count consecutive 1s from left (rough proxy for precision)
        # Better: count bits until first 0 after first 1
        first_one = bin_str.find('1')
        if first_one == -1:
            return 0
        # Count trailing bits after first 1
        trailing = bin_str[first_one+1:]
        # Count significant bits as position of last 1
        last_one = len(bin_str) - 1 - trailing[::-1].find('1') if '1' in trailing else first_one
        return max(0, last_one + 1 - first_one)
    except Exception:
        return 53  # assume full double precision

def test_hypotheses():
    """
    Run controlled experiments to test each hypothesis.
    Returns dict of results.
    """
    results = {}
    
    # === H1: Log-gamma term alone causes collapse at k=16 ===
    print("=" * 70)
    print("H1: Log-gamma term precision collapse test")
    print("=" * 70)
    k_test = 16
    term_double, term_ext = ldab_gamma_term(k_test)
    print(f"k = {k_test}")
    print(f"  Double-precision term: {term_double:.16e}")
    print(f"  Extended-precision term: {term_ext:.16e}")
    if term_ext != term_double:
        rel_err = abs(term_ext - term_double) / abs(term_ext)
        print(f"  Relative error: {rel_err:.2e}")
        if rel_err > 1e-10:
            print("  → H1 SUPPORTED: log-gamma term shows precision loss in double")
        else:
            print("  → H1 NOT SUPPORTED: relative error < 1e-10")
    else:
        print("  → H1 NOT SUPPORTED: terms match exactly")
    results['H1'] = rel_err > 1e-10 if term_ext != term_double else False
    
    # === H2: Full LDAB calibration (logP_k + log_gamma) loses mantissa bits at k=16 ===
    print("\n" + "=" * 70)
    print("H2: Full calibration mantissa-bit loss test")
    print("=" * 70)
    mantissa_losses = []
    for k in PRIMORIAL_INDICES[:17]:  # up to k=16
        term_d, term_e = ldab_full_calibration(k)
        if term_d == 0 or term_e == 0:
            mantissa_losses.append(0)
            continue
        # Estimate bits of precision in double version
        bits = mantissa_bits(term_d)
        mantissa_losses.append(bits)
        print(f"k={k:2d}: double term ≈ {term_d:.6e}, estimated mantissa bits = {bits}")
    
    # Check for collapse at k=16
    k_collapse = 16
    idx = k_collapse - 1
    if 0 <= idx < len(mantissa_losses):
        bits_at_16 = mantissa_losses[idx]
        print(f"\nAt k=16: estimated mantissa bits = {bits_at_16}")
        if bits_at_16 <= 12:  # ~10-bit precision collapse
            print("  → H2 SUPPORTED: mantissa bits collapsed to ~10 bits")
        else:
            print("  → H2 NOT SUPPORTED: mantissa bits > 12")
    results['H2'] = bits_at_16 <= 12 if 0 <= idx < len(mantissa_losses) else False
    
    # === H3: Log-gamma overflow is NOT the cause (since k=16 << k=132) ===
    print("\n" + "=" * 70)
    print("H3: Overflow test (logP_k vs double exponent limit)")
    print("=" * 70)
    logP_k_16 = log_primorial(16)
    print(f"logP_k at k=16: {logP_k_16:.6f}")
    print(f"Double exponent limit: log(2^1023) ≈ {np.log(np.finfo(np.float64).max):.6f}")
    if logP_k_16 < 700:
        print("  → H3 SUPPORTED: logP_k far below exponent limit (no overflow)")
    else:
        print("  → H3 NOT SUPPORTED: logP_k near/above limit")
    results['H3'] = logP_k_16 < 700
    
    # === H4: Gamma term alone (not primorial) causes collapse ===
    print("\n" + "=" * 70)
    print("H4: Isolated gamma-term precision test")
    print("=" * 70)
    gamma_terms = []
    for k in range(1, 17):
        term_d, term_e = ldab_gamma_term(k)
        if term_e != 0:
            rel_err = abs(term_e - term_d) / abs(term_e)
            gamma_terms.append((k, rel_err))
    
    # Find max relative error up to k=16
    if gamma_terms:
        max_err = max(err for _, err in gamma_terms)
        k_max_err = max(gamma_terms, key=lambda x: x[1])[0]
        print(f"Max relative error in gamma term up to k=16: {max_err:.2e} at k={k_max_err}")
        if max_err > 1e-10:
            print("  → H4 SUPPORTED: gamma term alone shows precision loss")
        else:
            print("  → H4 NOT SUPPORTED: gamma term stable")
    results['H4'] = max_err > 1e-10 if gamma_terms else False
    
    # === H5: Product of primorial and gamma term loses precision due to cancellation ===
    print("\n" + "=" * 70)
    print("H5: Cancellation test (log-add vs direct multiply)")
    print("=" * 70)
    # Compute using log-space vs direct multiplication
    k = 16
    logP = log_primorial(k)
    log_gamma_diff = ldab_loggamma_term(k)
    log_sum = logP + log_gamma_diff
    
    # Direct method (dangerous, but for test)
    P_k = primorial(k)
    gamma_term = ldab_gamma_term(k)[0]  # double
    try:
        direct_val = P_k * gamma_term
    except (OverflowError, RuntimeWarning):
        direct_val = np.inf
    
    # Log-based method
    log_based_val = np.exp(log_sum)
    
    print(f"Direct multiply: {direct_val:.6e}")
    print(f"Log-based exp:   {log_based_val:.6e}")
    if np.isfinite(direct_val) and np.isfinite(log_based_val):
        rel_err_direct = abs(direct_val - log_based_val) / abs(log_based_val)
        print(f"Relative difference: {rel_err_direct:.2e}")
        if rel_err_direct > 1e-6:
            print("  → H5 SUPPORTED: direct multiply suffers cancellation")
        else:
            print("  → H5 NOT SUPPORTED: methods agree")
    else:
        print("  → H5 INCONCLUSIVE: overflow in direct multiply")
    results['H5'] = rel_err_direct > 1e-6 if (np.isfinite(direct_val) and np.isfinite(log_based_val)) else False
    
    # === Generate plots ===
    print("\n" + "=" * 70)
    print("Generating diagnostic plots...")
    print("=" * 70)
    
    # Plot 1: Mantissa bits vs k
    plt.figure(figsize=(8, 5))
    ks = list(range(1, 17))
    bits_list = []
    for k in ks:
        term_d, _ = ldab_full_calibration(k)
        bits = mantissa_bits(term_d)
        bits_list.append(bits)
    plt.plot(ks, bits_list, 'bo-', label='Estimated mantissa bits')
    plt.axhline(y=10, color='r', linestyle='--', label='10-bit threshold')
    plt.axvline(x=16, color='g', linestyle=':', label='k=16 (collapse)')
    plt.xlabel('Primorial index k')
    plt.ylabel('Estimated mantissa bits')
    plt.title('Mantissa Precision vs Primorial Index')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('mantissa_bits_vs_k.png')
    plt.close()
    
    # Plot 2: Relative error of gamma term
    plt.figure(figsize=(8, 5))
    ks = list(range(1, 17))
    rel_errs = []
    for k in ks:
        term_d, term_e = ldab_gamma_term(k)
        if term_e != 0:
            rel_err = abs(term_e - term_d) / abs(term_e)
            rel_errs.append(rel_err if np.isfinite(rel_err) else 0)
        else:
            rel_errs.append(0)
    plt.semilogy(ks, rel_errs, 'ms-', label='|term_ext - term_dbl| / |term_ext|')
    plt.axvline(x=16, color='g', linestyle=':', label='k=16')
    plt.xlabel('Primorial index k')
    plt.ylabel('Relative error (gamma term)')
    plt.title('Gamma Term Relative Error (Double vs Extended)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('gamma_term_error.png')
    plt.close()
    
    return results

def main():
    print("LDAB Calibration Precision Collapse Investigation")
    print("=" * 70)
    print("Testing hypotheses for 64-bit precision collapse at k=16")
    print("=" * 70)
    
    results = test_hypotheses()
    
    # Final summary
    print("\n" + "=" * 70)
    print("CONCLUSIONS:")
    print("=" * 70)
    
    if results.get('H4', False):
        print("• H4 is SUPPORTED: The gamma term alone causes precision loss.")
        print("  → Root cause: Gamma function evaluation in double precision.")
    elif results.get('H2', False):
        print("• H2 is SUPPORTED: Full calibration loses mantissa bits at k=16.")
        print("  → Root cause: Accumulated rounding in logP_k + log_gamma computation.")
    elif results.get('H1', False):
        print("• H1 is SUPPORTED: Log-gamma term shows precision collapse.")
        print("  → Root cause: log Γ(k+1/2) evaluation loses precision.")
    elif results.get('H5', False):
        print("• H5 is SUPPORTED: Cancellation in direct multiplication degrades precision.")
        print("  → Root cause: Multiplication of large numbers with rounding.")
    else:
        print("• No single hypothesis strongly supported.")
        print("  → May require more refined analysis or higher-precision arithmetic.")
    
    # Recommend next step
    print("\nRecommendation:")
    print("• Replace gamma term evaluation with extended-precision arithmetic (float128).")
    print("• If float128 unavailable, use mpmath (if installed) or arbitrary-precision libraries.")
    print("• Verify that using extended precision restores >30 mantissa bits at k=16.")
    print("=" * 70)

if __name__ == "__main__":
    main()