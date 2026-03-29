import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from scipy.special import gammaln, psi, polygamma
from scipy.optimize import minimize_scalar
import warnings
warnings.filterwarnings('ignore')

# Constants
MAX_K = 10  # primorial index upper bound (k ≥ 4 is critical)
PRIMES_UP_TO = 30  # to generate primorials up to k=10
MAX_N = 1000  # maximum n for truncation in LDAB series

def sieve_primes(limit):
    """Return list of primes up to limit using segmented sieve."""
    if limit < 2:
        return []
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i:limit+1:i] = False
    return np.nonzero(sieve)[0]

def primorials(k_max):
    """Return array of primorials P_k for k=1..k_max."""
    primes = sieve_primes(100)  # enough for k_max <= 10
    primorials_arr = np.ones(k_max + 1, dtype=np.float64)
    for k in range(1, k_max + 1):
        primorials_arr[k] = primorials_arr[k-1] * primes[k-1]
    return primorials_arr[1:]  # P_1 to P_k_max

def ldab_truncation_error(n, k, P_k):
    """
    Compute LDAB truncation error term for index n, primorial order k.
    Uses log-gamma to avoid overflow.
    """
    # LDAB error term: e_n = (-1)^{n+1} / (n * P_k^n) * Gamma(n+1) / Gamma(n + k + 1)
    # But more accurately, for the asymptotic expansion:
    # e_n ≈ (-1)^{n+1} / n * exp( -n log P_k + log Gamma(n+1) - log Gamma(n + k + 1) )
    log_term = -n * np.log(P_k) + gammaln(n + 1) - gammaln(n + k + 1)
    return np.exp(log_term) / n

def ldab_series_sum(k, P_k, N=MAX_N):
    """Compute truncated LDAB series sum S_k = sum_{n=1}^N e_n."""
    n = np.arange(1, N+1, dtype=np.float64)
    terms = ldab_truncation_error(n, k, P_k)
    return np.sum(terms)

def ldab_error_std_error(k, P_k, N=MAX_N, n_samples=500):
    """
    Estimate standard error of truncation error decay rate using bootstrap.
    Returns (mean_log_decay, std_log_decay).
    """
    # Compute log(|e_n|) for n=1..N
    n = np.arange(1, N+1, dtype=np.float64)
    log_abs_terms = np.log(np.abs(ldab_truncation_error(n, k, P_k)))
    
    # Fit log|e_n| ≈ a - b * log n  => decay rate b
    log_n = np.log(n)
    # Linear regression in log-log space
    X = np.vstack([np.ones_like(log_n), log_n]).T
    y = log_abs_terms
    # Solve (X^T X) beta = X^T y
    XtX = X.T @ X
    Xty = X.T @ y
    try:
        beta = np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        return (np.nan, np.nan)
    
    # Residuals for std error
    y_fit = X @ beta
    residuals = y - y_fit
    sigma2 = np.sum(residuals**2) / (len(n) - 2)
    # Std error of slope (decay rate b)
    se_b = np.sqrt(sigma2 / np.sum((log_n - np.mean(log_n))**2))
    
    return (beta[1], se_b)  # slope = decay rate, se_b = std error

def ldab_error_bootstrap(k, P_k, N=MAX_N, n_boot=200):
    """
    Bootstrap estimate of standard error of decay rate using log-space formulation.
    Returns (mean_decay, std_decay).
    """
    n = np.arange(1, N+1, dtype=np.float64)
    log_n = np.log(n)
    log_abs_terms = np.log(np.abs(ldab_truncation_error(n, k, P_k)))
    
    decay_rates = np.zeros(n_boot)
    for i in range(n_boot):
        # Resample residuals with replacement
        residuals = log_abs_terms - (log_n * log_abs_terms[-1] / log_n[-1])  # rough fit
        # Simple linear regression on resampled data
        perm = np.random.permutation(len(n))
        log_n_boot = log_n[perm]
        log_abs_terms_boot = log_abs_terms[perm]
        X = np.vstack([np.ones_like(log_n_boot), log_n_boot]).T
        y = log_abs_terms_boot
        try:
            beta = np.linalg.lstsq(X, y, rcond=None)[0]
            decay_rates[i] = beta[1]
        except:
            decay_rates[i] = np.nan
    
    return (np.nanmean(decay_rates), np.nanstd(decay_rates))

