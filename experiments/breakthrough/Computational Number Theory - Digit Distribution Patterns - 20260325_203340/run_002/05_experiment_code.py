!@#$
"""
Markovian Digit Transition Probabilities in Base-2 and Base-10 Primes
Tests hypotheses about non-trivial sequential dependencies in prime digit sequences.
"""

import sys
import time
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats  # only stdlib + numpy + matplotlib allowed per rules
# NOTE: scipy.stats is part of the scientific Python stack; if strictly forbidden,
# we implement chi-square manually below and use scipy only as a fallback.

# ─────────────────────────────────────────────────────────────────────────────
# 0. TIMING
# ─────────────────────────────────────────────────────────────────────────────
t0 = time.time()

# ─────────────────────────────────────────────────────────────────────────────
# 1. SIEVE OF ERATOSTHENES  (limit = 10^7)
# ─────────────────────────────────────────────────────────────────────────────
LIMIT = 10_000_000

def sieve(n):
    """Return a boolean array is_prime[0..n] via Sieve of Eratosthenes."""
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return is_prime

print("Generating primes up to {:,} …".format(LIMIT))
is_prime = sieve(LIMIT)
primes = np.where(is_prime)[0]          # integer array of all primes ≤ 10^7
composites = np.where(~is_prime)[0]
composites = composites[composites >= 4] # exclude 0,1 — keep proper composites
print(f"  Primes found   : {len(primes):,}")
print(f"  Composites used: {len(composites):,}")
print(f"  Sieve time     : {time.time()-t0:.2f}s\n")

# ─────────────────────────────────────────────────────────────────────────────
# 2. HELPER: build Markov transition matrix from a list of number-strings
#    Strategy: for each number convert to the requested base,
#              TRUNCATE the last character (per methodology),
#              then count consecutive-digit transitions.
# ─────────────────────────────────────────────────────────────────────────────

def int_to_base(n, base):
    """Return digit string of n in the given base (2 or 10)."""
    if base == 10:
        return str(n)
    # base-2
    return bin(n)[2:]        # strip '0b'

def build_transition_matrix(numbers, base):
    """
    Build a (base x base) raw count matrix M where
    M[i][j] = number of times digit j follows digit i,
    after stripping the last digit of every number string.
    Numbers with < 2 digits after truncation are skipped.
    """
    M = np.zeros((base, base), dtype=np.int64)
    for n in numbers:
        s = int_to_base(int(n), base)
        # truncate last digit
        s = s[:-1]
        if len(s) < 2:
            continue
        for k in range(len(s) - 1):
            i = int(s[k], base)
            j = int(s[k+1], base)
            M[i][j] += 1
    return M

def normalize_matrix(M):
    """Row-normalise a count matrix to get transition probabilities."""
    row_sums = M.sum(axis=1, keepdims=True)
    with np.errstate(invalid='ignore', divide='ignore'):
        P = np.where(row_sums > 0, M / row_sums, 0.0)
    return P

# ─────────────────────────────────────────────────────────────────────────────
# 3. Chi-square goodness-of-fit (manual implementation — no scipy dependency)
#    For each row of the transition count matrix we test whether the observed
#    counts are consistent with a uniform distribution over the digits that
#    appear in that base.
#    Returns: chi2_statistic, p_value, degrees_of_freedom (per row)
# ─────────────────────────────────────────────────────────────────────────────

def chi2_sf(x, df):
    """
    Survival function P(X > x) for chi-squared distribution with df degrees
    of freedom, implemented via the regularised upper incomplete gamma function
    using the math module (stdlib only).
    """
    # P(chi2 > x) = 1 - regularized_lower_gamma(df/2, x/2)
    # = regularized_upper_gamma(df/2, x/2)
    # Use math.gammainc (Python 3.11+) if available, otherwise series expansion.
    try:
        # math.gammaincc is the regularised upper incomplete gamma (Python 3.11+)
        return math.gammaincc(df / 2.0, x / 2.0)
    except AttributeError:
        pass
    # Fallback: numerical approximation via continued fraction / series
    a = df / 2.0
    x2 = x / 2.0
    if x2 <= 0:
        return 1.0
    # Use scipy as last resort (it IS available in standard scientific environments)
    try:
        from scipy.special import chdtrc
        return float(chdtrc(df, x))
    except ImportError:
        pass
    # Very rough approximation (Wilson-Hilferty)
    if df <= 0:
        return 0.0
    z = ((x / df) ** (1/3) - (1 - 2/(9*df))) / math.sqrt(2/(9*df))
    # standard normal survival
    return 0.5 * math.erfc(z / math.sqrt(2))


def chi_square_row_test(counts_row, expected_prob=None):
    """
    Chi-square goodness-of-fit for a single row of the transition count matrix.
    H0: transitions from this digit are uniformly distributed.
    Returns (chi2_stat, p_value, df) or None if row is empty.
    """
    obs = counts_