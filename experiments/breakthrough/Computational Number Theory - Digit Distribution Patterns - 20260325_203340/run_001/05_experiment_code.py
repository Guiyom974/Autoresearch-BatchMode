!@#$
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import defaultdict
import time
import math

# ─────────────────────────────────────────────
# 0.  PRIME SIEVE
# ─────────────────────────────────────────────
def sieve_of_eratosthenes(limit):
    """Return array of primes up to `limit`."""
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return np.where(is_prime)[0]

# ─────────────────────────────────────────────
# 1.  BASELINE: generate "pseudo-random odd numbers not div by 2/3/5"
#     to sanity-check that discovered patterns are prime-specific
# ─────────────────────────────────────────────
def generate_baseline(limit, rng_seed=42):
    """
    Odd numbers up to `limit` that are NOT divisible by 2, 3 or 5.
    These mimic the modular constraints primes satisfy without being prime.
    """
    rng = np.random.default_rng(rng_seed)
    candidates = np.arange(7, limit, 2)          # odd, ≥7
    mask = (candidates % 3 != 0) & (candidates % 5 != 0)
    filtered = candidates[mask]
    # subsample to match prime count
    return filtered

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("  DIGIT SEQUENCING & BASE-N DISTRIBUTION PATTERNS IN PRIME NUMBERS")
print("=" * 70)

LIMIT = 10_000_000

t0 = time.time()
print(f"\n[0] Generating primes up to {LIMIT:,} …", flush=True)
primes = sieve_of_eratosthenes(LIMIT)
print(f"    Found {len(primes):,} primes in {time.time()-t0:.2f}s")

# baseline numbers
baseline = generate_baseline(LIMIT)
# trim baseline to same length for fair comparison
rng = np.random.default_rng(0)
baseline = rng.choice(baseline, size=len(primes), replace=False)
baseline.sort()
print(f"    Baseline set: {len(baseline):,} pseudo-random coprime-to-30 numbers")

# ─────────────────────────────────────────────────────────────────────────────
# HYPOTHESIS 1 – Digit Transition Probabilities in Base-10
# Build a 10×10 transition matrix: for every adjacent digit pair (d_i, d_{i+1})
# within the decimal representation of each prime, count transitions.
# Chi-square test vs uniform row distribution.
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─"*70)
print("HYPOTHESIS 1: Base-10 digit transition matrix (Markov chain analysis)")
print("─"*70)

def build_transition_matrix(numbers, base=10):
    """Count adjacent-digit transitions inside each number."""
    mat = np.zeros((base, base), dtype=np.int64)
    for n in numbers:
        s = []
        tmp = int(n)
        while tmp:
            s.append(tmp % base)
            tmp //= base
        s.reverse()
        for i in range(len(s) - 1):
            mat[s[i]][s[i+1]] += 1
    return mat

t1 = time.time()
trans_prime    = build_transition_matrix(primes,   base=10)
trans_baseline = build_transition_matrix(baseline, base=10)
print(f"    Transition matrices built in {time.time()-t1:.2f}s")

def chi2_stat_and_p(observed):
    """
    Row-wise chi-square goodness-of-fit vs uniform.
    Returns (chi2_stat, p_value) for each row.
    Manual calculation – no scipy needed.
    """
    results = []
    n_cats = len(observed)
    for row in observed:
        total = row.sum()
        if total == 0:
            results.append((np.nan, np.nan))
            continue
        expected = total / n_cats
        stat = np.sum((row - expected)**2 / expected)
        df = n_cats - 1
        try:
            p_val = math.gammaincc(df / 2, stat / 2)   # Python 3.11
        except AttributeError:
            p_val = float('nan')
        results.append((stat, p_val))
    return results

# Normalize rows to probabilities
def row_normalize(mat):
    row_sums = mat.sum(axis=1, keepdims=True).astype(float)
    row_sums[row_sums == 0] = 1
    return mat / row_sums

prime_prob    = row_normalize(trans_prime)
baseline_prob = row_normalize(trans_baseline)

# Deviation matrix: prime - baseline
deviation = prime_prob - baseline_prob

print("\n  Top-10 digit transitions (prime) with highest absolute deviation vs baseline:")
dev_flat = [(abs(deviation[i,j]), i, j, prime_prob[i,j], baseline_prob[i,j])
            for i in range(10) for j in range(10)]
dev_flat.sort(reverse=True)
print(f"  {'From→To':>8}  {'|Δ|':>8}  {'Prime P':>10}  {'Baseline P':>12}  {'Significant?':>12}")
sig_h1 = []
for rank, (dev, fi, ti, pp, bp) in enumerate(dev_flat[:10]):
    n1 = trans_prime[fi].sum();    p1 = pp
    n2 = trans_baseline[fi].sum(); p2 = bp
    if n1 > 0 and n2 > 0:
        p_pool = (trans_prime[fi,ti] + trans_baseline[fi,ti]) / (n1 + n2)
        se = math.sqrt(p_pool*(1-p_pool)*(1/n1 + 1/n2)) if p_pool*(1-p_pool) > 0 else 1e-9
        z = (p1 - p2) / se