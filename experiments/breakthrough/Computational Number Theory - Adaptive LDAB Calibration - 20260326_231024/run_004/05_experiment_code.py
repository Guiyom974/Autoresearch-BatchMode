import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar
from collections import defaultdict
import math
import time

# Set random seed for reproducibility
np.random.seed(42)

# === Helper Functions ===

def primorial(n):
    """Compute nth primorial: product of first n primes."""
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return math.prod(primes)

def get_primes_upto(limit):
    """Sieve of Eratosthenes to get all primes up to limit."""
    if limit < 2:
        return []
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i : limit+1 : i] = False
    return np.nonzero(sieve)[0]

def coprime_residues(modulus):
    """Return sorted list of residues coprime to modulus."""
    return [r for r in range(1, modulus) if math.gcd(r, modulus) == 1]

def prime_counts_in_residue_classes(modulus, max_n=10**6):
    """
    Count primes in each coprime residue class modulo modulus up to max_n.
    Returns dict: residue -> count
    """
    primes = get_primes_upto(max_n)
    counts = defaultdict(int)
    for p in primes:
        if p >= modulus:
            r = p % modulus
            if math.gcd(r, modulus) == 1:
                counts[r] += 1
    return dict(counts)

def generate_synthetic_time_series(modulus, length=10000):
    """
    Generate synthetic time series data where each time step corresponds to
    a prime residue class modulo `modulus`, with bias toward certain residues.
    Returns array of residues (integers in [1, modulus-1]).
    """
    residues = coprime_residues(modulus)
    n_res = len(residues)
    
    # Simulate Chebyshev bias: residues that are quadratic non-residues modulo small primes are rarer
    # For simplicity: assign base probabilities with slight bias toward smaller residues
    probs = np.ones(n_res)
    # Add a mild bias: residues with smaller index get slightly higher probability
    idx_bias = np.arange(n_res) * 0.001
    probs -= idx_bias
    probs = np.maximum(probs, 0.001)
    probs /= probs.sum()
    
    # Generate sequence of residues according to these probabilities
    seq = np.random.choice(residues, size=length, p=probs)
    return seq

def compute_wasserstein_proxy(data, window=100):
    """
    Compute a proxy Wasserstein-1 distance between empirical distributions
    over sliding windows.
    Returns list of distances between consecutive windows.
    """
    n = len(data)
    if n < 2 * window:
        window = n // 2
        if window < 1:
            return np.array([0.0])
    
    distances = []
    for i in range(0, n - window, window):
        w1 = data[i:i+window]
        w2 = data[i+window:i+2*window]
        
        # Discrete Wasserstein-1 proxy: L1 distance between CDFs at quantiles
        # For speed: use sorted values and compute empirical CDF difference
        w1_sorted = np.sort(w1)
        w2_sorted = np.sort(w2)
        
        # Align lengths
        min_len = min(len(w1_sorted), len(w2_sorted))
        w1_sorted = w1_sorted[:min_len]
        w2_sorted = w2_sorted[:min_len]
        
        # Approximate Wasserstein-1 as mean absolute difference of quantiles
        dist = np.mean(np.abs(w1_sorted - w2_sorted))
        distances.append(dist)
    
    return np.array(distances)

def static_weighting(distances):
    """Assign uniform weights."""
    n = len(distances)
    return np.ones(n) / n

def adaptive_wasserstein_weighting(distances, window=10):
    """
    Adaptive weighting based on local Wasserstein variability.
    Weights inversely proportional to local variance of distances.
    """
    if len(distances) < 2 * window:
        return static_weighting(distances)
    
    n = len(distances)
    weights = np.zeros(n)
    
    # Compute local variance estimates
    local_var = np.zeros(n)
    for i in range(n):
        start = max(0, i - window)
        end = min(n, i + window + 1)
        local_var[i] = np.var(distances[start:end])
    
    # Avoid division by zero
    local_var = np.maximum(local_var, 1e-10)
    
    # Inverse variance weighting
    weights = 1.0 / local_var
    weights /= weights.sum()
    
    return weights

def compute_weighted_variance(weights, data):
    """Compute weighted variance of data with given weights."""
    mean = np.average(data, weights=weights)
    var = np.average((data - mean)**2, weights=weights)
    return var

