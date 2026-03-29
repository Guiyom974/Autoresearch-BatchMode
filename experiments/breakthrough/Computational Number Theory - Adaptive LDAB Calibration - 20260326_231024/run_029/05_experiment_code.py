import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from math import isqrt, prod
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Helper: Sieve of Eratosthenes for primes up to n ---
def sieve_primes(n):
    """Return list of primes ≤ n using optimized sieve."""
    if n < 2:
        return []
    size = n + 1
    sieve = bytearray(b"\x01") * size
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:n+1:step] = b"\x00" * ((n - start) // step + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]

# --- Helper: Compute primorial p_k#
def primorial(k, primes):
    """Return the k-th primorial: product of first k primes."""
    if k <= 0 or k > len(primes):
        raise ValueError(f"k={k} out of range (primes={len(primes)})")
    return prod(primes[:k])

# --- Helper: Compute gaps modulo primorial using segmented sieve ---
def compute_gaps_mod_primorial(P, window_size=10_000_000):
    """
    Generate all primes in [2, P] using segmented sieve,
    then compute gaps between consecutive primes.
    Returns list of gaps (g_i = p_{i+1} - p_i).
    """
    if P < 2:
        return []
    # First, get base primes up to sqrt(P)
    limit = isqrt(P) + 1
    base_primes = sieve_primes(limit)
    
    gaps = []
    # Handle first segment [2, limit]
    small_primes = sieve_primes(min(P, limit))
    for i in range(len(small_primes) - 1):
        gaps.append(small_primes[i+1] - small_primes[i])
    
    if P <= limit:
        return gaps
    
    # Now segmented sieve for [limit+1, P]
    low = limit + 1
    high = min(low + window_size - 1, P)
    
    while low <= P:
        # Boolean array for segment: True = prime
        segment_size = high - low + 1
        is_prime_seg = bytearray(b"\x01") * segment_size
        
        for p in base_primes:
            # Find first multiple of p in [low, high]
            start = ((low + p - 1) // p) * p
            if start < p * p:
                start = p * p
            if start > high:
                continue
            # Mark multiples
            for m in range(start, high + 1, p):
                is_prime_seg[m - low] = 0
        
        # Extract primes in segment
        for i, is_prime in enumerate(is_prime_seg):
            if is_prime:
                p = low + i
                # Add gap from previous prime (if any)
                if gaps:
                    prev = gaps[-1] + (p - (low + i - 1))  # WRONG: need actual prev prime
                    # Instead, better: track last prime seen
                    pass
        
        # Better: collect primes in segment first, then compute gaps
        seg_primes = []
        for i, is_prime in enumerate(is_prime_seg):
            if is_prime:
                seg_primes.append(low + i)
        
        if seg_primes:
            if gaps:
                # Gap between last prime before segment and first in segment
                # We need to know the last prime before low
                # We'll handle globally by tracking last prime
                pass
        
        low = high + 1
        high = min(low + window_size - 1, P)
    
    # Simpler: use full sieve up to P for correctness (since P is small for k<=8)
    # For k=8, P = primorial(8) = 9699690, which is manageable with standard sieve
    return sieve_primes(P)

# --- Direct primorial prime gap generator (for small k) ---
def primorial_prime_gaps(k):
    """
    Compute all primes p where p mod p_k# ∈ [2, p_k#-1] and p is prime.
    Then compute gaps between consecutive such primes.
    Uses full sieve up to primorial(k) (since primorial(8) ≈ 9.7e6).
    """
    primes_list = sieve_primes(2000)  # enough for k <= 8
    P = primorial(k, primes_list)
    
    # Sieve up to P (inclusive)
    primes_up_to_P = sieve_primes(P)
    
    # Filter primes that are coprime to P (i.e., not dividing P)
    # Since P = product of first k primes, primes dividing P are primes_list[:k]
    excluded = set(primes_list[:k])
    filtered_primes = [p for p in primes_up_to_P if p not in excluded]
    
    # Compute gaps between consecutive filtered primes
    if len(filtered_primes) < 2:
        return []
    gaps = [filtered_primes[i+1] - filtered_primes[i] for i in range(len(filtered_primes)-1)]
    return gaps

# --- Compute VMR (Variance-to-Mean Ratio) ---
def compute_vmr(gaps):
    """Compute variance-to-mean ratio for gaps."""
    if not gaps:
        return 0.0, 0.0, 0.0
    n = len(gaps)
    mean = sum(gaps) / n
    # Use unbiased variance (ddof=1), but VMR typically uses population variance (ddof=0)
    # We'll use population variance (as in research context)
    variance = sum((g - mean)**2 for g in gaps) / n
    vmr = variance / mean if mean != 0 else float('inf')
    return vmr, mean, variance

# --- Test Hypothesis 1: overflow in sum-of-squared-gaps ---
def test_hypothesis_1(k):
    """
    Compute VMR using:
    - 64-bit integer arithmetic (via Python int, but cast to np.int64 where possible)
    - arbitrary-precision (Python int)
    Compare sum_g, sum_g2, mean, variance, vmr.
    """
    gaps = primorial_prime_gaps(k)
    if not gaps:
        return {"error": "No gaps computed"}
    
    n = len(gaps)
    # Arbitrary precision (Python int)
    sum_g_exact = sum(gaps)
    sum_g2_exact = sum(g * g for g in gaps)
    mean_exact = sum_g_exact / n
    var_exact = (sum_g2_exact - n * mean_exact**2) / n  # population variance
    vmr_exact = var_exact / mean_exact if mean_exact != 0 else float('inf')
    
    # Try 64-bit simulation: cast to np.int64, but be careful about overflow
    try:
        # Convert to numpy int64 arrays
        gaps_arr = np.array(gaps, dtype=np.int64)
        sum_g_64 = np.sum(gaps_arr)
        sum_g2_64 = np.sum(gaps_arr * gaps_arr)
        
        # If overflow occurred, values will wrap around (mod 2^64)
        # We detect by comparing to exact values
        overflow_in_sum_g = (sum_g_64 != sum_g_exact)
        overflow_in_sum_g2 = (sum_g2_64 != sum_g2_exact)
        
        # Recompute mean/variance in 64-bit (but use float64 for division)
        mean_64 = float(sum_g_64) / n
        var_64 = (float(sum_g2_64) - n * mean_64**2) / n
        vmr_64 = var_64 / mean_64 if mean_64 != 0 else float('inf')
        
        return {
            "k": k,
            "n_gaps": n,
            "sum_g_exact": sum_g_exact,
            "sum_g_64": sum_g_64,
            "sum_g_overflow": overflow_in_sum_g,
            "sum_g2_exact": sum_g2_exact,
            "sum_g2_64": sum_g2_64,
            "sum_g2_overflow": overflow_in_sum_g2,
            "mean_exact": mean_exact,
            "mean_64": mean_64,
            "var_exact": var_exact,
            "var_64": var_64,
            "vmr_exact": vmr_exact,
            "vmr_64": vmr_64,
            "vmr_ratio": vmr_64 / vmr_exact if vmr_exact != 0 else float('inf')
        }
    except Exception as e:
        return {"error": str(e)}

# --- Main experiment ---
def main():
    print("="*80)
    print("RESEARCH TEST: Resolving Numerical Overflow Artifacts in Primorial Gap VMR")
    print("="*80)
    
    # Precompute primes up to, say, 20 (enough for k=8: primes[:8] = first 8 primes)
    primes = sieve_primes(20)
    print(f"Available primes: {primes} (len={len(primes)})")
    
    # Test k = 1 to 9 (focus on k=7,8,9)
    results = {}
    for k in range(1, 10):
        print(f"\n--- Testing k = {k} ---")
        try:
            res = test_hypothesis_1(k)
            results[k] = res
            if "error" in res:
                print(f"ERROR: {res['error']}")
                continue
            
            print(f"Number of gaps: {res['n_gaps']:,}")
            print(f"Sum of gaps (exact): {res['sum_g_exact']:,}")
            print(f"Sum of gaps (64-bit): {res['sum_g_64']:,}")
            print(f"Sum of gaps overflow? {res['sum_g_overflow']}")
            print(f"Sum of squared gaps (exact): {res['sum_g2_exact']:,}")
            print(f"Sum of squared gaps (64-bit): {res['sum_g2_64']:,}")
            print(f"Sum of squared gaps overflow? {res['sum_g2_overflow']}")
            print(f"Mean (exact): {res['mean_exact']:.6f}")
            print(f"Mean (64-bit): {res['mean_64']:.6f}")
            print(f"Variance (exact): {res['var_exact']:.6e}")
            print(f"Variance (64-bit): {res['var_64']:.6e}")
            print(f"VMR (exact): {res['vmr_exact']:.6e}")
            print(f"VMR (64-bit): {res['vmr_64']:.6e}")
            print(f"VMR ratio (64-bit / exact): {res['vmr_ratio']:.6e}")
            
            # Hypothesis 1: overflow in sum_g2
            if res['sum_g2_overflow']:
                print(">>> CONFIRMED: Overflow in sum of squared gaps")
            elif res['sum_g_overflow']:
                print(">>> Overflow in sum of gaps (less critical for VMR)")
            else:
                print(">>> No overflow detected in intermediates")
                
        except Exception as e:
            print(f"Exception at k={k}: {e}")
            results[k] = {"error": str(e)}
    
    # --- Plot VMR vs k ---
    print("\n--- Generating VMR plot ---")
    ks = []
    vmr_exacts = []
    vmr_64s = []
    for k in sorted(results.keys()):
        r = results[k]
        if "error" not in r and r.get('vmr_exact') is not None and r.get('vmr_64') is not None:
            try:
                if r['vmr_exact'] > 0 and r['vmr_64'] > 0:
                    ks.append(k)
                    vmr_exacts.append(r['vmr_exact'])
                    vmr_64s.append(r['vmr_64'])
            except Exception:
                pass
    
    plt.figure(figsize=(10, 6))
    plt.plot(ks, vmr_exacts, 'o-', label='VMR (arbitrary precision)', color='blue')
    plt.plot(ks, vmr_64s, 's--', label='VMR (64-bit simulation)', color='red')
    plt.axvline(x=8, color='gray', linestyle=':', alpha=0.7, label='k=8')
    plt.yscale('log')
    plt.xlabel('k (primorial index)')
    plt.ylabel('Variance-to-Mean Ratio (VMR)')
    plt.title('Primorial Gap VMR vs k: 64-bit vs Arbitrary Precision')
    plt.legend()
    plt.grid(True, which='both', ls=':', alpha=0.5)
    plt.tight_layout()
    plt.savefig('vmr_vs_k.png', dpi=150)
    plt.close()
    print("Saved plot: vmr_vs_k.png")
    
    # --- Final hypothesis assessment ---
    print("\n" + "="*80)
    print("HYPOTHESIS TESTING SUMMARY")
    print("="*80)
    
    # Hypothesis 1: overflow in sum_g2 at k=8
    k8 = results.get(8, {})
    k7 = results.get(7, {})
    
    print("\nHypothesis 1: VMR collapse at k=8 caused by overflow in sum of squared gaps.")
    print("-" * 70)
    
    if "error" not in k8 and "error" not in k7:
        print(f"k=7: VMR (exact) = {k7.get('vmr_exact', 'N/A'):.3e}")
        print(f"k=8: VMR (exact) = {k8.get('vmr_exact', 'N/A'):.3e}")
        print(f"k=8: VMR (64-bit) = {k8.get('vmr_64', 'N/A'):.3e}")
        
        if k8.get('sum_g2_overflow'):
            print("\n✓ CONFIRMED: Sum of squared gaps overflows in 64-bit at k=8.")
            print("  → This explains the VMR collapse (artifactual drop).")
            print("  → The true VMR at k=8 is likely consistent with trend, not 1.65.")
        else:
            print("\n✗ NOT CONFIRMED: No overflow in sum_g2 detected.")
            print("  → Consider other sources (e.g., mean computation, floating-point rounding)")
            
        # Show ratio of VMRs
        vmr7_exact = k7.get('vmr_exact', 0)
        vmr8_exact = k8.get('vmr_exact', 0)
        vmr8_64 = k8.get('vmr_64', 0)
        
        print(f"\nVMR drop from k=7 to k=8:")
        print(f"  Exact: {vmr7_exact:.3e} → {vmr8_exact:.3e} (ratio = {vmr8_exact/vmr7_exact:.3e})")
        print(f"  64-bit: {vmr7_exact:.3e} → {vmr8_64:.3e} (ratio = {vmr8_64/vmr7_exact:.3e})")
        
        if vmr8_64 < vmr8_exact * 0.999:  # >0.1% discrepancy
            print("\n>>> Strong evidence that 64-bit arithmetic corrupts k=8 VMR.")
    else:
        print("Skipping hypothesis 1 assessment: missing data for k=7 or k=8.")
    
    print("\n" + "="*80)
    print("CONCLUSIONS:")
    print("-" * 70)
    
    # Determine conclusion
    overflow_detected = False
    for k in [7, 8, 9]:
        r = results.get(k, {})
        if "error" not in r and r.get('sum_g2_overflow', False):
            overflow_detected = True
            print(f"1. Overflow in sum_g2 confirmed at k={k}.")
    
    if overflow_detected:
        print("2. The VMR collapse at k=8 is likely caused by integer overflow in")
        print("   sum-of-squared-gaps accumulation (Hypothesis 1 is CONFIRMED).")
        print("3. Use arbitrary-precision arithmetic (Python int) for k ≥ 8 to avoid artifacts.")
    else:
        print("2. No overflow detected in intermediates for k=7,8,9.")
        print("3. Alternative explanations (e.g., floating-point rounding) require further study.")
    
    print("4. Recommended fix: Replace all gap accumulation in numpy with Python int or")
    print("   use numpy.int128 if available (not in standard numpy), or use Decimal.")
    print("="*80)

if __name__ == "__main__":
    main()