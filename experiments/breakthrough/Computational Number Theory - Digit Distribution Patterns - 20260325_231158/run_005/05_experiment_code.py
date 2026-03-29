import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import math
import sys
from collections import Counter

# =============================================================================
# CONFIGURATION
# =============================================================================

MAX_PRIME = 10_000_000  # Upper bound for prime generation
SEGMENT_SIZE = 100_000  # For segmented sieve
BASES = [210, 2310]  # Primorial bases: 2*3*5*7 and 2*3*5*7*11
PREFIX_LENGTHS = [1, 2, 3]  # Leading digit lengths to test
P_VALUE_THRESHOLD = 0.01

# =============================================================================
# PRIME GENERATION (Segmented Sieve)
# =============================================================================

def simple_sieve(limit):
    """Generate primes up to limit using simple sieve."""
    if limit < 2:
        return np.array([], dtype=np.int64)
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i:limit+1:i] = False
    return np.nonzero(sieve)[0].astype(np.int64)

def segmented_sieve(n):
    """Generate all primes up to n using segmented sieve for memory efficiency."""
    if n < 2:
        return np.array([], dtype=np.int64)
    
    limit = int(n**0.5) + 1
    base_primes = simple_sieve(limit)
    primes = list(base_primes)
    
    low = limit
    high = min(low + SEGMENT_SIZE, n + 1)
    
    while low <= n:
        sieve = np.ones(high - low, dtype=bool)
        
        for p in base_primes:
            start = ((low + p - 1) // p) * p
            sieve[start - low:high - low:p] = False
        
        new_primes = np.nonzero(sieve)[0] + low
        primes.extend(new_primes)
        
        low = high
        high = min(low + SEGMENT_SIZE, n + 1)
    
    return np.array(primes, dtype=np.int64)

# =============================================================================
# BASE CONVERSION
# =============================================================================

def to_primorial_base(n, base):
    """Convert n to primorial base representation (list of digits, MSB first)."""
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return digits[::-1]  # MSB first

def get_leading_digits(n, base, length):
    """Get the first 'length' digits of n in the given base."""
    digits = to_primorial_base(n, base)
    if len(digits) < length:
        return None  # Number too short
    return tuple(digits[:length])

# =============================================================================
# STATISTICAL TESTS
# =============================================================================

def chi_square_test(observed, expected=None):
    """
    Perform chi-squared goodness-of-fit test.
    If expected is None, assumes uniform distribution.
    """
    observed = np.array(observed, dtype=float)
    observed = observed[observed > 0]  # Remove zeros for valid test
    
    if len(observed) < 2:
        return np.nan, np.nan, "Insufficient categories"
    
    if expected is None:
        expected = np.full(len(observed), observed.sum() / len(observed))
    else:
        expected = np.array(expected, dtype=float)
        expected = expected * (observed.sum() / expected.sum())
    
    # Ensure expected values are reasonable
    if np.any(expected < 1):
        # Merge small categories or use caution
        mask = expected >= 0.5
        if mask.sum() < 2:
            return np.nan, np.nan, "Expected frequencies too small"
        observed = observed[mask]
        expected = expected[mask]
    
    chi2, p_value = stats.chisquare(observed, expected)
    return chi2, p_value, "OK"

def kl_divergence(observed, expected=None):
    """Calculate KL divergence from uniform distribution."""
    observed = np.array(observed, dtype=float)
    observed = observed / observed.sum()
    
    if expected is None:
        expected = np.full(len(observed), 1.0 / len(observed))
    else:
        expected = np.array(expected, dtype=float)
        expected = expected / expected.sum()
    
    # Avoid log(0)
    mask = observed > 1e-10
    kl = np.sum(observed[mask] * np.log(observed[mask] / expected[mask]))
    return kl

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_leading_digits(primes, base, prefix_length):
    """Analyze leading digit distribution for given base and prefix length."""
    # Count frequencies
    counts = Counter()
    valid_primes = 0
    
    for p in primes:
        prefix = get_leading_digits(p, base, prefix_length)
        if prefix is not None:
            counts[prefix] += 1
            valid_primes += 1
    
    if valid_primes == 0:
        return None
    
    # Calculate expected uniform frequency
    num_symbols = base ** prefix_length
    # But not all prefixes are equally likely due to number size distribution
    # For proper comparison, we use the observed distribution vs uniform hypothesis
    
    frequencies = list(counts.values())
    num_categories = len(frequencies)
    
    # Chi-squared test against uniform
    chi2, p_value, status = chi_square_test(frequencies)
    
    # KL divergence from uniform
    kl = kl_divergence(frequencies)
    
    # Effect size (Cramer's V)
    if chi2 == chi2 and num_categories > 1 and valid_primes > 0:  # not NaN
        val = chi2 / (float(valid_primes) * (num_categories - 1))
        cramers_v = np.sqrt(max(0.0, val))
    else:
        cramers_v = np.nan
    
    return {
        'base': base,
        'prefix_length': prefix_length,
        'valid_primes': valid_primes,
        'num_categories': num_categories,
        'frequencies': frequencies,
        'chi2': chi2,
        'p_value': p_value,
        'kl_divergence': kl,
        'cramers_v': cramers_v,
        'status': status,
        'counts': counts
    }

def create_visualization(results_by_base, filename='primorial_analysis.png'):
    """Create visualization of leading digit distributions."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Leading Digit Distributions in Primorial Bases', fontsize=14)
    
    colors = ['#1f77b4', '#ff7f0e']
    
    for idx, (base, results) in enumerate(results_by_base.items()):
        # Plot 1: Chi-squared statistics by prefix length
        ax1 = axes[idx, 0]
        lengths = [r['prefix_length'] for r in results]
        chi2_vals = [r['chi2'] if r['chi2'] == r['chi2'] else 0 for r in results]
        ax1.bar(lengths, chi2_vals, color=colors[idx], alpha=0.7)
        ax1.set_xlabel('Prefix Length')
        ax1.set_ylabel('Chi-Squared Statistic')
        ax1.set_title(f'Base-{base}: Chi-Squared by Prefix Length')
        
        # Plot 2: P-values (log scale)
        ax2 = axes[idx, 1]
        p_vals = [max(r['p_value'], 1e-300) if r['p_value'] == r['p_value'] else 1 for r in results]
        ax2.bar(lengths, -np.log10(p_vals), color=colors[idx], alpha=0.7)
        ax2.axhline(-np.log10(P_VALUE_THRESHOLD), color='r', linestyle='--', label=f'p={P_VALUE_THRESHOLD}')
        ax2.set_xlabel('Prefix Length')
        ax2.set_ylabel('-log10(p-value)')
        ax2.set_title(f'Base-{base}: Significance by Prefix Length')
        ax2.legend()
        
        # Plot 3: KL Divergence
        ax3 = axes[idx, 2]
        kl_vals = [r['kl_divergence'] for r in results]
        ax3.bar(lengths, kl_vals, color=colors[idx], alpha=0.7)
        ax3.set_xlabel('Prefix Length')
        ax3.set_ylabel('KL Divergence (bits)')
        ax3.set_title(f'Base-{base}: KL Divergence by Prefix Length')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\n[Visualization saved to {filename}]")
    plt.close()

def print_distribution_sample(counts, base, prefix_length, max_display=10):
    """Print sample of the distribution."""
    print(f"\n  Top prefixes (Base-{base}, length-{prefix_length}):")
    sorted_items = sorted(counts.items(), key=lambda x: -x[1])[:max_display]
    for prefix, count in sorted_items:
        prefix_str = ' '.join(str(d) for d in prefix)
        print(f"    {prefix_str}: {count}")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 80)
    print("RESEARCH ANALYSIS: Prefix N-Gram Biases in High-Order Primorial Bases")
    print("=" * 80)
    
    # Generate primes
    print(f"\n[1] Generating primes up to {MAX_PRIME:,}...")
    primes = segmented_sieve(MAX_PRIME)
    print(f"    Found {len(primes):,} primes")
    
    # Filter to meaningful range (exclude very small primes)
    meaningful_primes = primes[primes > 100]  # Need enough digits in high bases
    print(f"    Using {len(meaningful_primes):,} primes > 100 for analysis")
    
    # Store results
    all_results = {}
    
    # Test each base
    for base in BASES:
        print(f"\n{'='*60}")
        print(f"HYPOTHESIS 1 TEST: Base-{base} Leading Digit Distributions")
        print(f"{'='*60}")
        
        base_results = []
        
        for length in PREFIX_LENGTHS:
            print(f"\n  Prefix length: {length}")
            result = analyze_leading_digits(meaningful_primes, base, length)
            
            if result is None:
                print(f"    ERROR: No valid primes with {length} digits in base-{base}")
                continue
            
            base_results.append(result)
            
            # Print statistics
            print(f"    Valid primes analyzed: {result['valid_primes']:,}")
            print(f"    Number of categories: {result['num_categories']}")
            print(f"    Chi-squared: {result['chi2']:.4f}" if result['chi2'] == result['chi2'] else "    Chi-squared: N/A")
            print(f"    p-value: {result['p_value']:.2e}" if result['p_value'] == result['p_value'] else "    p-value: N/A")
            print(f"    KL divergence: {result['kl_divergence']:.6f}")
            print(f"    Cramer's V (effect size): {result['cramers_v']:.4f}" if result['cramers_v'] == result['cramers_v'] else "    Cramer's V: N/A")
            
            # Significance test
            if result['p_value'] == result['p_value']:
                if result['p_value'] < P_VALUE_THRESHOLD:
                    print(f"    *** SIGNIFICANT DEVIATION FROM UNIFORM (p < {P_VALUE_THRESHOLD}) ***")
                else:
                    print(f"    No significant deviation (p >= {P_VALUE_THRESHOLD})")
            
            # Show sample distribution
            if result['counts']:
                print_distribution_sample(result['counts'], base, length, 8)
        
        all_results[base] = base_results
    
    # Create visualization
    print(f"\n[2] Creating visualization...")
    create_visualization(all_results)
    
    # Additional analysis: Compare with power-of-two base as reference
    print(f"\n{'='*60}")
    print("COMPARISON: Base-32 (Power-of-Two) Reference")
    print(f"{'='*60}")
    
    ref_results = []
    for length in PREFIX_LENGTHS:
        result = analyze_leading_digits(meaningful_primes, 32, length)
        if result:
            ref_results.append(result)
            print(f"\n  Base-32, length-{length}:")
            print(f"    KL divergence: {result['kl_divergence']:.6f}")
            print(f"    p-value: {result['p_value']:.2e}" if result['p_value'] == result['p_value'] else "    p-value: N/A")
    
    # =============================================================================
    # CONCLUSIONS
    # =============================================================================
    
    print("\n" + "=" * 80)
    print("CONCLUSIONS")
    print("=" * 80)
    
    # Summarize findings for each base
    significant_findings = []
    
    for base in BASES:
        print(f"\nBase-{base} (Primorial):")
        for r in all_results[base]:
            length = r['prefix_length']
            kl = r['kl_divergence']
            p = r['p_value']
            
            if p == p and p < P_VALUE_THRESHOLD:
                sig = "SIGNIFICANT"
                significant_findings.append((base, length, kl, p))
            else:
                sig = "not significant"
            
            print(f"  Length-{length}: KL={kl:.6f}, p={p:.2e if p==p else 'N/A'} ({sig})")
    
    # Compare with Base-32
    print(f"\nBase-32 (Power-of-Two) Reference:")
    for r in ref_results:
        print(f"  Length-{r['prefix_length']}: KL={r['kl_divergence']:.6f}")
    
    # Overall conclusion
    print(f"\n{'='*60}")
    print("HYPOTHESIS 1 ASSESSMENT:")
    print(f"{'='*60}")
    
    if significant_findings:
        print("SUPPORTED: Statistically significant deviations from uniform distribution")
        print(f"  Found in {len(significant_findings)} base/length combinations:")
        for base, length, kl, p in significant_findings:
            print(f"    - Base-{base}, length-{length}: p={p:.2e}, KL={kl:.6f}")
    else:
        print("NOT SUPPORTED: No statistically significant deviations found")
    
    # Compare primorial vs power-of-two
    print(f"\n{'='*60}")
    print("PRIMORIAL vs POWER-OF-TWO COMPARISON:")
    print(f"{'='*60}")
    
    primorial_kl = np.mean([r['kl_divergence'] for base in BASES for r in all_results[base]])
    power2_kl = np.mean([r['kl_divergence'] for r in ref_results]) if ref_results else 0
    
    print(f"  Average KL divergence (Primorial bases): {primorial_kl:.6f}")
    print(f"  Average KL divergence (Base-32): {power2_kl:.6f}")
    
    if primorial_kl > power2_kl:
        print(f"  → Primorial bases show HIGHER structural bias than Base-32")
    else:
        print(f"  → Primorial bases show LOWER or comparable structural bias to Base-32")
    
    print(f"\n{'='*60}")
    print("FINAL CONCLUSION:")
    print(f"{'='*60}")
    
    # Determine if hypothesis is supported
    any_significant = len(significant_findings) > 0
    primorial_stronger = primorial_kl > power2_kl * 1.5  # 50% higher threshold
    
    if any_significant:
        conclusion = (
            f"HYPOTHESIS 1 is SUPPORTED. High-order primorial bases (Base-210, Base-2310) "
            f"exhibit statistically significant non-uniform leading digit distributions "
            f"(p < {P_VALUE_THRESHOLD}). The KL divergence values indicate {'pronounced' if primorial_kl > 0.01 else 'moderate'} "
            f"structural biases in these representations."
        )
    else:
        conclusion = (
            f"HYPOTHESIS 1 is NOT SUPPORTED. Despite theoretical expectations, "
            f"no statistically significant deviations from uniform distribution were detected "
            f"in the leading digit patterns of primes in Base-210 or Base-2310."
        )
    
    print(conclusion)
    
    # Additional insight
    print(f"\nADDITIONAL INSIGHT:")
    if primorial_stronger and any_significant:
        print("  The high-order primorial bases DO show stronger structural biases than")
        print("  power-of-two bases, contrary to the lower-order primorial findings.")
        print("  This suggests the primorial structure becomes more influential at higher orders.")
    elif not primorial_stronger:
        print("  Power-of-two bases remain competitive or superior in revealing")
        print("  positional n-gram biases, even when compared to high-order primorials.")
        print("  This may indicate that the primorial structure's theoretical advantages")
        print("  are offset by practical sampling limitations or deeper number-theoretic")
        print("  properties not captured by simple digit analysis.")
    
    print(f"\n{'='*80}")
    print("END OF ANALYSIS")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()