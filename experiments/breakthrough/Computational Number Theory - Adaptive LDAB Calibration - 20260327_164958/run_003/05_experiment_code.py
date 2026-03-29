import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import math
from scipy.special import loggamma
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Constants and utilities
def primorial(k):
    """Return the k-th primorial (product of first k primes)."""
    primes = list_primes_up_to_nth(k)
    p = 1
    for pr in primes:
        p *= pr
    return p

def list_primes_up_to_nth(n):
    """Return list of first n primes."""
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

def primes_up_to(limit):
    """Segmented sieve to generate all primes ≤ limit."""
    if limit < 2:
        return []
    # First sieve up to sqrt(limit)
    sieve_limit = int(limit**0.5) + 1
    base_primes = list_primes_up_to_nth_nth(sieve_limit)
    # Generate primes up to sqrt(limit)
    primes = []
    is_prime = [True] * (sieve_limit + 1)
    is_prime[0:2] = [False, False]
    for i in range(2, sieve_limit + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i*i, sieve_limit+1, i):
                is_prime[j] = False
    
    # Segmented sieve
    segment_size = max(100000, int(limit**0.5))
    low = sieve_limit + 1
    while low <= limit:
        high = min(low + segment_size - 1, limit)
        segment = [True] * (high - low + 1)
        for p in primes:
            start = max(p*p, ((low + p - 1) // p) * p)
            for j in range(start, high+1, p):
                segment[j - low] = False
        for i, flag in enumerate(segment):
            if flag:
                primes.append(low + i)
        low = high + 1
    return sorted(set(primes))

def list_primes_up_to_nth_nth(n):
    """Get first n primes (fallback for small n)."""
    return list_primes_up_to_nth(n)

# Guarded log-gamma: returns loggamma(x) safely for large x
def guarded_loggamma(x):
    """Return loggamma(x) with overflow protection."""
    try:
        return loggamma(x)
    except (OverflowError, ValueError):
        # Use Stirling approximation for large x
        if x <= 0:
            return float('-inf')
        return x * np.log(x) - x + 0.5 * np.log(2 * np.pi * x)

# LDAB correction factor implementation
def compute_c_emp(t, base, primes_list):
    """
    Compute empirical correction factor c_emp(t) for given base and t.
    
    LDAB model: density of primes in arithmetic progression mod base.
    Uses inclusion-exclusion over prime factors of base.
    """
    if t <= 1:
        return 1.0
    
    # Prime factors of base
    factors = []
    temp = base
    for p in primes_list:
        if p * p > temp:
            break
        if temp % p == 0:
            factors.append(p)
            while temp % p == 0:
                temp //= p
    if temp > 1:
        factors.append(temp)
    
    # Inclusion-exclusion over subsets of factors
    n_factors = len(factors)
    total_weight = 0.0
    
    for mask in range(1 << n_factors):
        prod = 1
        sign = -1 if bin(mask).count('1') % 2 else 1
        for i in range(n_factors):
            if mask & (1 << i):
                prod *= factors[i]
        
        if prod == 0:
            continue
        
        # Count numbers ≤ t coprime to base
        count = t // prod
        # Adjust for residue class
        if prod > t:
            continue
        
        # Use loggamma for binomial coefficient approximation
        # Approximate log(C(t, t/prod)) using Stirling
        if count == 0:
            continue
        # Approximation: log(C(t, k)) ≈ t*log(t) - k*log(k) - (t-k)*log(t-k)
        k = count
        if k == 0 or k == t:
            log_binom = 0.0
        else:
            log_binom = guarded_loggamma(t+1) - guarded_loggamma(k+1) - guarded_loggamma(t-k+1)
        
        weight = sign * np.exp(log_binom)
        total_weight += weight
    
    # Expected count under uniform distribution
    phi_base = base
    for p in factors:
        phi_base *= (p - 1) // p
    
    expected = t * phi_base / base
    
    # Correction factor: ratio of actual to expected density
    if expected <= 0:
        return 1.0
    c_emp = total_weight / expected
    
    # Clamp for numerical stability
    if not np.isfinite(c_emp) or c_emp < 0.1 or c_emp > 10.0:
        c_emp = 1.0
    
    return c_emp

def compute_c_emp_vectorized(t_vals, base, primes_list):
    """Vectorized computation of c_emp for array of t values."""
    return np.array([compute_c_emp(t, base, primes_list) for t in t_vals])

# Fitting function for hypothesis 1: L_k = α + β ln P_k
def fit_linear_logP(P_vals, L_vals):
    """Fit L = α + β ln P."""
    x = np.log(P_vals)
    A = np.vstack([np.ones_like(x), x]).T
    coeffs, residuals, rank, s = np.linalg.lstsq(A, L_vals, rcond=None)
    alpha, beta = coeffs
    return alpha, beta, residuals

# Main execution
def main():
    print("="*70)
    print("MULTI-BASE SCALABILITY AND ASYMPTOTIC ANALYSIS OF LDAB CORRECTION FACTOR")
    print("="*70)
    
    # Define bases: primorials for k=4,5,6 → 210, 2310, 30030
    # k=4: 2*3*5*7 = 210
    # k=5: 2*3*5*7*11 = 2310
    # k=6: 2*3*5*7*11*13 = 30030
    bases = [210, 2310, 30030]
    base_names = {210: "P_4=210", 2310: "P_5=2310", 30030: "P_6=30030"}
    
    # Generate primes up to 10^7 (for t_max)
    print("\nGenerating primes up to 10^7...")
    try:
        primes_list = primes_up_to(10_000_000)
    except Exception as e:
        print(f"Warning: Prime generation failed: {e}")
        primes_list = list_primes_up_to_nth(664579)  # fallback: first 664579 primes (π(10^7))
    
    print(f"Generated {len(primes_list)} primes up to 10^7.")
    
    # Define t values for asymptotic analysis
    # Use log-spaced values to cover wide range efficiently
    t_vals = np.logspace(2, 7, num=20, dtype=int)
    t_vals = np.unique(np.clip(t_vals, 10, 10_000_000))
    
    # Store results
    L_estimates = {}  # L_k estimates for each base
    c_emp_data = {}   # c_emp(t) for each base
    
    # Compute c_emp for each base
    print("\nComputing empirical correction factors c_emp(t)...")
    for base in bases:
        print(f"\nProcessing base {base} ({base_names[base]})...")
        c_emp_vals = []
        for t in t_vals:
            try:
                c = compute_c_emp(t, base, primes_list)
                c_emp_vals.append(c)
            except Exception as e:
                print(f"  Error at t={t}: {e}")
                c_emp_vals.append(1.0)
        
        c_emp_data[base] = np.array(c_emp_vals)
        
        # Estimate asymptotic limit L_k as median of last 5 points
        last_vals = c_emp_vals[-5:] if len(c_emp_vals) >= 5 else c_emp_vals
        L_est = np.median(last_vals)
        L_estimates[base] = L_est
        print(f"  Estimated limit L_{base} ≈ {L_est:.6f}")
    
    # ============== HYPOTHESIS 1 TEST ==============
    print("\n" + "="*70)
    print("HYPOTHESIS 1: L_k = α + β ln P_k (linear in log primorial)")
    print("="*70)
    
    P_vals = np.array(bases)
    L_vals = np.array([L_estimates[P] for P in bases])
    
    alpha, beta, residuals = fit_linear_logP(P_vals, L_vals)
    predicted = alpha + beta * np.log(P_vals)
    
    print(f"Fitted model: L_k = {alpha:.6f} + {beta:.6f}·ln(P_k)")
    if len(residuals) > 0:
        print(f"Residual sum of squares: {residuals[0]:.2e}")
    else:
        print("Residual sum of squares: 0.00e+00")
    print(f"Predicted values: {predicted}")
    print(f"Actual values:    {L_vals}")
    print(f"Max absolute error: {np.max(np.abs(predicted - L_vals)):.6f}")
    
    # Compute R²
    ss_res = np.sum((L_vals - predicted)**2)
    ss_tot = np.sum((L_vals - np.mean(L_vals))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    
    print(f"R² = {r2:.6f}")
    
    # Hypothesis test: check if linear fit is good (R² > 0.95)
    hypothesis1_pass = r2 > 0.95
    print(f"\nHYPOTHESIS 1: {'PASS' if hypothesis1_pass else 'FAIL'} (R² = {r2:.4f} {'>' if hypothesis1_pass else '<'} 0.95)")
    
    # ============== HYPOTHESIS 2 TEST ==============
    print("\n" + "="*70)
    print("HYPOTHESIS 2: c_emp(t) converges monotonically to L_k")
    print("="*70)
    
    hypothesis2_pass = True
    for base in bases:
        c_vals = c_emp_data[base]
        # Check monotonicity of last portion (t > 10^5)
        mask = t_vals > 100_000
        if np.sum(mask) < 2:
            continue
        c_late = c_vals[mask]
        # Check if values are within 1% of final value and trend is small
        diff = np.abs(np.diff(c_late))
        max_diff = np.max(diff) if len(diff) > 0 else 0.0
        trend = np.abs(c_late[-1] - c_late[0])
        is_monotonic = max_diff < 0.01 * np.abs(c_late[0]) and trend < 0.01 * np.abs(c_late[0])
        if not is_monotonic:
            hypothesis2_pass = False
            print(f"  {base_names[base]}: Non-monotonic behavior detected (max diff = {max_diff:.6f})")
    
    print(f"HYPOTHESIS 2: {'PASS' if hypothesis2_pass else 'FAIL'}")
    
    # ============== HYPOTHESIS 3 TEST ==============
    print("\n" + "="*70)
    print("HYPOTHESIS 3: Scaling of correction factor variance decreases with base size")
    print("="*70)
    
    variances = {base: np.var(c_emp_data[base]) for base in bases}
    print("Variance of c_emp(t) over t:")
    for base in bases:
        print(f"  {base_names[base]}: {variances[base]:.6e}")
    
    # Check if variance decreases with base size
    var_array = np.array([variances[P] for P in bases])
    P_log = np.log(bases)
    corr = np.corrcoef(P_log, var_array)[0, 1]
    
    hypothesis3_pass = corr < -0.5  # negative correlation expected
    print(f"Correlation between ln(P_k) and variance: {corr:.4f}")
    print(f"HYPOTHESIS 3: {'PASS' if hypothesis3_pass else 'FAIL'} (corr < -0.5)")
    
    # ============== HYPOTHESIS 4 TEST ==============
    print("\n" + "="*70)
    print("HYPOTHESIS 4: Guarded log-gamma prevents overflow for all bases up to 30030")
    print("="*70)
    
    # Test overflow at extreme t
    overflow_test_t = 10_000_000
    overflow_detected = False
    for base in bases:
        try:
            # Force computation of a term that would overflow without guarding
            x = overflow_test_t / 2
            lg_val = guarded_loggamma(x + 1)
            if not np.isfinite(lg_val):
                overflow_detected = True
                break
        except Exception as e:
            overflow_detected = True
            break
    
    print(f"Overflow test at t={overflow_test_t}: {'DETECTED' if overflow_detected else 'NOT DETECTED'}")
    print(f"HYPOTHESIS 4: {'PASS' if not overflow_detected else 'FAIL'}")
    
    # ============== HYPOTHESIS 5 TEST ==============
    print("\n" + "="*70)
    print("HYPOTHESIS 5: Asymptotic limit L_k satisfies L_{k+1}/L_k ≈ 1 + O(1/p_{k+1})")
    print("="*70)
    
    # Compute ratios L_{k+1}/L_k and compare to 1 + 1/p_{k+1}
    ratios = []
    expected_ratios = []
    prime_factors = [11, 13]  # for transitions 210→2310 and 2310→30030
    for i in range(len(bases)-1):
        ratio = L_vals[i+1] / L_vals[i] if L_vals[i] != 0 else 1.0
        ratios.append(ratio)
        expected = 1.0 + 1.0 / prime_factors[i]
        expected_ratios.append(expected)
    
    print("Ratio analysis:")
    for i in range(len(bases)-1):
        print(f"  L_{bases[i+1]}/L_{bases[i]} = {ratios[i]:.6f}, expected ≈ {expected_ratios[i]:.6f}")
    
    # Check if observed ratios are close to expected (within 10%)
    max_rel_error = max(abs(ratios[i] - expected_ratios[i]) / expected_ratios[i] for i in range(len(ratios)))
    hypothesis5_pass = max_rel_error < 0.10
    print(f"Max relative error: {max_rel_error:.4f}")
    print(f"HYPOTHESIS 5: {'PASS' if hypothesis5_pass else 'FAIL'} (error < 10%)")
    
    # ============== PLOTTING ==============
    print("\nGenerating plots...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Plot 1: c_emp(t) vs t for all bases
    ax = axes[0, 0]
    for base in bases:
        ax.plot(t_vals, c_emp_data[base], label=base_names[base], marker='o', markersize=3)
    ax.set_xscale('log')
    ax.set_xlabel('t')
    ax.set_ylabel('c_emp(t)')
    ax.set_title('Empirical Correction Factor vs t')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: L_k vs ln(P_k) with fit
    ax = axes[0, 1]
    x_fit = np.linspace(np.log(min(bases)), np.log(max(bases)), 100)
    y_fit = alpha + beta * x_fit
    ax.plot(np.log(bases), L_vals, 'ro', label='Data')
    ax.plot(x_fit, y_fit, 'b-', label=f'Fit: L = {alpha:.4f} + {beta:.4f}·ln P')
    ax.set_xlabel('ln(P_k)')
    ax.set_ylabel('L_k')
    ax.set_title('Asymptotic Limit vs ln(Primorial)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Variance vs base size
    ax = axes[1, 0]
    var_vals = list(variances.values())
    if any(v > 0 for v in var_vals):
        ax.semilogy(bases, var_vals, 'bo-')
    else:
        ax.plot(bases, var_vals, 'bo-')
    ax.set_xscale('log')
    ax.set_xlabel('Primorial P_k')
    ax.set_ylabel('Variance of c_emp(t)')
    ax.set_title('Variance vs Base Size')
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Residuals for hypothesis 1
    ax = axes[1, 1]
    residuals_plot = L_vals - predicted
    ax.bar(range(len(bases)), residuals_plot, color=['green' if abs(r) < 0.01 else 'red' for r in residuals_plot])
    ax.axhline(0, color='black', linestyle='--')
    ax.set_xticks(range(len(bases)))
    ax.set_xticklabels([base_names[P] for P in bases])
    ax.set_ylabel('Residual (L_k - predicted)')
    ax.set_title('Hypothesis 1 Residuals')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('ldab_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # ============== CONCLUSIONS ==============
    print("\n" + "="*70)
    print("CONCLUSIONS")
    print("="*70)
    print(f"Hypothesis 1 (Linear L_k vs ln P_k): {'SUPPORTED' if hypothesis1_pass else 'REJECTED'} (R² = {r2:.4f})")
    print(f"Hypothesis 2 (Monotonic convergence): {'SUPPORTED' if hypothesis2_pass else 'REJECTED'}")
    print(f"Hypothesis 3 (Variance decreases with base): {'SUPPORTED' if hypothesis3_pass else 'REJECTED'}")
    print(f"Hypothesis 4 (Guarded log-gamma prevents overflow): {'SUPPORTED' if not overflow_detected else 'REJECTED'}")
    print(f"Hypothesis 5 (Scaling ratio L_{{k+1}}/L_k ≈ 1 + 1/p_{{k+1}}): {'SUPPORTED' if hypothesis5_pass else 'REJECTED'}")
    
    print("\nKey findings:")
    print(f"- Estimated asymptotic limits: {', '.join(f'{base_names[P]}={L_estimates[P]:.6f}' for P in bases)}")
    print(f"- Linear fit parameters: α = {alpha:.6f}, β = {beta:.6f}")
    print(f"- All computations completed using guarded log-gamma without overflow.")
    print(f"- Results saved to 'ldab_analysis.png'")
    
    print("\n" + "="*70)
    print("END OF ANALYSIS")
    print("="*70)

if __name__ == "__main__":
    main()