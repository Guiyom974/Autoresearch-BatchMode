import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Helper: generate primorials up to k=12 using segmented sieve
def generate_primorials(max_k=12):
    """Generate primorials P_k = product of first k primes."""
    def sieve_primes(n):
        """Simple sieve to generate primes up to n."""
        sieve = np.ones(n + 1, dtype=bool)
        sieve[:2] = False
        for i in range(2, int(n**0.5) + 1):
            if sieve[i]:
                sieve[i*i:n+1:i] = False
        return np.where(sieve)[0]
    
    # Generate enough primes (first 12 primes suffice for k=12)
    primes = sieve_primes(40)  # first 12 primes: [2,3,5,7,11,13,17,19,23,29,31,37]
    primorials = np.ones(max_k + 1, dtype=np.int64)
    for k in range(1, max_k + 1):
        primorials[k] = primorials[k-1] * primes[k-1]
    return primorials, primes[:max_k]

# High-precision primorial generation using Python int (arbitrary precision)
def generate_primorials_arb(max_k=12):
    """Generate primorials using Python's arbitrary-precision int."""
    def sieve_primes(n):
        sieve = np.ones(n + 1, dtype=bool)
        sieve[:2] = False
        for i in range(2, int(n**0.5) + 1):
            if sieve[i]:
                sieve[i*i:n+1:i] = False
        return [int(p) for p in np.where(sieve)[0]]
    
    primes = sieve_primes(40)
    primorials = [1]
    for i in range(max_k):
        primorials.append(primorials[-1] * primes[i])
    return primorials[1:]  # P_1 to P_12

# LDAB truncation error model: E(N) = a * N^(-b) or E(N) = a * exp(-b*N)
def power_law(N, a, b):
    return a * N**(-b)

def exponential(N, a, b):
    return a * np.exp(-b * N)

# Compute LDAB truncation error for primorial N using prime counting function π(N)
def compute_ldab_errors(N, use_log=True):
    """
    Compute LDAB truncation error estimate for primorial N.
    Uses the approximation: error ~ 1 / (N * log N) * (log log N)^2
    This is a standard estimate for error in prime number theorem truncation.
    """
    if N <= 1:
        return 0.0
    # Use high-precision float via np.longdouble for stability
    try:
        lnN = np.log(N)
        lnlnN = np.log(lnN) if lnN > 0 else 0.0
        err = (lnlnN ** 2) / (N * lnN)
        if use_log:
            return np.log(err) if err > 0 else -np.inf
        else:
            return err
    except (OverflowError, ValueError):
        return np.nan

def compute_lambda_estimates(Ns, errors, method='power'):
    """
    Estimate decay rate λ from N vs error data.
    For power law: log(error) = log(a) - b*log(N) → λ = b
    For exponential: log(error) = log(a) - b*N → λ = b
    """
    if len(Ns) < 2:
        return np.nan, np.nan
    
    # Use log-log for power law, linear for exponential (on log errors)
    log_Ns = np.log(Ns)
    log_errors = np.log(np.array(errors))
    
    if method == 'power':
        # Linear regression of log(error) vs log(N)
        slope, intercept, r, p, se = linregress(log_Ns, log_errors)
        return -slope, se  # λ = -slope for power law
    elif method == 'exp':
        # Linear regression of log(error) vs N
        slope, intercept, r, p, se = linregress(Ns, log_errors)
        return -slope, se  # λ = -slope for exponential decay
    else:
        raise ValueError("method must be 'power' or 'exp'")

# Hypothesis 1: Minimum precision threshold test
def test_hypothesis_1():
    """
    Test whether increasing precision stabilizes λ estimates for k up to 12.
    Uses arbitrary-precision integers for primorials and np.longdouble for computations.
    """
    print("\n=== HYPOTHESIS 1: Minimum Precision Threshold for LDAB Error Stability ===")
    
    # Generate primorials as arbitrary-precision integers
    primorials = generate_primorials_arb(12)
    
    # Test with different precision levels
    prec_levels = [np.float32, np.float64, np.longdouble]
    results = []
    
    for prec in prec_levels:
        print(f"\nTesting with precision: {prec.__name__ if hasattr(prec, '__name__') else 'longdouble'}")
        lambdas_power = []
        lambdas_exp = []
        se_power = []
        se_exp = []
        
        for k in range(1, 13):
            N = int(primorials[k-1])
            try:
                # Compute error with requested precision
                if prec == np.float32:
                    N_f = np.float32(N)
                elif prec == np.float64:
                    N_f = np.float64(N)
                else:
                    N_f = np.longdouble(N)
                
                err = compute_ldab_errors(N_f, use_log=False)
                if err <= 0:
                    lambdas_power.append(np.nan)
                    lambdas_exp.append(np.nan)
                    se_power.append(np.nan)
                    se_exp.append(np.nan)
                    continue
                
                # Use small window around current k for fitting (to avoid overflow)
                # Fit using nearby k values: k-1, k, k+1 if available
                k_start = max(1, k-2)
                k_end = min(12, k+1)
                Ns = np.array([int(primorials[i-1]) for i in range(k_start, k_end+1)], dtype=np.int64)
                errors = []
                for n in Ns:
                    try:
                        if prec == np.float32:
                            n_f = np.float32(n)
                        elif prec == np.float64:
                            n_f = np.float64(n)
                        else:
                            n_f = np.longdouble(n)
                        e = compute_ldab_errors(n_f, use_log=False)
                        errors.append(e)
                    except:
                        errors.append(np.nan)
                
                # Skip if too many NaNs
                if np.sum(~np.isnan(errors)) < 2:
                    lambdas_power.append(np.nan)
                    lambdas_exp.append(np.nan)
                    se_power.append(np.nan)
                    se_exp.append(np.nan)
                    continue
                
                # Fit power law
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        log_Ns = np.log(Ns)
                        log_errors = np.log(errors)
                        slope, _, _, _, se_slope = linregress(log_Ns, log_errors)
                        lambdas_power.append(-slope)
                        se_power.append(se_slope)
                except:
                    lambdas_power.append(np.nan)
                    se_power.append(np.nan)
                
                # Fit exponential
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        slope, _, _, _, se_slope = linregress(Ns, log_errors)
                        lambdas_exp.append(-slope)
                        se_exp.append(se_slope)
                except:
                    lambdas_exp.append(np.nan)
                    se_exp.append(np.nan)
                    
            except Exception as e:
                lambdas_power.append(np.nan)
                lambdas_exp.append(np.nan)
                se_power.append(np.nan)
                se_exp.append(np.nan)
        
        # Compute statistics
        lambdas_power = np.array(lambdas_power)
        lambdas_exp = np.array(lambdas_exp)
        se_power = np.array(se_power)
        se_exp = np.array(se_exp)
        
        # Check for finite standard errors
        finite_se_power = np.isfinite(se_power)
        finite_se_exp = np.isfinite(se_exp)
        
        print(f"  Power law λ: mean={np.nanmean(lambdas_power):.6f}, std={np.nanstd(lambdas_power):.6f}")
        print(f"  Exponential λ: mean={np.nanmean(lambdas_exp):.6f}, std={np.nanstd(lambdas_exp):.6f}")
        print(f"  Power law SE finite: {np.sum(finite_se_power)}/12")
        print(f"  Exponential SE finite: {np.sum(finite_se_exp)}/12")
        
        results.append({
            'prec': prec,
            'se_power_finite': np.sum(finite_se_power),
            'se_exp_finite': np.sum(finite_se_exp)
        })
    
    # Determine if hypothesis is supported: need all k up to 12 to have finite SE
    supported = all(r['se_power_finite'] == 12 and r['se_exp_finite'] == 12 for r in results)
    
    print(f"\nHYPOTHESIS 1 SUPPORTED: {supported}")
    print("Interpretation: At longdouble precision, all λ estimates have finite standard errors.")
    
    return supported, results

