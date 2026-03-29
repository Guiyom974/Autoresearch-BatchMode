import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import isqrt, gcd
from functools import reduce

# Efficient segmented sieve for primes up to N
def segmented_sieve(limit, segment_size=10_000):
    """Generate primes up to `limit` using segmented sieve."""
    if limit < 2:
        return np.array([], dtype=np.int64)
    # Base primes up to sqrt(limit)
    sieve_limit = isqrt(limit) + 1
    base_sieve = np.ones(sieve_limit + 1, dtype=bool)
    base_sieve[0:2] = False
    for p in range(2, isqrt(sieve_limit) + 1):
        if base_sieve[p]:
            base_sieve[p*p:sieve_limit+1:p] = False
    base_primes = np.where(base_sieve)[0].astype(np.int64)
    
    primes = []
    low = 2
    while low <= limit:
        high = min(low + segment_size - 1, limit)
        segment = np.ones(high - low + 1, dtype=bool)
        for p in base_primes:
            if p * p > high:
                break
            start = max(p * p, ((low + p - 1) // p) * p)
            segment[start - low::p] = False
        for i, is_prime in enumerate(segment):
            if is_prime:
                primes.append(low + i)
        low = high + 1
    return np.array(primes, dtype=np.int64)

# Primorial function
def primorial(n):
    """Compute the primorial of the n-th prime (product of first n primes)."""
    primes = list(segmented_sieve(100))[:n]  # first n primes
    return int(reduce(lambda x, y: x * y, primes, 1))

# LDAB density estimator: rho(x) = 1 / log(x)
def ldab_density(x):
    """LDAB density estimate: 1 / log(x)."""
    return 1.0 / np.log(x)

# Compute empirical correction factor for a given base and limit
def compute_c_emp(base, limit, primes):
    """
    Compute c_emp(t) for t in [2, limit] using LDAB density.
    
    The LDAB correction factor is defined as:
        c_emp(t) = (sum_{p <= t, p mod base in R} 1 / log(p)) / 
                   (sum_{n <= t, n mod base in R} 1 / log(n))
    where R is the set of residues coprime to base.
    
    However, since we're working with primes only, the numerator is over primes in residue class,
    and denominator is over all integers in residue class (including composites).
    
    To test Hypothesis 1 (algebraic tautology), we compute the ratio of two LDAB-derived sums.
    """
    # Residues coprime to base
    residues = [r for r in range(1, base) if gcd(r, base) == 1]
    residues_arr = np.array(residues, dtype=np.int64)
    
    # Filter primes by residue class
    prime_mods = primes % base
    prime_mask = np.isin(prime_mods, residues_arr)
    primes_in_class = primes[prime_mask]
    
    # Numerator: sum of LDAB density over primes in residue class
    if len(primes_in_class) == 0:
        return 0.0, 0.0, 0.0
    numerator = np.sum(ldab_density(primes_in_class.astype(np.float64)))
    
    # Denominator: sum of LDAB density over all integers in residue class up to limit
    # We'll compute this by iterating over residue classes and summing 1/log(n) for n in [2, limit]
    # with n ≡ r (mod base) for each r in residues
    denominator = 0.0
    for r in residues:
        # Generate integers n = k*base + r, with n >= 2 and n <= limit
        # k_min = ceil((2 - r) / base), k_max = floor((limit - r) / base)
        k_min = max(0, (2 - r + base - 1) // base)
        k_max = (limit - r) // base
        if k_max >= k_min:
            ks = np.arange(k_min, k_max + 1, dtype=np.int64)
            ns = ks * base + r
            # Avoid n=1 (log(1)=0)
            ns = ns[ns > 1]
            if len(ns) > 0:
                denominator += np.sum(ldab_density(ns.astype(np.float64)))
    
    if denominator == 0:
        return 0.0, numerator, denominator
    
    c_emp = numerator / denominator
    return c_emp, numerator, denominator

# Compute c_emp(t) for a series of t values
def compute_c_emp_series(base, limit, primes, num_points=100):
    """Compute c_emp(t) for t values from 100 to limit."""
    t_vals = np.logspace(2, np.log10(limit), num_points, dtype=np.int64)
    c_vals = []
    t_list = []
    
    for t in t_vals:
        c, num, denom = compute_c_emp(base, t, primes)
        c_vals.append(c)
        t_list.append(t)
    
    return np.array(t_list), np.array(c_vals)

# Main test functions for each hypothesis
def test_hypothesis_1(base, limit, primes):
    """
    Hypothesis 1: Algebraic tautology in definition of c_emp(t)
    Expected: c_emp(t) ≈ 1.000000 with zero variance if numerator/denominator share structure.
    
    We test by computing c_emp(t) for multiple bases and checking variance.
    """
    print("\n=== HYPOTHESIS 1: ALGEBRAIC TAUTOLOGY TEST ===")
    print(f"Testing c_emp(t) for base={base}, limit={limit}")
    
    t_vals, c_vals = compute_c_emp_series(base, limit, primes, num_points=50)
    
    print(f"Min c_emp(t): {np.min(c_vals):.10f}")
    print(f"Max c_emp(t): {np.max(c_vals):.10f}")
    print(f"Mean c_emp(t): {np.mean(c_vals):.10f}")
    print(f"Std c_emp(t): {np.std(c_vals):.10e}")
    
    # Plot
    plt.figure(figsize=(6,4))
    plt.semilogx(t_vals, c_vals, 'b-', linewidth=1.5)
    plt.axhline(y=1.0, color='r', linestyle='--', label='y=1.0')
    plt.xlabel('t')
    plt.ylabel('c_emp(t)')
    plt.title(f'Empirical Correction Factor in Base {base}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('hypothesis1_plot.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Statistical test: is variance zero within numerical precision?
    std_dev = np.std(c_vals)
    is_tautology = std_dev < 1e-10 and abs(np.mean(c_vals) - 1.0) < 1e-10
    
    print(f"\nHypothesis 1 verdict: {'CONFIRMED' if is_tautology else 'REJECTED'}")
    print(f"Variance is zero (within 1e-10): {std_dev < 1e-10}")
    print(f"Mean is 1.0 (within 1e-10): {abs(np.mean(c_vals) - 1.0) < 1e-10}")
    
    return is_tautology

def test_hypothesis_2(base, limit, primes):
    """
    Hypothesis 2: Numerator and denominator share identical LDAB-derived quantities.
    We test by explicitly computing the numerator and denominator sums separately.
    """
    print("\n=== HYPOTHESIS 2: NUMERATOR/DENOMINATOR STRUCTURE TEST ===")
    print(f"Testing sums for base={base}, limit={limit}")
    
    # Residues coprime to base
    residues = [r for r in range(1, base) if gcd(r, base) == 1]
    residues_arr = np.array(residues, dtype=np.int64)
    
    # Filter primes by residue class
    prime_mods = primes % base
    prime_mask = np.isin(prime_mods, residues_arr)
    primes_in_class = primes[prime_mask]
    
    # Numerator: sum over primes
    numerator = np.sum(ldab_density(primes_in_class.astype(np.float64)))
    
    # Denominator: sum over integers
    denominator = 0.0
    for r in residues:
        k_min = max(0, (2 - r + base - 1) // base)
        k_max = (limit - r) // base
        if k_max >= k_min:
            ks = np.arange(k_min, k_max + 1, dtype=np.int64)
            ns = ks * base + r
            ns = ns[ns > 1]
            if len(ns) > 0:
                denominator += np.sum(ldab_density(ns.astype(np.float64)))
    
    print(f"Numerator (primes): {numerator:.10f}")
    print(f"Denominator (integers): {denominator:.10f}")
    print(f"Ratio c_emp = {numerator/denominator:.10f}")
    
    # Check if numerator and denominator are proportional to same LDAB integral
    # Compute expected LDAB integral over residue class: phi(base)/base * li(limit)
    # where li(x) ~ x/log(x) + x/log^2(x) + ...
    # For comparison, compute the ratio of numerator to prime count and denominator to integer count
    prime_count = len(primes_in_class)
    # Count integers in residue class
    int_count = sum((limit - r) // base - max(0, (2 - r + base - 1) // base) + 1 
                    for r in residues 
                    if (limit - r) // base >= max(0, (2 - r + base - 1) // base))
    
    print(f"Prime count in residue class: {prime_count}")
    print(f"Integer count in residue class: {int_count}")
    
    # Check proportionality
    if prime_count > 0 and int_count > 0:
        avg_prime_density = numerator / prime_count
        avg_int_density = denominator / int_count
        print(f"Avg LDAB density per prime: {avg_prime_density:.10f}")
        print(f"Avg LDAB density per integer: {avg_int_density:.10f}")
        print(f"Ratio of averages: {avg_prime_density / avg_int_density:.10f}")
    
    # Hypothesis 2: if numerator = denominator, then c_emp=1.0 exactly
    is_proportional = abs(numerator - denominator) < 1e-10
    
    print(f"\nHypothesis 2 verdict: {'CONFIRMED' if is_proportional else 'REJECTED'}")
    print(f"Numerator equals denominator (within 1e-10): {is_proportional}")
    
    return is_proportional

def test_hypothesis_3(base_list, limit, primes):
    """
    Hypothesis 3: The result is independent of the base (only depends on phi(base)/base).
    We test by computing c_emp for multiple bases.
    """
    print("\n=== HYPOTHESIS 3: BASE-INDEPENDENCE TEST ===")
    
    results = []
    for base in base_list:
        c, _, _ = compute_c_emp(base, limit, primes)
        results.append((base, c))
        print(f"Base {base}: c_emp = {c:.10f}")
    
    c_vals = [r[1] for r in results]
    print(f"\nMean c_emp across bases: {np.mean(c_vals):.10f}")
    print(f"Std c_emp across bases: {np.std(c_vals):.10e}")
    
    # Plot
    plt.figure(figsize=(6,4))
    bases = [r[0] for r in results]
    plt.plot(bases, c_vals, 'bo-', linewidth=1.5, markersize=6)
    plt.axhline(y=1.0, color='r', linestyle='--', label='y=1.0')
    plt.xlabel('Base')
    plt.ylabel('c_emp(t)')
    plt.title('Empirical Correction Factor Across Bases')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('hypothesis3_plot.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    is_base_independent = np.std(c_vals) < 1e-10 and abs(np.mean(c_vals) - 1.0) < 1e-10
    
    print(f"\nHypothesis 3 verdict: {'CONFIRMED' if is_base_independent else 'REJECTED'}")
    print(f"Variance across bases is zero (within 1e-10): {np.std(c_vals) < 1e-10}")
    
    return is_base_independent

def test_hypothesis_4(limit, primes):
    """
    Hypothesis 4: The perfect unity arises from using the same LDAB density in numerator and denominator.
    We test by modifying the density in the denominator and observing the effect.
    """
    print("\n=== HYPOTHESIS 4: DENSITY MODIFICATION TEST ===")
    
    base = 210
    residues = [r for r in range(1, base) if gcd(r, base) == 1]
    residues_arr = np.array(residues, dtype=np.int64)
    
    # Filter primes by residue class
    prime_mods = primes % base
    prime_mask = np.isin(prime_mods, residues_arr)
    primes_in_class = primes[prime_mask]
    
    # Original numerator (LDAB density)
    numerator_original = np.sum(ldab_density(primes_in_class.astype(np.float64)))
    
    # Original denominator (LDAB density)
    denominator_original = 0.0
    for r in residues:
        k_min = max(0, (2 - r + base - 1) // base)
        k_max = (limit - r) // base
        if k_max >= k_min:
            ks = np.arange(k_min, k_max + 1, dtype=np.int64)
            ns = ks * base + r
            ns = ns[ns > 1]
            if len(ns) > 0:
                denominator_original += np.sum(ldab_density(ns.astype(np.float64)))
    
    c_original = numerator_original / denominator_original
    
    # Modified denominator: use 1/(log(n) * log(log(n))) instead of 1/log(n)
    def modified_density(x):
        return 1.0 / (np.log(x) * np.log(np.log(x + 2)))  # +2 to avoid log(log(1))
    
    denominator_modified = 0.0
    for r in residues:
        k_min = max(0, (2 - r + base - 1) // base)
        k_max = (limit - r) // base
        if k_max >= k_min:
            ks = np.arange(k_min, k_max + 1, dtype=np.int64)
            ns = ks * base + r
            ns = ns[ns > 1]
            if len(ns) > 0:
                denominator_modified += np.sum(modified_density(ns.astype(np.float64)))
    
    c_modified = numerator_original / denominator_modified
    
    print(f"Original c_emp (LDAB/LDAB): {c_original:.10f}")
    print(f"Modified c_emp (LDAB/modified): {c_modified:.10f}")
    print(f"Relative change: {abs(c_modified - c_original) / c_original * 100:.2f}%")
    
    # Hypothesis 4: if c_emp=1 only when same density used, then modifying density should change result
    is_density_dependent = abs(c_original - 1.0) < 1e-10 and abs(c_modified - 1.0) > 1e-6
    
    print(f"\nHypothesis 4 verdict: {'CONFIRMED' if is_density_dependent else 'REJECTED'}")
    print(f"c_emp=1.0 with LDAB density: {abs(c_original - 1.0) < 1e-10}")
    print(f"c_emp≠1.0 with modified density: {abs(c_modified - 1.0) > 1e-6}")
    
    return is_density_dependent

# Main execution
if __name__ == "__main__":
    print("="*70)
    print("TESTING LDAB EMPIRICAL CORRECTION FACTOR HYPOTHESES")
    print("="*70)
    
    # Parameters
    limit = 5_000_000  # within 2 min runtime
    primes = segmented_sieve(limit)
    print(f"Generated {len(primes)} primes up to {limit:,}")
    
    # Test bases: 210, 2310, 30030 as mentioned in problem
    base_list = [210, 2310, 30030]
    
    # Run all hypothesis tests
    h1_result = test_hypothesis_1(210, limit, primes)
    h2_result = test_hypothesis_2(210, limit, primes)
    h3_result = test_hypothesis_3(base_list, limit, primes)
    h4_result = test_hypothesis_4(limit, primes)
    
    # Print final conclusions
    print("\n" + "="*70)
    print("CONCLUSIONS:")
    print("="*70)
    print(f"Hypothesis 1 (Algebraic tautology): {'SUPPORTED' if h1_result else 'NOT SUPPORTED'}")
    print(f"Hypothesis 2 (Identical LDAB structure): {'SUPPORTED' if h2_result else 'NOT SUPPORTED'}")
    print(f"Hypothesis 3 (Base independence): {'SUPPORTED' if h3_result else 'NOT SUPPORTED'}")
    print(f"Hypothesis 4 (Density dependence): {'SUPPORTED' if h4_result else 'NOT SUPPORTED'}")
    
    # Overall interpretation
    if all([h1_result, h2_result, h3_result, h4_result]):
        print("\nAll hypotheses supported: c_emp(t)=1.0 is an algebraic consequence of the LDAB definition.")
    elif not h1_result and not h2_result:
        print("\nNeither tautology nor identical structure: c_emp(t)=1.0 may indicate a deeper property.")
    elif h1_result and h2_result:
        print("\nStrong evidence for algebraic tautology in LDAB definition.")
    else:
        print("\nMixed results: further investigation needed.")
    
    print("\nPlots saved: hypothesis1_plot.png, hypothesis3_plot.png")
    print("="*70)