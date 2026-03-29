!@#$
"""
Research: Markovian Transition Matrices of Internal Digits in Base-2 and Base-10 Primes
Tests hypotheses about non-uniform digit transitions in prime numbers.
"""

import sys
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.stats import chi2_contingency
from scipy.stats import chi2 as chi2_dist
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────
LIMIT = 10_000_000          # sieve up to 10^7 (fast enough for <2 min)
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

print("=" * 70)
print("Markovian Transition Analysis of Internal Digits in Prime Numbers")
print(f"Sieve limit: {LIMIT:,}")
print("=" * 70)
t0 = time.time()

# ─────────────────────────────────────────────────────────────
# STEP 1 – Prime / Composite generation via Sieve of Eratosthenes
# ─────────────────────────────────────────────────────────────
def sieve(n):
    """Return boolean array; is_prime[k] == True iff k is prime."""
    is_p = np.ones(n + 1, dtype=bool)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            is_p[i*i::i] = False
    return is_p

print("\n[1] Running Sieve of Eratosthenes …", end=" ", flush=True)
is_prime = sieve(LIMIT)
primes     = np.where(is_prime)[0].astype(np.int32)
composites = np.where(~is_prime & (np.arange(LIMIT + 1) > 3))[0].astype(np.int32)
# keep only odd composites (closest baseline to odd primes > 2)
odd_composites = composites[composites % 2 == 1]
print(f"done  ({time.time()-t0:.1f}s)  |  primes: {len(primes):,}  |  odd composites: {len(odd_composites):,}")

# ─────────────────────────────────────────────────────────────
# STEP 2 – Helper: build transition matrix from a sequence of integers
# ─────────────────────────────────────────────────────────────

def build_transition_matrix(numbers, base, strip_last=True):
    """
    Build an (base x base) transition count matrix for INTERNAL digits.
    'Internal' = all digits except the last (terminal) one.
    Numbers with fewer than 3 digits (in given base) are skipped because
    stripping the terminal digit leaves nothing to form a pair.
    """
    mat = np.zeros((base, base), dtype=np.int64)
    for n in numbers:
        if base == 10:
            s = str(n)
        else:
            s = bin(n)[2:]          # strip '0b' prefix
        if strip_last:
            s = s[:-1]              # remove terminal digit
        if len(s) < 2:
            continue
        for i in range(len(s) - 1):
            d_i   = int(s[i],   base)
            d_ip1 = int(s[i+1], base)
            mat[d_i, d_ip1] += 1
    return mat

def normalize_rows(mat):
    """Row-normalize a count matrix to get transition probabilities."""
    row_sums = mat.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1           # avoid div-by-zero for empty rows
    return mat / row_sums

# ─────────────────────────────────────────────────────────────
# STEP 3 – Build matrices
# ─────────────────────────────────────────────────────────────
# Work on primes >= 100 (need ≥3 base-10 digits so internal seq is non-empty)
primes_b10    = primes[primes >= 100]
composites_b10 = odd_composites[odd_composites >= 100]

# For base-2 we need numbers where bin representation has ≥ 3 bits (n >= 4)
primes_b2     = primes[primes >= 7]          # 7 = 0b111 → internal='11' OK
composites_b2 = odd_composites[odd_composites >= 7]

print("\n[2] Building Base-10 transition matrices …", end=" ", flush=True)
cnt_p10  = build_transition_matrix(primes_b10,     base=10, strip_last=True)
cnt_c10  = build_transition_matrix(composites_b10, base=10, strip_last=True)
print(f"done  ({time.time()-t0:.1f}s)")

print("[3] Building Base-2  transition matrices …", end=" ", flush=True)
cnt_p2   = build_transition_matrix(primes_b2,     base=2, strip_last=True)
cnt_c2   = build_transition_matrix(composites_b2, base=2, strip_last=True)
print(f"done  ({time.time()-t0:.1f}s)")

prob_p10 = normalize_rows(cnt_p10)
prob_c10 = normalize_rows(cnt_c10)
prob_p2  = normalize_rows(cnt_p2)
prob_c2  = normalize_rows(cnt_c2)

# ─────────────────────────────────────────────────────────────
# STEP 4 – Statistical Testing
# ─────────────────────────────────────────────────────────────

def chi2_test_matrix(obs, exp_counts):
    """
    Cell-wise chi-squared test using:
        chi2 = sum( (O - E)^2 / E )  over all cells with E > 0
    Returns chi2 statistic, p-value, degrees of freedom.
    """
    mask = exp_counts > 0
    o = obs[mask].astype(float)
    e = exp_counts[mask].astype(float)
    # scale expected to same total as observed
    e = e * (o.sum() / e.sum())
    chi2_stat = np.sum((o - e) ** 2 / e)
    dof = mask.sum() - 1
    p_val = 1.0 - chi2_dist.cdf(chi2_stat, dof)
    return chi2_stat, p_val, dof

def row_chi2(obs_row, exp_row):
    """Chi-squared test for a single row (one source digit)."""
    mask = exp_row > 0
    if mask.sum