def test_hypothesis_1():
    """
    Hypothesis 1: Log-space error parameterization eliminates precision collapse at k ≥ 4.
    Test: Compute decay rate standard errors for k=1..8 using log-space regression.
    """
    print("\n=== HYPOTHESIS 1 TEST: Log-Space Error Parameterization ===")
    print("Testing finite standard errors for k ≥ 4 using float64 only.")
    
    k_vals = np.arange(1, MAX_K+1)
    P_vals = primorials(MAX_K)
    
    results = []
    for k, P_k in zip(k_vals, P_vals):
        try:
            decay, se = ldab_error_std_error(k, P_k)
            results.append((k, P_k, decay, se))
            status = "PASS" if np.isfinite(se) and not np.isnan(se) else "FAIL"
            print(f"k={k:2d}, P_k={P_k:12.0f}, decay={decay:8.4f}, SE={se:.6e}, {status}")
        except Exception as e:
            print(f"k={k:2d}, P_k={P_k:12.0f}, ERROR: {e}")
            results.append((k, P_k, np.nan, np.nan))
    
    # Check hypothesis: all SEs finite for k ≥ 4?
    k_ge4_se = [se for k, _, _, se in results if k >= 4]
    all_finite = all(np.isfinite(se) and not np.isnan(se) for se in k_ge4_se)
    
    print(f"\nHypothesis 1: {'SUPPORTED' if all_finite else 'REJECTED'}")
    print(f"Standard errors for k ≥ 4 are {'all finite' if all_finite else 'not all finite'}")
    return all_finite

def test_hypothesis_2():
    """
    Hypothesis 2: Asymptotic decay rate b_k satisfies b_k = 1 + O(1/log P_k).
    Test: Fit b_k and compare to 1 + c/log(P_k) for some c.
    """
    print("\n=== HYPOTHESIS 2 TEST: Asymptotic Decay Rate Scaling ===")
    print("Testing b_k = 1 + O(1/log P_k) for k ≥ 2.")
    
    k_vals = np.arange(2, MAX_K+1)
    P_vals = primorials(MAX_K)[1:]  # skip P_1
    
    decay_rates = []
    for k, P_k in zip(k_vals, P_vals):
        decay, _ = ldab_error_std_error(k, P_k)
        decay_rates.append(decay)
    
    log_P = np.log(P_vals)
    b_vals = np.array(decay_rates)
    
    # Fit b_k = 1 + c / log P_k
    y = b_vals - 1.0
    X = 1.0 / log_P
    c_hat = np.dot(X, y) / np.dot(X, X)
    
    b_pred = 1.0 + c_hat / log_P
    residuals = b_vals - b_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((b_vals - np.mean(b_vals))**2)
    r_squared = 1 - ss_res/ss_tot if ss_tot > 0 else 0.0
    
    print(f"Fitted model: b_k = 1 + {c_hat:.4f}/log(P_k)")
    print(f"R² = {r_squared:.4f}")
    
    for i, (k, P_k, b, b_p) in enumerate(zip(k_vals, P_vals, b_vals, b_pred)):
        print(f"k={k:2d}, P_k={P_k:8.0f}, b_k={b:.6f}, pred={b_p:.6f}, diff={b-b_p:.6e}")
    
    # Check if model explains >90% variance
    hypothesis_passed = r_squared > 0.90
    print(f"\nHypothesis 2: {'SUPPORTED' if hypothesis_passed else 'REJECTED'}")
    print(f"R² = {r_squared:.4f} {'≥ 0.90' if hypothesis_passed else '< 0.90'}")
    return hypothesis_passed

