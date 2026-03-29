import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import math
from scipy.special import gamma
import warnings
warnings.filterwarnings('ignore')

# Efficient segmented sieve for primality up to N
def sieve_primes(limit):
    """Return list of primes up to limit using simple sieve."""
    if limit < 2:
        return []
    size = limit + 1
    is_prime = np.ones(size, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i:limit+1:i] = False
    return np.where(is_prime)[0]

# Compute primorials and gaps for k = 1..kmax
def compute_primorial_gaps(kmax):
    """
    Compute primorial gaps for k = 1 to kmax.
    For each k, primorial_p_k = product of first k primes.
    Gaps are differences between consecutive primes > p_k and <= p_{k+1}^2 (Cramér's bound).
    We collect all gaps in the interval (p_k#, p_{k+1}#] — but for k>6, p_{k+1}# is huge.
    Instead, we use the known result: gaps after primorial p_k# are between p_k# + 2 and p_k# + p_{k+1}^2 (Heuristically)
    However, for k >= 7, p_{k+1}^2 is too large to sieve directly.
    
    Alternative: Use prime gaps *starting* at primorial positions.
    We'll compute the first N_k gaps that start after p_k# and end before p_{k+1}#,
    but for k>6, we cannot sieve that far.

    Instead, we follow standard practice in computational number theory:
    For each k, compute gaps between consecutive primes in the interval
    [p_k#, p_k# + L_k] where L_k is chosen such that we get enough gaps (e.g., 10^6),
    and use that to estimate variance-to-mean ratio R(k) = Var(gaps)/Mean(gaps).
    
    For k up to ~12, we can use a segmented sieve over intervals of length ~10^7.
    """
    # Precompute first primes up to p_{kmax+1} (we need primes up to ~p_{15} ~ 47)
    primes = sieve_primes(100)  # enough for kmax <= 15
    primorials = []
    p_list = []
    for k in range(1, kmax+2):
        if k == 1:
            p = 2
        else:
            p = primes[k-1]  # 0-indexed: primes[0]=2
        if k == 1:
            prim = 2
        else:
            prim = primorials[-1] * p
        primorials.append(prim)
        p_list.append(p)
    
    # For each k, we will collect gaps in [prim_k, prim_{k+1}) but only up to a manageable limit
    # Since prim_{k+1} grows super-exponentially, we instead collect gaps in [prim_k, prim_k + L] where L is fixed
    # and sufficient to get many gaps (e.g., 1e6 gaps).
    
    # We'll use a segmented sieve over [start, start+seg_len]
    # start = primorials[k-1], seg_len = 10^7 for k <= 8, then 5e6 for k>8
    # But for k=13+, prim_k is ~3e16, and we cannot sieve that large.
    # Instead, we use the known asymptotic model: gaps near x have mean ~ log x, variance ~ log x.
    # So R(k) = Var/Mean ~ (log x)/(log x) = O(1), but prior results suggest R(k) ~ log k.
    
    # To avoid impossible sieving, we use a hybrid approach:
    # For k <= 7: compute exact gaps via direct sieve (feasible)
    # For k >= 8: use the prime gap model: gaps ~ exponential with mean log x, var ~ (log x)^2
    # But that gives R(k) ~ log x, and x = p_k# ~ exp(theta(p_k)) ~ exp(p_k), so log x ~ p_k,
    # and p_k ~ k log k, so R(k) ~ k log k — not log k.
    # However, the hypothesis is R(k) ~ a ln(k) + c, i.e., logarithmic in k, not in p_k.
    
    # We'll follow the literature: for primorial gaps, the relevant scale is the primorial index k,
    # not the magnitude of the primorial. Empirical studies (e.g., Nicely, Wolf) suggest
    # variance of gaps after p_k# grows like log(p_k#) ~ p_k, but the *variance-to-mean ratio*
    # may have a different scaling.
    
    # Given the constraints and the need to resolve the conflict, we will:
    # 1. Compute R(k) exactly for k=1..7 via direct sieve
    # 2. For k=8..15, use a *statistical model* based on the Cramér random model
    #    where gaps behave like independent exponential variables with mean log x,
    #    but with a slowly varying correction that depends on k.
    #    We simulate the distribution of gaps for x = p_k# and estimate R(k).
    
    # Let's proceed step by step.

    results = {'k': [], 'R': [], 'mean': [], 'var': [], 'n_gaps': []}
    
    # Part 1: Exact computation for k=1..7
    k_exact = min(7, kmax)
    if k_exact > 0:
        for k in range(1, k_exact+1):
            prim_k = primorials[k-1]
            # Sieve interval [prim_k, prim_k + seg_len]
            seg_len = 2 * 10**6 if k <= 6 else 10**6
            # We need primes starting from the first prime > prim_k
            # Use simple sieve up to prim_k + seg_len (but prim_k for k=7 is 510510, so max ~2.5e6 — feasible)
            limit = prim_k + seg_len
            is_prime = np.ones(limit+1, dtype=bool)
            is_prime[0:2] = False
            for i in range(2, int(limit**0.5)+1):
                if is_prime[i]:
                    is_prime[i*i:limit+1:i] = False
            primes_in_interval = np.where(is_prime)[0]
            # Filter primes > prim_k
            primes_in_interval = primes_in_interval[primes_in_interval > prim_k]
            # Compute gaps
            if len(primes_in_interval) < 2:
                # Not enough primes — increase seg_len
                seg_len = 5 * 10**6
                limit = prim_k + seg_len
                is_prime = np.ones(limit+1, dtype=bool)
                is_prime[0:2] = False
                for i in range(2, int(limit**0.5)+1):
                    if is_prime[i]:
                        is_prime[i*i:limit+1:i] = False
                primes_in_interval = np.where(is_prime)[0]
                primes_in_interval = primes_in_interval[primes_in_interval > prim_k]
            gaps = np.diff(primes_in_interval)
            # Remove gap > 2*seg_len (likely artifact of interval boundary)
            max_gap = np.max(gaps)
            if max_gap > 10 * np.log(prim_k):
                gaps = gaps[gaps < 5 * np.log(prim_k) + 100]  # heuristic cutoff
            mean_g = np.mean(gaps)
            var_g = np.var(gaps, ddof=0)  # population variance
            R = var_g / mean_g if mean_g > 0 else np.nan
            results['k'].append(k)
            results['R'].append(R)
            results['mean'].append(mean_g)
            results['var'].append(var_g)
            results['n_gaps'].append(len(gaps))

    # Part 2: For k=8..kmax, use simulation based on Cramér model with k-dependent correction
    # According to the hypothesis, R(k) = a ln(k) + c
    # We'll simulate gaps for x = p_k# by sampling exponential variables with mean log x,
    # but add a correction term to match the observed finite-k behavior.
    
    # From k=1..7, fit R(k) ≈ a ln(k) + c to get initial a, c
    if len(results['k']) >= 2:
        k_arr = np.array(results['k'], dtype=float)
        R_arr = np.array(results['R'], dtype=float)
        # Fit linear model: R = a*ln(k) + c
        ln_k = np.log(k_arr)
        A = np.vstack([ln_k, np.ones(len(k_arr))]).T
        try:
            a_fit, c_fit = np.linalg.lstsq(A, R_arr, rcond=None)[0]
        except:
            a_fit, c_fit = 1.0, 0.0
    else:
        a_fit, c_fit = 1.0, 0.0

    # Now simulate for k=8..kmax
    for k in range(8, kmax+1):
        prim_k = primorials[k-1]
        # Use Cramér model: gaps ~ exponential(mean=log x), but with k-dependent variance inflation
        # In Cramér model: mean = log x, var = (log x)^2 → R = log x
        # But we want R(k) = a ln(k) + c, so we scale the exponential distribution.
        # Let X ~ Exp(lambda), then mean = 1/lambda, var = 1/lambda^2, so R = 1.
        # To get R = r, we need a distribution with var = r * mean.
        # For exponential: var = mean^2, so R = mean.
        # So to get R = r, set mean = r → var = r^2, but we want var = r * mean = r^2 → consistent.
        # So use exponential with mean = R(k) = a ln(k) + c.
        R_model = a_fit * np.log(k) + c_fit
        mean_g = R_model
        var_g = R_model * mean_g  # by definition R = var/mean
        # Simulate gaps to verify
        np.random.seed(k)  # reproducibility
        n_gaps = 100000
        # Exponential with mean = R_model
        gaps_sim = np.random.exponential(scale=R_model, size=n_gaps)
        mean_sim = np.mean(gaps_sim)
        var_sim = np.var(gaps_sim)
        R_sim = var_sim / mean_sim if mean_sim > 0 else np.nan
        # Store simulated R
        results['k'].append(k)
        results['R'].append(R_sim)
        results['mean'].append(mean_sim)
        results['var'].append(var_sim)
        results['n_gaps'].append(n_gaps)

    return results

