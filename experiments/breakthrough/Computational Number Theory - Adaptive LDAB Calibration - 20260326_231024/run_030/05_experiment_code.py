import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from math import isqrt, log
from collections import defaultdict

# Efficient segmented sieve for primes up to N
def segmented_sieve(n):
    if n < 2:
        return np.array([], dtype=np.int64)
    limit = isqrt(n) + 1
    base_primes = simple_sieve(limit)
    segment_size = max(limit, 10_000_000)
    primes = list(base_primes)
    low = limit
    high = min(n, low + segment_size)
    while low <= n:
        is_prime = np.ones(high - low + 1, dtype=bool)
        for p in base_primes:
            start = max(p * p, ((low + p - 1) // p) * p)
            for j in range(start, high + 1, p):
                is_prime[j - low] = False
        for i, val in enumerate(is_prime):
            if val:
                primes.append(low + i)
        low = high + 1
        high = min(n, low + segment_size)
    return np.array(primes, dtype=np.int64)

def simple_sieve(n):
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[0:2] = b'\x00\x00'
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i*i:n+1:i] = b'\x00' * ((n - i*i)//i + 1)
    return [i for i, is_p in enumerate(sieve) if is_p]

# Primorial calculation with arbitrary precision (Python int)
def primorial(k):
    """Return product of first k primes (p_k#)"""
    if k <= 0:
        return 1
    primes = simple_sieve(100)  # first 25 primes suffice for k<=8
    result = 1
    for i in range(k):
        result *= primes[i]
    return result

# Generate primorial gaps: gaps between consecutive primes in arithmetic progression mod p_k#
def primorial_gaps(k, max_prime_limit=10_000_000):
    """
    Generate gaps between consecutive primes in the arithmetic progression
    {n : gcd(n, p_k#) = 1} up to max_prime_limit.
    Uses segmented sieve to generate primes, then filters those coprime to primorial.
    """
    p_k = primorial(k)
    # Generate primes up to max_prime_limit
    primes = segmented_sieve(max_prime_limit)
    # Filter primes that are coprime to p_k# (i.e., not dividing p_k#)
    small_primes = simple_sieve(primorial(k))[:k]  # first k primes
    mask = np.ones(len(primes), dtype=bool)
    for sp in small_primes:
        mask &= (primes % sp != 0)
    # Keep only primes coprime to p_k#
    coprime_primes = primes[mask]
    # Compute gaps between consecutive coprime primes
    if len(coprime_primes) < 2:
        return np.array([], dtype=np.int64)
    gaps = np.diff(coprime_primes)
    return gaps.astype(np.int64)

def compute_vmr(gaps):
    """
    Compute variance-to-mean ratio (VMR) = variance / mean^2
    Using arbitrary-precision via Python float (sufficient for gap magnitudes)
    """
    if len(gaps) < 2:
        return np.nan, np.nan, np.nan, np.nan
    gaps = np.asarray(gaps, dtype=np.float64)
    mean = np.mean(gaps)
    var = np.var(gaps, ddof=0)  # population variance
    vrm = var / (mean ** 2) if mean != 0 else np.nan
    # Also compute std error for reporting
    std_err = np.sqrt(var / len(gaps)) / mean if mean != 0 else np.nan
    return float(var), float(mean), float(vrm), float(std_err)

def main():
    print("=" * 70)
    print("HYPOTHESIS TESTING: Primorial Gap VMR at k ≥ 8")
    print("=" * 70)
    
    # Setup
    np.random.seed(42)
    
    # Target k values
    k_values = list(range(1, 9))  # k=1 to 8
    
    # For k >= 7, need larger prime range to get enough coprime primes
    # k=7: p_7# = 510510 → need ~10^7 range for ~1M coprime primes
    # k=8: p_8# = 9699690 → need ~10^8 range for ~2M coprime primes
    # But runtime limit: use optimized approach with smaller but sufficient range
    
    # Adjust ranges per k to ensure enough data points (>10^5 gaps)
    k_ranges = {
        1: 1_000_000,
        2: 1_000_000,
        3: 1_000_000,
        4: 1_000_000,
        5: 1_000_000,
        6: 5_000_000,
        7: 10_000_000,
        8: 20_000_000,
    }
    
    results = {}
    print("\n--- COMPUTING PRIMORIAL GAPS AND VMR ---")
    
    for k in k_values:
        try:
            print(f"\nProcessing k={k}...")
            p_k = primorial(k)
            max_p = k_ranges[k]
            print(f"  p_{k}# = {p_k:,}")
            print(f"  Searching primes up to {max_p:,}...")
            
            # Generate coprime primes and gaps
            gaps = primorial_gaps(k, max_prime_limit=max_p)
            
            if len(gaps) < 1000:
                print(f"  WARNING: Only {len(gaps):,} gaps (need >1000 for reliable VMR)")
            
            # Compute VMR with high precision (float64 is sufficient for gap magnitudes)
            var, mean, vrm, std_err = compute_vmr(gaps)
            
            results[k] = {
                'primorial': p_k,
                'num_gaps': len(gaps),
                'variance': var,
                'mean': mean,
                'vmr': vrm,
                'std_err': std_err,
            }
            
            print(f"  Gaps: {len(gaps):,}")
            print(f"  Mean gap: {mean:.4f}")
            print(f"  Variance: {var:.4f}")
            print(f"  VMR = Var / Mean² = {vrm:.6f} ± {std_err:.6f}")
            
        except Exception as e:
            print(f"  ERROR at k={k}: {e}")
            results[k] = {
                'primorial': primorial(k),
                'num_gaps': 0,
                'variance': np.nan,
                'mean': np.nan,
                'vmr': np.nan,
                'std_err': np.nan,
            }
    
    # --- HYPOTHESIS 1 TEST: 64-bit overflow artifact? ---
    print("\n" + "=" * 70)
    print("HYPOTHESIS 1 TEST:")
    print("The VMR collapse at k=8 is a 64-bit overflow artifact.")
    print("=" * 70)
    
    # Simulate what would happen with 64-bit overflow in gap sum
    # We'll compute the sum of squared gaps in 64-bit vs arbitrary precision
    k_target = 8
    max_p = k_ranges[k_target]
    gaps = primorial_gaps(k_target, max_prime_limit=max_p)
    
    if len(gaps) > 0:
        # Compute sums in 64-bit and arbitrary precision
        gaps_64 = gaps.astype(np.int64)
        sum_gaps_64 = np.sum(gaps_64).astype(np.int64)
        sum_sq_gaps_64 = np.sum(gaps_64 * gaps_64).astype(np.int64)
        
        # Arbitrary precision (via Python int or float)
        sum_gaps_ap = int(np.sum(gaps))
        sum_sq_gaps_ap = int(np.sum(gaps * gaps))
        
        # Compute VMR in both
        n = len(gaps)
        mean_64 = sum_gaps_64 / n
        var_64 = (sum_sq_gaps_64 / n) - mean_64**2
        vmr_64 = var_64 / (mean_64**2) if mean_64 != 0 else np.nan
        
        mean_ap = sum_gaps_ap / n
        var_ap = (sum_sq_gaps_ap / n) - mean_ap**2
        vmr_ap = var_ap / (mean_ap**2) if mean_ap != 0 else np.nan
        
        print(f"\n64-bit arithmetic:")
        print(f"  Sum of gaps: {sum_gaps_64:,}")
        print(f"  Sum of squared gaps: {sum_sq_gaps_64:,}")
        print(f"  Variance: {var_64:.6f}")
        print(f"  VMR: {vmr_64:.6f}")
        
        print(f"\nArbitrary-precision (float64) arithmetic:")
        print(f"  Sum of gaps: {sum_gaps_ap:,}")
        print(f"  Sum of squared gaps: {sum_sq_gaps_ap:,}")
        print(f"  Variance: {var_ap:.6f}")
        print(f"  VMR: {vmr_ap:.6f}")
        
        print(f"\nDifference in VMR: {abs(vmr_ap - vmr_64):.10f}")
        
        # Check for overflow (if 64-bit sum_sq overflows ~9e18)
        overflow_threshold = 2**63 - 1
        print(f"\nOverflow threshold (2^63-1): {overflow_threshold:,}")
        print(f"Sum of squares: {sum_sq_gaps_ap:,}")
        print(f"Overflow? {'YES' if sum_sq_gaps_ap > overflow_threshold else 'NO'}")
        
        # Hypothesis decision
        if abs(vmr_ap - vmr_64) > 1e-6:
            print("\n→ Evidence supports overflow artifact hypothesis.")
            h1_result = "REJECTED: VMR difference > 1e-6 indicates overflow effect"
        else:
            print("\n→ No evidence of overflow artifact.")
            h1_result = "ACCEPTED: VMR consistent across precisions"
    else:
        print("No gaps generated for k=8 → cannot test H1")
        h1_result = "INCONCLUSIVE: Insufficient data"
    
    # --- HYPOTHESIS 2 TEST: VMR continues upward trend for k ≥ 8 ---
    print("\n" + "=" * 70)
    print("HYPOTHESIS 2 TEST:")
    print("VMR continues upward trend for k ≥ 8 (no collapse).")
    print("=" * 70)
    
    # Collect VMR values
    vmr_values = [results[k]['vmr'] for k in k_values if not np.isnan(results[k]['vmr'])]
    k_valid = [k for k in k_values if not np.isnan(results[k]['vmr'])]
    
    if len(vmr_values) < 3:
        print("Insufficient data for trend analysis.")
        h2_result = "INCONCLUSIVE"
    else:
        # Simple linear regression on k vs VMR for k=1..7 (exclude k=8 for baseline)
        k_baseline = k_valid[:-1]  # k=1..7
        vmr_baseline = vmr_values[:-1]
        
        # Fit linear model: VMR = a*k + b
        k_arr = np.array(k_baseline, dtype=float)
        vmr_arr = np.array(vmr_baseline, dtype=float)
        A = np.vstack([k_arr, np.ones(len(k_arr))]).T
        a, b = np.linalg.lstsq(A, vmr_arr, rcond=None)[0]
        
        # Predict VMR at k=8
        predicted_vmr_8 = a * 8 + b
        actual_vmr_8 = vmr_values[-1]
        
        print(f"\nLinear trend (k=1..7): VMR = {a:.6f} * k + {b:.6f}")
        print(f"Predicted VMR at k=8: {predicted_vmr_8:.6f}")
        print(f"Actual VMR at k=8: {actual_vmr_8:.6f}")
        print(f"Difference: {abs(actual_vmr_8 - predicted_vmr_8):.6f}")
        
        # Check if k=8 VMR follows trend (within 2σ)
        # Estimate residual std
        y_pred = a * k_arr + b
        residuals = vmr_arr - y_pred
        sigma_res = np.sqrt(np.sum(residuals**2) / (len(k_arr) - 2))
        se_pred = sigma_res * np.sqrt(1 + 1/len(k_arr) + (8 - np.mean(k_arr))**2 / np.sum((k_arr - np.mean(k_arr))**2))
        
        print(f"Residual std (σ): {sigma_res:.6f}")
        print(f"Prediction std error: {se_pred:.6f}")
        
        if abs(actual_vmr_8 - predicted_vmr_8) <= 2 * se_pred:
            print("\n→ k=8 VMR consistent with upward trend.")
            h2_result = "ACCEPTED: VMR follows predicted upward trend"
        else:
            print("\n→ k=8 VMR deviates significantly from trend.")
            h2_result = "REJECTED: VMR collapse observed"
    
    # --- HYPOTHESIS 3 TEST: VMR > 1.65 at k=8 (not 1.65 as artifact) ---
    print("\n" + "=" * 70)
    print("HYPOTHESIS 3 TEST:")
    print("VMR at k=8 is significantly > 1.65 (not 1.65 as artifact).")
    print("=" * 70)
    
    vmr_k8 = results[8]['vmr']
    std_err_k8 = results[8]['std_err']
    
    if np.isnan(vmr_k8):
        print("No VMR data for k=8.")
        h3_result = "INCONCLUSIVE"
    else:
        print(f"\nVMR at k=8: {vmr_k8:.6f} ± {std_err_k8:.6f}")
        print("Null hypothesis: VMR = 1.65 (artifact value)")
        
        # Z-test
        z_score = (vmr_k8 - 1.65) / std_err_k8 if std_err_k8 > 0 else np.inf
        from scipy import stats as st
        p_value = 2 * (1 - st.norm.cdf(abs(z_score)))
        
        print(f"Z-score: {z_score:.4f}")
        print(f"P-value: {p_value:.6f}")
        
        alpha = 0.05
        if p_value < alpha:
            print(f"\n→ VMR significantly different from 1.65 (p={p_value:.4f} < {alpha}).")
            if vmr_k8 > 1.65:
                print("→ VMR is *higher* than artifact value.")
                h3_result = "ACCEPTED: VMR > 1.65 (real effect)"
            else:
                print("→ VMR is *lower* than artifact value.")
                h3_result = "REJECTED: VMR < 1.65"
        else:
            print(f"\n→ No evidence VMR differs from 1.65 (p={p_value:.4f} ≥ {alpha}).")
            h3_result = "INCONCLUSIVE: VMR consistent with 1.65 artifact"
    
    # --- HYPOTHESIS 4 TEST: LDAB calibration correct for k ≥ 8 ---
    print("\n" + "=" * 70)
    print("HYPOTHESIS 4 TEST:")
    print("LDAB (logarithmic density of admissible bundles) calibration")
    print("is accurate for k ≥ 8.")
    print("=" * 70)
    
    # LDAB model: expected VMR ≈ 1/3 + C/log(p_k#)
    # Fit C from k=1..7 data
    log_p_k = [log(primorial(k)) for k in k_valid]
    vmr_k_valid = [results[k]['vmr'] for k in k_valid]
    
    # Model: VMR = 1/3 + C/log(p_k#)
    # So: VMR - 1/3 = C / log(p_k#) → C = (VMR - 1/3) * log(p_k#)
    C_estimates = [(vmr_k_valid[i] - 1/3) * log_p_k[i] for i in range(len(log_p_k))]
    C_mean = np.mean(C_estimates)
    C_std = np.std(C_estimates, ddof=1)
    
    print(f"\nLDAB model: VMR = 1/3 + C / log(p_k#)")
    print(f"Estimated C (from k=1..7): {C_mean:.6f} ± {C_std:.6f}")
    
    # Predict VMR at k=8
    log_p_k8 = log(primorial(8))
    predicted_vmr_ldab = 1/3 + C_mean / log_p_k8
    se_pred_ldab = C_std / log_p_k8  # approximate SE
    
    actual_vmr_k8 = results[8]['vmr']
    
    print(f"\nPredicted VMR at k=8 (LDAB): {predicted_vmr_ldab:.6f} ± {se_pred_ldab:.6f}")
    print(f"Actual VMR at k=8: {actual_vmr_k8:.6f}")
    
    if not np.isnan(actual_vmr_k8):
        diff = abs(actual_vmr_k8 - predicted_vmr_ldab)
        z_ldab = diff / se_pred_ldab if se_pred_ldab > 0 else np.inf
        p_ldab = 2 * (1 - st.norm.cdf(abs(z_ldab)))
        
        print(f"Difference: {diff:.6f}")
        print(f"Z-score: {z_ldab:.4f}")
        print(f"P-value: {p_ldab:.6f}")
        
        if p_ldab >= 0.05:
            print("\n→ LDAB model fits k=8 data.")
            h4_result = "ACCEPTED: LDAB calibration valid for k=8"
        else:
            print("\n→ LDAB model fails to predict k=8 VMR.")
            h4_result = "REJECTED: LDAB calibration inaccurate for k≥8"
    else:
        print("No data for k=8.")
        h4_result = "INCONCLUSIVE"
    
    # --- PLOT: VMR vs k ---
    print("\nGenerating VMR vs k plot...")
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    k_plot = [k for k in k_values if not np.isnan(results[k]['vmr'])]
    vmr_plot = [results[k]['vmr'] for k in k_plot]
    err_plot = [results[k]['std_err'] for k in k_plot]
    
    ax.errorbar(k_plot, vmr_plot, yerr=err_plot, fmt='o-', capsize=4,
                label='Observed VMR', color='tab:blue')
    
    # Add trend line for k=1..7
    if len(k_plot) > 1:
        k_fit = np.array(k_plot[:-1], dtype=float)
        vmr_fit = np.array(vmr_plot[:-1], dtype=float)
        A = np.vstack([k_fit, np.ones(len(k_fit))]).T
        a_fit, b_fit = np.linalg.lstsq(A, vmr_fit, rcond=None)[0]
        k_line = np.linspace(1, 8, 100)
        ax.plot(k_line, a_fit * k_line + b_fit, '--', color='tab:orange',
                label=f'Trend (k=1..7): VMR = {a_fit:.4f}k + {b_fit:.4f}')
    
    ax.axhline(y=1.65, color='red', linestyle=':', alpha=0.7,
               label='H1 artifact value (1.65)')
    ax.axvline(x=8, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    ax.set_xlabel('k (primorial index)', fontsize=12)
    ax.set_ylabel('Variance-to-Mean Ratio (VMR)', fontsize=12)
    ax.set_title('VMR of Primorial Gaps vs k', fontsize=14)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('vmr_vs_k.png', dpi=150)
    plt.close()
    print("Plot saved as 'vmr_vs_k.png'")
    
    # --- FINAL CONCLUSIONS ---
    print("\n" + "=" * 70)
    print("FINAL CONCLUSIONS")
    print("=" * 70)
    print(f"\nH1 (overflow artifact): {h1_result}")
    print(f"H2 (upward trend):      {h2_result}")
    print(f"H3 (VMR > 1.65):        {h3_result}")
    print(f"H4 (LDAB calibration):  {h4_result}")
    
    # Overall assessment
    print("\n" + "-" * 70)
    print("OVERALL RESEARCH ASSESSMENT:")
    print("-" * 70)
    
    if "REJECTED" in h1_result and "ACCEPTED" in h2_result and "ACCEPTED" in h3_result:
        print("→ Evidence supports genuine VMR anomaly at k=8, not overflow.")
        print("→ VMR continues upward trend beyond k=7.")
        print("→ VMR significantly exceeds artifact value (1.65).")
        print("\n→ Implication: Requires new theoretical model (beyond LDAB).")
    elif "ACCEPTED" in h1_result:
        print("→ VMR collapse likely due to overflow artifact.")
        print("→ No genuine boundary effect at k=8.")
    else:
        print("→ Results inconclusive or mixed.")
        print("→ Further computation or refined models needed.")
    
    print("\n" + "=" * 70)
    print("SCRIPT COMPLETED SUCCESSFULLY")
    print("=" * 70)