def test_hypothesis_3():
    """
    Hypothesis 3: Guarded log-gamma formulation (run_038) yields consistent decay rates
    across k=1..8 with relative error < 1e-6.
    """
    print("\n=== HYPOTHESIS 3 TEST: Guarded Log-Gamma Consistency ===")
    print("Testing relative consistency of decay rates across k.")
    
    k_vals = np.arange(1, MAX_K+1)
    P_vals = primorials(MAX_K)
    
    decay_rates = []
    for k, P_k in zip(k_vals, P_vals):
        decay, se = ldab_error_std_error(k, P_k)
        decay_rates.append(decay)
    
    decay_rates = np.array(decay_rates)
    mean_decay = np.mean(decay_rates)
    rel_errors = np.abs((decay_rates - mean_decay) / mean_decay)
    
    max_rel_error = np.max(rel_errors)
    all_consistent = max_rel_error < 1e-6
    
    print(f"Mean decay rate: {mean_decay:.8f}")
    print(f"Max relative error: {max_rel_error:.2e}")
    
    for k, d, r in zip(k_vals, decay_rates, rel_errors):
        status = "PASS" if r < 1e-6 else "FAIL"
        print(f"k={k:2d}, decay={d:.8f}, rel_err={r:.2e} [{status}]")
    
    print(f"\nHypothesis 3: {'SUPPORTED' if all_consistent else 'REJECTED'}")
    print(f"Relative errors {'all < 1e-6' if all_consistent else 'not all < 1e-6'}")
    return all_consistent

def test_hypothesis_4():
    """
    Hypothesis 4: Bootstrap std error estimates match analytic std error estimates
    within 5% relative error for k ≥ 3.
    """
    print("\n=== HYPOTHESIS 4 TEST: Bootstrap-Analytic SE Consistency ===")
    print("Testing relative difference between bootstrap and analytic SE.")
    
    k_vals = np.arange(3, MAX_K+1)
    P_vals = primorials(MAX_K)[2:]  # k=3..MAX_K
    
    results = []
    for k, P_k in zip(k_vals, P_vals):
        analytic_decay, analytic_se = ldab_error_std_error(k, P_k)
        boot_decay, boot_se = ldab_error_bootstrap(k, P_k, n_boot=150)
        
        if analytic_se > 0 and boot_se > 0:
            rel_diff = np.abs(boot_se - analytic_se) / analytic_se
        else:
            rel_diff = np.nan
        
        results.append((k, analytic_se, boot_se, rel_diff))
        status = "PASS" if np.isfinite(rel_diff) and rel_diff < 0.05 else "FAIL"
        print(f"k={k:2d}, analytic_SE={analytic_se:.6e}, boot_SE={boot_se:.6e}, rel_diff={rel_diff:.2%} [{status}]")
    
    # Check all k≥3 have rel_diff < 5%
    rel_diffs = [d for _, _, _, d in results]
    all_within_5pct = all(np.isfinite(d) and d < 0.05 for d in rel_diffs)
    
    print(f"\nHypothesis 4: {'SUPPORTED' if all_within_5pct else 'REJECTED'}")
    print(f"All relative differences {'< 5%' if all_within_5pct else '≥ 5%'}")
    return all_within_5pct

def test_hypothesis_5():
    """
    Hypothesis 5: Polygamma-based error model yields decay rate estimates with
    relative standard error < 1% for k ≥ 4.
    """
    print("\n=== HYPOTHESIS 5 TEST: Polygamma Error Model ===")
    print("Testing relative std error < 1% for k ≥ 4 using psi (digamma) and polygamma.")
    
    k_vals = np.arange(4, MAX_K+1)
    P_vals = primorials(MAX_K)[3:]  # k=4..MAX_K
    
    # Use asymptotic expansion: log Gamma(n+k+1) - log Gamma(n+1) ≈ k * psi(n+1) + (k^2/2) * psi'(n+1) + ...
    # Then error term ~ exp(-n log P_k + k * psi(n+1) + ...) / n
    
    results = []
    for k, P_k in zip(k_vals, P_vals):
        n = np.arange(1, MAX_N+1, dtype=np.float64)
        
        # Asymptotic expansion up to second order
        log_gamma_diff = k * psi(n + 1) + (k**2 / 2) * polygamma(1, n + 1)
        log_term = -n * np.log(P_k) + log_gamma_diff
        log_abs_terms = log_term - np.log(n)
        
        # Linear fit in log-log space
        log_n = np.log(n)
        X = np.vstack([np.ones_like(log_n), log_n]).T
        y = log_abs_terms
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        decay_rate = beta[1]
        
        # Residual std error
        y_fit = X @ beta
        residuals = y - y_fit
        sigma2 = np.sum(residuals**2) / (len(n) - 2)
        se_decay = np.sqrt(sigma2 / np.sum((log_n - np.mean(log_n))**2))
        
        rel_se = se_decay / abs(decay_rate) if decay_rate != 0 else np.nan
        passed = rel_se < 0.01
        
        results.append((k, decay_rate, se_decay, rel_se))
        status = "PASS" if passed else "FAIL"
        print(f"k={k:2d}, decay={decay_rate:.6f}, SE={se_decay:.6e}, rel_SE={rel_se:.2%} [{status}]")
    
    all_passed = all(np.isfinite(r[3]) and r[3] < 0.01 for r in results)
    
    print(f"\nHypothesis 5: {'SUPPORTED' if all_passed else 'REJECTED'}")
    print(f"All relative std errors {'< 1%' if all_passed else '≥ 1%'}")
    return all_passed

