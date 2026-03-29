import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
from math import gcd

def sieve(n):
    """Returns an array of primes up to n."""
    sieve_arr = np.ones(n // 2, dtype=bool)
    limit = int(np.sqrt(n))
    for i in range(3, limit + 1, 2):
        if sieve_arr[i // 2]:
            sieve_arr[i * i // 2 :: i] = False
    primes = np.r_[2, 2 * np.nonzero(sieve_arr)[0][1:] + 1]
    return primes

def main():
    print("Starting Hypothesis 1 Testing: Adaptive Variance-Based Weighting for Wasserstein Metric")
    start_time = time.time()
    
    N = 10**7
    print(f"Generating primes up to {N}...")
    primes = sieve(N)
    print(f"Found {len(primes)} primes.")
    
    modulus = 210
    # Find allowed residue classes (coprime to 210)
    allowed_classes = [r for r in range(modulus) if gcd(r, modulus) == 1]
    class_to_idx = {r: i for i, r in enumerate(allowed_classes)}
    num_classes = len(allowed_classes)
    
    # Filter primes to only those > 210
    valid_primes = primes[primes > modulus]
    residues = valid_primes % modulus
    
    # Map residues to indices
    mapped_residues = np.array([class_to_idx[r] for r in residues])
    
    # Chunk the data into windows to simulate a stream and calculate rolling metrics
    window_size = 50000
    num_windows = len(mapped_residues) // window_size
    
    # Expected uniform probability across valid classes
    expected_prob = 1.0 / num_classes
    
    # Store empirical distributions per window
    empirical_dists = np.zeros((num_windows, num_classes))
    for w in range(num_windows):
        chunk = mapped_residues[w*window_size : (w+1)*window_size]
        counts = np.bincount(chunk, minlength=num_classes)
        empirical_dists[w] = counts / window_size
        
    # Static weights (uniform)
    static_weights = np.ones(num_classes)
    
    # Rolling variance and adaptive weights
    # We will use an expanding window or a lookback window to compute variance
    lookback = 10
    adaptive_wasserstein = []
    static_wasserstein = []
    
    for w in range(num_windows):
        obs = empirical_dists[w]
        
        # Calculate static Wasserstein (using Total Variation as proxy for discrete metric Wasserstein)
        # W = sum( weight_i * |obs_i - exp_i| )
        stat_w = np.sum(static_weights * np.abs(obs - expected_prob))
        static_wasserstein.append(stat_w)
        
        if w < lookback:
            # Not enough data for variance, use static
            adaptive_weights = static_weights
        else:
            # Calculate variance of each class over the lookback window
            recent_dists = empirical_dists[w-lookback:w]
            class_vars = np.var(recent_dists, axis=0)
            
            # Add small epsilon to avoid division by zero
            epsilon = 1e-9
            # Adaptive weights inversely proportional to variance
            inv_vars = 1.0 / (class_vars + epsilon)
            # Normalize weights so they sum to num_classes (same sum as static weights)
            adaptive_weights = inv_vars / np.sum(inv_vars) * num_classes
            
        adapt_w = np.sum(adaptive_weights * np.abs(obs - expected_prob))
        adaptive_wasserstein.append(adapt_w)
        
    static_wasserstein = np.array(static_wasserstein)
    adaptive_wasserstein = np.array(adaptive_wasserstein)
    
    # Exclude the initial lookback period from variance comparison
    stat_var = np.var(static_wasserstein[lookback:])
    adapt_var = np.var(adaptive_wasserstein[lookback:])
    
    reduction_pct = (stat_var - adapt_var) / stat_var * 100
    
    print("\n=== RESULTS ===")
    print(f"Variance of Static Weighted Wasserstein:   {stat_var:.8e}")
    print(f"Variance of Adaptive Weighted Wasserstein: {adapt_var:.8e}")
    print(f"Reduction in Temporal Variance:            {reduction_pct:.2f}%")
    
    # Check hypothesis
    hypothesis_passed = reduction_pct >= 20.0
    print(f"Hypothesis 1 Passed: {hypothesis_passed}")
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(range(lookback, num_windows), static_wasserstein[lookback:], label='Static Weights', alpha=0.7)
    plt.plot(range(lookback, num_windows), adaptive_wasserstein[lookback:], label='Adaptive Weights', alpha=0.7)
    plt.title('Temporal Evolution of Wasserstein-proxy Metric Modulo 210')
    plt.xlabel('Stream Window Index')
    plt.ylabel('Weighted Total Variation (Wasserstein Proxy)')
    plt.legend()
    plt.grid(True)
    plt.savefig('wasserstein_metric_variance.png')
    print("Saved plot to wasserstein_metric_variance.png")
    
    print(f"\nTotal Execution Time: {time.time() - start_time:.2f} seconds")
    
    print("\nCONCLUSIONS:")
    print("1. A rolling variance-based adaptive weighting scheme was successfully applied to prime residue classes modulo 210.")
    print(f"2. The temporal variance of the Wasserstein proxy metric was reduced by {reduction_pct:.2f}% compared to static weights.")
    if hypothesis_passed:
        print("3. The hypothesis is SUPPORTED: Adaptive weighting dynamically learns residue-class importance and significantly discounts variance noise.")
    else:
        print("3. The hypothesis is REJECTED/PARTIALLY SUPPORTED: The variance reduction did not meet the 20% threshold, suggesting that while adaptive weighting alters the metric, the chosen parameters or metric proxy may need refinement.")

if __name__ == "__main__":
    main()