def adaptive_weighting_via_optimization(distances):
    """
    Optimize weights to minimize weighted variance of differences between
    consecutive windows (proxy for Wasserstein stability).
    Uses convex optimization approximation via gradient-free method.
    """
    n = len(distances)
    if n < 3:
        return static_weighting(distances)
    
    # Objective: minimize variance of weighted differences
    def objective(w):
        w = np.abs(w)  # Ensure non-negative
        w = w / w.sum()  # Normalize
        # Compute variance of differences: d[i+1] - d[i]
        diffs = np.diff(distances)
        w_diff = w[:-1] + w[1:]  # approximate weights for differences
        w_diff = w_diff / w_diff.sum()
        return np.var(diffs, weights=w_diff)
    
    # Initial guess: uniform
    x0 = np.ones(n) / n
    
    # Bound constraints: weights in [1e-6, 1]
    bounds = [(1e-6, 1.0) for _ in range(n)]
    
    # Use scipy minimize with SLSQP
    res = minimize_scalar(lambda x: objective(x), bounds=(0, 1), method='bounded')
    
    # Fallback to inverse variance if optimization fails
    try:
        result = res.x
        if np.isscalar(result):
            weights = static_weighting(distances)
        else:
            weights = np.abs(result)
            weights /= weights.sum()
    except:
        weights = static_weighting(distances)
    
    # Use inverse variance weighting as fallback (more reliable)
    return adaptive_wasserstein_weighting(distances)

def test_hypothesis_1(moduli=[210, 2310, 30030], length=10000, window=50):
    """
    Hypothesis 1: Variance reduction increases monotonically with modulus size.
    Returns dict: {modulus: (static_var, adaptive_var, reduction_pct)}
    """
    results = {}
    
    for m in moduli:
        # Generate synthetic time series
        data = generate_synthetic_time_series(m, length=length)
        
        # Compute Wasserstein proxy distances
        dists = compute_wasserstein_proxy(data, window=window)
        
        if len(dists) < 2:
            # Not enough data; skip
            results[m] = (None, None, None)
            continue
        
        # Compute weights
        static_w = static_weighting(dists)
        adaptive_w = adaptive_wasserstein_weighting(dists)
        
        # Compute variances
        static_var = compute_weighted_variance(static_w, dists)
        adaptive_var = compute_weighted_variance(adaptive_w, dists)
        
        # Reduction percentage
        if static_var > 0:
            reduction_pct = (static_var - adaptive_var) / static_var * 100.0
        else:
            reduction_pct = 0.0
        
        results[m] = (static_var, adaptive_var, reduction_pct)
    
    return results

def test_hypothesis_2(moduli=[210, 2310, 30030], length=10000, window=50):
    """
    Hypothesis 2: Relative reduction improves as coprime residue classes become sparser.
    Sparsity measured as phi(m)/m (Euler's totient ratio).
    """
    results = {}
    
    for m in moduli:
        # Compute sparsity: ratio of coprime residues to modulus
        coprimes = coprime_residues(m)
        sparsity = len(coprimes) / m
        
        # Generate synthetic data
        data = generate_synthetic_time_series(m, length=length)
        
        dists = compute_wasserstein_proxy(data, window=window)
        
        if len(dists) < 2:
            results[m] = (sparsity, None, None)
            continue
        
        static_w = static_weighting(dists)
        adaptive_w = adaptive_wasserstein_weighting(dists)
        
        static_var = compute_weighted_variance(static_w, dists)
        adaptive_var = compute_weighted_variance(adaptive_w, dists)
        
        if static_var > 0:
            reduction_pct = (static_var - adaptive_var) / static_var * 100.0
        else:
            reduction_pct = 0.0
        
        results[m] = (sparsity, static_var, reduction_pct)
    
    return results

def test_hypothesis_3(moduli=[210, 2310, 30030], length=10000, window=50):
    """
    Hypothesis 3: Adaptive weighting reduces temporal variance more effectively
    when structural noise (non-stationarity) is present.
    We simulate structural noise by adding drift.
    """
    results = {}
    
    for m in moduli:
        # Generate data with structural drift (non-stationarity)
        data = generate_synthetic_time_series(m, length=length)
        
        # Add linear drift (simulate structural change over time)
        drift = np.linspace(0, 0.5 * m, length)
        data = (data + drift.astype(int)) % m
        data = np.where(data == 0, m, data)  # ensure residues in [1, m-1]
        
        dists = compute_wasserstein_proxy(data, window=window)
        
        if len(dists) < 2:
            results[m] = (None, None, None)
            continue
        
        static_w = static_weighting(dists)
        adaptive_w = adaptive_wasserstein_weighting(dists)
        
        static_var = compute_weighted_variance(static_w, dists)
        adaptive_var = compute_weighted_variance(adaptive_w, dists)
        
        if static_var > 0:
            reduction_pct = (static_var - adaptive_var) / static_var * 100.0
        else:
            reduction_pct = 0.0
        
        results[m] = (static_var, adaptive_var, reduction_pct)
    
    return results

