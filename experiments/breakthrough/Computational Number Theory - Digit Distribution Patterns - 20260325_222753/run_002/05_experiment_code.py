import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import math
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PRIME GENERATION: Segmented Sieve for Efficiency
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
    return np.nonzero(sieve)[0].astype(np.int64)

def segmented_sieve(n):
    """Generate primes up to n using segmented sieve for memory efficiency."""
    if n <= 10**7:  # For smaller n, use simple sieve
        return simple_sieve(n)
    
    # Segmented approach for larger n
    limit = int(n**0.5) + 1
    base_primes = simple_sieve(limit)
    primes = list(base_primes)
    
    segment_size = min(10**6, n // 10)
    low = limit
    
    while low <= n:
        high = min(low + segment_size - 1, n)
        segment = np.ones(high - low + 1, dtype=bool)
        
        for p in base_primes:
            start = ((low + p - 1) // p) * p
            segment[start - low::p] = False
        
        new_primes = np.nonzero(segment)[0].astype(np.int64) + low
        primes.extend(new_primes)
        low = high + 1
    
    return np.array(primes, dtype=np.int64)

# =============================================================================
# BASE CONVERSION AND DIGIT EXTRACTION
# =============================================================================

def to_base_n(num, base):
    """Convert number to digits in given base (most significant first)."""
    if num == 0:
        return [0]
    digits = []
    while num > 0:
        digits.append(num % base)
        num //= base
    return digits[::-1]  # Reverse to get most significant first

def get_leading_digit(num, base):
    """Get leading digit of number in given base."""
    while num >= base:
        num //= base
    return num

def get_terminal_digit(num, base):
    """Get terminal (last) digit of number in given base."""
    return num % base

# =============================================================================
# STATISTICAL TESTS
# =============================================================================

def kl_divergence(observed, expected):
    """Calculate Kullback-Leibler divergence."""
    # Add small epsilon to avoid log(0)
    obs = np.array(observed, dtype=np.float64) + 1e-10
    exp = np.array(expected, dtype=np.float64) + 1e-10
    obs /= obs.sum()
    exp /= exp.sum()
    return np.sum(obs * np.log(obs / exp))

def benford_expected(base):
    """Calculate Benford's Law expected probabilities for given base."""
    # Benford: P(d) = log_base(1 + 1/d) for d = 1 to base-1
    # Or equivalently: log(1 + 1/d) / log(base)
    digits = np.arange(1, base)
    probs = np.log(1 + 1/digits) / np.log(base)
    # Normalize (Benford doesn't include 0 as leading digit)
    return probs / probs.sum()

def chi_square_test(observed, expected):
    """Perform chi-square goodness of fit test."""
    obs = np.array(observed, dtype=np.float64)
    exp = np.array(expected, dtype=np.float64)
    # Scale expected to match observed total
    exp = exp * (obs.sum() / exp.sum())
    # Avoid zero expected
    mask = exp > 0
    chi2 = np.sum((obs[mask] - exp[mask])**2 / exp[mask])
    df = mask.sum() - 1
    p_value = 1 - stats.chi2.cdf(chi2, df) if df > 0 else 0
    return chi2, p_value, df

# =============================================================================
# HYPOTHESIS 1: Base-Specific Benford's Law Deviation
# =============================================================================

def test_hypothesis_1(primes, max_n):
    """Test: Base-2 primes follow Benford's Law better than Base-10, Base-16."""
    print("=" * 70)
    print("HYPOTHESIS 1: Base-Specific Benford's Law Deviation")
    print("Prediction: Base-2 > Base-16 > Base-10 (conformance to Benford's Law)")
    print("=" * 70)
    
    bases = [2, 10, 16]
    results = {}
    
    for base in bases:
        # Skip 2 for primes (only leading digit is 1)
        if base == 2: