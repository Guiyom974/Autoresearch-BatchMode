import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import linregress
import time

def get_primes(n):
    sieve = np.ones(n // 2, dtype=bool)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i*i // 2::i] = False
    return [2] + [2*i + 1 for i in range(1, n // 2) if sieve[i]]

def compute_gaps(k, primes, max_window=2*10**7):
    # Compute P_k
    p_k = 1
    for p in primes[:k]:
        p_k *= p
        
    window = min(p_k, max_window)
    
    # Sieve to find numbers coprime to P_k in [0, window]
    sieve = np.ones(window, dtype=bool)
    sieve[0] = False
    for p in primes[:k]:
        sieve[0::p] = False
        
    coprimes = np.nonzero(sieve)[0]
    if len(coprimes) < 2:
        return None, None
        
    gaps = np.diff(coprimes)
    return gaps, p_k

def main():
    print("Testing Hypothesis 1: The '0.80-scaling' of the variance-to-mean ratio of primorial gaps")
    
    primes = get_primes(100)
    
    k_values = []
    log_log_pk = []
    log_R_k = []
    
    R_k_values = []
    pk_values = []
    
    start_time = time.time()
    
    # We test k up to 12. For k > 8, we use a sampled window.
    for k in range(1, 13):
        if time.time() - start_time > 100:
            print("Time limit approaching, stopping at k =", k-1)
            break
            
        gaps, p_k = compute_gaps(k, primes, max_window=5*10**7)
        if gaps is None or len(gaps) < 100:
            print(f"k={k}: Not enough gaps sampled.")
            continue
            
        mean_gap = np.mean(gaps)
        var_gap = np.var(gaps)
        R_k = var_gap / mean_gap
        
        k_values.append(k)
        pk_values.append(p_k)
        R_k_values.append(R_k)
        
        llp = np.log(np.log(p_k))
        lr = np.log(R_k)
        
        log_log_pk.append(llp)
        log_R_k.append(lr)
        
        print(f"k = {k:2d} | P_k = {p_k:15d} | Mean = {mean_gap:7.3f} | Var = {var_gap:8.3f} | R(k) = {R_k:7.4f}")

    if len(k_values) > 2:
        slope, intercept, r_value, p_value, std_err = linregress(log_log_pk, log_R_k)
        print("\n--- Regression Results ---")
        print(f"Slope (beta) : {slope:.4f}")
        print(f"Intercept    : {intercept:.4f}")
        print(f"R-squared    : {r_value**2:.4f}")
        
        # Plotting
        plt.figure(figsize=(8, 6))
        plt.scatter(log_log_pk, log_R_k, color='blue', label='Data (R(k))')
        
        fit_line = [slope * x + intercept for x in log_log_pk]
        plt.plot(log_log_pk, fit_line, color='red', linestyle='--', label=f'Fit: beta={slope:.4f}')
        
        plt.xlabel('log(log(P_k))')
        plt.ylabel('log(R(k))')
        plt.title('Variance-to-Mean Ratio Scaling of Primorial Gaps')
        plt.legend()
        plt.grid(True)
        plt.savefig('hypothesis_scaling.png')
        print("Plot saved to hypothesis_scaling.png")
    else:
        slope = None
        print("Not enough data points to perform regression.")

    print("\nCONCLUSIONS:")
    if slope is not None:
        if 0.76 <= slope <= 0.84:
            print(f"The calculated scaling exponent beta = {slope:.4f} strongly supports the 0.80-scaling hypothesis.")
            print("The variance-to-mean ratio of primorial gaps indeed scales proportionally to (log P_k)^0.80.")
        elif slope > 1.0:
            print(f"The calculated scaling exponent beta = {slope:.4f} aligns more closely with the prior finding of 1.17.")
            print("This falsifies the 0.80-scaling hypothesis.")
        else:
            print(f"The calculated scaling exponent beta = {slope:.4f} falls outside the expected [0.76, 0.84] range.")
            print("The exact 0.80 scaling is not supported by this windowed sample, suggesting further investigation is needed.")
    else:
        print("Analysis incomplete due to lack of data points.")

if __name__ == "__main__":
    main()