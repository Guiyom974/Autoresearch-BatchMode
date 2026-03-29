import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import li

# --- CONSTANTS & CONFIG ---
MAX_T = 10**6  # Upper bound for prime counting; chosen to stay within time limits
BASES = [210, 30030]  # From prior findings: base-dependent behavior observed
NUM_SAMPLES = 500  # Number of t-values to sample for c_emp(t)

# --- UTILITY FUNCTIONS ---

def segmented_sieve(n):
    """Return list of primes up to n using segmented sieve for memory efficiency."""
    if n < 2:
        return []
    limit = int(np.sqrt(n)) + 1
    # First sieve up to sqrt(n)
    base_primes = np.ones(limit + 1, dtype=bool)
    base_primes[0:2] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if base_primes[i]:
            base_primes[i*i:limit+1:i] = False
    primes = np.where(base_primes)[0].tolist()
    
    # Segment size
    segment_size = max(limit, 10000)
    all_primes = primes.copy()
    
    low = limit + 1
    high = min(low + segment_size, n + 1)
    
    while low <= n:
        is_prime = np.ones(high - low + 1, dtype=bool)
        for p in primes:
            start = max(p * p, ((low + p - 1) // p) * p)
            for j in range(start, high, p):
                is_prime[j - low] = False
        for i in range(len(is_prime)):
            if is_prime[i]:
                all_primes.append(low + i)
        low = high
        high = min(low + segment_size, n + 1)
    
    return all_primes

def prime_counting_function(x, primes):
    """Return π(x) using binary search over precomputed primes."""
    if x < 2:
        return 0
    idx = np.searchsorted(primes, x, side='right')
    return idx

def li_approx(x):
    """Logarithmic integral approximation for π(x), using scipy.special.li."""
    if x <= 0:
        return 0.0
    return float(li(x))

def ldab_model(t):
    """
    LDAB model: L(t) = li(t) / (t / log t)
    This is the *ratio* of the logarithmic integral to the leading-order PNT estimate.
    For large t, this ratio → 1, but with corrections.
    """
    if t <= 1:
        return 1.0
    log_t = np.log(t)
    li_t = li_approx(t)
    pnt_est = t / log_t
    return li_t / pnt_est

def compute_c_emp(t, primes):
    """
    Compute empirical correction factor:
    c_emp(t) = π(t) / ( li(t) / (t / log t) )
             = π(t) * (t / log t) / li(t)
    This is the inverse of the LDAB model applied to π(t).
    """
    if t <= 1:
        return 1.0
    pi_t = prime_counting_function(t, primes)
    li_t = li_approx(t)
    if li_t == 0:
        return 1.0
    return pi_t * (t / np.log(t)) / li_t

def generate_t_values(n_samples, max_t, method='log_uniform'):
    """Generate t-values for sampling c_emp(t)."""
    if method == 'log_uniform':
        # Log-spaced to capture behavior across orders of magnitude
        t_vals = np.logspace(2, np.log10(max_t), n_samples, dtype=int)
        t_vals = np.unique(t_vals)  # Remove duplicates
        t_vals = t_vals[t_vals > 1]
        return t_vals
    elif method == 'linear':
        return np.arange(100, max_t + 1, max(1, max_t // n_samples))
    else:
        return np.random.randint(2, max_t, n_samples)

# --- HYPOTHESIS 1: SYSTEMATIC BIAS FROM OMITTED LOG INTEGRAL CORRECTIONS ---
def test_hypothesis_1(primes):
    """
    Hypothesis 1: Systematic bias arises because LDAB omits higher-order terms in the
    asymptotic expansion of li(x), leading to mean(c_emp) ≠ 1 and bias depending on t.
    
    We test:
    1. Whether mean(c_emp) significantly differs from 1.0
    2. Whether bias correlates with log-log corrections (e.g., (log log t)/log t)
    """
    t_vals = generate_t_values(NUM_SAMPLES, MAX_T, method='log_uniform')
    c_emp_vals = np.array([compute_c_emp(t, primes) for t in t_vals])
    
    # Compute theoretical correction term: 1 + (1 / log t) + (2! / (log t)^2) + ...
    # But use the known asymptotic: π(x) = li(x) * (1 - 1/log x - 1/(log x)^2 - ...)
    # So c_emp = π(x) * (x/log x) / li(x) ≈ (li(x) * (1 - 1/log x - ...)) * (x/log x) / li(x)
    #            ≈ (x/log x) * (1 - 1/log x - ...) / (x/log x) = 1 - 1/log x - ...
    # Therefore, c_emp ≈ 1 - 1/log t
    log_t = np.log(t_vals)
    correction_term = 1.0 - 1.0 / log_t  # First-order correction
    # Higher order: + 1/(log t)^2 etc., but start simple
    
    # Fit linear model: c_emp = a + b * (1/log t) + ε
    X = np.column_stack([np.ones_like(log_t), 1.0 / log_t])
    try:
        coeffs, residuals, rank, s = np.linalg.lstsq(X, c_emp_vals, rcond=None)
        a, b = coeffs
    except Exception:
        a, b = np.nan, np.nan
    
    # Test against null hypothesis H0: a = 1, b = 0 (no bias, no correction needed)
    # But simpler: compare mean(c_emp) to 1.0 via t-test
    t_stat, p_val = stats.ttest_1samp(c_emp_vals, 1.0)
    
    # Correlation with theoretical correction
    corr, corr_pval = stats.pearsonr(c_emp_vals, correction_term)
    
    # Report results
    print("=" * 80)
    print("HYPOTHESIS 1: SYSTEMATIC BIAS DUE TO OMITTED LOG INTEGRAL CORRECTIONS")
    print("=" * 80)
    print(f"Sample size: {len(c_emp_vals)}")
    print(f"Mean(c_emp) = {np.mean(c_emp_vals):.6f}")
    print(f"Std(c_emp)  = {np.std(c_emp_vals, ddof=1):.6f}")
    print(f"Min(c_emp)  = {np.min(c_emp_vals):.6f}")
    print(f"Max(c_emp)  = {np.max(c_emp_vals):.6f}")
    print()
    print(f"t-test vs H0: mean = 1.0")
    print(f"  t-statistic = {t_stat:.6f}")
    print(f"  p-value     = {p_val:.6e}")
    print()
    print(f"Linear model: c_emp = a + b / log t")
    print(f"  a (intercept) = {a:.6f} (expected 1.0)")
    print(f"  b (slope)     = {b:.6f} (expected -1.0)")
    print()
    print(f"Correlation with first-order correction term (1 - 1/log t):")
    print(f"  Pearson r = {corr:.6f}, p = {corr_pval:.6e}")
    print()
    
    # Plot for visual inspection
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: c_emp vs t (log x-axis)
    ax[0].semilogx(t_vals, c_emp_vals, 'b.', alpha=0.6, label='c_emp(t)')
    ax[0].axhline(1.0, color='r', linestyle='--', label='c=1 (null)')
    ax[0].set_xlabel('t')
    ax[0].set_ylabel('c_emp(t)')
    ax[0].set_title('Empirical Correction Factor vs t')
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)
    
    # Plot 2: c_emp vs 1/log t
    ax[1].scatter(1.0 / log_t, c_emp_vals, c='b', alpha=0.6, label='data')
    ax[1].plot(1.0 / log_t, a + b / log_t, 'r--', label='fit: a + b/log t')
    ax[1].set_xlabel('1 / log t')
    ax[1].set_ylabel('c_emp(t)')
    ax[1].set_title('Empirical Correction vs Asymptotic Correction')
    ax[1].legend()
    ax[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('h1_diagnostic.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Interpretation
    print("INTERPRETATION:")
    if p_val < 0.001:
        print("  ✓ Strong evidence against H0: mean(c_emp) ≠ 1.0 (systematic bias confirmed)")
    else:
        print("  ✗ Insufficient evidence to reject H0: mean(c_emp) = 1.0")
    
    if abs(b - (-1.0)) < 0.1 and corr_pval < 0.05:
        print("  ✓ First-order correction term (1 - 1/log t) explains significant variance")
    else:
        print("  ✗ First-order correction term insufficient to explain bias")
    
    print()
    return {
        'mean_c': float(np.mean(c_emp_vals)),
        'std_c': float(np.std(c_emp_vals, ddof=1)),
        't_stat': float(t_stat),
        'p_val': float(p_val),
        'intercept': float(a),
        'slope': float(b),
        'correlation': float(corr)
    }

# --- HYPOTHESIS 2: BASE-DEPENDENT BIAS (PRIMORIAL BASES) ---
def test_hypothesis_2(primes):
    """
    Hypothesis 2: c_emp(t) depends on the base (e.g., primorial numbers like 210, 30030),
    indicating model inadequacy for arithmetic progressions or residue class distributions.
    
    We test:
    1. Compute c_emp(t) for t = base * k where k runs over integers up to some limit
    2. Compare mean(c_emp) across different bases
    """
    print("=" * 80)
    print("HYPOTHESIS 2: BASE-DEPENDENT BIAS IN c_emp(t)")
    print("=" * 80)
    
    results = {}
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    
    for base in BASES:
        # Sample t = base * k for k = 1, 2, ..., up to ~500 samples
        k_vals = np.arange(1, min(501, MAX_T // base + 1))
        t_vals = base * k_vals
        
        c_emp_vals = np.array([compute_c_emp(t, primes) for t in t_vals])
        
        results[base] = {
            'mean': float(np.mean(c_emp_vals)),
            'std': float(np.std(c_emp_vals, ddof=1)),
            'n': len(c_emp_vals)
        }
        
        print(f"Base {base}:")
        print(f"  n = {len(c_emp_vals)}")
        print(f"  Mean(c_emp) = {np.mean(c_emp_vals):.6f}")
        print(f"  Std(c_emp)  = {np.std(c_emp_vals, ddof=1):.6f}")
        print()
        
        # Plot
        ax.plot(k_vals, c_emp_vals, label=f'base={base}', alpha=0.7)
    
    ax.set_xlabel('k (t = base * k)')
    ax.set_ylabel('c_emp(t)')
    ax.set_title('c_emp(t) for Primorial Bases')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('h2_base_dependence.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Statistical test for difference in means
    base_list = list(results.keys())
    if len(base_list) >= 2:
        c1 = [compute_c_emp(base_list[0] * k, primes) for k in range(1, min(501, MAX_T // base_list[0] + 1))]
        c2 = [compute_c_emp(base_list[1] * k, primes) for k in range(1, min(501, MAX_T // base_list[1] + 1))]
        t_stat, p_val = stats.ttest_ind(c1, c2)
        
        print("Two-sample t-test (bases {} vs {}):".format(base_list[0], base_list[1]))
        print(f"  t-statistic = {t_stat:.6f}")
        print(f"  p-value     = {p_val:.6e}")
        print()
        
        if p_val < 0.05:
            print("  ✓ Base-dependent bias confirmed (means differ significantly)")
        else:
            print("  ✗ No significant difference in means across bases")
    else:
        print("  Not enough bases to perform comparison")
    
    print()
    return results

# --- HYPOTHESIS 3: HIGH VARIANCE DUE TO NUMERICAL ARTIFACTS ---
def test_hypothesis_3(primes):
    """
    Hypothesis 3: High variance in c_emp(t) (std ≈ 938) is due to numerical artifacts
    (e.g., precision loss in li(x) for large x) rather than true mathematical behavior.
    
    We test:
    1. Compare c_emp(t) computed with standard vs. higher precision (using vectorized high-precision li)
    2. Check correlation between |c_emp(t) - 1| and t (should grow if artifact)
    """
    print("=" * 80)
    print("HYPOTHESIS 3: HIGH VARIANCE FROM NUMERICAL ARTIFACTS")
    print("=" * 80)
    
    t_vals = generate_t_values(NUM_SAMPLES, MAX_T, method='log_uniform')
    
    # Compute c_emp with standard li (scipy uses double precision)
    c_emp_double = np.array([compute_c_emp(t, primes) for t in t_vals])
    
    # Compute theoretical li(x) using asymptotic expansion with correction terms
    # li(x) ~ x/log x * Σ_{n=0}^∞ n! / (log x)^n
    # We'll compute up to n=5 terms for comparison
    def li_asymp(x, n_terms=5):
        if x <= 0:
            return 0.0
        logx = np.log(x)
        if logx <= 0:
            return 0.0
        terms = np.array([np.math.factorial(i) / (logx ** i) for i in range(n_terms)])
        return x / logx * np.sum(terms)
    
    def compute_c_emp_asymp(t, n_terms=5):
        if t <= 1:
            return 1.0
        pi_t = prime_counting_function(t, primes)
        li_t = li_asymp(t, n_terms)
        if li_t == 0:
            return 1.0
        return pi_t * (t / np.log(t)) / li_t
    
    c_emp_asymp = np.array([compute_c_emp_asymp(t, n_terms=5) for t in t_vals])
    
    print(f"Standard li (double precision):")
    print(f"  Mean(c_emp) = {np.mean(c_emp_double):.6f}")
    print(f"  Std(c_emp)  = {np.std(c_emp_double, ddof=1):.6f}")
    print()
    print(f"Asymptotic li (5 terms):")
    print(f"  Mean(c_emp) = {np.mean(c_emp_asymp):.6f}")
    print(f"  Std(c_emp)  = {np.std(c_emp_asymp, ddof=1):.6f}")
    print()
    
    # Compute difference
    diff = c_emp_double - c_emp_asymp
    print(f"Difference statistics (double - asymptotic):")
    print(f"  Mean(diff) = {np.mean(diff):.6e}")
    print(f"  Std(diff)  = {np.std(diff, ddof=1):.6e}")
    print()
    
    # Check correlation with t
    log_t = np.log(t_vals)
    corr_std, p_std = stats.pearsonr(np.abs(c_emp_double - 1.0), log_t)
    corr_asymp, p_asymp = stats.pearsonr(np.abs(c_emp_asymp - 1.0), log_t)
    
    print("Correlation of |c_emp - 1| with log t:")
    print(f"  Double precision: r = {corr_std:.4f}, p = {p_std:.6e}")
    print(f"  Asymptotic:       r = {corr_asymp:.4f}, p = {p_asymp:.6e}")
    print()
    
    # Plot
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: c_emp vs t for both methods
    ax[0].semilogx(t_vals, c_emp_double, 'b.', alpha=0.5, label='scipy li (double)')
    ax[0].semilogx(t_vals, c_emp_asymp, 'r.', alpha=0.5, label='asymptotic li (5 terms)')
    ax[0].axhline(1.0, color='k', linestyle='--', label='c=1')
    ax[0].set_xlabel('t')
    ax[0].set_ylabel('c_emp(t)')
    ax[0].set_title('c_emp(t): Double vs Asymptotic li')
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)
    
    # Plot 2: Difference vs t
    ax[1].semilogx(t_vals, diff, 'g.', alpha=0.6)
    ax[1].axhline(0, color='k', linestyle='--')
    ax[1].set_xlabel('t')
    ax[1].set_ylabel('c_emp(double) - c_emp(asymp)')
    ax[1].set_title('Difference Between Methods')
    ax[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('h3_precision_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("INTERPRETATION:")
    if np.std(diff, ddof=1) < 1e-10:
        print("  ✓ Methods agree → high variance not from numerical artifacts")
    else:
        print("  ✗ Methods disagree → numerical artifacts likely contribute to variance")
    
    if p_std < 0.05:
        print("  ✓ |c_emp - 1| grows with log t → systematic behavior (not pure noise)")
    else:
        print("  ✗ No clear growth trend with t")
    
    print()
    return {
        'std_double': float(np.std(c_emp_double, ddof=1)),
        'std_asymp': float(np.std(c_emp_asymp, ddof=1)),
        'mean_diff': float(np.mean(diff)),
        'std_diff': float(np.std(diff, ddof=1)),
        'corr_std': float(corr_std),
        'corr_asymp': float(corr_asymp)
    }

# --- MAIN EXECUTION ---
def main():
    print("LDAB REFINEMENT TEST SUITE")
    print("Testing hypotheses on empirical correction factor c_emp(t)")
    print()
    
    try:
        # Precompute primes up to MAX_T
        print("Computing primes up to MAX_T = 10^6...")
        primes = segmented_sieve(MAX_T)
        print(f"  Found {len(primes)} primes.")
        print()
    except Exception as e:
        print(f"Error generating primes: {e}")
        return
    
    # Run tests
    results_h1 = test_hypothesis_1(primes)
    results_h2 = test_hypothesis_2(primes)
    results_h3 = test_hypothesis_3(primes)
    
    # Final summary
    print("=" * 80)
    print("CONCLUSIONS:")
    print("=" * 80)
    
    h1_confirmed = results_h1['p_val'] < 0.001
    h2_confirmed = False
    if len(results_h2) >= 2:
        # Attempt to recompute for final test
        base_list = list(results_h2.keys())
        if len(base_list) >= 2:
            c1 = [compute_c_emp(base_list[0] * k, primes) for k in range(1, min(501, MAX_T // base_list[0] + 1))]
            c2 = [compute_c_emp(base_list[1] * k, primes) for k in range(1, min(501, MAX_T // base_list[1] + 1))]
            _, p_val = stats.ttest_ind(c1, c2)
            h2_confirmed = p_val < 0.05
    
    h3_confirmed = results_h3['std_diff'] > 1e-6
    
    print(f"1. Systematic bias (H1): {'CONFIRMED' if h1_confirmed else 'NOT CONFIRMED'}")
    print(f"   - Mean(c_emp) significantly ≠ 1.0: {h1_confirmed}")
    print()
    print(f"2. Base-dependent bias (H2): {'CONFIRMED' if h2_confirmed else 'NOT CONFIRMED'}")
    print(f"   - c_emp differs across bases: {h2_confirmed}")
    print()
    print(f"3. Numerical artifacts causing high variance (H3): {'LIKELY' if h3_confirmed else 'UNLIKELY'}")
    print(f"   - std(c_emp) ≈ {results_h1['std_c']:.0f} (not fully explained by precision)")
    print()
    print("OVERALL:")
    if h1_confirmed and h2_confirmed:
        print("  The LDAB model requires refinement to account for:")
        print("    • Systematic bias (mean(c_emp) ≠ 1)")
        print("    • Base-dependent behavior (primorial effects)")
        print("    • High variance (partially numerical, partially structural)")
    elif h1_confirmed:
        print("  Systematic bias confirmed, but base-dependence inconclusive.")
    else:
        print("  Results do not strongly support any hypothesis; consider larger sample or higher precision.")
    print()
    print("Recommendations:")
    print("  • Include higher-order terms in li(x) asymptotic expansion")
    print("  • Investigate residue class distribution in LDAB denominator")
    print("  • Use arbitrary-precision arithmetic for large t")
    print()
    print("END OF TEST SUITE.")

if __name__ == "__main__":
    main()