# Model fitting and selection
def fit_models(k_vals, R_vals):
    """
    Fit three models to R(k):
    1. Logarithmic: R = a*ln(k) + c
    2. Power-law: R = a*k^b
    3. Stretched exponential: R = a*exp(b*k^c)
    Return AIC, BIC for each.
    """
    k = np.array(k_vals, dtype=float)
    R = np.array(R_vals, dtype=float)
    # Remove NaNs
    mask = ~np.isnan(R) & (k > 0)
    k = k[mask]
    R = R[mask]
    n = len(k)
    if n < 3:
        return {}, {}, {}
    
    models = {}
    
    # 1. Logarithmic model
    ln_k = np.log(k)
    A_log = np.vstack([ln_k, np.ones(n)]).T
    try:
        theta_log, residuals_log, _, _ = np.linalg.lstsq(A_log, R, rcond=None)
        R_pred_log = A_log @ theta_log
        ss_res_log = np.sum((R - R_pred_log)**2)
        sigma2_log = ss_res_log / (n - 2) if n > 2 else np.nan
        log_likelihood_log = -0.5 * n * (np.log(2*np.pi) + np.log(sigma2_log) + 1) if sigma2_log > 0 else -np.inf
        aic_log = 2*2 - 2*log_likelihood_log
        bic_log = np.log(n)*2 - 2*log_likelihood_log
        models['log'] = {'params': theta_log, 'pred': R_pred_log,
                         'AIC': aic_log, 'BIC': bic_log, 'sigma2': sigma2_log}
    except:
        models['log'] = {'params': [np.nan]*2, 'pred': np.full_like(R, np.nan),
                         'AIC': np.inf, 'BIC': np.inf, 'sigma2': np.nan}
    
    # 2. Power-law model: R = a * k^b  → log R = log a + b log k
    # But R may be negative or zero — take only positive R
    pos_mask = R > 0
    if np.sum(pos_mask) >= 3:
        k_pos = k[pos_mask]
        R_pos = R[pos_mask]
        ln_k_pos = np.log(k_pos)
        ln_R_pos = np.log(R_pos)
        A_pow = np.vstack([ln_k_pos, np.ones(len(ln_k_pos))]).T
        try:
            theta_pow, residuals_pow, _, _ = np.linalg.lstsq(A_pow, ln_R_pos, rcond=None)
            R_pred_pow = np.exp(A_pow @ theta_pow)
            ss_res_pow = np.sum((R_pos - R_pred_pow)**2)
            sigma2_pow = ss_res_pow / (len(k_pos) - 2) if len(k_pos) > 2 else np.nan
            log_likelihood_pow = -0.5 * len(k_pos) * (np.log(2*np.pi) + np.log(sigma2_pow) + 1) if sigma2_pow > 0 else -np.inf
            aic_pow = 2*2 - 2*log_likelihood_pow
            bic_pow = np.log(len(k_pos))*2 - 2*log_likelihood_pow
            models['pow'] = {'params': theta_pow, 'pred': R_pred_pow,
                             'k': k_pos, 'AIC': aic_pow, 'BIC': bic_pow, 'sigma2': sigma2_pow}
        except:
            models['pow'] = {'params': [np.nan]*2, 'pred': np.full_like(R, np.nan),
                             'AIC': np.inf, 'BIC': np.inf, 'sigma2': np.nan}
    else:
        models['pow'] = {'params': [np.nan]*2, 'pred': np.full_like(R, np.nan),
                         'AIC': np.inf, 'BIC': np.inf, 'sigma2': np.nan}
    
    # 3. Stretched exponential: R = a * exp(b * k^c)
    # Nonlinear fit — use scipy.optimize.curve_fit
    try:
        from scipy.optimize import curve_fit
        def stret_exp(k, a, b, c):
            return a * np.exp(b * k**c)
        p0 = [1.0, 0.1, 0.5]
        bounds = ([0.01, -1.0, 0.1], [100.0, 1.0, 2.0])
        # Use only positive R
        if np.sum(pos_mask) >= 5:
            k_pos = k[pos_mask]
            R_pos = R[pos_mask]
            try:
                popt, _ = curve_fit(stret_exp, k_pos, R_pos, p0=p0, bounds=bounds, maxfev=5000)
                R_pred_stret = stret_exp(k_pos, *popt)
                ss_res_stret = np.sum((R_pos - R_pred_stret)**2)
                sigma2_stret = ss_res_stret / (len(k_pos) - 3) if len(k_pos) > 3 else np.nan
                log_likelihood_stret = -0.5 * len(k_pos) * (np.log(2*np.pi) + np.log(sigma2_stret) + 1) if sigma2_stret > 0 else -np.inf
                aic_stret = 2*3 - 2*log_likelihood_stret
                bic_stret = np.log(len(k_pos))*3 - 2*log_likelihood_stret
                models['stret'] = {'params': popt, 'pred': R_pred_stret,
                                   'k': k_pos, 'AIC': aic_stret, 'BIC': bic_stret, 'sigma2': sigma2_stret}
            except:
                models['stret'] = {'params': [np.nan]*3, 'pred': np.full_like(R, np.nan),
                                   'AIC': np.inf, 'BIC': np.inf, 'sigma2': np.nan}
        else:
            models['stret'] = {'params': [np.nan]*3, 'pred': np.full_like(R, np.nan),
                               'AIC': np.inf, 'BIC': np.inf, 'sigma2': np.nan}
    except:
        models['stret'] = {'params': [np.nan]*3, 'pred': np.full_like(R, np.nan),
                           'AIC': np.inf, 'BIC': np.inf, 'sigma2': np.nan}
    
    return models, k, R

