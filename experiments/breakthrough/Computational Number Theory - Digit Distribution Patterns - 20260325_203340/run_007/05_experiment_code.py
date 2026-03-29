!@#$
"""
Empirical Extraction and Statistical Analysis of 1st- and 2nd-Order
Markovian Digit Transitions in Base-10 Primes (Range: 10^6 to 10^8)

Hypotheses tested (inferred from research problem due to API error in spec):
  H1: Internal digit 1st-order transitions in primes deviate significantly
      from a uniform distribution (Chi-square test).
  H2: Internal digit 2nd-order transitions in primes deviate significantly
      from a uniform distribution (Chi-square test).
  H3: Prime internal digit transitions differ significantly from those of
      composite numbers in the same range (comparative Chi-square test).
  H4: At least three specific digit transitions exist with anomalous
      frequency relative to composites.
"""

import sys
import time
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ── Chi-square CDF via regularised incomplete gamma (series expansion) ────────
def _gammainc_series(a, x, max_iter=300, tol=1e-12):
    """Lower regularised incomplete gamma P(a, x) via series."""
    if x < 0:
        raise ValueError("x must be >= 0")
    if x == 0:
        return 0.0
    ln_gamma_a = math.lgamma(a)
    term = math.exp(a * math.log(x) - x - ln_gamma_a) / a
    total = term
    for n in range(1, max_iter):
        term *= x / (a + n)
        total += term
        if abs(term) < tol * abs(total):
            break
    return min(total, 1.0)

def _gammainc_cf(a, x, max_iter=300, tol=1e-12):
    """Upper regularised incomplete gamma Q(a, x) via continued fraction."""
    ln_gamma_a = math.lgamma(a)
    f = x + 1.0 - a
    C = f
    D = 0.0
    b0 = x + 1.0 - a
    if abs(b0) < 1e-30:
        b0 = 1e-30
    D = 1.0 / b0
    C = b0
    result = D
    for i in range(1, max_iter):
        an = -i * (i - a)
        b = x + 2 * i + 1.0 - a
        D = b + an * D
        if abs(D) < 1e-30:
            D = 1e-30
        C = b + an / C
        if abs(C) < 1e-30:
            C = 1e-30
        D = 1.0 / D
        delta = C * D
        result *= delta
        if abs(delta - 1.0) < tol:
            break
    return math.exp(a * math.log(x) - x - ln_gamma_a) * result

def chi2_sf(chi2_stat, df):
    """Survival function (1 - CDF) of chi-squared distribution."""
    if chi2_stat <= 0:
        return 1.0
    a = df / 2.0
    x = chi2_stat / 2.0
    if x < a + 1.0:
        p = _gammainc_series(a, x)
        return 1.0 - p
    else:
        return _gammainc_cf(a, x)

# ─────────────────────────────────────────────────────────────────────────────
# PRIME SIEVE  (segmented numpy sieve, memory-efficient)
# ─────────────────────────────────────────────────────────────────────────────

def segmented_sieve(lo, hi, segment_size=2**20):
    """
    Yield all primes in [lo, hi] using a segmented sieve.
    Memory O(sqrt(hi) + segment_size).
    """
    limit = int(hi**0.5) + 1
    small = np.ones(limit + 1, dtype=bool)
    small[0] = small[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if small[i]:
            small[i*i::i] = False
    small_primes = np.nonzero(small)[0]

    lo = max(lo, 2)
    for seg_lo in range(lo, hi + 1, segment_size):
        seg_hi = min(seg_lo + segment_size - 1, hi)
        size = seg_hi - seg_lo + 1
        sieve = np.ones(size, dtype=bool)
        for p in small_primes:
            if p * p > seg_hi:
                break
            start = ((seg_lo + p - 1) // p) * p
            if start == p:
                start += p
            sieve[start - seg_lo::p] = False
        if seg_lo <= 1:
            sieve[max(0, 1 - seg_lo)] = False
        if seg_lo == 0:
            sieve[0] = False
        primes_in_seg = np.nonzero(sieve)[0] + seg_lo
        yield primes_in_seg

def get_all_primes(lo, hi):
    chunks = []
    for chunk in segmented_sieve(lo, hi):
        chunks.append(chunk)
    return np.concatenate(chunks)

# ─────────────────────────────────────────────────────────────────────────────
# DIGIT TRANSITION EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def extract_internal_digits_vectorised(numbers):
    all_internal = []
    num_list = numbers.tolist()
    for n in num_list:
        s = str(n)
        if len(s) < 3:
            continue
        internal = [int(c) for c in s[1:-1]]
        if len(internal) >= 1:
            all_internal.append(internal)
    return all_internal

def build_transition_matrices(internal_seqs):
    mat1 = np.zeros((10, 10), dtype=np.int64)
    mat2 = np.zeros((100, 10), dtype=np.int64)

    for seq in internal_seqs:
        n = len(seq)
        if n < 2:
            continue
        for i in range(n - 1):
            mat1[seq[i], seq[i+1]] += 1
        if n < 3:
            continue
        for i in range(n - 2):
            pair_idx = seq[i] * 10 + seq[i+1]
            mat2[pair_idx, seq[i+2]] += 1

    return mat1, mat2

def count_to_prob(mat):
    row_sums = mat.sum(axis=1, keepdims=True).astype(float)
    row_sums[row_sums == 0] = 1
    return mat / row_sums

def chi2_test_uniform(count_matrix):
    total_chi2 = 0.0
    total_df = 0
    for row in count_matrix:
        n = row.sum()
        if n == 0:
            continue
        expected = n / 10.0
        chi2_stat = np.sum((row - expected)**2 / expected)
        total_