!@#$
"""
High-Resolution Analysis of 1st- and 2nd-Order Markovian Digit Transitions
in Base-10 Primes (10^6 to 10^8)

Hypotheses tested (inferred from research problem due to API error in spec):
  H1: Internal 1st-order digit transition probabilities of primes differ
      significantly from a uniform distribution (chi-square GoF).
  H2: Specific 2nd-order Markovian chains in primes show anomalous
      suppression/enhancement vs. odd composites (chi-square homogeneity).
  H3: The 1st-order transition probability matrix evolves measurably as
      prime magnitude increases across the 10^6–10^8 range.
"""

import sys
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

try:
    from scipy.stats import chi2 as _chi2
    def chi2_pvalue(stat, df):
        return float(_chi2.sf(stat, df))
except ImportError:
    import math
    def _lgamma(x):
        return math.lgamma(x)
    def chi2_pvalue(stat, df):
        k = df / 2.0
        x = stat / 2.0
        if x <= 0:
            return 1.0
        try:
            log_p = k * math.log(x) - x - _lgamma(k + 1)
            return min(1.0, math.exp(log_p) * 2)
        except Exception:
            return float("nan")

LOW  = 10**6
HIGH = 10**8
BANDS = [
    (10**6,   int(10**6.67)),
    (int(10**6.67), int(10**7.33)),
    (int(10**7.33), 10**8),
]
BAND_LABELS = ["10^6–10^{6.67}", "10^{6.67}–10^{7.33}", "10^{7.33}–10^8"]
MAX_COMPOSITES = 2_000_000
MAX_PRIMES_STAT = 5_000_000
ALPHA = 0.01

print("=" * 70)
print("STEP 1: Generating primes via segmented Sieve of Eratosthenes ...")
t0 = time.time()
LIMIT = HIGH

def segmented_sieve(limit):
    sqrt_limit = int(limit**0.5) + 1
    small = np.ones(sqrt_limit + 1, dtype=np.bool_)
    small[0] = small[1] = False
    for i in range(2, int(sqrt_limit**0.5) + 1):
        if small[i]:
            small[i*i::i] = False
    small_primes = np.nonzero(small)[0]
    seg_size = max(sqrt_limit, 2**19)
    primes_list = [small_primes[small_primes < sqrt_limit]]
    for low in range(sqrt_limit, limit + 1, seg_size):
        high = min(low + seg_size - 1, limit)
        sieve = np.ones(high - low + 1, dtype=np.bool_)
        for p in small_primes:
            start = max(p * p, ((low + p - 1) // p) * p)
            if start > high:
                continue
            sieve[start - low::p] = False
        if low <= 1:
            if 0 >= low: sieve[0 - low] = False
            if 1 >= low: sieve[1 - low] = False
        primes_list.append(np.nonzero(sieve)[0] + low)
    return np.concatenate(primes_list)

all_primes = segmented_sieve(LIMIT)
mask = (all_primes > LOW) & (all_primes < HIGH)
primes = all_primes[mask]
print(f"  Found {len(primes):,} primes in ({LOW}, {HIGH})  [{time.time()-t0:.1f}s]")

print("\nSTEP 2: Extracting odd composite control set ...")
t1 = time.time()
prime_set_full = set(all_primes.tolist())
rng = np.random.default_rng(42)
candidates = np.arange(LOW + 1, HIGH, 2, dtype=np.int64)
is_prime_flag = np.zeros(len(candidates), dtype=np.bool_)
idx = np.searchsorted(primes, candidates)
idx = np.clip(idx, 0, len(primes) - 1)
is_prime_flag = (primes[idx] == candidates)
composites_all_idx = np.nonzero(~is_prime_flag)[0]
if len(composites_all_idx) > MAX_COMPOSITES:
    chosen = rng.choice(composites_all_idx, size=MAX_COMPOSITES, replace=False)
    chosen.sort()
else:
    chosen = composites_all_idx
composites = candidates[chosen]
print(f"  Sampled {len(composites):,} odd composites  [{time.time()-t1:.1f}s]")

print("\nSTEP 3: Extracting internal digit sequences ...")
t2 = time.time()

def internal_digits_array(numbers):
    seqs = []
    for n in numbers:
        s = str(n)
        internal = s[1:-1]
        if len(internal) >= 2:
            seqs.append(np.frombuffer(internal.encode(), dtype=np.uint8) - ord('0'))
    return seqs

if len(primes) > MAX_PRIMES_STAT:
    idx_p = rng.choice(len(primes), size=MAX_PRIMES_STAT, replace=False)
    idx_p.sort()
    primes_use = primes[idx_p]
else:
    primes_use = primes

prime_seqs    = internal_digits_array(primes_use)
composite_seqs = internal_digits_array(composites)
print(f"  Prime sequences: {len(prime_seqs):,}  |  Composite sequences: {len(composite_seqs):,}")
print(f"  [{time.time()-t2:.1f}s]")

def build_first_order_matrix(seqs):
    M = np.zeros((10, 10), dtype=np.int64)