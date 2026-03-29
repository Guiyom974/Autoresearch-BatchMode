!@#$
import sys
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import chi2

# ============================================================
# CONFIGURATION
# ============================================================
LOWER = 10**6
UPPER = 10**7   # Using 10^7 instead of 10^8 to stay within 2-minute limit
                # The methodology is identical; scale is representative.
COMPOSITE_SAMPLE = 200000  # number of composites to sample for comparison

print("=" * 70)
print("MARKOVIAN DIGIT TRANSITIONS IN BASE-10 PRIMES")
print(f"Prime range: {LOWER:,} to {UPPER:,}")
print("=" * 70)

# ============================================================
# STEP 1 — SIEVE OF ERATOSTHENES (segmented, memory-efficient)
# ============================================================
def sieve_of_eratosthenes(limit):
    """Return boolean array is_prime[0..limit] using numpy bit sieve."""
    is_prime = np.ones(limit + 1, dtype=np.bool_)
    is_prime[0] = False
    is_prime[1] = False
    sqrt_limit = int(limit**0.5) + 1
    for i in range(2, sqrt_limit):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return is_prime

print("\n[1] Generating primes ...")
t0 = time.time()
is_prime_arr = sieve_of_eratosthenes(UPPER)
prime_indices = np.where(is_prime_arr[LOWER:UPPER+1])[0] + LOWER
primes = prime_indices  # array of prime numbers in range
n_primes = len(primes)
elapsed = time.time() - t0
print(f"    Found {n_primes:,} primes in [{LOWER:,}, {UPPER:,}] in {elapsed:.2f}s")

# Composites in range (sample for speed)
all_composite_indices = np.where(~is_prime_arr[LOWER:UPPER+1])[0] + LOWER
rng = np.random.default_rng(42)
if len(all_composite_indices) > COMPOSITE_SAMPLE:
    composite_sample = rng.choice(all_composite_indices, size=COMPOSITE_SAMPLE, replace=False)
else:
    composite_sample = all_composite_indices
composites = composite_sample
n_composites = len(composites)
print(f"    Sampled {n_composites:,} composite numbers for comparison")

# ============================================================
# STEP 2 — DIGIT EXTRACTION (internal digits, excluding final)
# ============================================================
def extract_internal_digits(numbers):
    """
    For each number, extract all digits EXCEPT the last digit.
    Returns a list of digit strings (as integer arrays).
    Only numbers with >= 3 digits are useful (need at least 2 internal digits
    to form a transition).
    """
    digit_sequences = []
    for n in numbers:
        s = str(n)
        # Exclude last digit (trivially constrained for primes)
        internal = s[:-1]
        if len(internal) >= 2:
            digit_sequences.append([int(c) for c in internal])
    return digit_sequences

print("\n[2] Extracting internal digit sequences ...")
t1 = time.time()
prime_seqs = extract_internal_digits(primes)
composite_seqs = extract_internal_digits(composites)
elapsed = time.time() - t1
print(f"    Extracted {len(prime_seqs):,} prime sequences, "
      f"{len(composite_seqs):,} composite sequences in {elapsed:.2f}s")

# ============================================================
# STEP 3 — BUILD 1ST-ORDER MARKOV TRANSITION MATRICES
# ============================================================
def build_first_order_matrix(sequences):
    """
    Build a 10x10 count matrix where M[i,j] = number of times digit j
    follows digit i in the internal digit sequences.
    """
    M = np.zeros((10, 10), dtype=np.int64)
    for seq in sequences:
        for k in range(len(seq) - 1):
            M[seq[k], seq[k+1]] += 1
    return M

print("\n[3] Building 1st-order Markov transition matrices ...")
t2 = time.time()
prime_M1 = build_first_order_matrix(prime_seqs)
composite_M1 = build_first_order_matrix(composite_seqs)
elapsed = time.time() - t2
print(f"    Built 1st-order matrices in {elapsed:.2f}s")
print(f"    Total prime 1st-order transitions:     {prime_M1.sum():,}")
print(f"    Total composite 1st-order transitions: {composite_M1.sum():,}")

# ============================================================
# STEP 4 — BUILD 2ND-ORDER MARKOV TRANSITION MATRICES
# ============================================================
def build_second_order_matrix(sequences):
    """
    Build a 100x10 count matrix where M[i*10+j, k] = number of times
    digit k follows the pair (i, j).
    """
    M = np.zeros((100, 10), dtype=np.int64)
    for seq in sequences:
        for k in range(len(seq) - 2):
            row = seq[k] * 10 + seq[k+1]
            col = seq[k+2]
            M[row, col] += 1
    return M

print("\n[4] Building 2nd-order Markov transition matrices ...")
t3 = time.time()
prime_M2 = build_second_order_matrix(prime_seqs)
composite_M2 = build_second_order_matrix(composite_seqs)
elapsed = time.time() - t3