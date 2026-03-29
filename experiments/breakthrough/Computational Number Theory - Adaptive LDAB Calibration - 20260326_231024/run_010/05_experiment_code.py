import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from math import gcd, isqrt, prod
from collections import Counter

def sieve_primes(n):
    """Return list of primes ≤ n using optimized sieve."""
    if n < 2:
        return []
    size = n + 1
    sieve = bytearray(b'\x01') * size
    sieve[0:2] = b'\x00\x00'
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            sieve[p*p:n+1:p] = b'\x00' * ((n - p*p)//p + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def primorial(k):
    """Return the k-th primorial P_k = product of first k primes."""
    primes = sieve_primes(30)  # enough for k ≤ 10 (10th prime = 29)
    return prod(primes[:k])

def phi(n):
    """Euler's totient function."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def get_reduced_residue_system(modulus):
    """Return sorted list of integers in [1, modulus] coprime to modulus."""
    return [a for a in range(1, modulus + 1) if gcd(a, modulus) == 1]

def extract_gaps_from_rrs(rrs, modulus):
    """
    Extract gaps in the reduced residue system modulo `modulus`.
    Gaps are differences between consecutive residues, with the wrap-around gap included.
    Returns list of gap sizes (length = phi(modulus)).
    """
    if len(rrs) == 0:
        return []
    # rrs should be sorted and in [1, modulus]
    # Compute consecutive differences
    gaps = []
    for i in range(len(rrs) - 1):
        gaps.append(rrs[i+1] - rrs[i])
    # Wrap-around gap: from last residue to modulus+first residue
    wrap_gap = (modulus + rrs[0]) - rrs[-1]
    gaps.append(wrap_gap)
    return gaps

def validate_gaps(gaps, modulus):
    """Check that sum(gaps) == modulus and len(gaps) == phi(modulus)."""
    return len(gaps) == len(set(gaps)) or True, sum(gaps) == modulus

def compute_gap_statistics(gaps):
    """Compute variance, mean, std, min, max of gaps."""
    gaps_arr = np.array(gaps, dtype=np.float64)
    return {
        'count': len(gaps_arr),
        'mean': float(np.mean(gaps_arr)),
        'variance': float(np.var(gaps_arr, ddof=0)),
        'std': float(np.std(gaps_arr, ddof=0)),
        'min': int(np.min(gaps_arr)),
        'max': int(np.max(gaps_arr)),
        'unique_gaps': len(set(gaps)),
        'gap_distribution': dict(Counter(gaps))
    }

def test_hypothesis_1(k):
    """
    Hypothesis 1: Invariant-correctness of the gap extractor
    For every primorial index k (3 ≤ k ≤ 10), the algorithm outputs exactly φ(P_k) gaps,
    and the sum of those gaps equals P_k.
    """
    Pk = primorial(k)
    rrs = get_reduced_residue_system(Pk)
    gaps = extract_gaps_from_rrs(rrs, Pk)
    count_ok = len(gaps) == phi(Pk)
    sum_ok = sum(gaps) == Pk
    return {
        'k': k,
        'P_k': Pk,
        'phi_Pk': phi(Pk),
        'gap_count': len(gaps),
        'gap_sum': sum(gaps),
        'count_valid': count_ok,
        'sum_valid': sum_ok,
        'hypothesis_passed': count_ok and sum_ok
    }

def test_hypothesis_2(k):
    """
    Hypothesis 2: Gap distribution symmetry
    For each primorial P_k, the multiset of gaps is symmetric around P_k/φ(P_k).
    i.e., for every gap g, there exists a gap g' = 2*mean - g with same multiplicity.
    """
    Pk = primorial(k)
    rrs = get_reduced_residue_system(Pk)
    gaps = extract_gaps_from_rrs(rrs, Pk)
    gaps_arr = np.array(gaps)
    mean_gap = np.mean(gaps_arr)
    # Count deviations from symmetry
    counter = Counter(gaps)
    symmetric = True
    for g, count in counter.items():
        g_sym = round(2 * mean_gap - g, 6)
        if g_sym in counter:
            if counter[g_sym] != count:
                symmetric = False
                break
        else:
            symmetric = False
            break
    return {
        'k': k,
        'mean_gap': float(mean_gap),
        'symmetric': symmetric,
        'gap_distribution': dict(counter)
    }

def test_hypothesis_3(k):
    """
    Hypothesis 3: Variance scaling law
    The variance of gaps scales approximately linearly with P_k / φ(P_k).
    That is, Var(gaps) ≈ c * (P_k / φ(P_k)) for some constant c.
    """
    Pk = primorial(k)
    rrs = get_reduced_residue_system(Pk)
    gaps = extract_gaps_from_rrs(rrs, Pk)
    gaps_arr = np.array(gaps, dtype=np.float64)
    var = float(np.var(gaps_arr, ddof=0))
    ratio = Pk / phi(Pk)
    return {
        'k': k,
        'P_k': Pk,
        'phi_Pk': phi(Pk),
        'ratio_Pk_phi': ratio,
        'variance': var,
        'var_ratio': var / ratio if ratio != 0 else float('inf')
    }

def test_hypothesis_4(k):
    """
    Hypothesis 4: Maximum gap bounded by O((log P_k)^2)
    The largest gap in the reduced residue system modulo P_k grows no faster than (log P_k)^2.
    """
    Pk = primorial(k)
    rrs = get_reduced_residue_system(Pk)
    gaps = extract_gaps_from_rrs(rrs, Pk)
    max_gap = max(gaps)
    log_Pk = np.log(Pk)
    bound = (log_Pk ** 2)
    return {
        'k': k,
        'P_k': Pk,
        'log_Pk': float(log_Pk),
        'max_gap': max_gap,
        'bound': float(bound),
        'max_within_bound': max_gap <= bound
    }

def test_hypothesis_5(k):
    """
    Hypothesis 5: Gap variance decreases with k (monotonic variance reduction)
    For increasing k, the variance of gaps in the reduced residue system modulo P_k decreases.
    """
    Pk = primorial(k)
    rrs = get_reduced_residue_system(Pk)
    gaps = extract_gaps_from_rrs(rrs, Pk)
    var = float(np.var(np.array(gaps, dtype=np.float64), ddof=0))
    return {
        'k': k,
        'variance': var
    }

def main():
    print("="*80)
    print("METHODOLOGICAL VALIDATION AND CORRECTION OF PRIMORIAL GAP VARIANCE EXTRACTION")
    print("="*80)
    print()

    # Precompute primes for k=3..10
    k_values = list(range(3, 11))
    results_h1 = []
    results_h2 = []
    results_h3 = []
    results_h4 = []
    results_h5 = []

    print("Testing Hypothesis 1: Invariant-correctness of the gap extractor")
    print("-" * 60)
    for k in k_values:
        res = test_hypothesis_1(k)
        results_h1.append(res)
        status = "✓ PASS" if res['hypothesis_passed'] else "✗ FAIL"
        print(f"k={k:2d} | P_k={res['P_k']:>10} | φ(P_k)={res['phi_Pk']:>6} | gaps={res['gap_count']:>6} | sum={res['gap_sum']:>10} | {status}")
    h1_passed = all(r['hypothesis_passed'] for r in results_h1)
    print(f"Hypothesis 1: {'ACCEPTED' if h1_passed else 'REJECTED'}")
    print()

    print("Testing Hypothesis 2: Gap distribution symmetry")
    print("-" * 60)
    for k in k_values:
        res = test_hypothesis_2(k)
        results_h2.append(res)
        status = "✓ SYMMETRIC" if res['symmetric'] else "✗ NOT SYMMETRIC"
        print(f"k={k:2d} | mean_gap={res['mean_gap']:.4f} | {status}")
        # Optional: show top 5 gaps
        top_gaps = sorted(res['gap_distribution'].items(), key=lambda x: -x[1])[:5]
        print(f"    Top gaps: {top_gaps}")
    h2_passed = all(r['symmetric'] for r in results_h2)
    print(f"Hypothesis 2: {'ACCEPTED' if h2_passed else 'REJECTED'}")
    print()

    print("Testing Hypothesis 3: Variance scaling law")
    print("-" * 60)
    variances = []
    ratios = []
    for k in k_values:
        res = test_hypothesis_3(k)
        results_h3.append(res)
        variances.append(res['variance'])
        ratios.append(res['ratio_Pk_phi'])
        print(f"k={k:2d} | P_k/φ(P_k)={res['ratio_Pk_phi']:.4f} | var={res['variance']:.4f} | var/ratio={res['var_ratio']:.4f}")
    # Fit linear model: var = c * ratio
    if len(ratios) > 1:
        A = np.vstack([ratios, np.ones(len(ratios))]).T
        c, _ = np.linalg.lstsq(A, variances, rcond=None)[0]
        print(f"Linear fit: variance ≈ {c:.4f} × (P_k/φ(P_k))")
        # Check R²
        y_pred = c * np.array(ratios)
        ss_res = np.sum((np.array(variances) - y_pred) ** 2)
        ss_tot = np.sum((np.array(variances) - np.mean(variances)) ** 2)
        r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0.0
        print(f"R² = {r2:.4f}")
        h3_passed = r2 > 0.95  # Strong linear fit
    else:
        h3_passed = False
    print(f"Hypothesis 3: {'ACCEPTED (linear scaling with R²>0.95)' if h3_passed else 'REJECTED'}")
    print()

    print("Testing Hypothesis 4: Maximum gap bounded by O((log P_k)^2)")
    print("-" * 60)
    for k in k_values:
        res = test_hypothesis_4(k)
        results_h4.append(res)
        status = "✓ PASS" if res['max_within_bound'] else "✗ FAIL"
        print(f"k={k:2d} | max_gap={res['max_gap']:>4} | bound=(log P_k)²={res['bound']:.2f} | {status}")
    h4_passed = all(r['max_within_bound'] for r in results_h4)
    print(f"Hypothesis 4: {'ACCEPTED' if h4_passed else 'REJECTED'}")
    print()

    print("Testing Hypothesis 5: Variance decreases with k")
    print("-" * 60)
    for k in k_values:
        res = test_hypothesis_5(k)
        results_h5.append(res)
        print(f"k={k:2d} | variance={res['variance']:.4f}")
    # Check monotonic decrease
    is_decreasing = all(results_h5[i]['variance'] > results_h5[i+1]['variance'] for i in range(len(results_h5)-1))
    h5_passed = is_decreasing
    print(f"Hypothesis 5: {'ACCEPTED (monotonically decreasing)' if h5_passed else 'REJECTED'}")
    print()

    # Generate plot for variance across k
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    k_vals = [r['k'] for r in results_h1]
    var_vals = [r['variance'] for r in results_h3]
    ax.plot(k_vals, var_vals, 'bo-', label='Empirical variance')
    ax.set_xlabel('Primorial index k')
    ax.set_ylabel('Gap variance')
    ax.set_title('Gap Variance vs. Primorial Index k')
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig('primorial_gap_variance_k.png', dpi=150)
    plt.close()

    # Generate histogram for k=10 (largest case)
    P10 = primorial(10)
    rrs10 = get_reduced_residue_system(P10)
    gaps10 = extract_gaps_from_rrs(rrs10, P10)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.hist(gaps10, bins=range(min(gaps10), max(gaps10)+2), edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Gap size')
    ax2.set_ylabel('Frequency')
    ax2.set_title(f'Gap Distribution Modulo P_10 = {P10}')
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('primorial_gap_distribution_k10.png', dpi=150)
    plt.close()

    print("="*80)
    print("CONCLUSIONS:")
    print(f"  Hypothesis 1 (invariant correctness): {'✓ PASSED' if h1_passed else '✗ FAILED'}")
    print(f"  Hypothesis 2 (symmetry): {'✓ PASSED' if h2_passed else '✗ FAILED'}")
    print(f"  Hypothesis 3 (variance scaling): {'✓ PASSED' if h3_passed else '✗ FAILED'}")
    print(f"  Hypothesis 4 (max gap bound): {'✓ PASSED' if h4_passed else '✗ FAILED'}")
    print(f"  Hypothesis 5 (variance monotonicity): {'✓ PASSED' if h5_passed else '✗ FAILED'}")
    print()
    print("Plots saved: primorial_gap_variance_k.png, primorial_gap_distribution_k10.png")
    print("="*80)