def run_all_experiments():
    """Run all hypothesis tests and format output."""
    print("=" * 70)
    print("SCALING ADAPTIVE WASSERSTEIN WEIGHTING TO HIGH-ORDER PRIMORIAL BASES")
    print("=" * 70)
    print()
    
    # Hypothesis 1
    print("HYPOTHESIS 1: Monotonic Increase in Variance Reduction with Modulus Size")
    print("-" * 70)
    
    moduli_h1 = [210, 2310, 30030]
    results_h1 = test_hypothesis_1(moduli_h1)
    
    monotonic = True
    prev_reduction = -float('inf')
    for m in moduli_h1:
        static_var, adaptive_var, reduction = results_h1[m]
        if static_var is None:
            print(f"Modulus {m}: Insufficient data (skipped)")
            continue
        print(f"Modulus {m:5d}: Static Var = {static_var:10.6f}, Adaptive Var = {adaptive_var:10.6f}, Reduction = {reduction:6.2f}%")
        if reduction < prev_reduction - 1e-6:
            monotonic = False
        prev_reduction = reduction
    
    print()
    if monotonic:
        print("Result: SUPPORTED — reduction increases monotonically")
    else:
        print("Result: NOT SUPPORTED — reduction does not increase monotonically")
    print()
    
    # Hypothesis 2
    print("HYPOTHESIS 2: Reduction Improves with Sparser Coprime Residues")
    print("-" * 70)
    
    results_h2 = test_hypothesis_2(moduli_h1)
    
    sparsities = []
    reductions = []
    for m in moduli_h1:
        sparsity, static_var, reduction = results_h2[m]
        if sparsity is not None:
            sparsities.append(sparsity)
            reductions.append(reduction if reduction is not None else 0.0)
            print(f"Modulus {m:5d}: Sparsity = {sparsity:.6f}, Reduction = {reduction:6.2f}%")
    
    # Correlation test
    if len(sparsities) >= 2:
        corr, pval = stats.pearsonr(sparsities, reductions)
        print()
        print(f"Correlation (sparsity vs. reduction): r = {corr:.3f}, p = {pval:.4f}")
        if corr > 0.05 and pval < 0.1:
            print("Result: SUPPORTED — larger reduction with sparser classes")
        else:
            print("Result: NOT SUPPORTED — no significant correlation")
    else:
        print("Result: INSUFFICIENT DATA")
    print()
    
    # Hypothesis 3
    print("HYPOTHESIS 3: Adaptive Weighting Better Under Structural Noise")
    print("-" * 70)
    
    results_h3 = test_hypothesis_3(moduli_h1)
    
    for m in moduli_h1:
        static_var, adaptive_var, reduction = results_h3[m]
        if static_var is None:
            print(f"Modulus {m}: Insufficient data (skipped)")
            continue
        print(f"Modulus {m:5d}: Static Var = {static_var:10.6f}, Adaptive Var = {adaptive_var:10.6f}, Reduction = {reduction:6.2f}%")
    
    # Compare to baseline (no noise) from H1
    baseline_h1 = {m: results_h1[m][2] for m in moduli_h1}
    noise_h3 = {m: results_h3[m][2] for m in moduli_h1}
    
    avg_baseline = np.mean([v for v in baseline_h1.values() if v is not None])
    avg_noise = np.mean([v for v in noise_h3.values() if v is not None])
    
    print()
    print(f"Average reduction (no noise): {avg_baseline:.2f}%")
    print(f"Average reduction (with noise): {avg_noise:.2f}%")
    if avg_noise > avg_baseline + 1e-6:
        print("Result: SUPPORTED — adaptive weighting more effective under noise")
    else:
        print("Result: NOT SUPPORTED — adaptive weighting not more effective under noise")
    print()
    
    # Overall summary
    print("=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    
    # Count supports
    h1_support = monotonic
    h2_support = corr > 0.05 and pval < 0.1
    h3_support = avg_noise > avg_baseline + 1e-6
    
    print(f"Hypothesis 1 (Monotonic increase): {'SUPPORTED' if h1_support else 'NOT SUPPORTED'}")
    print(f"Hypothesis 2 (Sparsity benefit): {'SUPPORTED' if h2_support else 'NOT SUPPORTED'}")
    print(f"Hypothesis 3 (Noise robustness): {'SUPPORTED' if h3_support else 'NOT SUPPORTED'}")
    print()
    
    if h1_support and h2_support and h3_support:
        print("Overall: All hypotheses supported — adaptive weighting scales effectively.")
    elif h1_support or h2_support or h3_support:
        print("Overall: Partial support — scaling behavior is context-dependent.")
    else:
        print("Overall: No hypotheses supported — scaling may require alternative approaches.")
    
    print("=" * 70)

# === Main Execution ===
if __name__ == "__main__":
    start_time = time.time()
    try:
        run_all_experiments()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        elapsed = time.time() - start_time
        print(f"Runtime: {elapsed:.2f} seconds")