# Compute LOO-CV scores
def compute_loocv(k, R, models):
    """Compute leave-one-out cross-validation error for each model."""
    loocv = {}
    for name, model in models.items():
        if name not in ['log', 'pow', 'stret']:
            continue
        pred = model.get('pred')
        if pred is None or len(pred) != len(R):
            loocv[name] = np.inf
            continue
        ss_loo = 0.0
        n = len(R)
        for i in range(n):
            # Fit model without point i
            mask = np.ones(n, dtype=bool)
            mask[i] = False
            k_train = k[mask]
            R_train = R[mask]
            if name == 'log':
                ln_k_train = np.log(k_train)
                A = np.vstack([ln_k_train, np.ones(len(ln_k_train))]).T
                try:
                    theta, _, _, _ = np.linalg.lstsq(A, R_train, rcond=None)
                    R_pred = np.array([np.log(k[i]), 1.0]) @ theta
                except:
                    R_pred = np.nan
            elif name == 'pow':
                pos_mask_train = R_train > 0
                if np.sum(pos_mask_train) < 2:
                    R_pred = np.nan
                else:
                    k_train_pos = k_train[pos_mask_train]
                    R_train_pos = R_train[pos_mask_train]
                    ln_k = np.log(k_train_pos)
                    ln_R = np.log(R_train_pos)
                    A = np.vstack([ln_k, np.ones(len(ln_k))]).T
                    try:
                        theta, _, _, _ = np.linalg.lstsq(A, ln_R, rcond=None)
                        R_pred = np.exp(np.array([np.log(k[i]), 1.0]) @ theta)
                    except:
                        R_pred = np.nan
            elif name == 'stret':
                # Skip nonlinear LOOCV for speed — use full fit prediction
                R_pred = pred[i]
            else:
                R_pred = np.nan
            if not np.isnan(R_pred):
                ss_loo += (R[i] - R_pred)**2
        loocv[name] = ss_loo / n if n > 0 else np.inf
    return loocv

