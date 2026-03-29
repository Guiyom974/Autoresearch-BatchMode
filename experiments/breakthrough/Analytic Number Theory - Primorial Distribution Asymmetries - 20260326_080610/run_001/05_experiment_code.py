import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import sys

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def sieve(limit):
    """Return list of all primes <= limit using Eratosthenes sieve."""
    is_prime = bytearray(b'\x01') * (limit + 1)
    is_prime[0:2] = b'\x00\x00'
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            start = p * p
            step = p
            is_prime[start:limit+1:step] = b'\x00' * ((limit - start) // step + 1)
    return [i for i in range(limit + 1) if is_prime[i]]

def compute_phi(m):
    """Compute Euler's totient phi(m) for integer m."""
    result = m
    p = 2
    while p * p <= m:
        if m % p == 0:
            result -= result // p
            while m % p == 0:
                m //= p
        p += 1 if p == 2 else 2
    if m > 1:
        result -= result // m
    return result

def kl_divergence(p, q):
    """Compute Kullback-Leibler divergence D(p||q). Both p and q are numpy arrays of same length."""
    mask = p > 0
    # If any q[mask] == 0 while p[mask] > 0, divergence is infinite; treat as large.
    # In our usage q is always positive.
    p_safe = p[mask]
    q_safe = q[mask]
    return np.sum(p_safe * np.log(p_safe / q_safe))

def leading_digit_distribution(numbers):
    """
    Compute the probability distribution of leading decimal digits (1-9) for an array of integers.
    numbers: numpy array of positive integers.
    Returns: numpy array of length 9 with probabilities for digits 1..9.
    """
    # Compute exponent of each number: floor(log10)
    exp = np.floor(np.log10(numbers)).astype(int)
    # Compute power of 10 corresponding to that exponent
    power = np.power(10, exp).astype(int)
    # Leading digit = first decimal digit
    leading = (numbers // power).astype(int)
    # Count occurrences for digits 1-9
    counts = np.bincount(leading, minlength=10)
    counts = counts[1:10]  # exclude digit 0
    total = counts.sum()
    if total == 0:
        return np.zeros(9)
    return counts / total

# ------------------------------------------------------------
# Main analysis
# ------------------------------------------------------------

def main():
    # Upper bound for prime generation and multiples
    MAX_N = 10_000_000

    print("=" * 70)
    print("Hypothesis 1: Uniform Generalization of LDAB Model Across Primorial Bases")
    print("=" * 70)
    print(f"\nGenerating primes up to {MAX_N:,} ...")
    primes = sieve(MAX_N)
    primes_arr = np.array(primes, dtype=np.int64)
    total_primes = len(primes)
    print(f"Total primes found: {total_primes:,}")

    # Primorial bases to test
    bases = [30, 210, 2310, 30030]

    # Pre-compute phi(m) and coprime residue indices for each base
    phi_dict = {}
    coprime_idx_dict = {}
    for m in bases:
        phi_dict[m] = compute_phi(m)
        coprime_idx_dict[m] = [i for i in range(m) if math.gcd(i, m) == 1]

    # Benford reference distribution (decimal leading digits)
    benford = np.array([np.log10(1 + 1 / d) for d in range(1, 10)])

    # Storage for per-base results
    results = {}

    # ------------------------------------------------------------
    # Test each primorial base
    # ------------------------------------------------------------
    for m in bases:
        print(f"\n{'='*50}")
        print(f"Base {m} (phi = {phi_dict[m]})")
        print('='*50)

        # --- Chebyshev bias test: prime distribution modulo m ---
        # Count primes in each residue class modulo m
        counts_residue = np.bincount(primes_arr % m, minlength=m)
        coprime_idx = coprime_idx_dict[m]
        obs_counts = counts_residue[coprime_idx]
        total_coprime = obs_counts.sum()
        # Observed conditional distribution over coprime residues
        p_residue = obs_counts / total_coprime
        # Expected uniform distribution over coprime residues
        q_residue = np.full(phi_dict[m], 1.0 / phi_dict[m])
        kl_residue = kl_divergence(p_residue, q_residue)
        print(f"  [Chebyshev bias] KL divergence (primes vs uniform): {kl_residue:.6e}")

        # --- LDAB leading-digit test: multiples of the primorial base ---
        # Generate all multiples of m up to MAX_N
        multiples = np.arange(m, MAX_N + 1, m, dtype=np.int64)
        # Compute leading-digit distribution for these multiples
        p_ld = leading_digit_distribution(multiples)
        # Compare to Benford (the LDAB reference)
        kl_ld = kl_divergence(p_ld, benford)
        threshold = 1e-3
        print(f"  [LDAB leading digits] KL divergence (multiples vs Benford): {kl_ld:.6e}")
        if kl_ld < threshold:
            print(f"  *** LDAB model holds (KL < {threshold}) ***")
        else:
            print(f"  *** LDAB model does NOT hold (KL >= {threshold}) ***")

        # Store results for later summary
        results[m] = {
            'kl_residue': kl_residue,
            'kl_ld': kl_ld,
            'p_ld': p_ld,
            'n_multiples': len(multiples)
        }

    # ------------------------------------------------------------
    # Visualisation
    # ------------------------------------------------------------
    # Plot leading-digit distributions for each base
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    digits = np.arange(1, 10)
    for idx, m in enumerate(bases):
        ax = axes[idx]
        p_ld = results[m]['p_ld']
        width = 0.35
        ax.bar(digits - width/2, p_ld, width, color='steelblue', label='Observed')
        ax.bar(digits + width/2, benford, width, color='coral', label='Benford')
        ax.set_xlabel('Leading Digit')
        ax.set_ylabel('Probability')
        ax.set_title(f'Base {m}\nKL = {results[m]["kl_ld"]:.4e}')
        ax.set_xticks(digits)
        ax.legend()
    plt.tight_layout()
    fig.savefig('leading_digits_by_base.png', dpi=150)
    plt.close(fig)
    print("\nPlot saved: leading_digits_by_base.png")

    # Plot KL divergences across bases
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    base_labels = [str(b) for b in bases]
    kl_vals = [results[b]['kl_ld'] for b in bases]
    colors = ['green' if k < 1e-3 else 'red' for k in kl_vals]
    ax.bar(base_labels, kl_vals, color=colors, alpha=0.7)
    ax.axhline(y=1e-3, color='black', linestyle='--', linewidth=2, label='Threshold 1e-3')
    ax.set_xlabel('Primorial Base')
    ax.set_ylabel('KL Divergence (LDAB vs Benford)')
    ax.set_title('KL Divergence of Leading-Digit Distributions')
    ax.legend()
    plt.tight_layout()
    fig.savefig('kl_divergences.png', dpi=150)
    plt.close(fig)
    print("Plot saved: kl_divergences.png")

    # ------------------------------------------------------------
    # Summary table
    # ------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"{'Base':<10} {'phi(m)':<8} {'KL (Residue)':<18} {'KL (Leading Digit)':<22} {'LDAB Holds?'}")
    print("-" * 70)
    for m in bases:
        kl_res = results[m]['kl_residue']
        kl_ld = results[m]['kl_ld']
        holds = "YES" if kl_ld < 1e-3 else "NO"
        print(f"{m:<10} {phi_dict[m]:<8} {kl_res:<18.6e} {kl_ld:<22.6e} {holds}")

    # ------------------------------------------------------------
    # Conclusions
    # ------------------------------------------------------------
    all_hold = all(results[m]['kl_ld'] < 1e-3 for m in bases)
    conclusion_text = (
        "\nCONCLUSIONS:\n"
        "=============\n"
    )
    if all_hold:
        conclusion_text += (
            "The LDAB model exhibits uniform generalization across all tested primorial bases.\n"
            "All KL divergences for leading-digit distributions are below the 1e-3 threshold,\n"
            "indicating that the Logarithmic-Density-Adjusted Benford model holds without\n"
            "any base-specific calibrations.\n"
        )
    else:
        conclusion_text += (
            "The LDAB model does NOT achieve uniform generalization across all primorial bases.\n"
            "Some KL divergences exceed the 1e-3 threshold, suggesting that base-specific\n"
            "adjustments may be required for those bases.\n"
        )
    print(conclusion_text)

if __name__ == '__main__':
    main()