import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import sys
import math

# Set recursion limit for safety
sys.setrecursionlimit(10000)

def segmented_sieve(limit):
    """Efficient segmented sieve to find all primes up to limit."""
    if limit < 2:
        return np.array([], dtype=np.int64)
    
    # Small sieve for base primes
    small_limit = int(np.sqrt(limit)) + 1
    small_sieve = np.ones(small_limit, dtype=bool)
    small_sieve[0:2] = False
    for i in range(2, int(np.sqrt(small_limit)) + 1):
        if small_sieve[i]:
            small_sieve[i*i::i] = False
    base_primes = np.where(small_sieve)[0].astype(np.int64)
    
    # Segmented sieve
    segment_size = max(small_limit, 32768)
    primes = list(base_primes[base_primes <= limit])
    
    for low in range(small_limit, limit + 1, segment_size):
        high = min(low + segment_size - 1, limit)
        segment = np.ones(high - low + 1, dtype=bool)
        
        for p in base_primes:
            if p * p > high:
                break
            start = max(p * p, ((low + p - 1) // p) * p)
            segment[start - low::p] = False
        
        new_primes = np.where(segment)[0] + low
        primes.extend(new_primes)
    
    return np.array(primes, dtype=np.int64)

def to_base(n, base):
    """Convert integer to digit list in given base (most significant first)."""
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return digits[::-1]

def get_ngrams(digits, n):
    """Extract all n-grams from digit sequence as tuples."""
    if len(digits) < n:
        return []
    return [tuple(digits[i:i+n]) for i in range(len(digits) - n + 1)]

def compute_kl_divergence(p_dist, q_dist, epsilon=1e-10):
    """Compute KL divergence D_KL(P || Q)."""
    # Normalize distributions
    p_total = sum(p_dist.values())
    q_total = sum(q_dist.values())
    
    if p_total == 0 or q_total == 0:
        return float('inf')
    
    # Create unified key set
    all_keys = set(p_dist.keys()) | set(q_dist.keys())
    
    kl = 0.0
    for key in all_keys:
        p_val = (p_dist.get(key, 0) + epsilon) / (p_total + epsilon * len(all_keys))
        q_val = (q_dist.get(key, 0) + epsilon) / (q_total + epsilon * len(all_keys))
        kl += p_val * np.log(p_val / q_val)
    
    return kl

def get_gap_ngrams(primes, base, ngram_size):
    """Get n-gram distribution of prime gaps in given base."""
    if len(primes) < 2:
        return Counter()
    
    gaps = primes[1:] - primes[:-1]
    all_ngrams = []
    
    for gap in gaps:
        digits = to_base(int(gap), base)
        ngrams = get_ngrams(digits, ngram_size)
        all_ngrams.extend(ngrams)
    
    return Counter(all_ngrams)

def get_composite_gaps(limit, base, ngram_size):
    """Generate composite gap n-grams (gaps between consecutive composites)."""
    # Find composites in range
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    
    composites = np.where(~sieve)[0]
    composites = composites[composites >= 4]  # Start from first composite gap
    
    if len(composites) < 2:
        return Counter()
    
    gaps = composites[1:] - composites[:-1]
    all_ngrams = []
    
    for gap in gaps:
        digits = to_base(int(gap), base)
        ngrams = get_ngrams(digits, ngram_size)
        all_ngrams.extend(ngrams)
    
    return Counter(all_ngrams)

def get_positional_ngrams(primes, base, ngram_size, position_type):
    """
    Get n-grams from specific positions of prime representations.
    position_type: 'prefix' (first n digits) or 'internal' (middle segment)
    """
    all_ngrams = []
    
    for p in primes:
        digits = to_base(int(p), base)
        if len(digits) < ngram_size:
            continue
            
        if position_type == 'prefix':
            # Take first ngram_size digits
            ngram = tuple(digits[:ngram_size])
            all_ngrams.append(ngram)
        elif position_type == 'internal':
            # Take middle segment (excluding first and last digit)
            if len(digits) < ngram_size + 2:
                continue
            start = (len(digits) - ngram_size) // 2
            ngram = tuple(digits[start:start + ngram_size])
            all_ngrams.append(ngram)
    
    return Counter(all_ngrams)

def get_composite_positional_ngrams(limit, base, ngram_size, position_type):
    """Get positional n-grams for composite numbers."""
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    
    composites = np.where(~sieve)[0]
    composites = composites[composites >= 4]
    
    all_ngrams = []
    
    for c in composites:
        digits = to_base(int(c), base)
        if len(digits) < ngram_size:
            continue
            
        if position_type == 'prefix':
            ngram = tuple(digits[:ngram_size])
            all_ngrams.append(ngram)
        elif position_type == 'internal':
            if len(digits) < ngram_size + 2:
                continue
            start = (len(digits) - ngram_size) // 2
            ngram = tuple(digits[start:start + ngram_size])
            all_ngrams.append(ngram)
    
    return Counter(all_ngrams)

def hypothesis_1_test(limit=500000, ngram_size=2):
    """
    Hypothesis 1: Inter-Prime Gap N-grams Show Greater KL Divergence 
    from Composite Gaps in Base-16 than in Base-10
    """
    print("=" * 70)
    print("HYPOTHESIS 1: Inter-Prime Gap N-grams - Base-16 vs Base-10 KL Divergence")
    print("=" * 70)
    
    print(f"Computing primes up to {limit}...")
    primes = segmented_sieve(limit)
    print(f"Found {len(primes)} primes")
    
    # Base-10 analysis
    print("\n--- Base-10 Analysis ---")
    prime_gap_ngrams_10 = get_gap_ngrams(primes, 10, ngram_size)
    composite_gap_ngrams_10 = get_composite_gaps(limit, 10, ngram_size)
    kl_10 = compute_kl_divergence(prime_gap_ngrams_10, composite_gap_ngrams_10)
    print(f"Prime gap n-grams (Base-10): {len(prime_gap_ngrams_10)} unique")
    print(f"Composite gap n-grams (Base-10): {len(composite_gap_ngrams_10)} unique")
    print(f"KL divergence (Base-10): {kl_10:.6f}")
    
    # Base-16 analysis
    print("\n--- Base-16 Analysis ---")
    prime_gap_ngrams_16 = get_gap_ngrams(primes, 16, ngram_size)
    composite_gap_ngrams_16 = get_composite_gaps(limit, 16, ngram_size)
    kl_16 = compute_kl_divergence(prime_gap_ngrams_16, composite_gap_ngrams_16)
    print(f"Prime gap n-grams (Base-16): {len(prime_gap_ngrams_16)} unique")
    print(f"Composite gap n-grams (Base-16): {len(composite_gap_ngrams_16)} unique")
    print(f"KL divergence (Base-16): {kl_16:.6f}")
    
    # Test hypothesis
    print(f"\n--- Hypothesis Test ---")
    print(f"Threshold: 0.05")
    print(f"Base-10 KL < 0.05: {kl_10 < 0.05} (value: {kl_10:.6f})")
    print(f"Base-16 KL > 0.05: {kl_16 > 0.05} (value: {kl_16:.6f})")
    print(f"Base-16 > Base-10: {kl_16 > kl_10}")
    
    hypothesis_supported = (kl_10 < 0.05) and (kl_16 > 0.05) and (kl_16 > kl_10)
    print(f"\nHYPOTHESIS 1 SUPPORTED: {hypothesis_supported}")
    
    return {
        'kl_10': kl_10,
        'kl_16': kl_16,
        'supported': hypothesis_supported
    }

def hypothesis_2_test(limit=500000, ngram_size=2):
    """
    Hypothesis 2: Prefix N-grams of Primes vs Composites Show Greater 
    Divergence in Higher Bases (Base-32 vs Base-8)
    """
    print("\n" + "=" * 70)
    print("HYPOTHESIS 2: Prefix N-grams - Base-32 vs Base-8 KL Divergence")
    print("=" * 70)
    
    print(f"Computing primes up to {limit}...")
    primes = segmented_sieve(limit)
    
    # Base-8 analysis
    print("\n--- Base-8 Prefix Analysis ---")
    prime_prefix_8 = get_positional_ngrams(primes, 8, ngram_size, 'prefix')
    composite_prefix_8 = get_composite_positional_ngrams(limit, 8, ngram_size, 'prefix')
    kl_8 = compute_kl_divergence(prime_prefix_8, composite_prefix_8)
    print(f"KL divergence (Base-8): {kl_8:.6f}")
    
    # Base-32 analysis
    print("\n--- Base-32 Prefix Analysis ---")
    prime_prefix_32 = get_positional_ngrams(primes, 32, ngram_size, 'prefix')
    composite_prefix_32 = get_composite_positional_ngrams(limit, 32, ngram_size, 'prefix')
    kl_32 = compute_kl_divergence(prime_prefix_32, composite_prefix_32)
    print(f"KL divergence (Base-32): {kl_32:.6f}")
    
    print(f"\n--- Hypothesis Test ---")
    print(f"Base-32 > Base-8: {kl_32 > kl_8}")
    ratio = kl_32 / kl_8 if kl_8 > 0 else float('inf')
    print(f"Ratio (Base-32 / Base-8): {ratio:.4f}")
    
    hypothesis_supported = kl_32 > kl_8
    print(f"\nHYPOTHESIS 2 SUPPORTED: {hypothesis_supported}")
    
    return {
        'kl_8': kl_8,
        'kl_32': kl_32,
        'supported': hypothesis_supported
    }

def hypothesis_3_test(limit=500000, ngram_size=2):
    """
    Hypothesis 3: Internal Positional N-grams Show Lower KL Divergence 
    than Prefix N-grams (Structural Randomness Hypothesis)
    """
    print("\n" + "=" * 70)
    print("HYPOTHESIS 3: Internal vs Prefix N-grams - Structural Randomness")
    print("=" * 70)
    
    print(f"Computing primes up to {limit}...")
    primes = segmented_sieve(limit)
    
    bases = [10, 16]
    results = {}
    
    for base in bases:
        print(f"\n--- Base-{base} Analysis ---")
        
        # Prefix n-grams
        prime_prefix = get_positional_ngrams(primes, base, ngram_size, 'prefix')
        composite_prefix = get_composite_positional_ngrams(limit, base, ngram_size, 'prefix')
        kl_prefix = compute_kl_divergence(prime_prefix, composite_prefix)
        
        # Internal n-grams
        prime_internal = get_positional_ngrams(primes, base, ngram_size, 'internal')
        composite_internal = get_composite_positional_ngrams(limit, base, ngram_size, 'internal')
        kl_internal = compute_kl_divergence(prime_internal, composite_internal)
        
        print(f"Prefix KL divergence: {kl_prefix:.6f}")
        print(f"Internal KL divergence: {kl_internal:.6f}")
        print(f"Internal < Prefix: {kl_internal < kl_prefix}")
        
        results[base] = {
            'prefix': kl_prefix,
            'internal': kl_internal,
            'ratio': kl_internal / kl_prefix if kl_prefix > 0 else float('inf')
        }
    
    # Overall test
    h3_supported = all(results[b]['internal'] < results[b]['prefix'] for b in bases)
    print(f"\n--- Hypothesis Test ---")
    print(f"Internal < Prefix in all bases: {h3_supported}")
    print(f"\nHYPOTHESIS 3 SUPPORTED: {h3_supported}")
    
    return {
        'results': results,
        'supported': h3_supported
    }

def hypothesis_4_test(limit=500000):
    """
    Hypothesis 4: First Digit Distribution of Prime Gaps Follows 
    Benford-like Law in Base-10 but Deviates in Base-16
    """
    print("\n" + "=" * 70)
    print("HYPOTHESIS 4: First Digit Distribution - Benford's Law Test")
    print("=" * 70)
    
    print(f"Computing primes up to {limit}...")
    primes = segmented_sieve(limit)
    gaps = primes[1:] - primes[:-1]
    
    def first_digit_dist(values, base):
        """Get distribution of first digits in given base."""
        counts = Counter()
        for v in values:
            if v <= 0:
                continue
            digits = to_base(int(v), base)
            counts[digits[0]] += 1
        total = sum(counts.values())
        return {k: v/total for k, v in counts.items()} if total > 0 else {}
    
    def chi_square_test(observed, expected_keys, base):
        """Simple chi-square test against uniform distribution."""
        total = sum(observed.values())
        if total == 0:
            return float('inf')
        
        # Expected under uniform distribution (excluding 0 for first digit)
        expected_prob = 1.0 / (base - 1)  # digits 1 to base-1
        
        chi_sq = 0.0
        for d in range(1, base):
            obs = observed.get(d, 0) * total
            exp = expected_prob * total
            if exp > 0:
                chi_sq += (obs - exp) ** 2 / exp
        
        return chi_sq
    
    # Benford's law expected for base-10: log10(1 + 1/d)
    benford_10 = {d: np.log10(1 + 1/d) for d in range(1, 10)}
    
    print("\n--- Base-10 First Digit Distribution ---")
    first_digits_10 = first_digit_dist(gaps, 10)
    for d in sorted(first_digits_10.keys()):
        print(f"  Digit {d}: {first_digits_10[d]:.4f} (Benford: {benford_10.get(d, 0):.4f})")
    
    chi_10 = chi_square_test(first_digits_10, range(1, 10), 10)
    print(f"Chi-square vs uniform: {chi_10:.4f}")
    
    # Check correlation with Benford
    benford_corr = np.corrcoef(
        [first_digits_10.get(d, 0) for d in range(1, 10)],
        [benford_10[d] for d in range(1, 10)]
    )[0, 1]
    print(f"Correlation with Benford's law: {benford_corr:.4f}")
    
    print("\n--- Base-16 First Digit Distribution ---")
    first_digits_16 = first_digit_dist(gaps, 16)
    for d in sorted(first_digits_16.keys()):
        print(f"  Digit {d}: {first_digits_16[d]:.4f}")
    
    chi_16 = chi_square_test(first_digits_16, range(1, 16), 16)
    print(f"Chi-square vs uniform: {chi_16:.4f}")
    
    # Benford for base-16
    benford_16 = {d: np.log(1 + 1/d) / np.log(16) for d in range(1, 16)}
    benford_corr_16 = np.corrcoef(
        [first_digits_16.get(d, 0) for d in range(1, 16)],
        [benford_16[d] for d in range(1, 16)]
    )[0, 1]
    print(f"Correlation with Benford's law (base-16): {benford_corr_16:.4f}")
    
    # Test: Base-10 follows Benford (high correlation), Base-16 deviates
    print(f"\n--- Hypothesis Test ---")
    print(f"Base-10 Benford correlation > 0.8: {benford_corr > 0.8}")
    print(f"Base-16 Benford correlation < Base-10: {benford_corr_16 < benford_corr}")
    
    hypothesis_supported = (benford_corr > 0.8) and (benford_corr_16 < benford_corr)
    print(f"\nHYPOTHESIS 4 SUPPORTED: {hypothesis_supported}")
    
    # Create visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Base-10 plot
    digits_10 = list(range(1, 10))
    obs_10 = [first_digits_10.get(d, 0) for d in digits_10]
    benf_10 = [benford_10[d] for d in digits_10]
    axes[0].bar(digits_10, obs_10, alpha=0.7, label='Observed')
    axes[0].plot(digits_10, benf_10, 'r-o', label='Benford')
    axes[0].set_xlabel('First Digit')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title(f'Base-10 First Digit (r={benford_corr:.3f})')
    axes[0].legend()
    
    # Base-16 plot
    digits_16 = list(range(1, 16))
    obs_16 = [first_digits_16.get(d, 0) for d in digits_16]
    benf_16 = [benford_16[d] for d in digits_16]
    axes[1].bar(digits_16, obs_16, alpha=0.7, label='Observed')
    axes[1].plot(digits_16, benf_16, 'r-o', label='Benford')
    axes[1].set_xlabel('First Digit')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title(f'Base-16 First Digit (r={benford_corr_16:.3f})')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('hypothesis4_first_digit.png', dpi=150)
    print(f"\nSaved plot: hypothesis4_first_digit.png")
    
    return {
        'benford_corr_10': benford_corr,
        'benford_corr_16': benford_corr_16,
        'chi_10': chi_10,
        'chi_16': chi_16,
        'supported': hypothesis_supported
    }

def hypothesis_5_test(limit=500000, ngram_size=2):
    """
    Hypothesis 5: Entropy of Prime Gap N-grams Increases with Base
    """
    print("\n" + "=" * 70)
    print("HYPOTHESIS 5: Entropy of Prime Gap N-grams vs Base")
    print("=" * 70)
    
    print(f"Computing primes up to {limit}...")
    primes = segmented_sieve(limit)
    
    bases = [4, 8, 10, 16, 32]
    entropies = []
    
    print("\n--- Entropy Analysis ---")
    for base in bases:
        gap_ngrams = get_gap_ngrams(primes, base, ngram_size)
        
        if len(gap_ngrams) == 0:
            entropies.append(0)
            continue
        
        # Calculate Shannon entropy
        total = sum(gap_ngrams.values())
        probs = [count / total for count in gap_ngrams.values()]
        entropy = -sum(p * np.log2(p) for p in probs if p > 0)
        
        # Normalize by maximum possible entropy
        max_entropy = np.log2(min(base ** ngram_size, len(gap_ngrams)))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        entropies.append(normalized_entropy)
        print(f"Base-{base}: entropy = {entropy:.4f}, normalized = {normalized_entropy:.4f}")
    
    # Test: entropy increases with base (monotonic trend)
    increases = sum(1 for i in range(len(entropies)-1) if entropies[i+1] >= entropies[i])
    total_comparisons = len(entropies) - 1
    monotonic_ratio = increases / total_comparisons if total_comparisons > 0 else 0
    
    print(f"\n--- Hypothesis Test ---")
    print(f"Monotonic increases: {increases}/{total_comparisons} ({monotonic_ratio:.2%})")
    
    # Use Spearman correlation
    if len(bases) > 2:
        spearman_corr = np.corrcoef(bases, entropies)[0, 1]
        print(f"Spearman correlation (base vs entropy): {spearman_corr:.4f}")
        hypothesis_supported = spearman_corr > 0.5
    else:
        hypothesis_supported = monotonic_ratio > 0.6
    
    print(f"\nHYPOTHESIS 5 SUPPORTED: {hypothesis_supported}")
    
    # Create visualization
    plt.figure(figsize=(8, 6))
    plt.plot(bases, entropies, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Base')
    plt.ylabel('Normalized Entropy')
    plt.title('Entropy of Prime Gap N-grams vs Base')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.1)
    plt.savefig('hypothesis5_entropy.png', dpi=150)
    print(f"Saved plot: hypothesis5_entropy.png")
    
    return {
        'bases': bases,
        'entropies': entropies,
        'supported': hypothesis_supported
    }

def create_summary_plot(all_results):
    """Create summary visualization of all hypothesis tests."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    # H1: KL divergence comparison
    h1 = all_results.get('h1', {})
    if 'kl_10' in h1 and 'kl_16' in h1:
        axes[0].bar(['Base-10', 'Base-16'], [h1['kl_10'], h1['kl_16']], 
                   color=['blue', 'green'], alpha=0.7)
        axes[0].axhline(y=0.05, color='r', linestyle='--', label='Threshold')
        axes[0].set_ylabel('KL Divergence')
        axes[0].set_title('H1: Gap N-gram KL Divergence')
        axes[0].legend()
    
    # H2: Prefix comparison
    h2 = all_results.get('h2', {})
    if 'kl_8' in h2 and 'kl_32' in h2:
        axes[1].bar(['Base-8', 'Base-32'], [h2['kl_8'], h2['kl_32']], 
                   color=['orange', 'purple'], alpha=0.7)
        axes[1].set_ylabel('KL Divergence')
        axes[1].set_title('H2: Prefix N-gram KL Divergence')
    
    # H3: Internal vs Prefix
    h3 = all_results.get('h3', {})
    if 'results' in h3:
        bases = sorted(h3['results'].keys())
        prefix_vals = [h3['results'][b]['prefix'] for b in bases]
        internal_vals = [h3['results'][b]['internal'] for b in bases]
        x = np.arange(len(bases))
        width = 0.35
        axes[2].bar(x - width/2, prefix_vals, width, label='Prefix', alpha=0.7)
        axes[2].bar(x + width/2, internal_vals, width, label='Internal', alpha=0.7)
        axes[2].set_xticks(x)
        axes[2].set_xticklabels([f'B{b}' for b in bases])
        axes[2].set_ylabel('KL Divergence')
        axes[2].set_title('H3: Internal vs Prefix')
        axes[2].legend()
    
    # H4: Benford correlations
    h4 = all_results.get('h4', {})
    if 'benford_corr_10' in h4 and 'benford_corr_16' in h4:
        axes[3].bar(['Base-10', 'Base-16'], 
                   [h4['benford_corr_10'], h4['benford_corr_16']], 
                   color=['cyan', 'magenta'], alpha=0.7)
        axes[3].axhline(y=0.8, color='r', linestyle='--', label='Threshold')
        axes[3].set_ylabel('Benford Correlation')
        axes[3].set_title('H4: First Digit Benford Correlation')
        axes[3].legend()
    
    # H5: Entropy vs Base
    h5 = all_results.get('h5', {})
    if 'bases' in h5 and 'entropies' in h5:
        axes[4].plot(h5['bases'], h5['entropies'], 'go-', linewidth=2, markersize=8)
        axes[4].set_xlabel('Base')
        axes[4].set_ylabel('Normalized Entropy')
        axes[4].set_title('H5: Entropy vs Base')
        axes[4].grid(True, alpha=0.3)
    
    # Summary: Support status
    supported = [
        h1.get('supported', False),
        h2.get('supported', False),
        h3.get('supported', False),
        h4.get('supported', False),
        h5.get('supported', False)
    ]
    colors = ['green' if s else 'red' for s in supported]
    axes[5].barh(['H1', 'H2', 'H3', 'H4', 'H5'], 
                [1 if s else 0 for s in supported], 
                color=colors, alpha=0.7)
    axes[5].set_xlim(-0.1, 1.1)
    axes[5].set_xlabel('Supported (1) / Not Supported (0)')
    axes[5].set_title('Hypothesis Support Summary')
    
    plt.tight_layout()
    plt.savefig('hypotheses_summary.png', dpi=150)
    print(f"\nSaved summary plot: hypotheses_summary.png")

def main():
    """Main execution function."""
    print("=" * 70)
    print("RESEARCH HYPOTHESES TESTING: Positional N-Gram Patterns")
    print("and Inter-Prime Gap Digit Sequences in Higher Bases")
    print("=" * 70)
    
    # Use moderate limit for 2-minute runtime constraint
    LIMIT = 200000  # Adjusted for time constraint
    
    all_results = {}
    
    # Run all hypothesis tests
    try:
        all_results['h1'] = hypothesis_1_test(LIMIT, ngram_size=2)
    except Exception as e:
        print(f"Error in H1: {e}")
        all_results['h1'] = {'supported': False, 'error': str(e)}
    
    try:
        all_results['h2'] = hypothesis_2_test(LIMIT, ngram_size=2)
    except Exception as e:
        print(f"Error in H2: {e}")
        all_results['h2'] = {'supported': False, 'error': str(e)}
    
    try:
        all_results['h3'] = hypothesis_3_test(LIMIT, ngram_size=2)
    except Exception as e:
        print(f"Error in H3: {e}")
        all_results['h3'] = {'supported': False, 'error': str(e)}
    
    try:
        all_results['h4'] = hypothesis_4_test(LIMIT)
    except Exception as e:
        print(f"Error in H4: {e}")
        all_results['h4'] = {'supported': False, 'error': str(e)}
    
    try:
        all_results['h5'] = hypothesis_5_test(LIMIT, ngram_size=2)
    except Exception as e:
        print(f"Error in H5: {e}")
        all_results['h5'] = {'supported': False, 'error': str(e)}
    
    # Create summary visualization
    try:
        create_summary_plot(all_results)
    except Exception as e:
        print(f"Error creating summary plot: {e}")
    
    # Print final conclusions
    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    
    print("\nSUMMARY OF HYPOTHESIS TESTS:")
    print("-" * 50)
    
    h1_status = "SUPPORTED" if all_results.get('h1', {}).get('supported', False) else "NOT SUPPORTED"
    h2_status = "SUPPORTED" if all_results.get('h2', {}).get('supported', False) else "NOT SUPPORTED"
    h3_status = "SUPPORTED" if all_results.get('h3', {}).get('supported', False) else "NOT SUPPORTED"
    h4_status = "SUPPORTED" if all_results.get('h4', {}).get('supported', False) else "NOT SUPPORTED"
    h5_status = "SUPPORTED" if all_results.get('h5', {}).get('supported', False) else "NOT SUPPORTED"
    
    print(f"H1 (Gap N-grams Base-16 > Base-10):     {h1_status}")
    print(f"H2 (Prefix Base-32 > Base-8):           {h2_status}")
    print(f"H3 (Internal < Prefix randomness):      {h3_status}")
    print(f"H4 (Benford Base-10, deviate Base-16):  {h4_status}")
    print(f"H5 (Entropy increases with base):       {h5_status}")
    
    supported_count = sum([
        all_results.get('h1', {}).get('supported', False),
        all_results.get('h2', {}).get('supported', False),
        all_results.get('h3', {}).get('supported', False),
        all_results.get('h4', {}).get('supported', False),
        all_results.get('h5', {}).get('supported', False)
    ])
    
    print(f"\nOVERALL: {supported_count}/5 hypotheses supported")
    
    print("\nKEY FINDINGS:")
    print("-" * 50)
    
    # H1 details
    h1 = all_results.get('h1', {})
    if 'kl_10' in h1 and 'kl_16' in h1:
        print(f"1. Gap N-gram KL divergence: Base-10={h1['kl_10']:.4f}, Base-16={h1['kl_16']:.4f}")
        if h1['kl_16'] > h1['kl_10']:
            print("   Higher bases DO show greater divergence in gap patterns.")
        else:
            print("   No significant increase in divergence with higher base.")
    
    # H2 details
    h2 = all_results.get('h2', {})
    if 'kl_8' in h2 and 'kl_32' in h2:
        print(f"2. Prefix N-gram KL divergence: Base-8={h2['kl_8']:.4f}, Base-32={h2['kl_32']:.4f}")
    
    # H3 details
    h3 = all_results.get('h3', {})
    if 'results' in h3:
        for base in sorted(h3['results'].keys()):
            r = h3['results'][base]
            print(f"3. Base-{base}: Prefix={r['prefix']:.4f}, Internal={r['internal']:.4f}, ratio={r['ratio']:.4f}")
    
    # H4 details
    h4 = all_results.get('h4', {})
    if 'benford_corr_10' in h4:
        print(f"4. Benford correlation: Base-10={h4['benford_corr_10']:.4f}, Base-16={h4['benford_corr_16']:.4f}")
    
    # H5 details
    h5 = all_results.get('h5', {})
    if 'bases' in h5:
        print(f"5. Entropy progression: {list(zip(h5['bases'], [f'{e:.3f}' for e in h5['entropies']]))}")
    
    print("\nIMPLICATIONS:")
    print("-" * 50)
    if supported_count >= 3:
        print("Multiple hypotheses supported: Positional and gap-based digit")
        print("patterns show meaningful structure distinguishing primes from")
        print("composites, with base-dependent effects.")
    elif supported_count >= 1:
        print("Limited support: Some positional/gap patterns show promise,")
        print("but effects are subtle and require larger samples.")
    else:
        print("Null findings: No significant positional or gap-based patterns")
        print("detected, consistent with previous Base-2 n-gram results.")
        print("Prime digit sequences may be statistically indistinguishable")
        print("from random sequences at the n-gram level.")
    
    print("\n" + "=" * 70)
    print("END OF ANALYSIS")
    print("=" * 70)

if __name__ == "__main__":
    main()