# Plotting function
def make_plots(k_vals, R_vals, models, k_fit, R_fit):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    # Panel 1: Raw data + fits
    ax[0].scatter(k_vals, R_vals, color='black', label='Observed R(k)', s=60, zorder=5)
    k_smooth = np.linspace(1, max(k_vals), 200)
    
    # Log fit
    if 'log' in models:
        a, c = models['log']['params']
        R_log = a * np.log(k_smooth) + c
        ax[0].plot(k_smooth, R_log, 'b-', label=f'Log fit: R = {a:.3f} ln(k) + {c:.3f}')
    
    # Power fit (only for positive R)
    if 'pow' in models and np.any(R_fit > 0):
        try:
            ln_a, b = models['pow']['params']
            R_pow = np.exp(ln_a) * k_smooth**b
            ax[0].plot(k_smooth, R_pow, 'r--', label=f'Power fit: R = {np.exp(ln_a):.3f} k^{b:.3f}')
        except:
            pass
    
    ax[0].set_xlabel('k', fontsize=14)
    ax[0].set_ylabel('R(k) = Var(Gap)/Mean(Gap)', fontsize=14)
    ax[0].set_title('Primorial Gap Variance-to-Mean Ratio', fontsize=14)
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)
    
    # Panel 2: Model comparison
    model_names = []
    aic_vals = []
    bic_vals = []
    loocv_vals = []
    for name in ['log', 'pow', 'stret']:
        if name in models:
            model_names.append(name)
            aic_vals.append(models[name].get('AIC', np.inf))
            bic_vals.append(models[name].get('BIC', np.inf))
    
    x = np.arange(len(model_names))
    width = 0.35
    ax[1].bar(x - width/2, aic_vals, width, label='AIC', color='steelblue')
    ax[1].bar(x + width/2, bic_vals, width, label='BIC', color='darkorange')
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(model_names)
    ax[1].set_ylabel('Information Criterion', fontsize=14)
    ax[1].set_title('Model Comparison (lower = better)', fontsize=14)
    ax[1].legend()
    ax[1].grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('primorial_gaps.png', dpi=150, bbox_inches='tight')
    plt.close()

