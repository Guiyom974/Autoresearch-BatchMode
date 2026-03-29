!@#$
"""
Robust Statistical Extraction of 1st- and 2nd-Order Markovian Digit Transitions
in Internal Base-10 Primes (10^6 to 10^8)

NOTE: The hypotheses section contained an API error message, so hypotheses are
inferred directly from the research problem description:

H1: Internal digits of primes (10^6–10^8) exhibit non-uniform 1st-order
    Markovian transition probabilities (i.e., P(D_i|D_{i-1}) ≠ 1/10 for all pairs).
H2: Internal digits of primes exhibit non-uniform 2nd-order Markovian
    transition probabilities beyond what 1st-order captures.
H3: Prime internal-digit transition matrices differ significantly from those
    of composite numbers in the same range.
H4: Specific digit pairs or triplets exhibit statistically significant
    localized biases (higher or lower frequency than uniform expectation).
"""

import sys
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.stats import chi2  # only scipy.stats used for chi2 distribution CDF

# ---------------------------------------------------------------------------
# 0. Utility: chi-square test without scipy.stats.chi2_contingency
#    (uses numpy only for computation, scipy.stats.chi2 for p-value)
# ---------------------------------------------------------------------------
try:
    from scipy.stats import chi2 as _chi2_dist
    _has_scipy = True
except ImportError:
    _has_scipy = False

def chi2_pvalue(chi2_stat, dof):
    """Return p-value for chi-square statistic and degrees of freedom."""
    if _has_scipy:
        return 1.0 - _chi2_dist.cdf(chi2_stat, dof)
    # fallback: very rough approximation via regularised gamma (not used if scipy present)
    return float('nan')

# ---------------------------------------------------------------------------
# 1. Sieve of Eratosthenes up to N
# ---------------------------------------------------------------------------
def sieve_of_eratosthenes(limit):
    """Return boolean array: is_prime[i] == True iff i is prime, 0 <= i <= limit."""
    is_prime = np.ones(limit + 1, dtype=np.bool_)
    is_prime[0] = False
    is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return is_prime

# ---------------------------------------------------------------------------
# 2. Extract internal digit sequences
#    "internal" = all digits strictly between first and last digit
#    For a 7-digit number like 1234567 → internal = "23456"
# ---------------------------------------------------------------------------
def extract_internal_digits(numbers_array):
    """
    Given a numpy array of integers, return a list of numpy int8 arrays
    representing the internal digit sequences (first & last digit stripped).
    Only numbers with at least 3 digits (i.e., at least 1 internal digit)
    are included; for Markov transitions we need at least 2 internal digits
    so only numbers with >= 4 digits (>= 2 internal digits) qualify.
    Numbers in 10^6–10^8 have 7–9 digits → 5–7 internal digits each. Fine.
    """
    sequences = []
    for n in numbers_array:
        s = str(n)
        internal = s[1:-1]          # strip first and last digit
        if len(internal) >= 2:      # need at least 2 for a transition
            sequences.append(np.array([int(c) for c in internal], dtype=np.int8))
    return sequences

# ---------------------------------------------------------------------------
# 3. Build 1st-order transition count matrix (10 x 10)
# ---------------------------------------------------------------------------
def build_first_order_counts(sequences):
    """Count matrix C[i,j] = number of times digit i is followed by digit j."""
    C = np.zeros((10, 10), dtype=np.int64)
    for seq in sequences:
        for k in range(len(seq) - 1):
            C[seq[k], seq[k+1]] += 1
    return C

# ---------------------------------------------------------------------------
# 4. Build 2nd-order transition count tensor (10 x 10 x 10)
#    C[i,j,k] = count of (i→j→k)
# ---------------------------------------------------------------------------
def build_second_order_counts(sequences):
    """Count tensor C[i,j,k] = times digit pair (i,j) is followed by k."""
    C = np.zeros((10, 10, 10), dtype=np.int64)
    for seq in sequences:
        for k in range(len(seq) - 2):
            C[seq[k], seq[k+1], seq[k+2]] += 1
    return C

# ---------------------------------------------------------------------------
# 5. Counts → probability matrix (row-normalised)
# ---------------------------------------------------------------------------
def counts_to_prob(C):
    """Row-normalise: P[i, ...] = C[i, ...] / sum(C[i, ...])."""
    row_sums = C.sum(axis=-1, keepdims=True)
    with np.errstate(invalid='ignore', divide='ignore'):
        P = np.where(row_sums > 0, C / row_sums, 0.0)
    return P

# ---------------------------------------------------------------------------
# 6. KL divergence from uniform (base-10)
# ---------------------------------------------------------------------------
def kl_from_uniform(prob_matrix):
    """
    KL(P || U) where U = 1/10 for each possible next digit.
    Computed row by row; rows with zero mass are skipped.
    Returns total KL divergence (sum over all context states).
    """
    uniform = 1.0 / 10.0
    kl_total = 0.0
    rows = prob_matrix.reshape(-1, 10)
    for row in rows:
        row_sum = row.sum()
        if row_sum < 1e-12:
            continue
        for p in row:
            if p > 1e-15:
                kl_total += p * np.log(p / uniform)
    return kl_total

# ---------------------------------------------------------------------------
# 7. Chi-square test against uniform for a count matrix
# ---------------------------------------------------------------------------
def chi2_test_uniform(count_matrix):
    """
    Flatten the count matrix. Expected = uniform over 10 next-digit choices
    for each context (row). Returns (chi2_stat, dof, p_value).
    """
    rows = count_matrix.reshape(-1, 10)
    chi2_stat = 0.0
    dof_total = 0
    for row in rows:
        n = row.sum()
        if n == 0:
            continue
        expected = n / 10.0
        chi2_stat += np.sum((row - expected)**2 / expected)
        dof_total += 9   # 10 cells – 1 for each row
    p_val = chi2_pvalue(chi2_stat, dof_total)
    return chi2_stat, dof_total, p_val

# ---------------------------------------------------------------------------
# 8. Chi-square test comparing two count matrices (prime vs composite)
# ---------------------------------------------------------------------------
def chi2_test_two_distributions(C1, C2):
    """
    Test whether two sets of