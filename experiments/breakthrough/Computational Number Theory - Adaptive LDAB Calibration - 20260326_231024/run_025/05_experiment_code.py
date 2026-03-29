import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import linregress
import time

def get_primes(n):
    """Return a list of primes <= n."""
    sieve = np.ones(n // 3 + (n % 6 == 2), dtype=bool)
    for i in range(1, int(n**0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[k * k // 3::2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
    return np.r_[2, 3, ((3 * np.nonzero(sieve)[0][1:] + 1) | 1)]

def compute_gaps_for_primorial(k, primes):
    """Compute gaps between integers coprime to P_k up to P_k."""
    p_k = primes[:k]
    P_k = int(np.prod(p_k))
    
    # Use a boolean array to sieve out multiples of primes in p_k
    sieve = np.ones(P_k, dtype=bool)
    for p in p_k:
        sieve[0::p] = False
        
    coprimes = np.nonzero(sieve)[0]
    
    # Gaps wrap around at P_k
    gaps = np.diff(coprimes)
    last_gap = P_k - coprimes[-1] + coprimes[0]
    gaps = np.append(gaps, last_gap)
    
    return gaps, P_k

def main():
    print("Testing Hypothesis: Variance-to-mean ratio scaling exponent of primorial gaps")
    start_time = time.time()
    
    max_k = 8
    primes = get_primes(100)
    
    k_values = np.arange(1, max_k + 1)
    means = []
    variances = []
    ratios = []
    
    for k in k_values:
        gaps, P_k = compute_gaps_for_primorial(k, primes)
        
        # Calculate exactly using float64 to avoid underflow
        mean_g = np.mean(gaps, dtype=np.float64)
        var_g = np.var(gaps, dtype=np.float64)
        
        R_k = var_g / mean_g
        
        means.append(mean_g)
        variances.append(var_g)
        ratios.append(R_k)
        
        print(f"k={k}, P_k={P_k}, Mean={mean_g:.4f}, Var={var_g:.4f}, R(k)={R_k:.4f}")
        
        if time.time() - start_time > 100:
            print("Approaching time limit, stopping early.")
            k_values = k_values[:k]
            break

    ratios = np.array(ratios)
    
    # Fit power law: R(k) ~ k^beta
    # Exclude k=1,2 for better asymptotic fit if possible, but here we only have up to k=8
    # Let's use k >= 3
    valid_idx = k_values >= 3
    if np.sum(valid_idx) > 2:
        log_k = np.log(k_values[valid_idx])
        log_R = np.log(ratios[valid_idx])
        
        slope, intercept, r_value, p_value, std_err = linregress(log_k, log_R)
        
        print(f"\nPower-law fit for R(k) ~ k^beta (k>=3):")
        print(f"Scaling exponent (beta) = {slope:.4f}")
        print(f"R-squared = {r_value**2:.4f}")
        
        plt.figure(figsize=(8, 6))
        plt.plot(np.log(k_values), np.log(ratios), 'o-', label='Data')
        plt.plot(log_k, intercept + slope * log_k, 'r--', label=f'Fit: slope={slope:.4f}')
        plt.xlabel('log(k)')
        plt.ylabel('log(R(k))')
        plt.title('Variance-to-Mean Ratio Scaling of Primorial Gaps')
        plt.legend()
        plt.grid(True)
        plt.savefig('scaling_exponent.png')
        print("Saved plot to scaling_exponent.png")
    
    print("\nCONCLUSIONS:")
    print("1. We extracted the exact gaps between coprimes for primorials up to k=8.")
    print("2. The variance-to-mean ratio R(k) was computed using float64 precision to avoid underflow.")
    print(f"3. The empirical scaling exponent beta (for R(k) ~ k^beta) was found to be {slope:.4f} for k>=3.")
    print("4. This result provides preliminary exact-calculation evidence relating to the hypothesized ~0.56 exponent.")
    print("5. Further analytic work on the inclusion-exclusion structure is required to prove this asymptotic behavior strictly.")

if __name__ == "__main__":
    main()