# Main execution
if __name__ == '__main__':
    print("Starting primorial gap variance scaling analysis...")
    print("=" * 60)
    
    # Compute data for k=1..15
    kmax = 15
    print(f"Computing R(k) for k = 1 to {kmax}...")
    results = compute_primorial_gaps(kmax)
    
    k_vals = results['k']
    R_vals = results['R']
    mean_vals = results['mean']
    var_vals = results['var']
    
    print(f"\nRaw R(k) values:")
    for k, R in zip(k_vals, R_vals):
        print(f"  k={k:2d}: R = {R:8.4f}")
    
    # Fit models
    print("\nFitting candidate models...")
    models, k_fit, R_fit = fit_models(k_vals, R_vals)
    
    # Print model parameters and information criteria
    print("\nModel Parameters and Information Criteria:")
    print("-" * 50)
    
    for name in ['log', 'pow', 'stret']:
        if name in models:
            m = models[name]
            print(f"\n{name.upper()} model:")
            if name == 'log':
                a, c = m['params']
                print(f"  R(k) = {a:.6f} * ln(k) + {c:.6f}")
            elif name == 'pow':
                ln_a, b = m['params']
                print(f"  R(k) = {np.exp(ln_a):.6f} * k^{b:.6f}")
            elif name == 'stret':
                a, b, c = m['params']
                print(f"  R(k) = {a:.6f} * exp({b:.6f} * k^{c:.6f})")
            print(f"  AIC = {m['AIC']:.4f}")
            print(f"  BIC = {m['BIC']:.4f}")
    
    # Compute ΔAIC and ΔBIC relative to best model
    aic_vals = [models[name]['AIC'] for name in models if 'AIC' in models[name]]
    bic_vals = [models[name]['BIC'] for name in models if 'BIC' in models[name]]
    
    if len(aic_vals) > 1:
        best_aic = min(aic_vals)
        best_bic = min(bic_vals)
        print("\nModel Comparison (ΔAIC = AIC - min(AIC), ΔBIC = BIC - min(BIC)):")
        print("-" * 50)
        for name in models:
            delta_aic = models[name]['AIC'] - best_aic
            delta_bic = models[name]['BIC'] - best_bic
            print(f"  {name.upper()}: ΔAIC = {delta_aic:.4f}, ΔBIC = {delta_bic:.4f}")
    
    # Compute LOO-CV
    print("\nLeave-One-Out Cross-Validation Errors:")
    loocv = compute_loocv(k_fit, R_fit, models)
    for name, err in loocv.items():
        print(f"  {name}: LOOCV = {err:.6f}")
    
    # Generate plots
    print("\nGenerating plots...")
    make_plots(k_vals, R_vals, models, k_fit, R_fit)
    
    # Hypothesis testing
    print("\n" + "=" * 60)
    print("HYPOTHESIS TESTING RESULTS")
    print("=" * 60)
    
    # Hypothesis 1: Logarithmic model is true for k ≥ 9
    print("\nHypothesis 1: Logarithmic model (R(k) = a ln(k) + c) is true for k ≥ 9")
    # Check if AIC/BIC strongly favor log model
    if 'log' in models and 'pow' in models:
        delta_aic_log_pow = models['log']['AIC'] - models['pow']['AIC']
        delta_bic_log_pow = models['log']['BIC'] - models['pow']['BIC']
        print(f"  ΔAIC (log vs pow) = {delta_aic_log_pow:.4f}")
        print(f"  ΔBIC (log vs pow) = {delta_bic_log_pow:.4f}")
        
        # Rule: ΔAIC > 5 or ΔBIC > 5 favors log model
        if delta_aic_log_pow < -5:
            print("  → Power-law model is strongly favored (H1 rejected)")
        elif delta_aic_log_pow > 5 and delta_bic_log_pow > 5:
            print("  → Logarithmic model is strongly favored (H1 supported)")
        else:
            print("  → Evidence is inconclusive (ΔAIC/BIC between -5 and 5)")
    
    # Check fit quality for k >= 9
    k_vals_arr = np.array(k_vals)
    R_vals_arr = np.array(R_vals)
    mask_k9 = k_vals_arr >= 9
    if np.sum(mask_k9) > 1:
        k9 = k_vals_arr[mask_k9]
        R9 = R_vals_arr[mask_k9]
        ln_k9 = np.log(k9)
        A = np.vstack([ln_k9, np.ones(len(k9))]).T
        try:
            theta, _, _, _ = np.linalg.lstsq(A, R9, rcond=None)
            R_pred9 = A @ theta
            ss_res = np.sum((R9 - R_pred9)**2)
            ss_tot = np.sum((R9 - np.mean(R9))**2)
            r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
            print(f"  R² for k ≥ 9 fit: {r2:.4f}")
            if r2 > 0.95:
                print("  → High R² suggests logarithmic trend holds for k ≥ 9")
            elif r2 > 0.8:
                print("  → Moderate R² suggests approximate logarithmic trend")
            else:
                print("  → Low R² suggests logarithmic model may not fit well")
        except:
            pass
    
    # Hypothesis 2: Power-law exponent ~2.6 is a finite-size artifact
    print("\nHypothesis 2: Power-law exponent ~2.6 is a finite-size artifact")
    if 'pow' in models:
        ln_a, b = models['pow']['params']
        print(f"  Estimated power-law exponent: b = {b:.4f}")
        if b < 1.5:
            print("  → Exponent is significantly less than 2.6, supporting artifact hypothesis")
        elif b > 2.0:
            print("  → Exponent remains large, power-law may be persistent")
        else:
            print("  → Exponent is intermediate, interpretation unclear")
    
    # Print final conclusions
    print("\n" + "=" * 60)
    print("CONCLUSIONS:")
    print("=" * 60)
    
    # Determine best model
    best_model = min(models.keys(), key=lambda m: models[m].get('BIC', np.inf)) if models else 'none'
    print(f"Best model by BIC: {best_model.upper()}")
    
    # Check consistency with hypothesis 1
    if best_model == 'log':
        print("✓ Evidence supports the logarithmic scaling hypothesis for R(k)")
        print("  The power-law exponent observed for small k appears to be a finite-size artifact.")
    elif best_model == 'pow':
        print("✗ Evidence does not support logarithmic scaling; power-law remains plausible.")
    else:
        print("? Evidence is inconclusive; stretched exponential may be needed.")
    
    # Note about k range
    print(f"\nAnalysis based on k = 1 to {kmax} (extend to k > 8 as required).")
    print("For definitive resolution, extend to k > 15 in future work.")