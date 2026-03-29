!@#$
#!/usr/bin/env python3
"""
Prime Digit Sequencing Research Script
Tests 5 hypotheses about digit patterns in prime numbers across bases.
"""

import sys
import math
import time
from collections import Counter
from typing import List, Tuple, Dict

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from scipy import stats

# =============================================================================
# CONFIGURATION
# =============================================================================

MAX_PRIME = 10_000_000  # 10^7
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# =============================================================================
# PRIME GENERATION (Segmented Sieve for memory efficiency)
# =============================================================================

def simple_sieve(limit: int) -> List[int]:
    """Generate primes up to limit using simple sieve."""
    sieve = bytearray(b'\x01') * (limit + 1)
    sieve[0:2] = b'\x00\x00'
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00' * ((limit - i*i) // i + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def segmented_sieve(n: int) -> np.ndarray:
    """
    Memory-efficient segmented sieve to generate primes up to n.
    Returns numpy array of primes.
    """
    if n < 2:
        return np.array([], dtype=np.int64)
    
    # Small primes for sieving segments
    limit = int(math.sqrt(n)) + 1
    small_primes = simple_sieve(limit)
    
    # Estimate number of primes: n / log(n)
    estimated_count = max(100, int(n / math.log(n + 1)) + 1000)
    primes = np.zeros(estimated_count, dtype=np.int64)
    count = 0
    
    # Add small primes
    for p in small_primes:
        if p > n:
            break
        primes[count] = p
        count += 1
    
    # Segment size optimized for cache
    segment_size = min(32768, max(1000, limit))
    
    for low in range(max(limit, 2), n + 1, segment_size):
        high = min(low + segment_size - 1, n)
        sieve = bytearray(b'\x01') * (high - low + 1)
        
        for p in small_primes:
            if p * p > high:
                break
            # Start at first multiple of p >= low
            start = ((low + p - 1) // p) * p
            if start < p * p:
                start = p * p
            sieve[start - low::p] = b'\x00' * ((high - start) // p + 1)
        
        for i, is_prime in enumerate(sieve):
            if is_prime:
                if count >= len(primes):
                    # Expand array if needed
                    new_primes = np.zeros(len(primes) * 2, dtype=np.int64)
                    new_primes[:count] = primes[:count]
                    primes = new_primes
                primes[count] = low + i
                count += 1
    
    return primes[:count]

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def to_base(n: int, base: int) -> List[int]:
    """Convert number to list of digits in given base (MSB first)."""
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    return digits[::-1]

def to_base_str(n: int, base: int) -> str:
    """Convert number to string representation in given base."""
    if base == 10:
        return str(n)
    elif base == 16:
        return hex(n)[2:].upper()
    elif base == 2:
        return bin(n)[2:]
    else:
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = []
        while n > 0:
            result.append(digits[n % base])
            n //= base
        return ''.join(reversed(result))

def digit_sum(n: int, base: int = 10) -> int:
    """Sum of digits in given base."""
    total = 0
    while n > 0:
        total += n % base
        n //= base
    return total

def generate_random_odds(n: int, count: int, exclude_div5: bool = True) -> np.ndarray:
    """Generate random odd numbers for comparison."""
    # Generate random odd numbers in range [3, n]
    # Ensure they're odd and not divisible by 5 if requested
    result = []
    attempts = 0
    max_attempts = count * 100
    
    while len(result) < count and attempts < max_attempts:
        num = np.random.randint(2, n + 1)
        if num % 2 == 0:
            num += 1
        if num > n:
            continue
        if exclude_div5 and num % 5 == 0:
            continue
        result.append(num)
        attempts += 1
    
    return np.array(result, dtype=np.int64)

# =============================================================================
# HYPOTHESIS TESTING
# =============================================================================

class PrimeResearch:
    def __init__(self, max_prime: int = MAX_PRIME):
        self.max_prime = max_prime
        self.primes = None
        self.prime_set = None
        self.random_odds = None
        
    def generate_data(self):
        """Generate primes and comparison data."""
        print(f"Generating primes up to {self.max_prime:,}...")
        t0 = time.time()
        self.primes = segmented_sieve(self.max_prime)
        self.prime_set = set(self.primes)
        print(f"  Found {len(self.primes):,} primes in {time.time()-t0:.2f}s")
        
        # Generate comparable random odd numbers (excluding multiples of 5)
        print("Generating random odd numbers for comparison...")
        self.random_odds = generate_random_odds(
            self.max_prime, 
            min(len(self.primes), 500_000),
            exclude_div5=True
        )
        print(f"  Generated {len(self.random_odds):,} random odds")
        
    # -------------------------------------------------------------------------
    # HYPOTHESIS 1: Internal Digit Transition Bias
    # -------------------------------------------------------------------------
    
    def test_hypothesis_1(self) -> Dict:
        """
        H1: Internal digit pairs in primes show non-uniform transition probabilities.
        """
        print("\n" + "="*70)
        print("HYPOTHESIS 1: Internal Digit Transition Bias")
        print("="*70)
        
        # Focus on primes > 100 to have sufficient internal digits
        large_primes = self.primes[self.primes >= 100]
        
        # Build transition matrices for internal digits (excluding last digit)
        prime_transitions = np.zeros((10, 10), dtype=np.int64)
        random_transitions = np.zeros((10,