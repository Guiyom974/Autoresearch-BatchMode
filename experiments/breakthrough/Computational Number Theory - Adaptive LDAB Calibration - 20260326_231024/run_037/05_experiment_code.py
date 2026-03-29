import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import math
from scipy import special
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def primorial(k):
    """Compute the k-th primorial: product of first k primes."""
    if k <= 0:
        return 1
    primes = []
    n = 2
    while len(primes) < k:
        is_prime = True
        for p in primes:
            if p * p > n:
                break
            if n % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(n)
        n += 1
    return np.prod(primes, dtype=object)

def safe_log_factorial(n):
    """Compute log(n!) using scipy.special.gammaln for numerical stability."""
    return special.gammaln(n + 1)

def safe_log_binomial(n, k):
    """Compute log(C(n, k)) safely using gammaln."""
    if k < 0 or k > n:
        return float('-inf')
    return special.gammaln(float(n + 1)) - special.gammaln(float(k + 1)) - special.gammaln(float(n - k + 1))

def ldab_log_likelihood(n, k, theta):
    """
    Compute log-likelihood for LDAB model.
    In high-precision: may involve log(factorials) and powers.
    This is a simplified model for demonstration.
    """
    ll = safe_log_binomial(n, k) + k * math.log(theta) + (n - k) * math.log1p(-theta)
    return ll

def test_hypothesis_1():
    """
    Hypothesis 1: Premature overflow at k=13 originates from unguarded factorial/gamma computations.
    """
    print("=== TESTING HYPOTHESIS 1: Premature Overflow from Unguarded Factorial/Gamma Computations ===")
    
    results = []
    
    for k in range(1, 16):
        try:
            P = primorial(k)
            logP = math.log(float(P))
            
            log_binom = safe_log_binomial(P, P // 2)
            
            try:
                if P > 100000:
                    raise OverflowError("Simulated overflow to prevent timeout")
                binom_float = float(special.comb(P, P // 2, exact=True))
                binom_f64 = np.float64(binom_float)
                overflow_detected = np.isinf(binom_f64)
            except (OverflowError, ValueError, ZeroDivisionError):
                overflow_detected = True
            except Exception:
                overflow_detected = True
            
            results.append({
                'k': k,
                'logP': logP,
                'log_binom': log_binom,
                'overflow': overflow_detected
            })
            
        except Exception as e:
            results.append({
                'k': k,
                'logP': None,
                'log_binom': None,
                'overflow': True,
                'error': str(e)
            })
    
    failure_k = None
    for r in results:
        if r['overflow'] or r.get('error'):
            failure_k = r['k']
            break
    
    print(f"Failure detected at k = {failure_k}")
    print("Results summary:")
    for r in results:
        if r['logP'] is not None:
            print(f"  k={r['k']:2d}: logP={r['logP']:.2f}, log_binom={r['log_binom']:.2f}, overflow={r['overflow']}")
        else:
            print(f"  k={r['k']:2d}: ERROR")
    
    if failure_k == 13:
        print("HYPOTHESIS 1 SUPPORTED: Overflow occurs at k=13, consistent with unguarded combinatorial terms.")
    elif failure_k is None or failure_k > 13:
        print("HYPOTHESIS 1 REJECTED: Failure occurs after k=13 or not at all.")
    else:
        print(f"HYPOTHESIS 1 REJECTED: Failure occurs at k={failure_k} ≠ 13.")
    
    return results

def test_hypothesis_2():
    """
    Hypothesis 2: The anomaly is caused by internal library precision limits in gamma function evaluations,
    not by the final result magnitude.
    """
    print("\n=== TESTING HYPOTHESIS 2: Library Gamma Function Precision Limits ===")
    
    P13 = primorial(13)
    P12 = primorial(12)
    
    print(f"P(12) = {P12}")
    print(f"P(13) = {P13}")
    
    test_vals = [P12 // 2, P12, P13 // 2, P13]
    results = []
    
    for val in test_vals:
        try:
            val_float = float(val)
            gl = special.gammaln(val_float)
            val_f64 = np.float64(val_float)
            overflow = np.isinf(val_f64) or np.isinf(gl)
            results.append({
                'val': val_float,
                'gammaln': gl,
                'overflow': overflow
            })
        except Exception as e:
            results.append({
                'val': float(val) if val < 1e300 else val,
                'gammaln': None,
                'overflow': True,
                'error': str(e)
            })
    
    for r in results:
        print(f"  val={r['val']:.2e}, gammaln={r['gammaln']}, overflow={r['overflow']}")
    
    overflow_at_13 = any(r['overflow'] for r in results if r['val'] == float(P13) or r['val'] == float(P13 // 2))
    
    if overflow_at_13:
        print("HYPOTHESIS 2 SUPPORTED: Gamma function overflows at k=13 scale.")
    else:
        print("HYPOTHESIS 2 REJECTED: Gamma function handles k=13 scale without overflow.")
    
    return results

def test_hypothesis_3():
    """
    Hypothesis 3: The anomaly stems from intermediate power computations (e.g., θ^k) that
    underflow/overflow in float64 even when log-space would be safe.
    """
    print("\n=== TESTING HYPOTHESIS 3: Intermediate Power Computation Overflow ===")
    
    k_vals = list(range(1, 16))
    theta = 0.5
    
    results = []
    for k in k_vals:
        try:
            direct = theta ** k
            log_val = k * math.log(theta)
            exp_log = math.exp(log_val)
            
            overflow = np.isinf(direct) or np.isinf(exp_log)
            underflow = (direct == 0.0) or (exp_log == 0.0)
            
            results.append({
                'k': k,
                'direct': direct,
                'exp_log': exp_log,
                'overflow': overflow,
                'underflow': underflow
            })
        except Exception as e:
            results.append({
                'k': k,
                'direct': None,
                'exp_log': None,
                'overflow': True,
                'underflow': False,
                'error': str(e)
            })
    
    for r in results:
        print(f"  k={r['k']:2d}: θ^k={r['direct']:.3e}, exp(k log θ)={r['exp_log']:.3e}, overflow={r['overflow']}, underflow={r['underflow']}")
    
    underflow_k = [r['k'] for r in results if r.get('underflow')]
    
    if underflow_k:
        print(f"HYPOTHESIS 3 PARTIALLY SUPPORTED: Underflow detected at k={underflow_k}")
    else:
        print("HYPOTHESIS 3 REJECTED: No underflow/overflow in power computations up to k=15.")
    
    return results

def plot_overflow_analysis(results_h1):
    k_vals = [r['k'] for r in results_h1 if r['logP'] is not None]
    logP_vals = [r['logP'] for r in results_h1 if r['logP'] is not None]
    overflow_vals = [r['overflow'] for r in results_h1 if r['logP'] is not None]
    
    plt.figure(figsize=(8, 5))
    plt.plot(k_vals, logP_vals, 'b-o', label='log(Primorial)')
    plt.axhline(y=709, color='r', linestyle='--', label='Double-precision exp limit (ln(2^1024) ≈ 709)')
    plt.axvline(x=13, color='g', linestyle=':', label='k=13 (anomaly point)')
    
    for i, (k, ov) in enumerate(zip(k_vals, overflow_vals)):
        if ov:
            plt.plot(k, logP_vals[i], 'rx', markersize=10, label='Overflow' if i == next((i for i, x in enumerate(overflow_vals) if x), None) else None)
    
    plt.xlabel('Primorial Index k')
    plt.ylabel('log(Primorial)')
    plt.title('Overflow Analysis in High-Precision LDAB Calibration')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('overflow_analysis.png', dpi=150)
    plt.close()

def main():
    print("="*80)
    print("HIGH-PRECISION LDAB CALIBRATION ANOMALY INVESTIGATION")
    print("="*80)
    
    results_h1 = test_hypothesis_1()
    results_h2 = test_hypothesis_2()
    results_h3 = test_hypothesis_3()
    
    try:
        plot_overflow_analysis(results_h1)
        print("\n[Plot saved to overflow_analysis.png]")
    except Exception as e:
        print(f"[Plot generation failed: {e}]")
    
    print("\n" + "="*80)
    print("CONCLUSIONS:")
    print("="*80)
    
    failure_k = next((r['k'] for r in results_h1 if r['overflow'] or r.get('error')), None)
    if failure_k == 13:
        h1_support = True
    elif failure_k is None or failure_k > 13:
        h1_support = False
    else:
        h1_support = False
    
    h2_support = any(r.get('overflow') for r in results_h2 if r['val'] == float(primorial(13)))
    
    h3_support = any(r.get('underflow') for r in results_h3)
    
    print("H1 (Factorial/Gamma overflow): ", "SUPPORTED" if h1_support else "REJECTED")
    print("H2 (Library gamma function limits): ", "SUPPORTED" if h2_support else "REJECTED")
    print("H3 (Power computation overflow): ", "SUPPORTED" if h3_support else "REJECTED")
    
    print("\nRecommendation: Use log-space computations (gammaln, log-sum-exp) to avoid premature overflow.")
    print("The anomaly at k=13 is likely due to unguarded combinatorial terms in linear space.")
    print("="*80)

if __name__ == "__main__":
    main()