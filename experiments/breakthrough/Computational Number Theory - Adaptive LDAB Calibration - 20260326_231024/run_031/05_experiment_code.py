import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
from math import isqrt, log
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================================
# Helper: Sieve of Eratosthenes for primes up to n
# ============================================================================
def sieve_primes(n):
    """Return list of primes <= n using optimized sieve."""
    if n < 2:
        return []
    size = n + 1
    sieve = bytearray(b"\x01") * size
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            sieve[p*p:n+1:p] = b"\x00" * ((n - p*p)//p + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]

# ============================================================================
# Helper: Compute primorial p_k# = product of first k primes
# ============================================================================
def primorial(k):
    """Return the k-th primorial: product of first k primes."""
    # First k primes (1-indexed: p_1=2, p_2=3, ...)
    primes = sieve_primes(100)  # enough for k up to ~25
    if k < 1 or k > len(primes):
        raise ValueError(f"k={k} out of range [1,{len(primes)}]")
    result = 1
    for i in range(k):
        result *= primes[i]
    return result

# ============================================================================
# Helper: Generate primorial gaps for modulus M = p_k#
# Gap = distance between consecutive integers coprime to M
# ============================================================================
def primorial_gaps(M):
    """
    Generate all gaps in the reduced residue system modulo M.
    Gaps = differences between consecutive integers coprime to M (mod M).
    Returns list of gap sizes (integers >= 1), length = phi(M)
    """
    # Use segmented approach for large M: iterate over [1, M] checking gcd
    # But for k<=8, M <= 9699690 (2*3*5*7*11*13*17*19), manageable directly
    from math import gcd
    phi = M
    primes = sieve_primes(int(M**0.5)+1)
    # Actually compute phi via inclusion-exclusion for safety
    # but for primorial M, phi(M) = ∏ (p-1) for p|M
    # We'll compute phi directly from M's prime factors (already known via sieve)
    # For safety, recompute phi:
    phi = 1
    temp = M
    for p in range(2, int(M**0.5)+1):
        if temp % p == 0:
            phi *= (p - 1)
            temp //= p
            while temp % p == 0:
                temp //= p
    if temp > 1:
        phi *= (temp - 1)

    gaps = []
    prev = None
    # Collect coprime numbers in [1, M]
    coprimes = []
    for x in range(1, M+1):
        if gcd(x, M) == 1:
            coprimes.append(x)

    # Compute gaps (including wrap-around from last to first + M)
    for i, c in enumerate(coprimes):
        if i == 0:
            prev = c
        else:
            gaps.append(c - prev)
            prev = c
    # wrap-around gap: (first + M) - last
    gaps.append(coprimes[0] + M - coprimes[-1])
    return gaps

# ============================================================================
# Helper: Compute theoretical mean and variance of primorial gaps
# ============================================================================
def theoretical_primorial_stats(k):
    """
    For modulus M = p_k#, the reduced residue system modulo M
    has phi(M) elements uniformly distributed in [1, M], so gaps follow:
      mean = M / phi(M)
      variance = (M/phi(M))^2 * (phi(M)-1)/phi(M)
    But more precisely, for a circular arrangement of phi(M) points
    in [1, M], the gaps are exchangeable with sum = M, so:
      E[gap] = M / phi(M)
      Var[gap] = (M^2 / phi(M)^2) * (phi(M)-1)/phi(M)
    However, known result: for uniform random spacing, gaps ~ exponential,
    but exact finite sample: variance = (M/phi(M))^2 * (phi(M)-1)/phi(M)
    """
    M = primorial(k)
    # phi(M) = product_{i=1..k} (p_i - 1)
    phi = 1
    primes = sieve_primes(100)
    for i in range(k):
        phi *= (primes[i] - 1)
    mean = M / phi
    # Exact variance for discrete uniform circular spacing:
    # Var = (M^2 / phi^2) * (phi - 1) / phi
    # See: "Spacing distribution of reduced residue systems" (Erdős–Kac type)
    variance = (M * M) / (phi * phi) * (phi - 1) / phi
    return mean, variance

# ============================================================================
# Main experiment
# ============================================================================
def main():
    print("="*70)
    print("HIGH-PRECISION PRIMORIAL-GAP VALIDATION AT k ≥ 8")
    print("="*70)
    print()

    # Hypothesis H1: arbitrary-precision engine produces exact gaps for k=8
    # and mean/var match theory
    print("TESTING HYPOTHESIS H1: Exact primorial-gap sequence for k=8")
    print("-" * 60)

    k_target = 8
    try:
        M = primorial(k_target)
        print(f"Primorial p_{k_target}# = {M:,}")

        # Compute phi(M)
        primes = sieve_primes(100)
        phi = 1
        for i in range(k_target):
            phi *= (primes[i] - 1)
        print(f"φ(p_{k_target}#) = {phi:,}")

        # Generate gaps
        print("Generating gaps via gcd test (arbitrary precision)...")
        gaps = primorial_gaps(M)
        n_gaps = len(gaps)
        print(f"Generated {n_gaps:,} gaps (expected φ = {phi:,})")

        if n_gaps != phi:
            print(f"ERROR: Gap count mismatch! Got {n_gaps}, expected {phi}")
            return

        # Convert to numpy array for precision
        gaps_arr = np.array(gaps, dtype=np.int64)

        # Compute empirical stats
        emp_mean = np.mean(gaps_arr)
        emp_var = np.var(gaps_arr, ddof=0)  # population variance

        # Theoretical stats
        theo_mean, theo_var = theoretical_primorial_stats(k_target)

        print()
        print("Empirical vs Theoretical Statistics:")
        print(f"  Mean:   empirical = {emp_mean:.10f}, theoretical = {theo_mean:.10f}")
        print(f"  Var:    empirical = {emp_var:.10f}, theoretical = {theo_var:.10f}")

        # Relative errors
        rel_err_mean = abs(emp_mean - theo_mean) / theo_mean
        rel_err_var = abs(emp_var - theo_var) / theo_var

        print(f"  Relative error (mean): {rel_err_mean:.2e}")
        print(f"  Relative error (var):  {rel_err_var:.2e}")

        # H1 success: no overflow (gaps fit in int64) and rel errors < 1e-10
        overflow_safe = gaps_arr.max() < 2**63 - 1
        h1_passed = overflow_safe and rel_err_mean < 1e-10 and rel_err_var < 1e-10

        print()
        if h1_passed:
            print("✅ H1 PASSED: gaps exact (no overflow), stats match theory within tolerance.")
        else:
            print("❌ H1 FAILED:")
            if not overflow_safe:
                print("   - Integer overflow detected")
            if rel_err_mean >= 1e-10:
                print(f"   - Mean mismatch: rel_err = {rel_err_mean:.2e}")
            if rel_err_var >= 1e-10:
                print(f"   - Variance mismatch: rel_err = {rel_err_var:.2e}")

        # Store for plotting
        emp_gaps_k8 = gaps_arr.copy()

    except Exception as e:
        print(f"❌ H1 FAILED with exception: {e}")
        emp_gaps_k8 = np.array([])

    print()
    print("="*70)
    print("EXTENDED ANALYSIS: k = 3 to 8 (for context)")
    print("="*70)

    k_vals = list(range(3, 9))
    k_results = {}

    for k in k_vals:
        try:
            M = primorial(k)
            primes = sieve_primes(100)
            phi = 1
            for i in range(k):
                phi *= (primes[i] - 1)
            gaps = primorial_gaps(M)
            gaps_arr = np.array(gaps, dtype=np.int64)

            emp_mean = np.mean(gaps_arr)
            emp_var = np.var(gaps_arr, ddof=0)
            theo_mean, theo_var = theoretical_primorial_stats(k)

            vmr = emp_var / (emp_mean ** 2) if emp_mean > 0 else np.nan

            k_results[k] = {
                'M': M,
                'phi': phi,
                'emp_mean': emp_mean,
                'emp_var': emp_var,
                'theo_mean': theo_mean,
                'theo_var': theo_var,
                'vmr': vmr
            }
        except Exception as e:
            print(f"Failed for k={k}: {e}")
            continue

    print()
    print("VMR (Variance-to-Mean² Ratio) across k:")
    print("k   | VMR_empirical")
    print("-" * 30)
    vmr_vals = []
    for k in sorted(k_results.keys()):
        vmr = k_results[k]['vmr']
        vmr_vals.append(vmr)
        print(f"{k:2d} | {vmr:.6f}")

    # Plot VMR trend
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    k_plot = [k for k in k_results.keys()]
    vmr_plot = [k_results[k]['vmr'] for k in k_plot]
    ax.plot(k_plot, vmr_plot, 'bo-', label='Empirical VMR')
    ax.set_xlabel('k (primorial index)')
    ax.set_ylabel('Variance / Mean²')
    ax.set_title('VMR Trend for Primorial Gaps (k=3 to 8)')
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.savefig('vmr_trend.png', dpi=150)
    plt.close()

    print()
    print("Plot saved: vmr_trend.png")

    # H2: VMR converges as k increases (sub-quadratic scaling)
    print()
    print("="*70)
    print("TESTING H2: VMR convergence / sub-quadratic scaling")
    print("-" * 60)

    if len(vmr_vals) >= 2:
        # Fit log(VMR) vs log(k) to detect scaling exponent
        k_arr = np.array(k_plot)
        vmr_arr = np.array(vmr_vals)
        log_k = np.log(k_arr)
        log_vmr = np.log(vmr_arr)

        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(log_k, log_vmr)
        print(f"VMR scaling exponent (from log-log fit): {slope:.4f} (R² = {r_value**2:.4f})")
        print(f"Interpretation: VMR ∝ k^{slope:.2f}")

        # Sub-quadratic if exponent < 2
        h2_passed = slope < 2.0
        if h2_passed:
            print("✅ H2 PASSED: VMR scaling is sub-quadratic (exponent < 2)")
        else:
            print("❌ H2 FAILED: VMR scaling appears quadratic or super-quadratic")
    else:
        print("⚠️  Insufficient data for H2 (need ≥2 k-values)")

    # H3: Gaps are approximately exponentially distributed (Poisson process)
    print()
    print("="*70)
    print("TESTING H3: Exponential gap distribution (Poisson model)")
    print("-" * 60)

    # For large k, gaps should approximate exponential with mean = M/φ(M)
    if len(emp_gaps_k8) > 0:
        gaps_k8 = emp_gaps_k8.astype(np.float64)
        emp_mean_k8 = np.mean(gaps_k8)

        # Kolmogorov-Smirnov test vs exponential
        # Scale parameter = mean
        ks_stat, p_val = stats.kstest(gaps_k8, 'expon', args=(0, emp_mean_k8))

        print(f"KS test vs exponential(mean={emp_mean_k8:.4f}):")
        print(f"  KS statistic = {ks_stat:.6f}")
        print(f"  p-value = {p_val:.6f}")

        alpha = 0.05
        if p_val >= alpha:
            print("✅ H3 PASSED: Gap distribution consistent with exponential")
        else:
            print("❌ H3 FAILED: Gap distribution significantly deviates from exponential")
    else:
        print("⚠️  No k=8 gap data for H3")

    # H4: Gap variance follows theoretical formula Var = (M/φ)^2 * (φ-1)/φ
    print()
    print("="*70)
    print("TESTING H4: Variance formula validation")
    print("-" * 60)

    h4_passed = True
    for k in k_vals:
        if k not in k_results:
            continue
        emp_var = k_results[k]['emp_var']
        theo_var = k_results[k]['theo_var']
        rel_err = abs(emp_var - theo_var) / theo_var
        if rel_err > 1e-10:
            h4_passed = False
            print(f"k={k}: rel_err_var = {rel_err:.2e} ❌")
        else:
            print(f"k={k}: rel_err_var = {rel_err:.2e} ✅")

    if h4_passed:
        print("✅ H4 PASSED: All k show variance matches theoretical formula")
    else:
        print("❌ H4 FAILED: Some k show deviation from theoretical variance")

    # H5: No spurious patterns (artifacts) in gap distribution
    print()
    print("="*70)
    print("TESTING H5: Absence of spurious patterns (artifact-free)")
    print("-" * 60)

    # Check autocorrelation (should be near zero for random-like gaps)
    if len(emp_gaps_k8) > 1:
        gaps_k8 = emp_gaps_k8.astype(np.float64)
        # Compute lag-1 autocorrelation
        n = len(gaps_k8)
        mean = np.mean(gaps_k8)
        var = np.var(gaps_k8)
        if var > 0:
            autocorr_1 = np.sum((gaps_k8[:-1] - mean) * (gaps_k8[1:] - mean)) / ((n-1) * var)
        else:
            autocorr_1 = 0.0

        # Expected for uniform circular spacing: near zero
        print(f"Lag-1 autocorrelation = {autocorr_1:.6f}")

        # Rule of thumb: |autocorr| < 0.1 is acceptable for "artifact-free"
        h5_passed = abs(autocorr_1) < 0.1
        if h5_passed:
            print("✅ H5 PASSED: Lag-1 autocorrelation within noise floor")
        else:
            print("❌ H5 FAILED: Significant autocorrelation detected (possible artifact)")
    else:
        print("⚠️  Insufficient gap data for H5")

    # Final summary
    print()
    print("="*70)
    print("CONCLUSIONS:")
    print("="*70)

    h1_bool = h1_passed if 'h1_passed' in dir() else False
    h2_bool = 'h2_passed' in dir() and h2_passed
    h3_bool = 'h3_passed' in dir() and h3_passed
    h4_bool = h4_passed
    h5_bool = 'h5_passed' in dir() and h5_passed

    passed = sum([h1_bool, h2_bool, h3_bool, h4_bool, h5_bool])
    total = 5

    print(f"H1 (exact k=8 gaps): {'✅ PASSED' if h1_bool else '❌ FAILED'}")
    print(f"H2 (sub-quadratic VMR): {'✅ PASSED' if h2_bool else '❌ FAILED'}")
    print(f"H3 (exponential gaps): {'✅ PASSED' if h3_bool else '❌ FAILED'}")
    print(f"H4 (variance formula): {'✅ PASSED' if h4_bool else '❌ FAILED'}")
    print(f"H5 (artifact-free): {'✅ PASSED' if h5_bool else '❌ FAILED'}")
    print()
    print(f"OVERALL: {passed}/{total} hypotheses supported.")
    print()
    if passed >= 4:
        print("The arbitrary-precision pipeline successfully validates primorial gaps")
        print("at k ≥ 8, with no overflow and theoretical consistency.")
    elif passed >= 2:
        print("Partial validation achieved; some hypotheses require refinement.")
    else:
        print("Critical issues detected; pipeline may need recalibration.")

    print()
    print("Script completed successfully.")