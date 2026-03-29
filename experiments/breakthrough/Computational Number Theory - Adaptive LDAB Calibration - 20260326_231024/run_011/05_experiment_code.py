import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from math import gcd, isqrt
from collections import Counter

def primes_up_to(n):
    """Return list of primes up to n using sieve."""
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            sieve[p*p:n+1:p] = b"\x00" * ((n - p*p)//p + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def primorial(k):
    """Return k-th primorial P_k = product of first k primes."""
    primes = primes_up_to(50)  # enough for k up to 7
    if k < 1 or k > len(primes):
        raise ValueError(f"k must be between 1 and {len(primes)}")
    P = 1
    for i in range(k):
        P *= primes[i]
    return P, primes[:k]

def totient_primorial(k):
    """Return φ(P_k) for primorial P_k."""
    primes = primes_up_to(50)
    if k < 1 or k > len(primes):
        raise ValueError(f"k must be between 1 and {len(primes)}")
    phi = 1
    for i in range(k):
        phi *= (primes[i] - 1)
    return phi

def get_reduced_residue_system(P):
    """
    Return sorted list of integers in [1, P] coprime to P.
    Uses segmented approach for large P to avoid memory issues.
    """
    # For small P (k <= 7, P <= 510510), direct computation is fine
    residues = []
    for a in range(1, P + 1):
        if gcd(a, P) == 1:
            residues.append(a)
    return np.array(residues, dtype=np.int64)

def compute_gaps(residues, P):
    """Compute gaps between consecutive residues, including wrap-around."""
    if len(residues) < 2:
        return np.array([], dtype=np.int64)
    n = len(residues)
    gaps = np.diff(residues)
    last_gap = residues[0] + (P - residues[-1])
    return np.append(gaps, last_gap)

def test_hypothesis_1():
    """
    Hypothesis 1: Var(gap) ~ (P_k / φ(P_k))^2, with Var / (P_k/φ(P_k))^2 → 1 as k increases.
    """
    print("=== Testing Hypothesis 1: Variance scales as square of mean gap ===")
    
    results = []
    for k in range(3, 8):  # k = 3 to 7
        P, primes = primorial(k)
        phi_P = totient_primorial(k)
        
        # Compute reduced residue system
        residues = get_reduced_residue_system(P)
        n = len(residues)
        
        # Compute gaps
        gaps = compute_gaps(residues, P)
        
        # Compute mean and variance
        mean_gap = np.mean(gaps)
        var_gap = np.var(gaps, ddof=0)  # population variance
        
        # Theoretical prediction: mean = P / φ(P), variance = (P / φ(P))^2
        theoretical_mean = P / phi_P
        theoretical_var = theoretical_mean ** 2
        
        # Ratio
        var_ratio = var_gap / theoretical_var if theoretical_var != 0 else np.nan
        
        results.append({
            'k': k,
            'P': P,
            'phi_P': phi_P,
            'mean_gap': mean_gap,
            'theoretical_mean': theoretical_mean,
            'var_gap': var_gap,
            'theoretical_var': theoretical_var,
            'var_ratio': var_ratio,
            'n_gaps': n
        })
        
        print(f"k={k}: P={P}, φ(P)={phi_P}")
        print(f"  Mean gap: {mean_gap:.6f} (theory: {theoretical_mean:.6f})")
        print(f"  Variance: {var_gap:.6f} (theory: {theoretical_var:.6f})")
        print(f"  Var / (mean)^2 = {var_ratio:.6f}")
        print()
    
    # Check trend
    ratios = [r['var_ratio'] for r in results]
    print(f"Variance-to-mean² ratios for k=3..7: {ratios}")
    print(f"Mean ratio: {np.mean(ratios):.6f}, Std: {np.std(ratios):.6f}")
    
    # Check if ratio approaches 1
    if abs(ratios[-1] - 1.0) < 0.05:
        print("✓ Hypothesis 1 SUPPORTED: Ratio is close to 1 for largest k")
    else:
        print("✗ Hypothesis 1 NOT SUPPORTED: Ratio deviates significantly from 1")
    
    return results

def test_hypothesis_2():
    """
    Hypothesis 2: The distribution of gaps is approximately geometric with parameter p = φ(P)/P.
    Equivalently, gaps follow P(g) ≈ p (1-p)^{g-1} for g = 1,2,3,...
    We test via empirical mean and variance: for geometric, Var = (1-p)/p² = mean² - mean.
    So check if var ≈ mean² - mean.
    """
    print("=== Testing Hypothesis 2: Gap distribution is geometric ===")
    
    results = []
    for k in range(3, 8):
        P, _ = primorial(k)
        phi_P = totient_primorial(k)
        residues = get_reduced_residue_system(P)
        gaps = compute_gaps(residues, P)
        
        mean_gap = np.mean(gaps)
        var_gap = np.var(gaps, ddof=0)
        
        # For geometric (starting at 1): Var = mean² - mean
        geometric_var = mean_gap**2 - mean_gap
        diff = var_gap - geometric_var
        rel_error = abs(diff) / geometric_var if geometric_var > 0 else np.nan
        
        results.append({
            'k': k,
            'mean': mean_gap,
            'var': var_gap,
            'geom_var': geometric_var,
            'rel_error': rel_error
        })
        
        print(f"k={k}: mean={mean_gap:.4f}, var={var_gap:.4f}, geom_var={geometric_var:.4f}")
        print(f"  Relative error: {rel_error*100:.2f}%")
    
    print()
    avg_rel_error = np.mean([r['rel_error'] for r in results])
    if avg_rel_error < 0.05:
        print("✓ Hypothesis 2 SUPPORTED: Gap distribution closely matches geometric")
    else:
        print(f"✗ Hypothesis 2 NOT STRONGLY SUPPORTED: Avg rel error = {avg_rel_error*100:.1f}%")
    
    return results

def test_hypothesis_3():
    """
    Hypothesis 3: The variance-to-mean ratio (CMF) approaches 1 as k→∞.
    For geometric: Var/Mean = Mean - 1 → ∞, so CMF = (Mean - 1) → ∞.
    But for primorial gaps, mean grows like P/φ(P) ~ log log P, so CMF should grow slowly.
    Actually: CMF = Var/Mean = (mean²)/mean = mean → ∞.
    So we test: Var/Mean / mean → 1 (i.e., Var/Mean² → 1).
    This is same as Hypothesis 1, but we rephrase to confirm consistency.
    """
    print("=== Testing Hypothesis 3: Variance-to-mean ratio scaling ===")
    
    results = []
    for k in range(3, 8):
        P, _ = primorial(k)
        phi_P = totient_primorial(k)
        residues = get_reduced_residue_system(P)
        gaps = compute_gaps(residues, P)
        
        mean_gap = np.mean(gaps)
        var_gap = np.var(gaps, ddof=0)
        
        # CMF = Var / Mean
        cmf = var_gap / mean_gap if mean_gap > 0 else np.nan
        # Expected: CMF ≈ mean - 1 (geometric), so CMF / mean ≈ 1 - 1/mean
        ratio_to_mean = cmf / mean_gap if mean_gap > 0 else np.nan
        
        results.append({
            'k': k,
            'mean': mean_gap,
            'var': var_gap,
            'cmf': cmf,
            'cmf_over_mean': ratio_to_mean
        })
        
        print(f"k={k}: mean={mean_gap:.2f}, var={var_gap:.2f}, CMF={cmf:.2f}")
        print(f"  CMF/mean = {ratio_to_mean:.6f} (should approach 1)")
    
    print()
    ratios = [r['cmf_over_mean'] for r in results]
    print(f"CMF/mean ratios: {ratios}")
    if all(abs(r - 1.0) < 0.05 for r in ratios):
        print("✓ Hypothesis 3 SUPPORTED: CMF/mean → 1")
    else:
        print("✗ Hypothesis 3 NOT SUPPORTED: CMF/mean deviates from 1")
    
    return results

def plot_gap_distributions(results_h1):
    """Plot gap distributions for k=3 to 7."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()
    
    for idx, r in enumerate(results_h1):
        k = r['k']
        P = r['P']
        residues = get_reduced_residue_system(P)
        gaps = compute_gaps(residues, P)
        
        ax = axes[idx]
        
        # Plot histogram of gaps
        max_gap = int(max(gaps))
        gap_counts = Counter(gaps)
        gap_vals = sorted(gap_counts.keys())
        counts = [gap_counts[g] for g in gap_vals]
        
        ax.bar(gap_vals, counts, width=0.8, alpha=0.7, label='Empirical')
        
        # Overlay theoretical geometric: p = φ(P)/P
        phi_P = r['phi_P']
        p = phi_P / P
        theoretical_probs = [p * (1-p)**(g-1) * len(gaps) for g in gap_vals]
        ax.plot(gap_vals, theoretical_probs, 'r--', label='Geometric (p={:.3f})'.format(p))
        
        ax.set_xlabel('Gap size')
        ax.set_ylabel('Count')
        ax.set_title(f'Primorial Gap Distribution (k={k}, P={P})')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Hide extra subplot if any
    if len(results_h1) < len(axes):
        for i in range(len(results_h1), len(axes)):
            axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('primorial_gap_distributions.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved gap distribution plot: primorial_gap_distributions.png")

def main():
    print("="*70)
    print("PRIMORIAL GAP VARIANCE ANALYSIS (Artifact-Free Extraction)")
    print("="*70)
    print()
    
    # Run all hypothesis tests
    results_h1 = test_hypothesis_1()
    print()
    
    results_h2 = test_hypothesis_2()
    print()
    
    results_h3 = test_hypothesis_3()
    print()
    
    # Generate plots
    try:
        plot_gap_distributions(results_h1)
    except Exception as e:
        print(f"Warning: Plot generation failed: {e}")
    
    # Final summary
    print("="*70)
    print("CONCLUSIONS:")
    print("-"*70)
    
    # Hypothesis 1 evaluation
    ratios_h1 = [r['var_ratio'] for r in results_h1]
    h1_pass = all(abs(r - 1.0) < 0.1 for r in ratios_h1[-2:])  # last two k's
    print(f"Hypothesis 1 (Var ~ mean²): {'SUPPORTED' if h1_pass else 'NOT SUPPORTED'}")
    print(f"  Final ratio (k=7): {ratios_h1[-1]:.6f} (target: 1.0)")
    
    # Hypothesis 2 evaluation
    avg_rel_err_h2 = np.mean([r['rel_error'] for r in results_h2])
    h2_pass = avg_rel_err_h2 < 0.1
    print(f"Hypothesis 2 (Geometric gaps): {'SUPPORTED' if h2_pass else 'NOT SUPPORTED'}")
    print(f"  Avg relative error: {avg_rel_err_h2*100:.2f}%")
    
    # Hypothesis 3 evaluation
    ratios_h3 = [r['cmf_over_mean'] for r in results_h3]
    h3_pass = all(abs(r - 1.0) < 0.1 for r in ratios_h3[-2:])
    print(f"Hypothesis 3 (CMF scaling): {'SUPPORTED' if h3_pass else 'NOT SUPPORTED'}")
    print(f"  Final CMF/mean (k=7): {ratios_h3[-1]:.6f} (target: 1.0)")
    
    print()
    if h1_pass and h2_pass and h3_pass:
        print("OVERALL: All hypotheses supported — artifact-free extraction validates theoretical predictions.")
    else:
        print("OVERALL: Some hypotheses not fully supported — further analysis needed.")
    
    print("="*70)

if __name__ == "__main__":
    main()