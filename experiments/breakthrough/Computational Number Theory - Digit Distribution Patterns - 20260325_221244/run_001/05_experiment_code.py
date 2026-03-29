import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter
import math

# =============================================================================
# EFFICIENT PRIME GENERATION (Segmented Sieve)
# =============================================================================

def simple_sieve(limit):
    """Generate primes up to limit using simple sieve."""
    if limit < 2:
        return []
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return np.where(sieve)[0].tolist()

def segmented_sieve(low, high):
    """Generate primes in range [low, high) using segmented sieve."""
    if high <= low:
        return []
    
    limit = int(high**0.5) + 1
    base_primes = simple_sieve(limit)
    
    # Size of segment
    segment_size = min(32768, high - low)
    primes = []
    
    for seg_start in range(low, high, segment_size):
        seg_end = min(seg_start + segment_size, high)
        sieve = np.ones(seg_end - seg_start, dtype=bool)
        
        for p in base_primes:
            if p * p >= seg_end:
                break
            # First multiple of p in segment
            start = ((seg_start + p - 1) // p) * p
            if start < p * p:
                start = p * p
            sieve[start - seg_start::p] = False
        
        # Collect primes from this segment
        segment_primes = np.where(sieve)[0] + seg_start
        # Filter: must be >= 2 and actually prime (sieve may include 1)
        segment_primes = segment_primes[(segment_primes >= 2) & (segment_primes < seg_end)]
        primes.extend(segment_primes.tolist())
    
    return primes

# =============================================================================
# DIGIT UTILITIES
# =============================================================================

def get_digits(n, base=10):
    """Get digits of n in given base (most significant first)."""
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return digits[::-1]  # Reverse to get most significant first

def get_last_digit(n, base=10):
    """Get last digit of n in given base."""
    return n % base

def build_transition_matrix(numbers, base=10):
    """
    Build digit transition matrix for given numbers.
    Returns (transition_matrix, total_transitions_per_digit)
    """
    # Count transitions: from_digit -> to_digit
    transitions = np.zeros((base, base), dtype=np.int64)
    digit_counts = np.zeros(base, dtype=np.int64)  # Count of each digit as "from"
    
    for n in numbers:
        digits = get_digits(n, base)
        if len(digits) < 2:
            continue
        for i in range(len(digits) - 1):
            from_d = digits[i]
            to_d = digits[i+1]
            transitions[from_d, to_d] += 1
            digit_counts[from_d] += 1
    
    # Convert to probabilities (avoid division by zero)
    trans_prob = np.zeros((base, base), dtype=np.float64)
    for i in range(base):
        if digit_counts[i] > 0:
            trans_prob[i, :] = transitions[i, :] / digit_counts[i]
    
    return trans_prob, transitions, digit_counts

def build_position_digit_distribution(numbers, base=10, max_positions=10):
    """Build distribution of digits by position from right (0=units)."""
    position_counts = [Counter() for _ in range(max_positions)]
    
    for n in numbers:
        digits = get_digits(n, base)
        # Pad with leading zeros conceptually, but we only care about actual digits
        # Position 0 = rightmost digit (units)
        rev_digits = digits[::-1]
        for pos, d in enumerate(rev_digits[:max_positions]):
            position_counts[pos][d] += 1
    
    return position_counts

# =============================================================================
# RANDOM BASELINE GENERATORS
# =============================================================================

def generate_random_odds(n, low, high, exclude_5=True):
    """Generate n random odd numbers in [low, high), optionally excluding those ending in 5."""
    result = []
    attempts = 0
    max_attempts = n * 100
    
    while len(result) < n and attempts < max_attempts:
        # Generate random odd number
        r = np.random.randint(low // 2, (high + 1) // 2) * 2 + 1
        if r < low:
            r += 2
        if r >= high:
            continue
        
        if exclude_5 and r % 10 == 5:
            attempts += 1
            continue
        
        result.append(r)
        attempts += 1
    
    return result

# =============================================================================
# STATISTICAL TESTS
# =============================================================================

def chi_square_test(observed, expected):
    """Perform chi-square test, handling zero expected values."""
    mask = expected > 0
    if np.sum(mask) < 2:
        return np.nan, 1.0
    
    chi2 = np.sum((observed[mask] - expected[mask])**2 / expected[mask])
    df = np.sum(mask) - 1
    p_value = 1 - stats.chi2.cdf(chi2, df) if df > 0 else 1.0
    return chi2, p_value

def z_score_test(observed, expected, total):
    """Calculate z-score for observed vs expected proportion."""
    if expected <= 0