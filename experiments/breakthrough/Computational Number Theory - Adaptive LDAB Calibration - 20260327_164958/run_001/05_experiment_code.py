import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import gamma, gammaln
from scipy.integrate import quad
import time
import math

# ============== Efficient Prime Sieve (Segmented) ==============
def segmented_sieve(limit, segment_size=10**6):
    """Generate primes up to `limit` using segmented sieve."""
    if limit < 2:
        return np.array([], dtype=np.int64)
    
    # First sieve up to sqrt(limit)
    sqrt_limit = int(math.isqrt(limit)) + 1
    base_primes = np.ones(sqrt_limit + 1, dtype=bool)
    base_primes[0:2] = False
    for i in range(2, int(math.isqrt(sqrt_limit)) + 1):
        if base_primes[i]:
            base_primes[i*i:sqrt_limit+1:i] = False
    primes = np.where(base_primes)[0].astype(np.int64)
    
    # Segment sieve
    primes_out = []
    low = sqrt_limit + 1
    high = min(low + segment_size, limit + 1)
    while low <= limit:
        segment = np.ones(high - low + 1, dtype=bool)
        for p in primes:
            if p * p > high:
                break
            start = max(p * p, ((low + p - 1) // p) * p)
            segment[start - low:high - low + 1:p] = False
        indices = np.where(segment)[0] + low
        primes_out.extend(indices)
        low = high
        high = min(low + segment_size, limit + 1)
    
    return np.array(primes_out, dtype=np.int64)

def primorial(k):
    """Compute the k-th primorial: product of first k primes."""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
              73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
              179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
              283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
              419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
    if k <= 0:
        return 1
    if k > len(primes):
        raise ValueError(f"Primorial for k={k} > {len(primes)} unsupported (need {k} primes)")
    result = 1
    for i in range(k):
        result *= primes[i]
    return result

def get_leading_digit(n, base):
    """Get leading digit of n in given base (1-indexed, 1..base-1)."""
    if n <= 0:
        return 0
    while n >= base:
        n //= base
    return n

# ============== LDAB Log-Density Function ==============
def ldab_log_density(x, base):
    """
    LDAB log-density for leading digit x in base.
    Based on Benford-like formula: P(x) = log_base(1 + 1/x)
    Returns log(P(x)) for x in 1..base-1.
    """
    if x < 1 or x >= base:
        return -np.inf
    return np.log1p(1.0 / x) / np.log(base)

# ============== Analytic Predictor for c(t) ==============
def analytic_alpha(t):
    """
    Compute α(t) = 1 + (2/π) * ∫₀^{T(t)} (sin u)/u du
    where T(t) ~ log(t)/(2π)
    """
    T = np.log(t) / (2 * np.pi)
    # Sine integral: Si(z) = ∫₀^z (sin u)/u du
    from scipy.special import si
    Si_T = si(T)
    alpha = 1.0 + (2.0 / np.pi) * Si_T
    return alpha

def analytic_c(t):
    """c(t) = 1/α(t)"""
    return 1.0 / analytic_alpha(t)

# ============== Empirical Correction Factor ==============
def empirical_c(primes, base, window_size=None):
    """
    Estimate c empirically by minimizing KL divergence between
    observed leading-digit distribution and LDAB model.
    Returns c such that corrected density = c * LDAB_density
    (normalized to sum to 1).
    """
    if len(primes) == 0:
        return 1.0
    
    # Compute leading digits
    digits = np.array([get_leading_digit(p, base) for p in primes], dtype=np.int64)
    # Count frequencies for digits 1..base-1
    counts = np.bincount(digits, minlength=base)[1:]  # index 0 unused
    total = counts.sum()
    if total == 0:
        return 1.0
    
    observed = counts / total
    
    # LDAB model
    x_vals = np.arange(1, base)
    ldab_probs = np.exp(ldab_log_density(x_vals, base))
    ldab_probs /= ldab_probs.sum()
    
    # Define KL divergence as function of c
    def kl_div(c):
        # Corrected density: c * LDAB, renormalized
        corrected = c * ldab_probs
        corrected /= corrected.sum()
        # Avoid log(0)
        mask = observed > 0
        kl = np.sum(observed[mask] * np.log(observed[mask] / corrected[mask]))
        return kl
    
    # Minimize kl_div over c > 0 using golden-section search
    from scipy.optimize import minimize_scalar
    res = minimize_scalar(kl_div, bounds=(0.1, 10.0), method='bounded')
    c_opt = res.x
    return c_opt

# ============== Sliding-Window Empirical c(t) ==============
def compute_ct_series(primes, base, window_size=10000):
    """
    Compute empirical c(t) for t = primes[i] using sliding window.
    Returns arrays: t_vals, c_vals
    """
    n = len(primes)
    if n == 0:
        return np.array([]), np.array([])
    
    t_vals = []
    c_vals = []
    for i in range(window_size, n):
        window = primes[i - window_size:i]
        c = empirical_c(window, base)
        t_vals.append(primes[i])
        c_vals.append(c)
    return np.array(t_vals), np.array(c_vals)

# ============== KL Divergence Between Empirical and Corrected LDAB ==============
def kl_divergence_empirical_corrected(primes, base, c):
    """
    Compute KL(P_empirical || P_corrected_LDAB)
    where P_corrected = c * P_LDAB, normalized.
    """
    digits = np.array([get_leading_digit(p, base) for p in primes], dtype=np.int64)
    counts = np.bincount(digits, minlength=base)[1:]
    total = counts.sum()
    if total == 0:
        return np.inf
    observed = counts / total
    
    x_vals = np.arange(1, base)
    ldab_probs = np.exp(ldab_log_density(x_vals, base))
    corrected_probs = c * ldab_probs
    corrected_probs /= corrected_probs.sum()
    
    mask = observed > 0
    kl = np.sum(observed[mask] * np.log(observed[mask] / corrected_probs[mask]))
    return kl

# ============== Main Execution ==============
def main():
    print("=" * 70)
    print("Testing Hypothesis 1: Analytic Predictor for Correction Factor")
    print("=" * 70)
    
    # Parameters
    base_list = [210, 2310, 30030]
    max_prime = 2 * 10**6  # Keep within time limit
    window_size = 5000
    
    # Generate primes once (up to max)
    print(f"Generating primes up to {max_prime:,}...")
    primes = segmented_sieve(max_prime)
    print(f"Found {len(primes):,} primes.")
    
    # Prepare plots
    fig, axes = plt.subplots(1, len(base_list), figsize=(5 * len(base_list), 4), squeeze=False)
    fig.suptitle("Empirical c(t) vs Analytic c(t) for LDAB Correction", fontsize=14)
    
    results_summary = {}
    all_mare = []
    
    for idx, base in enumerate(base_list):
        print(f"\n--- Base {base} ---")
        
        # Compute empirical c(t) series
        print(f"Computing empirical c(t) with window size {window_size}...")
        t_vals, c_emp_vals = compute_ct_series(primes, base, window_size)
        
        if len(t_vals) == 0:
            print("No data points for this base.")
            continue
        
        # Compute analytic c(t) at same t_vals
        c_analytic_vals = np.array([analytic_c(t) for t in t_vals])
        
        # Compute MARE
        rel_errors = np.abs((c_emp_vals - c_analytic_vals) / (c_analytic_vals + 1e-12))
        mare = np.mean(rel_errors)
        all_mare.append(mare)
        
        # Print results
        print(f"MARE = {mare:.6f} (target ≤ 0.05)")
        print(f"Mean empirical c(t) = {np.mean(c_emp_vals):.6f}")
        print(f"Mean analytic c(t) = {np.mean(c_analytic_vals):.6f}")
        print(f"Std empirical c(t) = {np.std(c_emp_vals):.6f}")
        print(f"Std analytic c(t) = {np.std(c_analytic_vals):.6f}")
        
        # Hypothesis test: MARE ≤ 5% ?
        passed = mare <= 0.05
        print(f"Hypothesis 1 {'PASSES' if passed else 'FAILS'} (MARE ≤ 0.05)")
        
        # Store for summary
        results_summary[base] = {
            'mare': mare,
            'passed': passed,
            'c_emp_mean': np.mean(c_emp_vals),
            'c_analytic_mean': np.mean(c_analytic_vals)
        }
        
        # Plot
        ax = axes[0, idx]
        ax.plot(t_vals, c_emp_vals, 'b-', label='Empirical c(t)', alpha=0.7)
        ax.plot(t_vals, c_analytic_vals, 'r--', label='Analytic c(t)', alpha=0.7)
        ax.set_xlabel('Prime bound t')
        ax.set_ylabel('Correction factor c(t)')
        ax.set_title(f'Base {base}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axhline(y=1.0, color='k', linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('hypothesis1_ct_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # ============== Additional: KL Divergence Verification ==============
    print("\n" + "=" * 70)
    print("Verifying KL Divergence < 1e-4 with Adaptive Correction")
    print("=" * 70)
    
    kl_results = {}
    for base in base_list:
        print(f"\nBase {base}:")
        # Use full prime list (not sliding window) for final KL
        c_opt = empirical_c(primes, base)
        kl = kl_divergence_empirical_corrected(primes, base, c_opt)
        print(f"Optimal c = {c_opt:.6f}")
        print(f"KL(P_emp || P_corrected) = {kl:.2e}")
        passed_kl = kl < 1e-4
        print(f"KL < 1e-4: {'YES' if passed_kl else 'NO'}")
        kl_results[base] = {'c_opt': c_opt, 'kl': kl, 'passed_kl': passed_kl}
    
    # ============== Output Summary ==============
    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    
    print("\nHypothesis 1: Analytic Predictor for Correction Factor")
    print("-" * 50)
    for base in base_list:
        res = results_summary.get(base, {})
        mare = res.get('mare', np.nan)
        passed = res.get('passed', False)
        print(f"Base {base}: MARE = {mare:.6f} → {'PASS' if passed else 'FAIL'}")
    
    overall_h1_passed = all(results_summary.get(b, {}).get('passed', False) for b in base_list)
    print(f"\nOverall Hypothesis 1: {'ACCEPTED' if overall_h1_passed else 'REJECTED'}")
    
    print("\nKL Divergence Verification:")
    print("-" * 50)
    for base in base_list:
        res = kl_results.get(base, {})
        kl = res.get('kl', np.nan)
        passed = res.get('passed_kl', False)
        c_opt = res.get('c_opt', np.nan)
        print(f"Base {base}: KL = {kl:.2e}, c_opt = {c_opt:.6f} → {'PASS' if passed else 'FAIL'}")
    
    overall_kl_passed = all(kl_results.get(b, {}).get('passed_kl', False) for b in base_list)
    print(f"\nOverall KL < 1e-4: {'ACHIEVED' if overall_kl_passed else 'NOT ACHIEVED'}")
    
    print("\n" + "=" * 70)
    print("Final Assessment:")
    print("=" * 70)
    if overall_h1_passed and overall_kl_passed:
        print("✅ Both Hypothesis 1 and KL < 1e-4 requirements are met.")
        print("   Adaptive LDAB calibration is analytically predictable and effective.")
    elif overall_h1_passed:
        print("⚠️  Hypothesis 1 is accepted, but KL < 1e-4 not achieved for all bases.")
    elif overall_kl_passed:
        print("⚠️  KL < 1e-4 achieved, but analytic predictor deviates >5%.")
    else:
        print("❌ Neither Hypothesis 1 nor KL < 1e-4 fully satisfied.")
        print("   Further refinement of α(t) or c(t) model needed.")
    
    print("\nPlot saved: hypothesis1_ct_comparison.png")
    print("=" * 70)

if __name__ == "__main__":
    start_time = time.time()
    try:
        main()
    except Exception as e:
        print(f"\n⚠️  ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    finally:
        elapsed = time.time() - start_time
        print(f"\nRuntime: {elapsed:.1f} seconds")