def generate_plots():
    """Generate and save plots for visual verification (no plt.show)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    print("\n=== GENERATING PLOTS ===")
    
    # Plot 1: Decay rates vs k
    k_vals = np.arange(1, MAX_K+1)
    P_vals = primorials(MAX_K)
    decay_rates = []
    for k, P_k in zip(k_vals, P_vals):
        decay, _ = ldab_error_std_error(k, P_k)
        decay_rates.append(decay)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(k_vals, decay_rates, 'bo-', label='Decay rate $b_k$')
    ax.axhline(y=1.0, color='r', linestyle='--', label='Expected limit $b=1$')
    ax.set_xlabel('Primorial index $k$', fontsize=12)
    ax.set_ylabel('Decay rate $b_k$', fontsize=12)
    ax.set_title('LDAB Truncation Error Decay Rates', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('ldab_decay_rates.png', dpi=150)
    plt.close()
    
    # Plot 2: Log-log plot for k=4
    k = 4
    P_k = primorials(MAX_K)[3]
    n = np.arange(1, MAX_N+1, dtype=np.float64)
    log_abs_terms = np.log(np.abs(ldab_truncation_error(n, k, P_k)))
    log_n = np.log(n)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(log_n, log_abs_terms, 'b-', label='log |e_n|')
    # Fit line
    X = np.vstack([np.ones_like(log_n), log_n]).T
    y = log_abs_terms
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    ax.plot(log_n, X @ beta, 'r--', label=f'Fit: log|e_n| ≈ {beta[0]:.3f} + {beta[1]:.3f} log n')
    ax.set_xlabel('log n', fontsize=12)
    ax.set_ylabel('log |truncation error|', fontsize=12)
    ax.set_title(f'LDAB Error Decay for k={k}, P_k={int(P_k)}', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('ldab_loglog_k4.png', dpi=150)
    plt.close()

def main():
    print("="*70)
    print("LDAB CALIBRATION ERROR MODEL HYPOTHESIS TESTING SUITE")
    print("="*70)
    
    # Run all hypothesis tests
    h1 = test_hypothesis_1()
    h2 = test_hypothesis_2()
    h3 = test_hypothesis_3()
    h4 = test_hypothesis_4()
    h5 = test_hypothesis_5()
    
    # Generate plots
    generate_plots()
    
    # Print summary
    print("\n" + "="*70)
    print("CONCLUSIONS:")
    print("="*70)
    print("Hypothesis 1 (Log-space eliminates precision collapse): ", 
          "SUPPORTED" if h1 else "REJECTED")
    print("Hypothesis 2 (Asymptotic scaling b_k = 1 + O(1/log P_k)): ", 
          "SUPPORTED" if h2 else "REJECTED")
    print("Hypothesis 3 (Guarded log-gamma consistency): ", 
          "SUPPORTED" if h3 else "REJECTED")
    print("Hypothesis 4 (Bootstrap-analytic SE consistency): ", 
          "SUPPORTED" if h4 else "REJECTED")
    print("Hypothesis 5 (Polygamma model with rel_SE < 1%): ", 
          "SUPPORTED" if h5 else "REJECTED")
    
    all_passed = all([h1, h2, h3, h4, h5])
    print("\nOverall: ", "ALL HYPOTHESES SUPPORTED" if all_passed else "SOME HYPOTHESES REJECTED")
    print("\nNote: All tests used only float64 arithmetic (no arbitrary precision).")
    print("Plots saved as: ldab_decay_rates.png, ldab_loglog_k4.png")
    print("="*70)

if __name__ == "__main__":
    main()