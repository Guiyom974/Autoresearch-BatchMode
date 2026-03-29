!@#$
"""
Research Script: Markovian Dependencies in Base-10 Prime Digit Sequences
Tests hypotheses about transition probabilities of internal digits of primes up to 10^7.

Hypotheses (derived from research problem, as original hypothesis text was unavailable):
  H1: 1st-order internal digit transitions in primes deviate significantly
      from a uniform distribution (chi-square test, p < 0.05).
  H2: 2nd-order internal digit transitions in primes deviate significantly
      from a uniform distribution (chi-square test, p < 0.05).
  H3: Individual rows of the 1st-order transition matrix (i.e., the conditional
      distributions P(d_{i+1}=j | d_i=i)) are significantly non-uniform,
      indicating that the current internal digit predicts the next one.
  H4: The most-frequent internal digit pairs/triplets differ from what would be
      expected under uniform digit usage.
"""

import sys
import logging
import time
import warnings
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import chi2

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# 1.  PRIME GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def sieve_of_eratosthenes(limit: int) -> np.ndarray:
    """Return array of primes up to and including `limit`."""
    log.info("Sieve of Eratosthenes up to %d …", limit)
    t0 = time.time()
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = False
    primes = np.flatnonzero(is_prime)
    log.info("  → %d primes found in %.2f s", len(primes), time.time() - t0)
    return primes


# ─────────────────────────────────────────────────────────────────────────────
# 2.  INTERNAL DIGIT EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def extract_internal_sequences(primes: np.ndarray):
    """
    For each prime with at least 3 digits return the *internal* substring
    (strip first and last character).
    Returns a flat list of digit-integer sequences.
    """
    log.info("Extracting internal digit sequences …")
    t0 = time.time()
    sequences = []
    for p in primes:
        s = str(p)
        if len(s) >= 3:
            internal = [int(c) for c in s[1:-1]]
            sequences.append(internal)
    log.info(
        "  → %d primes with internal digits (≥3 digits) in %.2f s",
        len(sequences),
        time.time() - t0,
    )
    return sequences


# ─────────────────────────────────────────────────────────────────────────────
# 3.  MARKOVIAN TRANSITION COUNTING
# ─────────────────────────────────────────────────────────────────────────────

def build_transition_matrices(sequences):
    """
    Returns:
        pair_counts   : np.ndarray shape (10, 10)  — counts of (d_i, d_{i+1})
        triplet_counts: np.ndarray shape (10,10,10) — counts of (d_i,d_{i+1},d_{i+2})
        pair_total    : int
        triplet_total : int
    """
    log.info("Building 1st- and 2nd-order transition count matrices …")
    t0 = time.time()

    pair_counts    = np.zeros((10, 10),    dtype=np.int64)
    triplet_counts = np.zeros((10, 10, 10), dtype=np.int64)

    for seq in sequences:
        n = len(seq)
        for i in range(n - 1):
            pair_counts[seq[i], seq[i + 1]] += 1
        for i in range(n - 2):
            triplet_counts[seq[i], seq[i + 1], seq[i + 2]] += 1

    pair_total    = int(pair_counts.sum())
    triplet_total = int(triplet_counts.sum())
    log.info(
        "  → %d pair transitions, %d triplet transitions in %.2f s",
        pair_total, triplet_total, time.time() - t0,
    )
    return pair_counts, triplet_counts, pair_total, triplet_total


def normalize_rows(counts: np.ndarray) -> np.ndarray:
    """Row-normalize a count matrix; rows that sum to 0 become uniform."""
    row_sums = counts.sum(axis=-1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1, row_sums)
    return counts / row_sums


# ─────────────────────────────────────────────────────────────────────────────
# 4.  CHI-SQUARE TESTS
# ─────────────────────────────────────────────────────────────────────────────

def chi2_uniform_test(observed_counts: np.ndarray, label: str):
    """
    Pearson chi-square goodness-of-fit test against a fully uniform distribution
    over the *same total count*.

    observed_counts : 1-D or 2-D array of integer counts.
    Returns chi2_stat, p_value, dof.
    """
    obs_flat = observed_counts.flatten().astype(float)
    total    = obs_flat.sum()
    n_cells  = obs_flat.size
    expected = np.full(n_cells, total / n_cells)

    # Remove cells with zero expected (none here, uniform → all equal)
    mask = expected > 0
    obs_flat = obs_flat[mask]
    exp_flat = expected[mask]

    chi2_stat = float(np.sum((obs_flat - exp_flat) ** 2 / exp_flat))
    dof       = int(mask.sum()) - 1
    p_value   = float(1.0 - chi2.cdf(chi2_stat, dof))

    log.info(
        "  [%s] χ²=%.4f, dof=%d, p=%.6e", label, chi2_stat, dof, p