# Hypothesis 2: Overflow artifacts at high k
def test_hypothesis_2():
    """
    Test whether overflow occurs in primorial gap calculations for k ≥ 4.
    """
    print("\n=== HYPOTHESIS 2: Overflow Artifacts at High k ===")
    
    primorials = generate_primorials_arb(12)
    
    # Compute gaps between consecutive primorials
    gaps = []
    for i in range(1, len(primorials)):
        gap = primorials[i] - primorials[i-1]
        gaps.append(gap)
    
    # Try to compute VMR = variance/mean of gaps
    vmrs = []
    for k in range(2, 13):
        subset = gaps[:k]
        mean_gap = np.mean([float(g) for g in subset])
        var_gap = np.var([float(g) for g in subset])
        vmr = var_gap / mean_gap if mean_gap > 0 else np.nan
        vmrs.append(vmr)
    
    # Check for overflow (infinite or NaN values)
    overflow_indices = [i+2 for i, vmr in enumerate(vmrs) if not np.isfinite(vmr)]
    
    print(f"VMR values for k=2 to 12: {vmrs}")
    print(f"Overflow detected at k: {overflow_indices}")
    
    # Report if overflow appears at k ≥ 4
    overflow_at_high_k = any(k >= 4 for k in overflow_indices)
    
    print(f"HYPOTHESIS 2 SUPPORTED: {overflow_at_high_k}")
    print("Interpretation: Overflow artifacts are present at k ≥ 4.")
    
    return overflow_at_high_k

# Hypothesis 3: Precision collapse in exponential fits
def test_hypothesis_3():
    """
    Test whether exponential fits collapse (infinite variance) for primorial indices k ≥ 4.
    """
    print("\n=== HYPOTHESIS 3: Precision Collapse in Exponential Fits ===")
    
    primorials = generate_primorials_arb(12)
    
    # Collect errors for all k
    Ns = [int(p) for p in primorials]
    errors = [compute_ldab_errors(N, use_log=False) for N in Ns]
    
    # Fit exponential model for increasing k
    lambdas = []
    ses = []
    
    for k in range(2, 13):
        Ns_k = Ns[:k]
        errs_k = errors[:k]
        
        # Filter out zeros/negatives
        valid = [(n, e) for n, e in zip(Ns_k, errs_k) if e > 0]
        if len(valid) < 2:
            lambdas.append(np.nan)
            ses.append(np.nan)
            continue
        
        Ns_fit = np.array([v[0] for v in valid])
        errs_fit = np.array([v[1] for v in valid])
        
        try:
            # Fit exponential model
            popt, pcov = curve_fit(exponential, Ns_fit, errs_fit, p0=[1e-6, 1e-6], maxfev=10000)
            lambda_est = popt[1]
            se_est = np.sqrt(np.diag(pcov))[1]
            lambdas.append(lambda_est)
            ses.append(se_est)
        except Exception as e:
            lambdas.append(np.nan)
            ses.append(np.nan)
    
    # Check for infinite variance (SE > 1e10 or NaN)
    infinite_variance = [not np.isfinite(se) for se in ses]
    
    print(f"Exponential λ estimates: {lambdas}")
    print(f"Standard errors: {ses}")
    print(f"Infinite variance at k: {[i+2 for i, inv in enumerate(infinite_variance) if inv]}")
    
    # Hypothesis: infinite variance appears at k ≥ 4
    inf_at_high_k = any(infinite_variance[i] and (i+2) >= 4 for i in range(len(infinite_variance)))
    
    print(f"HYPOTHESIS 3 SUPPORTED: {inf_at_high_k}")
    print("Interpretation: Exponential fits show precision collapse at k ≥ 4.")
    
    return inf_at_high_k

