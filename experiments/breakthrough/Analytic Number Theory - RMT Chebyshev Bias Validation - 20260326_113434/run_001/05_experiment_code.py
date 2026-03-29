import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib.pyplot as plt
import math
from collections import defaultdict

def sieve(n):
    """Sieve of Eratosthenes to find primes up to n."""
    sieve_arr = np.ones(n // 3 + (n % 6 == 2), dtype=bool)
    for i in range(1, int(n**0.5) // 3 + 1):
        if sieve_arr[i]:
            k = 3 * i + 1 | 1
            sieve_arr[k * k // 3::2 * k] = False
            sieve_arr[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
    primes = np.r_[2, 3, ((3 * np.nonzero(sieve_arr)[0][1:] + 1) | 1)]
    return primes[primes <= n]

def get_coprimes_and_qrs(mod):
    """Find coprimes and quadratic residues modulo mod."""
    coprimes = [a for a in range(1, mod) if math.gcd(a, mod) == 1]
    qrs = set((x * x) % mod for x in range(1, mod) if math.gcd(x, mod) == 1)
    nrs = set(coprimes) - qrs
    return coprimes, qrs, nrs

def run_experiment():
    print("Starting RMT-Corrected Chebyshev Bias Validation for Modulo 210...")
    
    LIMIT = 2 * 10**6
    MOD = 210
    
    primes = sieve(LIMIT)
    coprimes, qrs, nrs = get_coprimes_and_qrs(MOD)
    
    # Pre-calculate phi(MOD)
    phi = len(coprimes)
    
    # Track prime counts mod 210
    counts = {a: 0 for a in coprimes}
    
    # To store bias over time
    log_x_vals = []
    normalized_biases = []
    
    step = 5000
    for i in range(0, len(primes), step):
        chunk = primes[i:i+step]
        if len(chunk) == 0:
            break
            
        for p in chunk:
            rem = p % MOD
            if rem in counts:
                counts[rem] += 1
                
        current_x = chunk[-1]
        if current_x < 1000:
            continue
            
        # Calculate NR vs QR bias
        qr_count = sum(counts[a] for a in qrs)
        nr_count = sum(counts[a] for a in nrs)
        
        # Chebyshev bias: NR - QR
        bias = nr_count - qr_count
        
        # Normalize by sqrt(x) / log(x)
        normalization = math.sqrt(current_x) / math.log(current_x)
        normalized_bias = bias / normalization
        
        log_x_vals.append(math.log(current_x))
        normalized_biases.append(normalized_bias)

    # Calculate empirical variance (alpha_emp)
    alpha_emp = np.var(normalized_biases)
    
    # Theoretical alpha approximation based on RMT L-function zero sum
    # Formula given: alpha = (1/2pi) * sum(1/(1/4+gamma^2)) * log(q/pi)
    # By analytic number theory, sum(1/(1/4+gamma^2)) approx log(q) for each character
    # Summing over phi(q)-1 non-trivial characters
    sum_gamma_approx = (phi - 1) * math.log(MOD)
    alpha_theory = (1 / (2 * math.pi)) * sum_gamma_approx * math.log(MOD / math.pi)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(log_x_vals, normalized_biases, label='Empirical Normalized Bias (NR - QR)', color='blue', alpha=0.7)
    plt.axhline(y=np.mean(normalized_biases), color='red', linestyle='--', label=f'Mean = {np.mean(normalized_biases):.2f}')
    plt.fill_between(log_x_vals, 
                     np.mean(normalized_biases) - np.sqrt(alpha_emp), 
                     np.mean(normalized_biases) + np.sqrt(alpha_emp), 
                     color='red', alpha=0.2, label=f'Empirical Std Dev (sqrt(alpha) = {np.sqrt(alpha_emp):.2f})')
    
    plt.title(f'Chebyshev Bias Modulo {MOD} (Normalized)')
    plt.xlabel('log(x)')
    plt.ylabel('Normalized Bias: (NR - QR) / (sqrt(x)/log(x))')
    plt.legend()
    plt.grid(True)
    plt.savefig('chebyshev_bias_mod210.png')
    
    print("\n" + "="*50)
    print("CONCLUSIONS:")
    print("="*50)
    print(f"1. Evaluated primes up to {LIMIT} for Modulo {MOD}.")
    print(f"2. Number of Quadratic Residues: {len(qrs)}")
    print(f"3. Number of Non-Residues: {len(nrs)}")
    print(f"4. Empirical Mean of Normalized Bias: {np.mean(normalized_biases):.4f}")
    print(f"5. Empirical Variance (alpha_emp): {alpha_emp:.4f}")
    print(f"6. RMT Theoretical Variance Approx (alpha_theory): {alpha_theory:.4f}")
    print("\nAssessment of Hypothesis 1:")
    error_margin = abs(alpha_emp - alpha_theory) / alpha_theory * 100
    print(f"The empirical variance ({alpha_emp:.4f}) and the approximated RMT theoretical variance ({alpha_theory:.4f}) differ by {error_margin:.2f}%.")
    if error_margin < 50:
        print("The RMT Covariance model provides a reasonable order-of-magnitude validation for the variance factor alpha mod 210.")
    else:
        print("There is a significant deviation. This may be due to the asymptotic nature of the formula, the need for exact L-function zeros (rather than the logarithmic approximation used here), or finite-sample effects at x = 2*10^6.")

if __name__ == "__main__":
    run_experiment()