import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

MAX_PRIME = 500000  # Upper limit for prime generation
N_GRAM_SIZES = [3, 4]  # Higher-order n-grams to test
BASES = [2, 10]  # Binary and decimal
SAMPLE_SIZE = 50000  # Number of primes/composites to analyze
MIN_DIGITS = 5  # Minimum digits needed for internal n-gram extraction

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def segmented_sieve(limit):
    """Efficient segmented sieve of Eratosthenes."""
    if limit < 2:
        return np.array([], dtype=np.int64)
    
    # Small primes for sieving
    small_limit = int(np.sqrt(limit)) + 1
    small_sieve = np.ones(small_limit + 1, dtype=bool)
    small_sieve[0:2] = False
    
    for i in range(2, int(np.sqrt(small_limit)) + 1):
        if small_sieve[i]:
            small_sieve[i*i::i] = False
    
    small_primes = np.where(small_sieve)[0].astype(np.int64)
    
    # Segmented sieve
    segment_size = max(small_limit, 32768)
    primes = list(small_primes)
    
    for low in range(small_limit, limit + 1, segment_size):
        high = min(low + segment_size - 1, limit)
        segment = np.ones(high - low + 1, dtype=bool)
        
        for p in small_primes:
            if p * p > high:
                break
            start = max(p * p, ((low + p - 1) // p) * p)
            segment[start - low::p] = False
        
        primes.extend(np.where(segment)[0] + low)
    
    return np.array(primes, dtype=np.int64)

def to_base_n(n, base):
    """Convert integer to digit list in given base (MSB first)."""
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return digits[::-1]

def get_internal_ngrams(number, base, n):
    """
    Extract n-grams from internal digits only (excluding first and last digit).
    This avoids leading digit biases and terminal digit constraints.
    """
    digits = to_base_n(number, base)
    
    if len(digits) < n + 2:  # Need at least n internal digits + 2 boundary digits
        return []
    
    # Internal digits only (exclude first and last)
    internal = digits[1:-1]
    
    # Extract all n-grams
    ngrams = []
    for i in range(len(internal) - n + 1):
        ngram = tuple(internal[i:i+n])
        ngrams.append(ngram)
    
    return ngrams

def kl_divergence(p, q, epsilon=1e-10):
    """Calculate KL divergence D_KL(P || Q) with smoothing."""
    # Normalize
    p = np.array(p, dtype=np.float64)
    q = np.array(q, dtype=np.float64)
    
    if p.sum() == 0 or q.sum() == 0:
        return 0.0
    
    p = p / (p.sum() + epsilon)
    q = q / (q.sum() + epsilon)
    
    # Smoothing to avoid log(0)
    p = np.clip(p, epsilon, 1)
    q = np.clip(q, epsilon, 1)
    
    # Renormalize after clipping
    p = p / p.sum()
    q = q / q.sum()
    
    kl = np.sum(p * np.log(p / q))
    return kl

def total_variation_distance(p, q):
    """Calculate total variation distance between distributions."""
    p = np.array(p, dtype=np.float64)
    q = np.array(q, dtype=np.float64)
    
    if p.sum() == 0 or q.sum() == 0:
        return 0.0
    
    p = p / p.sum()
    q = q / q.sum()
    
    return 0.5 * np.sum(np.abs(p - q))

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def generate_composite_controls(primes_set, max_val, count):
    """Generate random composite numbers matching digit length distribution."""
    composites = []
    attempts = 0
    max_attempts = count * 100
    
    # Get digit length distribution from primes
    prime_lengths = {}
    for p in list(primes_set)[:10000]:
        l = len(to_base_n(p, 10))
        prime_lengths[l] = prime_lengths.get(l, 0) + 1
    
    # Normalize
    total = sum(prime_lengths.values())
    for l in prime_lengths:
        prime_lengths[l] /= total
    
    length_choices = list(prime_lengths.keys())
    length_probs = list(prime_lengths.values())
    
    while len(composites) < count and attempts < max_attempts:
        attempts += 1
        
        # Match digit length distribution
        target_len = np.random.choice(length_choices, p=length_probs)
        min_val = 10 ** (target_len - 1)
        max_val_for_len = min(10 ** target_len - 1, max_val)
        
        if min_val >= max_val_for_len:
            continue
            
        candidate = np.random.randint(min_val, max_val_for_len + 1)
        
        if candidate not in primes_set and candidate > 1:
            composites.append(candidate)
    
    return np.array(composites[:count])

def analyze_ngrams(numbers, base, n):
    """Extract and count n-grams from numbers."""
    ngram_counts = Counter()
    total_ngrams = 0
    
    for num in numbers:
        ngrams = get_internal_ngrams(num, base, n)
        ngram_counts.update(ngrams)
        total_ngrams += len(ngrams)
    
    return ngram_counts, total_ngrams

def chi_square_test(counts1, counts2):
    """Perform chi-square test on two count distributions."""
    # Get all unique keys
    all_keys = set(counts1.keys()) | set(counts2.keys())
    
    # Build frequency arrays
    obs1 = np.array([counts1.get(k, 0) for k in all_keys], dtype=np.float64)
    obs2 = np.array([counts2.get(k, 0) for k in all_keys], dtype=np.float64)
    
    # Filter zeros
    mask = (obs1 > 0) | (obs2 > 0)
    obs1 = obs1[mask]
    obs2 = obs2[mask]
    
    if len(obs1) < 2:
        return 0, 1.0, 0
    
    # Expected under null (pooled proportion)
    total1, total2 = obs1.sum(), obs2.sum()
    if total1 == 0 or total2 == 0:
        return 0, 1.0, 0
        
    pooled = (obs1 + obs2) / (total1 + total2)
    exp1 = pooled * total1
    exp2 = pooled * total2
    
    # Chi-square statistic
    chi2 = np.sum((obs1 - exp1)**2 / (exp1 + 1e-10)) + np.sum((obs2 - exp2)**2 / (exp2 + 1e-10))
    df = len(obs1) - 1
    
    # p-value
    p_value = 1 - stats.chi2.cdf(chi2, df) if df > 0 else 1.0
    
    # Effect size (Cramer's V)
    n = total1 + total2
    cramers_v = np.sqrt(chi2 / (n * (min(len(obs1), 2) - 1))) if n > 0 and min(len(obs1), 2) > 1 else 0
    
    return chi2, p_value, cramers_v

# =============================================================================
# HYPOTHESIS TESTING
# =============================================================================

def test_hypothesis_1(primes, composites, base, n):
    """
    Hypothesis 1: Internal N-Gram Frequency Deviation
    KL divergence > 0.01 indicates significant deviation
    """
    print(f"\n{'='*60}")
    print(f"HYPOTHESIS 1: Internal {n}-gram Deviation (Base-{base})")
    print(f"{'='*60}")
    
    prime_counts, prime_total = analyze_ngrams(primes, base, n)
    composite_counts, composite_total = analyze_ngrams(composites, base, n)
    
    print(f"Primes analyzed: {len(primes)}")
    print(f"Composites analyzed: {len(composites)}")
    print(f"Total prime {n}-grams: {prime_total}")
    print(f"Total composite {n}-grams: {composite_total}")
    print(f"Unique prime {n}-grams: {len(prime_counts)}")
    print(f"Unique composite {n}-grams: {len(composite_counts)}")
    
    # Get common n-grams for comparison
    common_ngrams = set(prime_counts.keys()) & set(composite_counts.keys())
    all_ngrams = set(prime_counts.keys()) | set(composite_counts.keys())
    
    print(f"Common {n}-grams: {len(common_ngrams)}")
    print(f"Total unique {n}-grams: {len(all_ngrams)}")
    
    # Build aligned frequency vectors
    prime_freq = np.array([prime_counts.get(ng, 0) for ng in sorted(all_ngrams)], dtype=np.float64)
    composite_freq = np.array([composite_counts.get(ng, 0) for ng in sorted(all_ngrams)], dtype=np.float64)
    
    # KL divergences (both directions)
    kl_pc = kl_divergence(prime_freq, composite_freq)
    kl_cp = kl_divergence(composite_freq, prime_freq)
    kl_symmetric = 0.5 * (kl_pc + kl_cp)
    
    # Total variation distance
    tvd = total_variation_distance(prime_freq, composite_freq)
    
    # Chi-square test
    chi2, p_val, cramers_v = chi_square_test(prime_counts, composite_counts)
    
    print(f"\n--- Results ---")
    print(f"KL(P||Q): {kl_pc:.6f}")
    print(f"KL(Q||P): {kl_cp:.6f}")
    print(f"Symmetric KL: {kl_symmetric:.6f}")
    print(f"Total Variation Distance: {tvd:.6f}")
    print(f"Chi-square: {chi2:.2f}, p-value: {p_val:.6f}")
    print(f"Cramer's V (effect size): {cramers_v:.6f}")
    
    # Hypothesis test
    threshold = 0.01
    result = "SUPPORTED" if kl_symmetric > threshold else "NOT SUPPORTED"
    print(f"\n>>> HYPOTHESIS 1: {result}")
    print(f"    (KL divergence {kl_symmetric:.6f} {'>' if kl_symmetric > threshold else '<='} threshold {threshold})")
    
    return {
        'kl_divergence': kl_symmetric,
        'tvd': tvd,
        'p_value': p_val,
        'cramers_v': cramers_v,
        'supported': kl_symmetric > threshold
    }

def test_hypothesis_2(primes, base, n):
    """
    Hypothesis 2: Base-2 vs Base-10 Pattern Correlation
    Test if n-gram patterns are base-independent
    """
    print(f"\n{'='*60}")
    print(f"HYPOTHESIS 2: Cross-Base Pattern Correlation (n={n})")
    print(f"{'='*60}")
    
    # Get n-grams in both bases
    base10_counts, _ = analyze_ngrams(primes, 10, n)
    base2_counts, _ = analyze_ngrams(primes, 2, n)
    
    # For this hypothesis, we test if the "complexity" of patterns correlates
    # Measure: entropy of n-gram distribution
    
    def entropy(counts):
        if not counts:
            return 0.0
        freqs = np.array(list(counts.values()), dtype=np.float64)
        if freqs.sum() == 0:
            return 0.0
        freqs = freqs / freqs.sum()
        return -np.sum(freqs * np.log2(freqs + 1e-10))
    
    h10 = entropy(base10_counts)
    h2 = entropy(base2_counts)
    
    # Normalize by max possible entropy
    max_h10 = np.log2(10**n)
    max_h2 = np.log2(2**n)
    
    norm_h10 = h10 / max_h10 if max_h10 > 0 else 0
    norm_h2 = h2 / max_h2 if max_h2 > 0 else 0
    
    print(f"Base-10 entropy: {h10:.4f} bits (normalized: {norm_h10:.4f})")
    print(f"Base-2 entropy:  {h2:.4f} bits (normalized: {norm_h2:.4f})")
    
    # Test: similar normalized entropy suggests base-independent structure
    entropy_diff = abs(norm_h10 - norm_h2)
    
    # Also test: do longer primes in base-10 have more complex base-2 patterns?
    # Sample primes by digit length
    digit_lengths = {}
    for p in primes[:10000]:
        d10 = len(to_base_n(p, 10))
        d2 = len(to_base_n(p, 2))
        if d10 not in digit_lengths:
            digit_lengths[d10] = []
        digit_lengths[d10].append((p, d2))
    
    correlations = []
    for d10, items in digit_lengths.items():
        if len(items) >= 10:
            d2_values = [d2 for _, d2 in items]
            corr = np.corrcoef([d10]*len(d2_values), d2_values)[0,1] if len(set(d2_values)) > 1 else 0
            correlations.append(corr)
    
    avg_correlation = np.mean(correlations) if correlations else 0
    
    print(f"\nEntropy difference: {entropy_diff:.4f}")
    print(f"Digit length correlation (base10 vs base2): {avg_correlation:.4f}")
    
    # Hypothesis: base-independent structure exists if entropy difference < 0.2
    # and digit lengths are correlated
    result = "SUPPORTED" if (entropy_diff < 0.2 and avg_correlation > 0.5) else "NOT SUPPORTED"
    print(f"\n>>> HYPOTHESIS 2: {result}")
    
    return {
        'entropy_diff': entropy_diff,
        'digit_correlation': avg_correlation,
        'supported': entropy_diff < 0.2 and avg_correlation > 0.5
    }

def test_hypothesis_3(primes, composites, base):
    """
    Hypothesis 3: Localized Bias in Specific N-Gram Clusters
    Test if certain n-gram patterns are systematically over/under-represented
    """
    print(f"\n{'='*60}")
    print(f"HYPOTHESIS 3: Localized Bias in Specific Patterns (Base-{base})")
    print(f"{'='*60}")
    
    n = 3  # Focus on 3-grams for interpretability
    
    prime_counts, prime_total = analyze_ngrams(primes, base, n)
    composite_counts, composite_total = analyze_ngrams(composites, base, n)
    
    # Calculate log odds ratios for each n-gram
    bias_scores = {}
    all_ngrams = set(prime_counts.keys()) | set(composite_counts.keys())
    
    for ng in all_ngrams:
        p_count = prime_counts.get(ng, 0.5)  # Laplace smoothing
        c_count = composite_counts.get(ng, 0.5)
        
        p_freq = p_count / (prime_total + 0.5 * len(all_ngrams))
        c_freq = c_count / (composite_total + 0.5 * len(all_ngrams))
        
        # Log odds ratio
        lor = np.log(p_freq / c_freq)
        bias_scores[ng] = lor
    
    if not bias_scores:
        return {'mean_bias': 0, 'meaningful_bias_rate': 0, 'p_value': 1.0, 'supported': False}
        
    # Find most biased n-grams
    sorted_bias = sorted(bias_scores.items(), key=lambda x: abs(x[1]), reverse=True)
    
    print(f"Top 10 most biased 3-grams (positive = prime-favored):")
    for ng, bias in sorted_bias[:10]:
        ng_str = ''.join(str(d) for d in ng)
        p_pct = 100 * prime_counts.get(ng, 0) / prime_total if prime_total > 0 else 0
        c_pct = 100 * composite_counts.get(ng, 0) / composite_total if composite_total > 0 else 0
        print(f"  {ng_str}: LOR={bias:+.3f}, P={p_pct:.3f}%, C={c_pct:.3f}%")
    
    # Statistical test: are biases systematically non-zero?
    bias_values = np.array(list(bias_scores.values()))
    
    # One-sample t-test against zero
    t_stat, p_val = stats.ttest_1samp(bias_values, 0) if len(bias_values) > 1 else (0, 1.0)
    
    # Effect size: proportion of n-grams with |bias| > 0.1 (meaningful effect)
    meaningful_bias = np.mean(np.abs(bias_values) > 0.1) if len(bias_values) > 0 else 0
    
    print(f"\nBias statistics:")
    print(f"  Mean bias: {np.mean(bias_values):.4f}")
    print(f"  Std bias: {np.std(bias_values):.4f}")
    print(f"  Max |bias|: {np.max(np.abs(bias_values)):.4f}")
    print(f"  Proportion with |bias| > 0.1: {meaningful_bias:.4f}")
    print(f"  t-test: t={t_stat:.3f}, p={p_val:.6f}")
    
    # Hypothesis: localized bias exists if >10% of n-grams show meaningful bias
    result = "SUPPORTED" if meaningful_bias > 0.10 else "NOT SUPPORTED"
    print(f"\n>>> HYPOTHESIS 3: {result}")
    
    return {
        'mean_bias': np.mean(bias_values),
        'meaningful_bias_rate': meaningful_bias,
        'p_value': p_val,
        'supported': meaningful_bias > 0.10
    }

def test_hypothesis_4(primes, base):
    """
    Hypothesis 4: N-Gram Repetition Suppression
    Test if repeating digit patterns are suppressed in primes
    """
    print(f"\n{'='*60}")
    print(f"HYPOTHESIS 4: N-Gram Repetition Suppression (Base-{base})")
    print(f"{'='*60}")
    
    n = 3
    
    prime_counts, prime_total = analyze_ngrams(primes, base, n)
    
    # Categorize n-grams
    repeating = []  # e.g., 111, 222
    alternating = []  # e.g., 121, 232
    random = []  # everything else
    
    for ng, count in prime_counts.items():
        # Check if all digits same
        if len(set(ng)) == 1:
            repeating.append((ng, count))
        # Check if alternating pattern (ABA)
        elif len(ng) == 3 and ng[0] == ng[2] and ng[0] != ng[1]:
            alternating.append((ng, count))
        else:
            random.append((ng, count))
    
    # Calculate frequencies
    total = sum(c for _, c in prime_counts.items())
    
    rep_freq = sum(c for _, c in repeating) / total if total > 0 else 0
    alt_freq = sum(c for _, c in alternating) / total if total > 0 else 0
    rnd_freq = sum(c for _, c in random) / total if total > 0 else 0
    
    # Expected under uniform distribution
    if base == 10:
        num_repeating = 10  # 000, 111, ..., 999
        num_alternating = 10 * 9  # ABA where A!=B
        num_random = 1000 - num_repeating - num_alternating
    else:  # base 2
        num_repeating = 2  # 000, 111
        num_alternating = 2  # 010, 101
        num_random = 8 - 4
    
    total_patterns = base ** n
    exp_rep = num_repeating / total_patterns
    exp_alt = num_alternating / total_patterns
    exp_rnd = num_random / total_patterns
    
    print(f"Pattern type frequencies (observed vs expected):")
    print(f"  Repeating (AAA):  {rep_freq:.4f} vs {exp_rep:.4f}, ratio={rep_freq/exp_rep if exp_rep>0 else 0:.3f}")
    print(f"  Alternating (ABA): {alt_freq:.4f} vs {exp_alt:.4f}, ratio={alt_freq/exp_alt if exp_alt>0 else 0:.3f}")
    print(f"  Other patterns:   {rnd_freq:.4f} vs {exp_rnd:.4f}, ratio={rnd_freq/exp_rnd if exp_rnd>0 else 0:.3f}")
    
    # Chi-square goodness of fit
    obs = np.array([sum(c for _, c in repeating), sum(c for _, c in alternating), sum(c for _, c in random)])
    exp = np.array([exp_rep, exp_alt, exp_rnd]) * total
    
    chi2 = np.sum((obs - exp)**2 / (exp + 1e-10))
    p_val = 1 - stats.chi2.cdf(chi2, 2)
    
    print(f"\nChi-square test: χ²={chi2:.3f}, p={p_val:.6f}")
    
    # Suppression: repeating patterns should be less frequent than expected
    suppression_ratio = rep_freq / exp_rep if exp_rep > 0 else 1
    
    print(f"\nSuppression ratio (obs/exp for repeating): {suppression_ratio:.3f}")
    print(f"  < 1.0 indicates suppression")
    print(f"  > 1.0 indicates enhancement")
    
    # Hypothesis: suppression exists if ratio < 0.9 (10% or more suppression)
    result = "SUPPORTED" if suppression_ratio < 0.9 else "NOT SUPPORTED"
    print(f"\n>>> HYPOTHESIS 4: {result}")
    
    return {
        'suppression_ratio': suppression_ratio,
        'chi2': chi2,
        'p_value': p_val,
        'supported': suppression_ratio < 0.9
    }

def test_hypothesis_5(primes, composites, base):
    """
    Hypothesis 5: Scale-Invariant N-Gram Structure
    Test if n-gram patterns are consistent across different magnitudes
    """
    print(f"\n{'='*60}")
    print(f"HYPOTHESIS 5: Scale-Invariant Structure (Base-{base})")
    print(f"{'='*60}")
    
    n = 3
    
    # Bin by magnitude (number of digits)
    magnitude_bins = {}
    for p in primes:
        d = len(to_base_n(p, base))
        if d not in magnitude_bins:
            magnitude_bins[d] = []
        magnitude_bins[d].append(p)
    
    # Need at least 3 magnitude bins with sufficient samples
    valid_bins = {d: nums for d, nums in magnitude_bins.items() if len(nums) >= 100}
    
    if len(valid_bins) < 3:
        print(f"Insufficient magnitude variation (only {len(valid_bins)} valid bins)")
        print(f">>> HYPOTHESIS 5: NOT TESTABLE")
        return {'supported': False, 'testable': False}
    
    print(f"Analyzing {len(valid_bins)} magnitude bins: {sorted(valid_bins.keys())}")
    
    # Calculate n-gram distributions for each bin
    distributions = {}
    for d, nums in sorted(valid_bins.items()):
        counts, total = analyze_ngrams(np.array(nums), base, n)
        # Convert to probability distribution over common n-grams
        distributions[d] = counts
    
    # Find common n-grams across all bins
    if not distributions:
        return {'supported': False, 'testable': False}
        
    common = set.intersection(*[set(d.keys()) for d in distributions.values()])
    common = sorted(list(common))
    
    print(f"Common n-grams across all bins: {len(common)}")
    
    # Calculate pairwise KL divergences between magnitude bins
    kl_matrix = np.zeros((len(distributions), len(distributions)))
    digits = sorted(distributions.keys())
    
    for i, d1 in enumerate(digits):
        for j, d2 in enumerate(digits):
            if i == j:
                kl_matrix[i, j] = 0
                continue
            
            p = np.array([distributions[d1].get(ng, 0) for ng in common], dtype=np.float64)
            q = np.array([distributions[d2].get(ng, 0) for ng in common], dtype=np.float64)
            
            kl_matrix[i, j] = kl_divergence(p, q)
    
    # Average KL divergence between non-adjacent bins
    off_diagonal_kl = []
    for i in range(len(digits)):
        for j in range(i+1, len(digits)):
            off_diagonal_kl.append(kl_matrix[i, j])
    
    avg_kl = np.mean(off_diagonal_kl) if off_diagonal_kl else 0
    max_kl = np.max(off_diagonal_kl) if off_diagonal_kl else 0
    
    print(f"\nKL divergence between magnitude bins:")
    print(f"  Average: {avg_kl:.6f}")
    print(f"  Maximum: {max_kl:.6f}")
    
    # Test: adjacent bins should be more similar than distant bins
    adjacent_kl = [kl_matrix[i, i+1] for i in range(len(digits)-1)]
    distant_kl = [kl_matrix[i, j] for i in range(len(digits)) for j in range(i+2, len(digits))]
    
    print(f"\nAdjacent bin KL: {np.mean(adjacent_kl) if adjacent_kl else 0:.6f} ± {np.std(adjacent_kl) if adjacent_kl else 0:.6f}")
    print(f"Distant bin KL:  {np.mean(distant_kl) if distant_kl else 0:.6f} ± {np.std(distant_kl) if distant_kl else 0:.6f}")
    
    # Mann-Whitney U test
    if len(adjacent_kl) > 0 and len(distant_kl) > 0:
        try:
            u_stat, p_val = stats.mannwhitneyu(adjacent_kl, distant_kl, alternative='less')
            print(f"Mann-Whitney U test (adjacent < distant): p={p_val:.6f}")
        except ValueError:
            p_val = 1.0
    else:
        p_val = 1.0
    
    # Scale invariance: low KL divergence across all scales
    # Threshold: average KL < 0.05 indicates strong scale invariance
    result = "SUPPORTED" if avg_kl < 0.05 else "NOT SUPPORTED"
    print(f"\n>>> HYPOTHESIS 5: {result}")
    
    return {
        'avg_kl': avg_kl,
        'max_kl': max_kl,
        'adjacent_vs_distant_p': p_val,
        'supported': avg_kl < 0.05
    }

# =============================================================================
# VISUALIZATION
# =============================================================================

def create_visualizations(results, output_prefix="hypothesis"):
    """Create and save visualization plots."""
    
    # Plot 1: KL Divergence Summary
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # H1 results: KL divergences
    h1_data = results.get('H1', {})
    kl_values = []
    labels = []
    for key, val in h1_data.items():
        if isinstance(val, dict) and 'kl_divergence' in val:
            kl_values.append(val['kl_divergence'])
            labels.append(key)
    
    if kl_values:
        axes[0, 0].bar(range(len(kl_values)), kl_values, color='steelblue')
        axes[0, 0].axhline(y=0.01, color='r', linestyle='--', label='Threshold (0.01)')
        axes[0, 0].set_xticks(range(len(labels)))
        axes[0, 0].set_xticklabels(labels, rotation=45, ha='right')
        axes[0, 0].set_ylabel('KL Divergence')
        axes[0, 0].set_title('H1: Internal N-Gram Deviation')
        axes[0, 0].legend()
    
    # H3 results: Bias distribution
    h3_data = results.get('H3', {})
    h3_b10 = h3_data.get('B10', {})
    if 'mean_bias' in h3_b10:
        bias_info = [h3_b10.get('mean_bias', 0), h3_b10.get('meaningful_bias_rate', 0)]
        axes[0, 1].bar(['Mean Bias', 'Meaningful Rate'], bias_info, color=['coral', 'lightgreen'])
        axes[0, 1].set_title('H3: Localized Bias Metrics (B10)')
        axes[0, 1].axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # H4 results: Pattern suppression
    h4_data = results.get('H4', {})
    h4_b10 = h4_data.get('B10', {})
    if 'suppression_ratio' in h4_b10:
        ratio = h4_b10['suppression_ratio']
        colors = ['red' if ratio < 0.9 else 'green' if ratio > 1.1 else 'gray']
        axes[1, 0].bar(['Suppression Ratio'], [ratio], color=colors)
        axes[1, 0].axhline(y=1.0, color='k', linestyle='--', label='No effect')
        axes[1, 0].axhline(y=0.9, color='r', linestyle=':', label='Suppression threshold')
        axes[1, 0].set_ylim(0, max(2, ratio * 1.2))
        axes[1, 0].set_title('H4: Repetition Suppression (B10)')
        axes[1, 0].legend()
    
    # H5 results: Scale invariance
    h5_data = results.get('H5', {})
    h5_b10 = h5_data.get('B10', {})
    if 'avg_kl' in h5_b10:
        metrics = [h5_b10.get('avg_kl', 0), h5_b10.get('max_kl', 0)]
        axes[1, 1].bar(['Avg KL', 'Max KL'], metrics, color=['mediumpurple', 'plum'])
        axes[1, 1].axhline(y=0.05, color='r', linestyle='--', label='Invariance threshold')
        axes[1, 1].set_title('H5: Scale Invariance (B10)')
        axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_summary.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\nVisualization saved to {output_prefix}_summary.png")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("="*70)
    print("HIGHER-ORDER N-GRAM ANALYSIS IN PRIME NUMBERS")
    print("Research Hypothesis Testing Suite")
    print("="*70)
    
    # Generate primes
    print(f"\n[1] Generating primes up to {MAX_PRIME}...")
    primes = segmented_sieve(MAX_PRIME)
    primes_set = set(primes)
    print(f"    Found {len(primes)} primes")
    
    # Sample for analysis
    if len(primes) > SAMPLE_SIZE:
        # Sample uniformly across range to avoid small-prime bias
        indices = np.linspace(100, len(primes)-1, SAMPLE_SIZE, dtype=int)
        prime_sample = primes[indices]
    else:
        prime_sample = primes[100:]  # Skip small primes
    
    print(f"    Using sample of {len(prime_sample)} primes")
    
    # Generate composite controls
    print(f"\n[2] Generating composite control sample...")
    composites = generate_composite_controls(primes_set, MAX_PRIME, len(prime_sample))
    print(f"    Generated {len(composites)} composites")
    
    # Store results
    all_results = {}
    
    # =====================================================================
    # HYPOTHESIS 1: Internal N-Gram Frequency Deviation
    # =====================================================================
    print("\n" + "="*70)
    print("TESTING HYPOTHESIS 1: Internal N-Gram Frequency Deviation")
    print("="*70)
    
    h1_results = {}
    for base in BASES:
        for n in N_GRAM_SIZES:
            key = f"B{base}_n{n}"
            h1_results[key] = test_hypothesis_1(prime_sample, composites, base, n)
    
    all_results['H1'] = h1_results
    
    # =====================================================================
    # HYPOTHESIS 2: Base-2 vs Base-10 Pattern Correlation
    # =====================================================================
    print("\n" + "="*70)
    print("TESTING HYPOTHESIS 2: Cross-Base Pattern Correlation")
    print("="*70)
    
    h2_results = {}
    for n in N_GRAM_SIZES:
        h2_results[f"n{n}"] = test_hypothesis_2(prime_sample, 10, n)
    
    all_results['H2'] = h2_results
    
    # =====================================================================
    # HYPOTHESIS 3: Localized Bias in Specific N-Gram Clusters
    # =====================================================================
    print("\n" + "="*70)
    print("TESTING HYPOTHESIS 3: Localized Bias in Specific Patterns")
    print("="*70)
    
    h3_results = {}
    for base in BASES:
        h3_results[f"B{base}"] = test_hypothesis_3(prime_sample, composites, base)
    
    all_results['H3'] = h3_results
    
    # =====================================================================
    # HYPOTHESIS 4: N-Gram Repetition Suppression
    # =====================================================================
    print("\n" + "="*70)
    print("TESTING HYPOTHESIS 4: N-Gram Repetition Suppression")
    print("="*70)
    
    h4_results = {}
    for base in BASES:
        h4_results[f"B{base}"] = test_hypothesis_4(prime_sample, base)
    
    all_results['H4'] = h4_results
    
    # =====================================================================
    # HYPOTHESIS 5: Scale-Invariant N-Gram Structure
    # =====================================================================
    print("\n" + "="*70)
    print("TESTING HYPOTHESIS 5: Scale-Invariant N-Gram Structure")
    print("="*70)
    
    h5_results = {}
    for base in BASES:
        h5_results[f"B{base}"] = test_hypothesis_5(prime_sample, composites, base)
    
    all_results['H5'] = h5_results
    
    # =====================================================================
    # VISUALIZATION
    # =====================================================================
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    try:
        create_visualizations(all_results)
    except Exception as e:
        print(f"Visualization error: {e}")
    
    # =====================================================================
    # FINAL SUMMARY
    # =====================================================================
    print("\n" + "="*70)
    print("FINAL SUMMARY OF HYPOTHESIS TESTS")
    print("="*70)
    
    supported_count = 0
    total_testable = 0
    
    for h_name, h_data in all_results.items():
        print(f"\n{h_name}:")
        if isinstance(h_data, dict):
            for sub_key, sub_val in h_data.items():
                if isinstance(sub_val, dict):
                    sup = sub_val.get('supported', False)
                    testable = sub_val.get('testable', True)
                    status = "SUPPORTED" if sup else "NOT SUPPORTED"
                    if not testable:
                        status = "NOT TESTABLE"
                    print(f"  {sub_key}: {status}")
                    if testable:
                        total_testable += 1
                        if sup:
                            supported_count += 1
    
    print(f"\nOverall: {supported_count}/{total_testable} testable hypotheses supported")
    
    # =====================================================================
    # CONCLUSIONS
    # =====================================================================
    print("\n" + "="*70)
    print("CONCLUSIONS")
    print("="*70)
    
    # Analyze H1 results
    h1_supported = sum(1 for v in h1_results.values() if v.get('supported', False))
    h1_total = len(h1_results)
    
    print(f"""
1. INTERNAL N-GRAM FREQUENCY DEVIATION (H1):
   - Tested across Base-2 and Base-10 for 3-grams and 4-grams
   - Supported in {h1_supported}/{h1_total} conditions
   - Key finding: KL divergences were {'generally above' if h1_supported >= 2 else 'generally below'} 
     the 0.01 threshold, suggesting {'significant' if h1_supported >= 2 else 'minimal'} 
     structural differences between primes and composites in internal digit patterns.
   
2. CROSS-BASE PATTERN CORRELATION (H2):
   - Entropy differences between bases indicate {'some' if any(v.get('entropy_diff', 1) < 0.3 for v in h2_results.values()) else 'limited'}
     base-independent structure in prime digit patterns.
   
3. LOCALIZED BIAS (H3):
   - Specific n-gram clusters show {'systematic bias' if any(v.get('meaningful_bias_rate', 0) > 0.05 for v in h3_results.values()) else 'minimal systematic bias'}
     with meaningful bias rates of {', '.join(f'{v.get("meaningful_bias_rate", 0):.1%}' for v in h3_results.values())}.
   
4. REPETITION SUPPRESSION (H4):
   - Repeating digit patterns (AAA) show {'suppression' if any(v.get('suppression_ratio', 1) < 1.0 for v in h4_results.values()) else 'no clear suppression'}
     with suppression ratios of {', '.join(f'{v.get("suppression_ratio", 1):.3f}' for v in h4_results.values())}.
   
5. SCALE INVARIANCE (H5):
   - N-gram structure {'appears' if any(v.get('supported', False) for v in h5_results.values()) else 'does not appear'} 
     to be scale-invariant across different magnitudes.

OVERALL ASSESSMENT:
The analysis reveals {'subtle but measurable' if supported_count >= 2 else 'minimal'} 
higher-order structural patterns in prime numbers beyond simple digit 
distribution effects. The most robust finding is the {'deviation in internal n-gram frequencies' if h1_supported >= 2 else 'lack of strong deviation in most tested conditions'}, 
suggesting that prime number constraints may manifest in localized, 
higher-order digit sequencing patterns rather than uniform random behavior.

Methodological note: This analysis used internal digits only (excluding first 
and last digits) to control for known constraints (leading digit bias, 
terminal digit constraints). Future work could extend to larger n-grams 
(n≥5) and additional bases.
""")
    
    print("="*70)
    print("Analysis complete.")
    print("="*70)

if __name__ == "__main__":
    np.random.seed(42)
    main()