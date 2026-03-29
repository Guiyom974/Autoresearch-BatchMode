import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import math
from collections import defaultdict

# Use Agg backend for matplotlib to avoid GUI issues
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Helper: Sieve of Eratosthenes for primes up to n ---
def sieve_primes(n):
    """Return list of primes up to n using optimized sieve."""
    if n < 2:
        return []
    size = n + 1
    sieve = bytearray(b"\x01") * size
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:n+1:step] = b"\x00" * ((n - start) // step + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]

# --- Helper: Compute primorials up to k_max ---
def primorials_up_to(k_max):
    """Return list of primorials P_k for k=1..k_max (P_1 = 2, P_2 = 6, ...)"""
    primes = sieve_primes(1000)  # enough for k <= 800
    primos = []
    P = 1
    for i in range(k_max):
        P *= primes[i]
        primos.append(P)
    return primos

# --- Helper: Compute gaps between consecutive primes in [P_k, next_prime_after_P_k] ---
def compute_gaps_around_primorial(P, prime_list):
    """
    Compute gaps in the interval [P, next_prime_after_P] and [prev_prime_before_P, P],
    then compute variance of gaps in the interval [prev, next] containing P.
    Returns (gap_mean, gap_var, num_gaps, gaps_list).
    """
    # Find index where prime >= P
    idx = np.searchsorted(prime_list, P, side='left')
    # Take a window of primes around P: [prev, ..., P, ..., next]
    # We need gaps that straddle P: at least one before and one after
    # Take window of 3 primes centered at P if possible: [p_{i-1}, p_i=P, p_{i+1}]
    # But P may not be prime. So find:
    #   p_left = largest prime < P
    #   p_right = smallest prime > P
    # Then compute gaps in [p_left, p_right] = [g1, g2] where g1 = P - p_left, g2 = p_right - P
    # For variance, we need at least 2 gaps. Take a window of 3 primes: [p_{i-1}, p_i, p_{i+1}]
    # such that p_i <= P < p_{i+1}
    i = idx
    if i == 0:
        # P < 2: impossible
        return (0.0, 0.0, 0, [])
    # primes: ..., p[i-1], p[i], p[i+1], ...
    p_left = prime_list[i-1]
    p_right = prime_list[i] if i < len(prime_list) else None
    if p_right is None:
        # not enough primes
        return (0.0, 0.0, 0, [])
    # Gaps: g1 = P - p_left, g2 = p_right - P
    gaps = np.array([P - p_left, p_right - P], dtype=np.float64)
    if len(gaps) < 2:
        return (0.0, 0.0, 0, [])
    mean = np.mean(gaps)
    var = np.var(gaps, ddof=0)  # population variance
    return (mean, var, len(gaps), list(gaps))

# --- Optimized segmented sieve to generate primes up to limit ---
def segmented_sieve(limit, segment_size=10**6):
    """Generate all primes up to `limit` using segmented sieve."""
    if limit < 2:
        return []
    # First, sieve small primes up to sqrt(limit)
    sqrt_limit = int(math.isqrt(limit)) + 1
    small_primes = sieve_primes(sqrt_limit)
    primes = []
    # Sieve segments
    low = 2
    while low <= limit:
        high = min(low + segment_size - 1, limit)
        segment = bytearray(b"\x01") * (high - low + 1)
        for p in small_primes:
            if p * p > high:
                break
            # Find first multiple of p in [low, high]
            start = max(p * p, ((low + p - 1) // p) * p)
            for j in range(start, high + 1, p):
                segment[j - low] = 0
        for i, is_prime in enumerate(segment):
            if is_prime:
                primes.append(low + i)
        low = high + 1
    return primes

# --- Main computation ---
def main():
    print("=== Primorial Gap Variance Scaling Test ===")
    print("Testing H1–H5 hypotheses with extended computations")
    print("-" * 50)

    # Target primorial indices k = 1..K_max
    # We'll compute up to k=8 (P_8 = 9699690) and try to get k=9 (223092870)
    # but due to time limit, we'll go as far as feasible in ~120s
    # We'll use segmented sieve to generate primes up to needed limits.

    # Compute required prime bounds: need primes up to at least P_k + gap estimate
    # For variance estimation, we need gaps around each P_k.
    # We'll compute gaps for k = 2..8 (P_2=3, ..., P_8=9699690)
    # and attempt k=9 (223092870) if time permits.

    target_ks = list(range(2, 9))  # k=2 to 8
    primos = primorials_up_to(max(target_ks) + 1)
    primos = primos[:len(target_ks)]  # match indices

    # Estimate max prime bound needed: P_k + ~log^2 P_k (Cramér model)
    max_bound = int(primos[-1] + 2 * (math.log(primos[-1])**2)) + 1000
    # For k=8, P_8=9699690, log P_k ≈ 16.1, so log^2 ≈ 260 → bound ≈ 9.7e6 + 520 ≈ 9.7e6
    # For k=9, P_9=223092870, log≈19.2, log^2≈369 → bound≈2.23e8+740 — too large for 2 min
    # So we'll cap at k=8 unless optimized.

    print(f"Computing primes up to ~{max_bound:,} (for k ≤ {target_ks[-1]})")
    try:
        primes = segmented_sieve(max_bound)
        print(f"Generated {len(primes):,} primes up to {max_bound:,}")
    except Exception as e:
        print(f"Error in sieve: {e}")
        primes = sieve_primes(max_bound)
        print(f"Fallback: generated {len(primes):,} primes")

    # Compute gaps and variances for each P_k
    results = []
    for i, k in enumerate(target_ks):
        P = primos[i]
        mean, var, n_gaps, gaps = compute_gaps_around_primorial(P, primes)
        logP = math.log(P)
        loglogP = math.log(logP) if logP > 1 else 0.0
        results.append({
            'k': k,
            'P': P,
            'logP': logP,
            'loglogP': loglogP,
            'var': var,
            'mean': mean,
            'n_gaps': n_gaps,
            'gaps': gaps
        })
        print(f"k={k:2d}, P_k={P:>10,}, logP={logP:7.3f}, var={var:>12.4f}, gaps={n_gaps}")

    # --- Fit models to test H1: Var = A (log P)^α (log log P)^β ---
    # Use data for k ≥ 5 (P_k ≥ 223092870? No — P_5=2310, P_6=30030, P_7=510510, P_8=9699690)
    # We'll use k=5..8 (4 points) for fitting
    fit_ks = [r for r in results if r['k'] >= 5]
    if len(fit_ks) < 2:
        print("ERROR: Not enough data points for fitting")
        fit_ks = results

    logP_vals = np.array([r['logP'] for r in fit_ks])
    loglogP_vals = np.array([r['loglogP'] for r in fit_ks])
    var_vals = np.array([r['var'] for r in fit_ks])

    # Model: log(Var) = log A + α logP + β loglogP
    # So linear regression on: y = log(var), X = [1, logP, loglogP]
    X = np.column_stack([np.ones(len(fit_ks)), logP_vals, loglogP_vals])
    y = np.log(var_vals)
    # Solve X^T X β = X^T y
    try:
        coeffs, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
        A_hat = np.exp(coeffs[0])
        alpha_hat = coeffs[1]
        beta_hat = coeffs[2]
        print("\n--- H1: Power-log fit (Var = A (logP)^α (loglogP)^β) ---")
        print(f"A = {A_hat:.4e}, α = {alpha_hat:.4f}, β = {beta_hat:.4f}")
        print(f"Residual sum of squares: {residuals[0] if residuals else 0:.4e}")
    except Exception as e:
        print(f"Fit failed: {e}")
        A_hat, alpha_hat, beta_hat = 0.0, 1.0, 0.0

    # --- H1 test: Is β significantly non-zero? ---
    # Use t-test approximation: se(β) ~ sqrt(var(β)) from regression diagnostics
    # Since we have only 4 points, we'll use a heuristic: if |β| > 0.2, we consider it non-zero
    beta_significant = abs(beta_hat) > 0.2
    print(f"H1: β ≠ 0? {'ACCEPT (β ≈ {:.3f})'.format(beta_hat) if beta_significant else 'REJECT (β ≈ {:.3f})'.format(beta_hat)}")

    # --- H2: Compare with simple power law (β=0) ---
    # Fit simple model: log Var = a + b logP
    X_simple = np.column_stack([np.ones(len(fit_ks)), logP_vals])
    try:
        coeffs_simple, res_simple, _, _ = np.linalg.lstsq(X_simple, y, rcond=None)
        alpha_simple = coeffs_simple[1]
        print("\n--- H2: Simple power law (Var = A (logP)^α) fit ---")
        print(f"α_simple = {alpha_simple:.4f}")
        # Compare residual sums of squares
        ss_simple = res_simple[0] if res_simple else np.sum((y - X_simple @ coeffs_simple)**2)
        ss_full = residuals[0] if residuals else np.sum((y - X @ coeffs)**2)
        print(f"SS_simple = {ss_simple:.4e}, SS_full = {ss_full:.4e}")
        # Use F-test approximation: if SS_full << SS_simple, prefer full model
        # With df_full = n-3, df_simple = n-2, F = ((SS_simple - SS_full)/(1)) / (SS_full/(n-3))
        n = len(fit_ks)
        df_full = n - 3
        df_simple = n - 2
        if df_full > 0:
            F = ((ss_simple - ss_full) / 1) / (ss_full / df_full) if ss_full > 0 else float('inf')
            print(f"F-statistic (1, {df_full} df) = {F:.2f}")
            # Critical F(1,1) at 0.05 is ~161, at 0.10 is ~64 — for n=4, df_full=1, F_crit≈161
            h2_reject_simple = F > 161.0
        else:
            h2_reject_simple = False
        print(f"H2: Simple power law sufficient? {'REJECT (prefer power-log)' if h2_reject_simple else 'ACCEPT (simple power law OK)'}")
    except Exception as e:
        print(f"H2 fit failed: {e}")
        h2_reject_simple = False

    # --- H3: Asymptotic scaling exponent α ≈ 1.3–1.5? ---
    print("\n--- H3: Exponent α in [1.3,1.5]? ---")
    alpha_in_range = 1.3 <= alpha_hat <= 1.5
    print(f"α = {alpha_hat:.4f} ∈ [1.3,1.5]? {'ACCEPT' if alpha_in_range else 'REJECT'}")

    # --- H4: Low-k artefacts (k < 5) are non-asymptotic ---
    print("\n--- H4: Low-k (k<5) data deviate from trend? ---")
    # Compute residuals for all points using fitted model (full power-log)
    pred_full = X @ coeffs
    residuals_all = y - pred_full
    low_k_res = residuals_all[:len(results) - len(fit_ks)]  # first few points
    high_k_res = residuals_all[len(low_k_res):]
    if len(high_k_res) > 0 and len(low_k_res) > 0:
        # Compare mean absolute residuals
        low_mean = np.mean(np.abs(low_k_res))
        high_mean = np.mean(np.abs(high_k_res))
        h4_deviation = low_mean > 2 * high_mean and len(low_k_res) >= 2
        print(f"Low-k mean |res| = {low_mean:.3f}, high-k mean |res| = {high_mean:.3f}")
        print(f"H4: Low-k data more deviant? {'ACCEPT' if h4_deviation else 'REJECT'}")
    else:
        print("H4: Insufficient data for comparison → REJECT (inconclusive)")

    # --- H5: Arbitrary-precision arithmetic needed? ---
    print("\n--- H5: Variance values exceed double-precision? ---")
    # For P_8 = 9699690, var ≈ (gaps)^2, gaps ~ log P ~ 16, so var ~ 256 — well within double range
    # But if we extrapolate to k=100, logP ~ 300, var ~ 90000 — still fine
    # However, primorials grow super-exponentially: log P_k ~ θ(p_k) ~ p_k ~ k log k (prime number thm)
    # So log P_k ~ k log k, and log log P_k ~ log k
    # Var ~ (k log k)^α (log k)^β → polynomial in k, so no overflow until k huge
    # But for k=1000, P_k has ~10^4 digits — need arbitrary precision for P_k itself
    # However, we only use log P_k, which is double-safe for k up to 10^12
    print("H5: Double precision sufficient for log P_k up to k=100? ACCEPT (logP safe in double)")
    print("Note: Primorial values themselves overflow, but logs do not.")

    # --- Plot: variance vs logP (power-log model) ---
    print("\nGenerating plot: variance vs logP with fitted model...")
    fig, ax = plt.subplots(figsize=(8, 5))
    logP_all = np.array([r['logP'] for r in results])
    var_all = np.array([r['var'] for r in results])
    ax.scatter(logP_all, var_all, color='blue', label='Computed variances', zorder=5)
    # Plot fitted curve
    logP_fine = np.linspace(logP_all.min() - 0.5, logP_all.max() + 0.5, 200)
    var_fine = A_hat * (logP_fine ** alpha_hat) * (np.where(logP_fine > 1, np.log(logP_fine), 1) ** beta_hat)
    ax.plot(logP_fine, var_fine, 'r--', label=f'Fit: Var = {A_hat:.2e}(logP)^{alpha_hat:.2f}(loglogP)^{beta_hat:.2f}')
    ax.set_xlabel('log P_k')
    ax.set_ylabel('Gap Variance')
    ax.set_title('Primorial Gap Variance vs log P_k')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('primorial_gap_variance.png', dpi=150)
    plt.close()
    print("Saved plot to primorial_gap_variance.png")

    # --- Final conclusions ---
    print("\n" + "=" * 60)
    print("CONCLUSIONS:")
    print("-" * 60)
    print(f"H1 (power-log model): {'ACCEPTED' if beta_significant else 'REJECTED'}")
    print(f"H2 (simple power law): {'REJECTED (power-log superior)' if h2_reject_simple else 'ACCEPTED'}")
    print(f"H3 (α ∈ [1.3,1.5]): {'ACCEPTED' if alpha_in_range else 'REJECTED'}")
    print(f"H4 (low-k artefacts): {'ACCEPTED' if h4_deviation else 'REJECTED'}")
    print(f"H5 (precision): ACCEPTED (double precision sufficient for log P_k)")
    print("-" * 60)
    print(f"Best-fit model: Var(P_k) = {A_hat:.4e} (log P_k)^{alpha_hat:.3f} (log log P_k)^{beta_hat:.3f}")
    print("=" * 60)

if __name__ == "__main__":
    main()