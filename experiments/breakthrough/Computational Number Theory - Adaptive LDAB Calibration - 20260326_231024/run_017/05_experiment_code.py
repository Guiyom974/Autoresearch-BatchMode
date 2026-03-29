import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import math

# Efficient segmented sieve for primality
def simple_sieve(limit):
    """Return list of primes up to limit using simple sieve."""
    if limit < 2:
        return []
    sieve = bytearray(b'\x01') * (limit + 1)
    sieve[0:2] = b'\x00\x00'
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p*p:limit+1:p] = b'\x00' * ((limit - p*p)//p + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def primorial(k):
    """Return the k-th primorial P_k = product of first k primes."""
    primes = simple_sieve(150)  # enough for k up to ~14
    if k <= 0 or k > len(primes):
        raise ValueError(f"k must be between 1 and {len(primes)}")
    return int(np.prod(primes[:k]))

def primes_up_to_n(n):
    """Return list of primes up to n."""
    return simple_sieve(n)

def compute_gaps_for_primorial(k):
    """Compute gaps between consecutive primes up to P_k#."""
    P_k = primorial(k)
    # Get all primes up to P_k#
    primes = primes_up_to_n(P_k)
    if len(primes) < 2:
        return np.array([])
    gaps = np.diff(primes)
    return gaps

def compute_variance_and_mean(gaps):
    """Compute mean and variance of gaps."""
    if len(gaps) < 2:
        return np.nan, np.nan
    mean = np.mean(gaps)
    var = np.var(gaps, ddof=0)  # population variance
    return mean, var

def compute_R(k):
    """Compute R(k) = variance / mean for primorial gaps up to P_k#."""
    try:
        gaps = compute_gaps_for_primorial(k)
        mean, var = compute_variance_and_mean(gaps)
        if mean <= 0:
            return np.nan
        return var / mean
    except Exception as e:
        print(f"Error computing R({k}): {e}")
        return np.nan

def generate_data(max_k=8):
    """Generate R(k) data for k=1..max_k."""
    k_vals = np.arange(1, max_k + 1)
    R_vals = []
    for k in k_vals:
        R_k = compute_R(int(k))
        R_vals.append(R_k)
    return k_vals, np.array(R_vals)

def power_law(x, A, beta):
    """Power-law model: R(k) = A * k^beta."""
    return A * x**beta

def log_model(x, A, alpha):
    """Logarithmic model: R(k) = A * (log k)^alpha."""
    return A * (np.log(x))**alpha

def fit_models(k_vals, R_vals):
    """Fit power-law and log models and compute AIC/BIC."""
    # Filter out NaNs
    valid = ~np.isnan(R_vals)
    k_vals = k_vals[valid]
    R_vals = R_vals[valid]
    
    if len(k_vals) < 3:
        return None, None, "Insufficient data points"
    
    # Power-law fit
    try:
        popt_pow, _ = curve_fit(power_law, k_vals, R_vals, p0=[1.0, 0.5], maxfev=5000)
        y_pred_pow = power_law(k_vals, *popt_pow)
        ss_res_pow = np.sum((R_vals - y_pred_pow)**2)
        n = len(R_vals)
        k_pow = 2  # number of parameters
        log_likelihood_pow = -n/2 * (np.log(2*np.pi) + np.log(ss_res_pow/n) + 1)
        AIC_pow = 2*k_pow - 2*log_likelihood_pow
        BIC_pow = k_pow*np.log(n) - 2*log_likelihood_pow
    except Exception as e:
        popt_pow = [np.nan, np.nan]
        AIC_pow = BIC_pow = np.inf
    
    # Log model fit (avoid log(0) for k=1)
    k_log = k_vals.copy()
    k_log[k_log == 1] = 1.0000001  # small epsilon to avoid log(0)
    try:
        popt_log, _ = curve_fit(log_model, k_log, R_vals, p0=[1.0, 1.0], maxfev=5000)
        y_pred_log = log_model(k_log, *popt_log)
        ss_res_log = np.sum((R_vals - y_pred_log)**2)
        k_log_params = 2
        log_likelihood_log = -n/2 * (np.log(2*np.pi) + np.log(ss_res_log/n) + 1)
        AIC_log = 2*k_log_params - 2*log_likelihood_log
        BIC_log = k_log_params*np.log(n) - 2*log_likelihood_log
    except Exception as e:
        popt_log = [np.nan, np.nan]
        AIC_log = BIC_log = np.inf
    
    return {
        'power': {'params': popt_pow, 'AIC': AIC_pow, 'BIC': BIC_pow, 'ss_res': ss_res_pow},
        'log': {'params': popt_log, 'AIC': AIC_log, 'BIC': BIC_log, 'ss_res': ss_res_log}
    }, None

def perform_hypothesis_tests(k_vals, R_vals):
    """Perform statistical tests for hypotheses."""
    results = {}
    
    # Filter valid data
    valid = ~np.isnan(R_vals)
    k_vals = k_vals[valid]
    R_vals = R_vals[valid]
    
    if len(k_vals) < 3:
        return {"error": "Insufficient data points"}
    
    # Hypothesis 1: Power-law dominance (β ≠ 0)
    try:
        popt_pow, _ = curve_fit(power_law, k_vals, R_vals, p0=[1.0, 0.5], maxfev=5000)
        beta_hat, beta_std = popt_pow[1], np.sqrt(np.diag(_)[1]) if _ is not None else np.nan
        t_stat = beta_hat / beta_std if beta_std > 0 else np.inf
        # Two-tailed p-value using t-distribution with n-2 df
        df = len(k_vals) - 2
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
        results['hypothesis1'] = {
            'beta_hat': beta_hat,
            'beta_std': beta_std,
            't_stat': t_stat,
            'p_value': p_value,
            'reject_H0': p_value < 0.05
        }
    except Exception as e:
        results['hypothesis1'] = {'error': str(e)}
    
    # Hypothesis 2: Log model better than power-law
    model_fits, err = fit_models(k_vals, R_vals)
    if model_fits:
        # Compare AIC and BIC
        results['hypothesis2'] = {
            'AIC_power': model_fits['power']['AIC'],
            'AIC_log': model_fits['log']['AIC'],
            'BIC_power': model_fits['power']['BIC'],
            'BIC_log': model_fits['log']['BIC'],
            'AIC_prefer_log': model_fits['log']['AIC'] < model_fits['power']['AIC'],
            'BIC_prefer_log': model_fits['log']['BIC'] < model_fits['power']['BIC'],
            'delta_AIC': model_fits['power']['AIC'] - model_fits['log']['AIC'],
            'delta_BIC': model_fits['power']['BIC'] - model_fits['log']['BIC']
        }
    else:
        results['hypothesis2'] = {'error': err}
    
    # Additional: compute R^2 for both models
    try:
        y_pred_pow = power_law(k_vals, *model_fits['power']['params'])
        ss_tot = np.sum((R_vals - np.mean(R_vals))**2)
        ss_res_pow = model_fits['power']['ss_res']
        r2_pow = 1 - ss_res_pow / ss_tot
        
        k_log = k_vals.copy()
        k_log[k_log == 1] = 1.0000001
        y_pred_log = log_model(k_log, *model_fits['log']['params'])
        ss_res_log = model_fits['log']['ss_res']
        r2_log = 1 - ss_res_log / ss_tot
        
        results['goodness_of_fit'] = {
            'R2_power': r2_pow,
            'R2_log': r2_log,
            'prefer_power': r2_pow > r2_log
        }
    except:
        results['goodness_of_fit'] = {'error': 'Could not compute R^2'}
    
    return results

def plot_results(k_vals, R_vals, save_path='primorial_gap_variance.png'):
    """Generate publication-quality plot."""
    valid = ~np.isnan(R_vals)
    k_vals = k_vals[valid]
    R_vals = R_vals[valid]
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    # Panel 1: Raw R(k) vs k
    ax[0].plot(k_vals, R_vals, 'bo-', label='Computed R(k)', markersize=6)
    ax[0].set_xlabel('k (primorial index)', fontsize=12)
    ax[0].set_ylabel('R(k) = variance / mean', fontsize=12)
    ax[0].set_title('Variance-to-Mean Ratio vs k', fontsize=14)
    ax[0].grid(True, alpha=0.3)
    ax[0].legend()
    
    # Panel 2: Log-log plot with fitted models
    k_fine = np.linspace(1, max(k_vals), 200)
    
    # Fit models again for plotting
    try:
        popt_pow, _ = curve_fit(power_law, k_vals, R_vals, p0=[1.0, 0.5], maxfev=5000)
        R_pow_fit = power_law(k_fine, *popt_pow)
    except:
        R_pow_fit = np.full_like(k_fine, np.nan)
        popt_pow = [np.nan, np.nan]
    
    k_log_fine = k_fine.copy()
    k_log_fine[k_log_fine == 1] = 1.0000001
    try:
        popt_log, _ = curve_fit(log_model, k_vals, R_vals, p0=[1.0, 1.0], maxfev=5000)
        R_log_fit = log_model(k_log_fine, *popt_log)
    except:
        R_log_fit = np.full_like(k_log_fine, np.nan)
        popt_log = [np.nan, np.nan]
    
    ax[1].loglog(k_vals, R_vals, 'bo', label='Data', markersize=8)
    if not np.isnan(popt_pow[0]):
        ax[1].loglog(k_fine, R_pow_fit, 'r--', label=f'Power-law: A·k^β (β={popt_pow[1]:.3f})')
    if not np.isnan(popt_log[0]):
        ax[1].loglog(k_log_fine, R_log_fit, 'g-.', label=f'Log model: A·(log k)^α (α={popt_log[1]:.3f})')
    ax[1].set_xlabel('k (primorial index)', fontsize=12)
    ax[1].set_ylabel('R(k)', fontsize=12)
    ax[1].set_title('Model Fits on Log-Log Scale', fontsize=14)
    ax[1].legend(fontsize=10)
    ax[1].grid(True, which='both', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

# Main execution
if __name__ == "__main__":
    print("="*70)
    print("PRIMORIAL GAP VARIANCE SCALING ANALYSIS")
    print("Testing Power-Law vs Logarithmic Scaling Hypotheses")
    print("="*70)
    
    # Compute data for k=1 to 8 to avoid timeout
    print("\n[Step 1] Computing primorial gap variance-to-mean ratios R(k)...")
    k_vals, R_vals = generate_data(max_k=8)
    
    print("\nComputed R(k) values:")
    for k, R in zip(k_vals, R_vals):
        print(f"  k = {int(k):2d}: R(k) = {R:.6f}")
    
    # Generate plot
    print("\n[Step 2] Generating visualization...")
    plot_results(k_vals, R_vals, save_path='primorial_gap_variance.png')
    print("  Saved plot to 'primorial_gap_variance.png'")
    
    # Perform hypothesis tests
    print("\n[Step 3] Performing statistical hypothesis tests...")
    results = perform_hypothesis_tests(k_vals, R_vals)
    
    # Print results for each hypothesis
    print("\n" + "-"*70)
    print("HYPOTHESIS 1: Power-Law Dominance (β ≠ 0)")
    print("-"*70)
    h1 = results.get('hypothesis1', {})
    if 'error' in h1:
        print(f"  ERROR: {h1['error']}")
    else:
        beta_hat = h1.get('beta_hat', np.nan)
        p_value = h1.get('p_value', np.nan)
        reject = h1.get('reject_H0', False)
        print(f"  Estimated β = {beta_hat:.6f}")
        print(f"  p-value = {p_value:.6f}")
        if reject:
            print("  ✅ REJECT null hypothesis (β = 0) at α=0.05")
            print("  → Evidence supports power-law scaling with non-zero exponent.")
        else:
            print("  ❌ FAIL to reject null hypothesis (β = 0) at α=0.05")
            print("  → Insufficient evidence for power-law scaling.")
    
    print("\n" + "-"*70)
    print("HYPOTHESIS 2: Log Model Better Than Power-Law")
    print("-"*70)
    h2 = results.get('hypothesis2', {})
    if 'error' in h2:
        print(f"  ERROR: {h2['error']}")
    else:
        print(f"  AIC (power) = {h2['AIC_power']:.2f}")
        print(f"  AIC (log)   = {h2['AIC_log']:.2f}")
        print(f"  ΔAIC = AIC_power - AIC_log = {h2['delta_AIC']:.2f}")
        if h2['AIC_prefer_log']:
            print("  ✅ AIC favors log model (ΔAIC > 0)")
        else:
            print("  ❌ AIC favors power-law model (ΔAIC ≤ 0)")
        
        print(f"  BIC (power) = {h2['BIC_power']:.2f}")
        print(f"  BIC (log)   = {h2['BIC_log']:.2f}")
        print(f"  ΔBIC = BIC_power - BIC_log = {h2['delta_BIC']:.2f}")
        if h2['BIC_prefer_log']:
            print("  ✅ BIC favors log model (ΔBIC > 0)")
        else:
            print("  ❌ BIC favors power-law model (ΔBIC ≤ 0)")
    
    print("\n" + "-"*70)
    print("GOODNESS-OF-FIT COMPARISON")
    print("-"*70)
    gof = results.get('goodness_of_fit', {})
    if 'error' in gof:
        print(f"  ERROR: {gof['error']}")
    else:
        print(f"  R² (power) = {gof['R2_power']:.6f}")
        print(f"  R² (log)   = {gof['R2_log']:.6f}")
        if gof['prefer_power']:
            print("  → Power model explains more variance (higher R²)")
        else:
            print("  → Log model explains more variance (higher R²)")
    
    # Final conclusions
    print("\n" + "="*70)
    print("CONCLUSIONS:")
    print("="*70)
    
    h1_reject = results.get('hypothesis1', {}).get('reject_H0', False)
    h2_AIC_log = results.get('hypothesis2', {}).get('AIC_prefer_log', False)
    h2_BIC_log = results.get('hypothesis2', {}).get('BIC_prefer_log', False)
    r2_log_higher = results.get('goodness_of_fit', {}).get('R2_log', 0) > results.get('goodness_of_fit', {}).get('R2_power', 0)
    
    if h1_reject:
        print("1. Evidence supports power-law scaling (β ≠ 0).")
    else:
        print("1. No sufficient evidence for power-law scaling (β may be zero).")
    
    if h2_AIC_log and h2_BIC_log and r2_log_higher:
        print("2. Logarithmic model is statistically superior (AIC, BIC, and R²).")
    elif not h2_AIC_log and not h2_BIC_log and not r2_log_higher:
        print("2. Power-law model is statistically superior (AIC, BIC, and R²).")
    else:
        print("2. Model comparison is inconclusive (conflicting criteria).")
    
    print("\nRecommendation: Extend computation to k ≥ 13 to resolve ambiguity.")
    print("="*70)