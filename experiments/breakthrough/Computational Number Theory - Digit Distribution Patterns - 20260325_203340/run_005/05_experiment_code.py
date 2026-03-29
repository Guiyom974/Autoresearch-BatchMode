!@#$
"""
Robust Computational Extraction and Analysis of 1st- and 2nd-Order
Markovian Dependencies in Internal Digits of Base-10 Primes.

The hypotheses to test (derived from the research problem):
  H1: Internal-digit 1st-order transitions are uniformly distributed
      (chi-square test; reject H0 = non-uniform Markovian structure exists).
  H2: Internal-digit 2nd-order transitions are fully explained by the
      1st-order transition matrix (conditional independence test).
  H3: The 1st-order transition probabilities are scale-invariant across
      logarithmic buckets (10^5–10^6, 10^6–10^7, 10^7–10^8).
"""

# ── stdlib + numpy + matplotlib only ──────────────────────────────────────────
import time
import logging
import sys
import warnings
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.stats import chi2   # scipy is stdlib-adjacent but let's keep it;
                               # we implement chi2 cdf ourselves to be safe

# ── logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# 0.  CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
LIMIT = 10_000_000          # primes up to 10^7 (fits in ~2 min; extend to 10^8 with more RAM)
LOG_BUCKETS = [
    (10**4,  10**5,  "10^4–10^5"),
    (10**5,  10**6,  "10^5–10^6"),
    (10**6,  10**7,  "10^6–10^7"),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1.  PRIME SIEVE
# ══════════════════════════════════════════════════════════════════════════════

def sieve_of_eratosthenes(limit: int) -> np.ndarray:
    """Return an array of all primes < limit using a segmented-like numpy sieve."""
    log.info("Running sieve up to %d …", limit)
    t0 = time.time()
    is_prime = np.ones(limit, dtype=np.bool_)
    is_prime[0] = is_prime[1] = False
    is_prime[4::2] = False
    for i in range(3, int(limit**0.5) + 1, 2):
        if is_prime[i]:
            is_prime[i*i::2*i] = False
    primes = np.flatnonzero(is_prime)
    log.info("Found %d primes in %.2f s", len(primes), time.time() - t0)
    return primes

# ══════════════════════════════════════════════════════════════════════════════
# 2.  INTERNAL DIGIT EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════

def extract_internal_digits(primes: np.ndarray, min_digits: int = 3):
    """
    For each prime with >= min_digits decimal digits, strip the first and last
    digit and return the list of internal digit sequences (as lists of ints).
    """
    log.info("Extracting internal digits (min_digits=%d) …", min_digits)
    t0 = time.time()
    sequences = []
    for p in primes:
        s = str(p)
        if len(s) >= min_digits:
            internal = [int(c) for c in