import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import math
import sys

# =============================================================================
# UTILITY FUNCTIONS: PRIME GENERATION AND BASE CONVERSION
# =============================================================================

def simple_sieve(limit):
    """Generate primes up to limit using simple sieve."""
    if limit < 2:
        return np.array([], dtype=np.int64)
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return np.where(sieve)[0].astype(np.int64)

def segmented_sieve(n):
    """Generate all primes up to n using segmented sieve for memory efficiency."""
    if n < 2:
        return np.array([], dtype=np.int64)
    
    if n <= 10**6:
        return simple_sieve(n)
    
    limit = int(n**0.5) + 1
    base_primes = simple_sieve(limit)
    primes = list(base_primes)
    
    segment_size = min(limit, 32768)
    low = limit
    
    while low <= n:
        high = min(low + segment_size - 1, n)
        sieve = np.ones(high - low + 1, dtype=bool)
        
        for p in base_primes:
            start = max(p * p, (low + p - 1) // p * p)
            sieve[start - low::p] = False
        
        primes.extend(np.where(sieve)[0].astype(np.int64) + low)
        low = high + 1
    
    return np.array(primes, dtype=np.int64)

def to_base(n, base):
    """Convert integer n to digit list in given base (MSB first)."""
    n = int(n)
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return digits[::-1]

def get_prefix(n, base, length):
    """Get first 'length' digits of n in given base."""
    digits = to_base(n, base)
    if len(digits) < length:
        return tuple([0] * (length - len(digits)) + digits)
    return tuple(digits[:length])

def get_suffix(n, base, length):
    """Get last 'length' digits of n in given base."""
    n = int(n)
    digits = []
    temp = n
    for _ in range(length):
        digits.append(temp % base)
        temp //= base
    return tuple(reversed(digits))

def get_ngram_at_position(n, base, pos, length):
    """Get n-gram starting at position pos (0-indexed from left)."""
    digits = to_base(n, base)
    if pos + length > len(digits):
        return None
    return tuple(digits[pos:pos + length])

# =============================================================================
# STATISTICAL FUNCTIONS: KL DIVERGENCE AND ENTROPY
# =============================================================================

def kl_divergence(p_dist, q_dist, epsilon=1e-10):
    """Compute KL divergence D_KL(P || Q) with smoothing."""
    p_sum = sum(p_dist.values())
    q_sum = sum(q_dist.values())
    
    if p_sum == 0 or q_sum == 0:
        return 0.0
    
    all_keys = set(p_dist.keys()) | set(q_dist.keys())
    
    kl = 0.0
    for k in all_keys:
        p_val = (p_dist.get(k, 0) + epsilon) / (p_sum + epsilon * len(all_keys))
        q_val = (q_dist.get(k, 0) + epsilon) / (q_sum + epsilon * len(all_keys))
        kl += p_val * math.log(p_val / q_val)
    
    return kl

def compute_entropy(dist):
    """Compute Shannon entropy of a distribution."""
    total = sum(dist.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for v in dist.values():
        p = v / total
        if p > 0:
            entropy -= p * math.log(p, 2)
    return entropy

# =============================================================================
# MAIN ANALYSIS FUNCTIONS
# =============================================================================

def analyze_prefix_ngrams(primes, base, ngram_length, sample_size=50000):
    """Analyze prefix n-gram distribution for primes vs uniform."""
    primes_sample = primes[:min(len(primes), sample_size)]
    
    min_val = base ** (ngram_length - 1) if ngram_length > 1 else 2
    valid_primes = primes_sample[primes_sample >= min_val]
    
    if len(valid_primes) < 100:
        return None, None, 0.0
    
    prime_prefixes = Counter()
    for p in valid_primes:
        prefix = get_prefix(p, base, ngram_length)
        prime_prefixes[prefix] += 1
    
    max_p = valid_primes[-1]
    uniform_samples = np.random.randint(min_val, max_p + 1, size=len(valid_primes))
    uniform_prefixes = Counter()
    for u in uniform_samples:
        prefix = get_prefix(u, base, ngram_length)
        uniform_prefixes[prefix] += 1
    
    kl = kl_divergence(prime_prefixes, uniform_prefixes)
    
    return prime_prefixes, uniform_prefixes, kl

def analyze_suffix_ngrams(primes, base, ngram_length, sample_size=50000):
    """Analyze suffix n-gram distribution (relevant to divisibility)."""
    primes_sample = primes[:min(len(primes), sample_size)]
    
    valid_primes = primes_sample[primes_sample > base]
    
    if len(valid_primes) < 100:
        return None, None, 0.0
    
    prime_suffixes = Counter()
    for p in valid_primes:
        suffix = get_suffix(p, base, ngram_length)
        prime_suffixes[suffix] += 1
    
    max_p = valid_primes[-1]
    uniform_samples = np.random.randint(base + 1, max_p + 1, size=len(valid_primes))
    uniform_suffixes = Counter()
    for u in uniform_samples:
        suffix = get_suffix(u, base, ngram_length)
        uniform_suffixes[suffix] += 1
    
    kl = kl_divergence(prime_suffixes, uniform_suffixes)
    
    return prime_suffixes, uniform_suffixes, kl

def analyze_internal_ngrams(primes, base, ngram_length, position, sample_size=50000):
    """Analyze internal n-gram at specific position."""
    primes_sample = primes[:min(len(primes), sample_size)]
    
    min_digits = position + ngram_length + 1
    min_val = base ** min_digits
    
    valid_primes = primes_sample[primes_sample >= min_val]
    
    if len(valid_primes) < 100:
        return None, None, 0.0
    
    prime_ngrams = Counter()
    for p in valid_primes:
        ng = get_ngram_at_position(p, base, position, ngram_length)
        if ng is not None:
            prime_ngrams[ng] += 1
    
    max_p = valid_primes[-1]
    uniform_samples = np.random.randint(min_val, max_p + 1, size=len(valid_primes))
    uniform_ngrams = Counter()
    for u in uniform_samples:
        ng = get_ngram_at_position(u, base, position, ngram_length)
        if ng is not None:
            uniform_ngrams[ng] += 1
    
    kl = kl_divergence(prime_ngrams, uniform_ngrams)
    
    return prime_ngrams, uniform_ngrams, kl

def analyze_base_residue_structure(base, primes):
    """Analyze how base structure affects prime distribution."""
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    valid_residues = [r for r in range(base) if gcd(r, base) == 1 and r > 0]
    
    residue_counts = Counter()
    count = 0
    for p in primes:
        if p > 2 and p <= 1000000:
            residue_counts[int(p) % base] += 1
            count += 1
        elif p > 1000000:
            break
    
    expected_per_residue = count / len(valid_residues) if valid_residues else 1
    
    deviation = 0.0
    for r in valid_residues:
        obs = residue_counts.get(r, 0)
        dev = (obs - expected_per_residue) ** 2 / max(expected_per_residue, 1)
        deviation += dev
    
    return valid_residues, residue_counts, deviation

# =============================================================================
# HYPOTHESIS TESTING
# =============================================================================

def test_hypothesis_1(primes, bases_config):
    print("=" * 70)
    print("HYPOTHESIS 1: Structural Primorial Advantage")
    print("=" * 70)
    
    results = {}
    
    for base_name, base, ngram_len in bases_config:
        print(f"\nTesting {base_name} (base {base}, n-gram length {ngram_len}):")
        prime_dist, uniform_dist, kl = analyze_prefix_ngrams(primes, base, ngram_len, 30000)
        
        if prime_dist is None:
            print(f"  Insufficient data for meaningful analysis")
            results[base_name] = {'kl': 0, 'entropy_prime': 0, 'entropy_uniform': 0}
            continue
        
        ent_prime = compute_entropy(prime_dist)
        ent_uniform = compute_entropy(uniform_dist)
        
        print(f"  KL divergence (prime || uniform): {kl:.6f}")
        print(f"  Prime entropy: {ent_prime:.4f} bits")
        print(f"  Uniform entropy: {ent_uniform:.4f} bits")
        print(f"  Entropy difference: {abs(ent_prime - ent_uniform):.4f}")
        
        results[base_name] = {
            'kl': kl,
            'entropy_prime': ent_prime,
            'entropy_uniform': ent_uniform,
            'base': base
        }
    
    primorial_kl = [results.get(k, {}).get('kl', 0) for k in ['Base-6', 'Base-30']]
    power2_kl = [results.get(k, {}).get('kl', 0) for k in ['Base-8', 'Base-32']]
    
    avg_primorial = np.mean([k for k in primorial_kl if k > 0]) if any(k > 0 for k in primorial_kl) else 0
    avg_power2 = np.mean([k for k in power2_kl if k > 0]) if any(k > 0 for k in power2_kl) else 0
    
    print(f"\n--- Comparison ---")
    print(f"Average KL divergence - Primorial bases: {avg_primorial:.6f}")
    print(f"Average KL divergence - Power-of-two bases: {avg_power2:.6f}")
    
    supported = avg_primorial > avg_power2
    if supported:
        ratio = avg_primorial / max(avg_power2, 1e-10)
        print(f"RESULT: SUPPORTED - Primorial bases show {ratio:.2f}x higher KL divergence")
    else:
        print(f"RESULT: NOT SUPPORTED - Power-of-two bases show higher or equal KL divergence")
    
    return results, supported

def test_hypothesis_2(primes):
    print("\n" + "=" * 70, flush=True)
    print("HYPOTHESIS 2: Suffix Bias and Base Factorization", flush=True)
    print("=" * 70, flush=True)
    
    bases = [6, 8, 10, 12, 30, 32]
    ngram_len = 2
    
    results = []
    
    for base in bases:
        print(f"\nBase {base}:", flush=True)
        
        temp = base
        factors = []
        d = 2
        while d * d <= temp:
            while temp % d == 0:
                factors.append(d)
                temp //= d
            d += 1
        if temp > 1:
            factors.append(temp)
        
        factor_score = len(factors) + sum(factors) / max(factors)
        
        prime_dist, uniform_dist, kl = analyze_suffix_ngrams(primes, base, ngram_len, 30000)
        
        if prime_dist is None:
            print(f"  Insufficient data", flush=True)
            continue
        
        valid_res, res_counts, deviation = analyze_base_residue_structure(base, primes)
        
        print(f"  Prime factors: {factors}", flush=True)
        print(f"  Factor complexity score: {factor_score:.2f}", flush=True)
        print(f"  Valid residues (coprime): {len(valid_res)} / {base}", flush=True)
        print(f"  Suffix KL divergence: {kl:.6f}", flush=True)
        print(f"  Residue deviation: {deviation:.2f}", flush=True)
        
        results.append({
            'base': base,
            'factors': factors,
            'factor_score': factor_score,
            'kl_suffix': kl,
            'residue_deviation': deviation,
            'valid_residues': len(valid_res)
        })
    
    if len(results) >= 3:
        factor_scores = [r['factor_score'] for r in results]
        kl_values = [r['kl_suffix'] for r in results]
        
        if len(set(factor_scores)) > 1 and len(set(kl_values)) > 1:
            corr = np.corrcoef(factor_scores, kl_values)[0, 1] if not np.isnan(np.corrcoef(factor_scores, kl_values)[0, 1]) else 0
            print(f"\n--- Correlation Analysis ---")
            print(f"Correlation (factor score vs KL divergence): {corr:.4f}")
            
            supported = corr > 0.3
            if supported:
                print("RESULT: SUPPORTED - Positive correlation between factor complexity and suffix bias")
            else:
                print("RESULT: NOT SUPPORTED - No clear positive correlation")
        else:
            print("\n--- Correlation Analysis ---")
            print("Insufficient variation for correlation")
            supported = False
    else:
        supported = False
    
    return results, supported

def test_hypothesis_3(primes):
    print("\n" + "=" * 70)
    print("HYPOTHESIS 3: Position-Dependent Bias Decay")
    print("=" * 70)
    
    base = 10
    ngram_len = 2
    positions = [0, 1, 2, 3]
    
    results = []
    
    for pos in positions:
        print(f"\nPosition {pos} (0 = prefix):")
        prime_dist, uniform_dist, kl = analyze_internal_ngrams(primes, base, ngram_len, pos, 25000)
        
        if prime_dist is None:
            print(f"  Insufficient data")
            continue
        
        print(f"  KL divergence: {kl:.6f}")
        print(f"  Unique n-grams observed: {len(prime_dist)}")
        
        results.append({
            'position': pos,
            'kl': kl,
            'num_ngrams': len(prime_dist) if prime_dist else 0
        })
    
    if len(results) >= 2:
        kls = [r['kl'] for r in results]
        positions_used = [r['position'] for r in results]
        
        decreases = sum(1 for i in range(len(kls)-1) if kls[i] > kls[i+1])
        total_comparisons = len(kls) - 1
        
        decay_ratio = decreases / total_comparisons if total_comparisons > 0 else 0
        
        print(f"\n--- Decay Analysis ---")
        print(f"KL values by position: {list(zip(positions_used, [f'{k:.6f}' for k in kls]))}")
        print(f"Decay ratio (positions where KL decreases): {decay_ratio:.2f}")
        
        supported = decay_ratio >= 0.5
        if supported:
            print("RESULT: SUPPORTED - General decay pattern observed")
        else:
            print("RESULT: NOT SUPPORTED - No clear decay pattern")
    else:
        supported = False
    
    return results, supported

def test_hypothesis_4(primes):
    print("\n" + "=" * 70)
    print("HYPOTHESIS 4: Base-30 Optimal Information Density")
    print("=" * 70)
    
    bases = [6, 8, 10, 12, 16, 20, 24, 30, 32, 36]
    ngram_len = 2
    
    results = []
    
    for base in bases:
        print(f"\nBase {base}:")
        
        info_per_digit = math.log2(base)
        
        prime_dist, uniform_dist, kl_prefix = analyze_prefix_ngrams(primes, base, ngram_len, 25000)
        _, _, kl_suffix = analyze_suffix_ngrams(primes, base, ngram_len, 25000)
        
        avg_kl = (kl_prefix + kl_suffix) / 2 if prime_dist else 0
        density_score = avg_kl * info_per_digit if avg_kl > 0 else 0
        
        print(f"  Info per digit: {info_per_digit:.3f} bits")
        print(f"  Average KL divergence: {avg_kl:.6f}")
        print(f"  Density score (KL × info): {density_score:.6f}")
        
        results.append({
            'base': base,
            'info_per_digit': info_per_digit,
            'kl_prefix': kl_prefix,
            'kl_suffix': kl_suffix,
            'avg_kl': avg_kl,
            'density_score': density_score
        })
    
    if results:
        best_by_kl = max(results, key=lambda x: x['avg_kl'])
        best_by_density = max(results, key=lambda x: x['density_score'])
        
        print(f"\n--- Optimization Analysis ---")
        print(f"Highest KL divergence: Base {best_by_kl['base']} ({best_by_kl['avg_kl']:.6f})")
        print(f"Highest density score: Base {best_by_density['base']} ({best_by_density['density_score']:.6f})")
        
        base30_result = next((r for r in results if r['base'] == 30), None)
        
        if base30_result:
            kl_rank = sorted(results, key=lambda x: x['avg_kl'], reverse=True).index(base30_result) + 1
            density_rank = sorted(results, key=lambda x: x['density_score'], reverse=True).index(base30_result) + 1
            
            print(f"\nBase-30 rankings:")
            print(f"  KL divergence rank: {kl_rank} / {len(results)}")
            print(f"  Density score rank: {density_rank} / {len(results)}")
            
            supported = density_rank <= 2 or (kl_rank <= 3 and density_rank <= 3)
            if supported:
                print("RESULT: SUPPORTED - Base-30 shows near-optimal performance")
            else:
                print("RESULT: NOT SUPPORTED - Base-30 not near-optimal")
        else:
            supported = False
    else:
        supported = False
    
    return results, supported

def test_hypothesis_5(primes):
    print("\n" + "=" * 70)
    print("HYPOTHESIS 5: Scalable N-Gram Detection")
    print("=" * 70)
    
    configs = [
        ('Base-6, 4-gram', 6, 4, 6*4),
        ('Base-8, 3-gram', 8, 3, 8*3),
        ('Base-12, 3-gram', 12, 3, 12*3),
        ('Base-16, 2-gram', 16, 2, 16*2),
        ('Base-32, 2-gram', 32, 2, 32*2),
    ]
    
    results = []
    
    for name, base, ngram_len, complexity in configs:
        print(f"\n{name} (complexity ~{complexity}):")
        prime_dist, uniform_dist, kl = analyze_prefix_ngrams(primes, base, ngram_len, 20000)
        
        if prime_dist is None:
            print(f"  Insufficient data")
            continue
        
        normalized_kl = kl / max(complexity, 1) if complexity > 0 else 0
        possible_ngrams = base ** ngram_len
        observed_ngrams = len(prime_dist) if prime_dist else 0
        coverage = observed_ngrams / min(possible_ngrams, 20000)
        
        print(f"  KL divergence: {kl:.6f}")
        print(f"  Normalized KL (per complexity): {normalized_kl:.8f}")
        print(f"  N-gram coverage: {coverage:.4f} ({observed_ngrams}/{min(possible_ngrams, 20000)})")
        
        results.append({
            'name': name,
            'base': base,
            'ngram_len': ngram_len,
            'complexity': complexity,
            'kl': kl,
            'normalized_kl': normalized_kl,
            'coverage': coverage
        })
    
    if len(results) >= 2:
        small_base = [r for r in results if r['base'] <= 8 and r['ngram_len'] >= 3]
        large_base = [r for r in results if r['base'] >= 16 and r['ngram_len'] <= 2]
        
        if small_base and large_base:
            avg_small_norm = np.mean([r['normalized_kl'] for r in small_base])
            avg_large_norm = np.mean([r['normalized_kl'] for r in large_base])
            
            print(f"\n--- Comparison ---")
            print(f"Small-base-long-gram normalized KL: {avg_small_norm:.8f}")
            print(f"Large-base-short-gram normalized KL: {avg_large_norm:.8f}")
            
            supported = avg_small_norm > avg_large_norm
            if supported:
                ratio = avg_small_norm / max(avg_large_norm, 1e-15)
                print(f"RESULT: SUPPORTED - Small bases with long n-grams {ratio:.2f}x better")
            else:
                print("RESULT: NOT SUPPORTED - Large bases with short n-grams perform better")
        else:
            print("\nInsufficient categories for comparison")
            supported = False
    else:
        supported = False
    
    return results, supported

# =============================================================================
# VISUALIZATION
# =============================================================================

def create_visualizations(h1_results, h2_results, h3_results, h4_results, h5_results):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Positional N-Gram Bias Analysis in Prime Number Distributions', fontsize=12)
    
    ax = axes[0, 0]
    if h1_results:
        names = list(h1_results.keys())
        kls = [h1_results[n]['kl'] for n in names]
        colors = ['green' if '6' in n or '30' in n else 'blue' for n in names]
        ax.bar(names, kls, color=colors, alpha=0.7)
        ax.set_ylabel('KL Divergence')
        ax.set_title('H1: Primorial vs Power-of-2 Bases')
        ax.tick_params(axis='x', rotation=45)
    
    ax = axes[0, 1]
    if h2_results:
        bases = [r['base'] for r in h2_results]
        kls = [r['kl_suffix'] for r in h2_results]
        ax.scatter(bases, kls, s=100, alpha=0.7, c='purple')
        for i, b in enumerate(bases):
            ax.annotate(str(b), (bases[i], kls[i]), textcoords="offset points", xytext=(0,5), ha='center')
        ax.set_xlabel('Base')
        ax.set_ylabel('Suffix KL Divergence')
        ax.set_title('H2: Base Factorization vs Suffix Bias')
    
    ax = axes[0, 2]
    if h3_results:
        positions = [r['position'] for r in h3_results]
        kls = [r['kl'] for r in h3_results]
        ax.plot(positions, kls, 'o-', color='red', linewidth=2, markersize=8)
        ax.set_xlabel('Position from Left (0 = prefix)')
        ax.set_ylabel('KL Divergence')
        ax.set_title('H3: Bias Decay by Position')
    
    ax = axes[1, 0]
    if h4_results:
        bases = [r['base'] for r in h4_results]
        densities = [r['density_score'] for r in h4_results]
        colors = ['red' if b == 30 else 'gray' for b in bases]
        ax.bar([str(b) for b in bases], densities, color=colors, alpha=0.7)
        ax.set_xlabel('Base')
        ax.set_ylabel('Density Score (KL × bits/digit)')
        ax.set_title('H4: Information Density by Base')
    
    ax = axes[1, 1]
    if h5_results:
        names = [r['name'].replace(', ', '\n') for r in h5_results]
        norm_kls = [r['normalized_kl'] * 1000000 for r in h5_results]
        ax.barh(names, norm_kls, color='teal', alpha=0.7)
        ax.set_xlabel('Normalized KL (×10⁶)')
        ax.set_title('H5: Scalable N-Gram Detection')
    
    ax = axes[1, 2]
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('prime_ngram_analysis.png', dpi=150, bbox_inches='tight')
    print("\nVisualization saved to 'prime_ngram_analysis.png'")
    
    return fig

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 70)
    print("POSITIONAL N-GRAM BIAS ANALYSIS OF PRIME NUMBERS")
    print("Research: Primorial and High-Order Base Distributions")
    print("=" * 70)
    
    print("\nGenerating primes up to 1 million...", flush=True)
    primes = segmented_sieve(1_000_000)
    print(f"Generated {len(primes):,} primes", flush=True)
    
    np.random.seed(42)
    
    h1_bases = [
        ('Base-6', 6, 2),
        ('Base-30', 30, 2),
        ('Base-8', 8, 2),
        ('Base-32', 32, 2),
    ]
    
    h1_results, h1_supported = test_hypothesis_1(primes, h1_bases)
    h2_results, h2_supported = test_hypothesis_2(primes)
    h3_results, h3_supported = test_hypothesis_3(primes)
    h4_results, h4_supported = test_hypothesis_4(primes)
    h5_results, h5_supported = test_hypothesis_5(primes)
    
    try:
        create_visualizations(h1_results, h2_results, h3_results, h4_results, h5_results)
    except Exception as e:
        print(f"\nVisualization error (non-critical): {e}")
    
    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    
    print(f"""
RESEARCH FINDINGS SUMMARY:

Hypothesis 1 (Structural Primorial Advantage): {'SUPPORTED' if h1_supported else 'NOT SUPPORTED'}
Hypothesis 2 (Suffix Bias & Factorization): {'SUPPORTED' if h2_supported else 'NOT SUPPORTED'}
Hypothesis 3 (Position-Dependent Decay): {'SUPPORTED' if h3_supported else 'NOT SUPPORTED'}
Hypothesis 4 (Base-30 Optimality): {'SUPPORTED' if h4_supported else 'NOT SUPPORTED'}
Hypothesis 5 (Scalable Detection): {'SUPPORTED' if h5_supported else 'NOT SUPPORTED'}
""")
    
    support_count = sum([h1_supported, h2_supported, h3_supported, h4_supported, h5_supported])
    print(f"Overall: {support_count}/5 hypotheses supported ({support_count*20}% confirmation rate)")

if __name__ == "__main__":
    main()