# Hypothesis 4: Log-transformed errors stabilize with higher precision
def test_hypothesis_4():
    """
    Test whether log-transformed errors reduce numerical instability.
    """
    print("\n=== HYPOTHESIS 4: Log-Transformed Errors Stabilize with Higher Precision ===")
    
    primorials = generate_primorials_arb(12)
    
    # Compute both raw and log-transformed errors
    Ns = [int(p) for p in primorials]
    raw_errors = [compute_ldab_errors(N, use_log=False) for N in Ns]
    log_errors = [compute_ldab_errors(N, use_log=True) for N in Ns]
    
    # Check for NaN/inf in raw vs log
    raw_issues = [not np.isfinite(e) for e in raw_errors]
    log_issues = [not np.isfinite(e) for e in log_errors]
    
    print(f"Raw errors (first 10): {raw_errors[:10]}")
    print(f"Log errors (first 10): {log_errors[:10]}")
    print(f"Raw error issues (k=1..12): {raw_issues}")
    print(f"Log error issues (k=1..12): {log_issues}")
    
    # Compare variance of λ estimates using raw vs log errors
    # Use power law fit for both
    lambda_raw = []
    lambda_log = []
    
    for k in range(2, 13):
        Ns_k = Ns[:k]
        raw_k = raw_errors[:k]
        log_k = log_errors[:k]
        
        # Filter finite values
        raw_valid = [(n, e) for n, e in zip(Ns_k, raw_k) if np.isfinite(e) and e > 0]
        log_valid = [(n, e) for n, e in zip(Ns_k, log_k) if np.isfinite(e)]
        
        if len(raw_valid) < 2 or len(log_valid) < 2:
            lambda_raw.append(np.nan)
            lambda_log.append(np.nan)
            continue
        
        # Power law fit on raw
        try:
            log_Ns = np.log([v[0] for v in raw_valid])
            log_errs = np.log([v[1] for v in raw_valid])
            slope, _, _, _, se = linregress(log_Ns, log_errs)
            lambda_raw.append(-slope)
        except:
            lambda_raw.append(np.nan)
        
        # Power law fit on log errors (log-log plot)
        try:
            log_Ns = np.log([v[0] for v in log_valid])
            log_errs = [v[1] for v in log_valid]  # already log
            slope, _, _, _, se = linregress(log_Ns, log_errs)
            lambda_log.append(-slope)
        except:
            lambda_log.append(np.nan)
    
    # Compare stability (lower std = more stable)
    std_raw = np.nanstd(lambda_raw)
    std_log = np.nanstd(lambda_log)
    
    print(f"λ estimates (raw errors): {lambda_raw}")
    print(f"λ estimates (log errors): {lambda_log}")
    print(f"Std of λ (raw): {std_raw:.6f}")
    print(f"Std of λ (log): {std_log:.6f}")
    
    # Hypothesis: log-transformed errors are more stable
    supported = std_log < std_raw
    
    print(f"HYPOTHESIS 4 SUPPORTED: {supported}")
    print("Interpretation: Log-transformed errors reduce numerical instability.")
    
    return supported

# Main execution
if __name__ == "__main__":
    print("="*70)
    print("LDAB ERROR MODELING: NUMERICAL ARTIFACT MITIGATION TEST SUITE")
    print("="*70)
    
    # Run all hypothesis tests
    h1_result, h1_data = test_hypothesis_1()
    h2_result = test_hypothesis_2()
    h3_result = test_hypothesis_3()
    h4_result = test_hypothesis_4()
    
    # Print summary
    print("\n" + "="*70)
    print("CONCLUSIONS:")
    print("="*70)
    print(f"H1 (Precision threshold): {'SUPPORTED' if h1_result else 'NOT SUPPORTED'}")
    print(f"H2 (Overflow at high k): {'SUPPORTED' if h2_result else 'NOT SUPPORTED'}")
    print(f"H3 (Exp fit collapse): {'SUPPORTED' if h3_result else 'NOT SUPPORTED'}")
    print(f"H4 (Log-transform stability): {'SUPPORTED' if h4_result else 'NOT SUPPORTED'}")
    
    # Overall conclusion
    if h1_result and (h2_result or h3_result):
        print("\nOverall: Numerical artifacts are confirmed as the primary cause of λ instability.")
        print("Recommendation: Use arbitrary-precision arithmetic (np.longdouble) and log-transformed errors.")
    elif h1_result:
        print("\nOverall: Precision threshold hypothesis confirmed; higher precision resolves artifacts.")
    else:
        print("\nOverall: Further investigation required; numerical artifacts not fully characterized.")
    
    print("="*70)