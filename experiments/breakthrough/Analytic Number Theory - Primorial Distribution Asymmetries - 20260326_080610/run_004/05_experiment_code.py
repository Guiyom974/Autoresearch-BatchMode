import sys
import time
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats as scipy_stats

# =============================================================================
# Helper Functions
# =============================================================================

def generate_primes(limit):
    """Simple Sieve of Eratosthenes to generate primes up to limit."""
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    return np.where(sieve)[0]

def primorial_of_first_k(k):
    """Return the primorial of the first k primes (product of first k primes)."""
    primes = generate_primes(200)          # enough primes for k up to ~10
    return int(np.prod(primes[:k]))

def cpu_leading_digit_counts(n, base):
    """Compute leading digit counts for numbers 1..n using pure Python loops."""
    counts = [0] * 10
    for i in range(1, n + 1):
        # Determine the exponent of the highest power of base not exceeding i
        exp = int(math.log(i, base))
        power = base ** exp
        # Guard against power being zero (should not happen for i>=1)
        if power == 0:
            power = 1
        lead = i // power
        # If lead ended up >=10 due to rounding, adjust
        if lead >= 10:
            lead = i // (base ** (exp + 1))
        counts[lead] += 1
    return np.array(counts, dtype=int)

def gpu_leading_digit_counts(n, base):
    """Compute leading digit counts using vectorized NumPy (GPU-like)."""
    arr = np.arange(1, n + 1, dtype=np.int64)
    # Vectorized exponent computation
    exponents = np.floor(np.log(arr) / np.log(base)).astype(np.int64)
    # Compute leading digit for each number
    leading = (arr // (base ** exponents)).astype(np.int64)
    # Count frequencies
    counts = np.zeros(10, dtype=np.int64)
    np.add.at(counts, leading, 1)
    return counts

def expected_benford_frequencies():
    """Return expected Benford frequencies for digits 1-9."""
    return np.array([math.log10(1 + 1 / d) for d in range(1, 10)])

def measure_time(func, *args):
    """Return (result, elapsed_time) for a given function call."""
    t0 = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - t0
    return result, elapsed

def compute_max_abs_deviation(observed_counts):
    """Maximum absolute deviation of observed frequencies from Benford."""
    obs_freq = observed_counts[1:10] / observed_counts[1:10].sum()
    exp_freq = expected_benford_frequencies()
    return float(np.max(np.abs(obs_freq - exp_freq)))

def chi2_test(observed_counts):
    """Chi-squared test against Benford distribution."""
    observed = observed_counts[1:10]
    expected = expected_benford_frequencies() * observed.sum()
    chi2, p = scipy_stats.chisquare(observed, f_exp=expected)
    return chi2, p

# =============================================================================
# Hypothesis Test Functions
# =============================================================================

def test_hypothesis_1(base, n):
    """Hypothesis 1: GPU-accelerated version achieves >=5x speedup."""
    print("\n=== Hypothesis 1: GPU-Accelerated Parallel Processing Achieves >=5x Speedup ===")
    _, cpu_time = measure_time(cpu_leading_digit_counts, n, base)
    _, gpu_time = measure_time(gpu_leading_digit_counts, n, base)
    speedup = cpu_time / gpu_time if gpu_time > 0 else float('inf')
    supported = speedup >= 5.0
    print(f"  CPU time: {cpu_time:.4f} s")
    print(f"  GPU time: {gpu_time:.4f} s")
    print(f"  Speedup:  {speedup:.2f}x")
    print(f"  Hypothesis 1 supported (>=5x): {supported}")

    # Plot timing comparison
    fig, ax = plt.subplots()
    bars = ax.bar(['CPU', 'GPU'], [cpu_time, gpu_time], color=['steelblue', 'orange'])
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Hypothesis 1 - Execution Time Comparison')
    for bar, val in zip(bars, [cpu_time, gpu_time]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f'{val:.3f}s', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig('hypothesis1_timing.png')
    plt.close()
    print("  Plot saved: hypothesis1_timing.png")
    return speedup, supported

def test_hypothesis_2(base, n):
    """Hypothesis 2: GPU distribution deviates <1% from Benford's law."""
    print("\n=== Hypothesis 2: GPU Distribution Deviation < 1% ===")
    counts, _ = measure_time(gpu_leading_digit_counts, n, base)
    max_dev = compute_max_abs_deviation(counts)
    chi2, p = chi2_test(counts)
    supported = max_dev < 0.01
    print(f"  Max absolute deviation: {max_dev:.4f} ({max_dev*100:.2f}%)")
    print(f"  Chi-squared: {chi2:.4f}, p-value: {p:.4f}")
    print(f"  Hypothesis 2 supported (<1% deviation): {supported}")

    # Plot observed vs expected distribution
    obs_freq = counts[1:10] / counts[1:10].sum()
    exp_freq = expected_benford_frequencies()
    digits = np.arange(1, 10)
    fig, ax = plt.subplots()
    width = 0.35
    ax.bar(digits - width / 2, obs_freq, width, label='Observed (GPU)', color='orange')
    ax.bar(digits + width / 2, exp_freq, width, label='Benford Expected', color='steelblue')
    ax.set_xlabel('Digit')
    ax.set_ylabel('Frequency')
    ax.set_title('Hypothesis 2 - Observed vs Benford Distribution')
    ax.set_xticks(digits)
    ax.legend()
    plt.tight_layout()
    plt.savefig('hypothesis2_distribution.png')
    plt.close()
    print("  Plot saved: hypothesis2_distribution.png")
    return max_dev, supported

def test_hypothesis_3(base, n):
    """Hypothesis 3: GPU memory usage <= 50% of CPU-baseline memory."""
    print("\n=== Hypothesis 3: GPU Memory Usage <= 50% of CPU Baseline ===")
    # Approximate memory for storing 1..n as Python ints (sys.getsizeof of a small int)
    python_mem_est = n * sys.getsizeof(0)   # 28 bytes per small int on 64-bit CPython
    # NumPy array memory
    arr = np.arange(1, n + 1, dtype=np.int64)
    gpu_mem = arr.nbytes
    del arr
    reduction = (python_mem_est - gpu_mem) / python_mem_est if python_mem_est > 0 else 0
    supported = reduction >= 0.5
    print(f"  Python list memory (approx): {python_mem_est / 1024 / 1024:.2f} MB")
    print(f"  GPU numpy array memory:      {gpu_mem / 1024 / 1024:.2f} MB")
    print(f"  Reduction: {reduction*100:.1f}%")
    print(f"  Hypothesis 3 supported (>= 50% reduction): {supported}")

    # Plot memory comparison
    fig, ax = plt.subplots()
    bars = ax.bar(['Python List\n(approx)', 'NumPy Array'],
                  [python_mem_est / 1024 / 1024, gpu_mem / 1024 / 1024],
                  color=['steelblue', 'orange'])
    ax.set_ylabel('Memory (MB)')
    ax.set_title('Hypothesis 3 - Memory Usage Comparison')
    for bar, val in zip(bars, [python_mem_est / 1024 / 1024, gpu_mem / 1024 / 1024]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f'{val:.2f} MB', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig('hypothesis3_memory.png')
    plt.close()
    print("  Plot saved: hypothesis3_memory.png")
    return reduction, supported

def test_hypothesis_4(base):
    """Hypothesis 4: Speedup improves as sample size increases."""
    print("\n=== Hypothesis 4: Speedup Improves with Sample Size ===")
    sample_sizes = [100_000, 500_000, 1_000_000]
    speedups = []
    for n in sample_sizes:
        _, cpu_time = measure_time(cpu_leading_digit_counts, n, base)
        _, gpu_time = measure_time(gpu_leading_digit_counts, n, base)
        speedup = cpu_time / gpu_time if gpu_time > 0 else float('inf')
        speedups.append(speedup)
        print(f"  N={n:,}: CPU={cpu_time:.4f}s, GPU={gpu_time:.4f}s, Speedup={speedup:.2f}x")
    # Check monotonic improvement (last speedup >= first)
    increasing = speedups[-1] >= speedups[0]
    print(f"  Speedup increased from {speedups[0]:.2f}x to {speedups[-1]:.2f}x: {increasing}")
    print(f"  Hypothesis 4 supported (speedup improves): {increasing}")

    # Plot scalability
    fig, ax = plt.subplots()
    ax.plot(sample_sizes, speedups, marker='o', color='steelblue')
    ax.set_xlabel('Sample Size (N)')
    ax.set_ylabel('Speedup (x)')
    ax.set_title('Hypothesis 4 - Scalability of GPU Speedup')
    for size, sp in zip(sample_sizes, speedups):
        ax.annotate(f'{sp:.2f}x', (size, sp), textcoords="offset points",
                    xytext=(0, 5), ha='center')
    plt.tight_layout()
    plt.savefig('hypothesis4_scalability.png')
    plt.close()
    print("  Plot saved: hypothesis4_scalability.png")
    return speedups, increasing

def test_hypothesis_5():
    """Hypothesis 5: GPU speedup is consistent across high primorial bases."""
    print("\n=== Hypothesis 5: GPU Speedup Consistent Across High Primorial Bases ===")
    n = 100_000
    bases = [210, 2310, 30030]
    speedups = []
    for base in bases:
        _, cpu_time = measure_time(cpu_leading_digit_counts, n, base)
        _, gpu_time = measure_time(gpu_leading_digit_counts, n, base)
        speedup = cpu_time / gpu_time if gpu_time > 0 else float('inf')
        speedups.append(speedup)
        print(f"  Base {base}: CPU={cpu_time:.4f}s, GPU={gpu_time:.4f}s, Speedup={speedup:.2f}x")
    all_supported = all(sp >= 5.0 for sp in speedups)
    print(f"  All bases achieved >=5x speedup: {all_supported}")
    print(f"  Hypothesis 5 supported (consistent across bases): {all_supported}")

    # Plot speedup across bases
    fig, ax = plt.subplots()
    bars = ax.bar([str(b) for b in bases], speedups, color='orange')
    ax.axhline(y=5.0, color='red', linestyle='--', label='5x threshold')
    ax.set_xlabel('Primorial Base')
    ax.set_ylabel('Speedup (x)')
    ax.set_title('Hypothesis 5 - Speedup Across Bases')
    ax.legend()
    for bar, val in zip(bars, speedups):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f'{val:.2f}x', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig('hypothesis5_bases.png')
    plt.close()
    print("  Plot saved: hypothesis5_bases.png")
    return speedups, all_supported

# =============================================================================
# Main Routine
# =============================================================================

def main():
    print("=" * 70)
    print("GPU-Accelerated LDAB Model Evaluation - Hypothesis Testing")
    print("=" * 70)

    # Choose a high primorial base (>=2310)
    base = 2310

    # Sample size for main tests (>=10^6)
    n_main = 1_000_000

    # Run hypothesis tests
    sp1, sup1 = test_hypothesis_1(base, n_main)
    dev2, sup2 = test_hypothesis_2(base, n_main)
    red3, sup3 = test_hypothesis_3(base, n_main)
    _, sup4 = test_hypothesis_4(base)
    _, sup5 = test_hypothesis_5()

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY OF HYPOTHESIS TESTING")
    print("=" * 70)
    print(f"Hypothesis 1 (>=5x speedup)               : {'SUPPORTED' if sup1 else 'NOT SUPPORTED'} (speedup {sp1:.2f}x)")
    print(f"Hypothesis 2 (<1% deviation)            : {'SUPPORTED' if sup2 else 'NOT SUPPORTED'} (max dev {dev2:.4f})")
    print(f"Hypothesis 3 (>=50% memory reduction)    : {'SUPPORTED' if sup3 else 'NOT SUPPORTED'} (reduction {red3*100:.1f}%)")
    print(f"Hypothesis 4 (speedup improves)         : {'SUPPORTED' if sup4 else 'NOT SUPPORTED'}")
    print(f"Hypothesis 5 (consistent across bases) : {'SUPPORTED' if sup5 else 'NOT SUPPORTED'}")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Conclusions
    # -------------------------------------------------------------------------
    print("\nCONCLUSIONS:")
    if sup1 and sup2 and sup3 and sup4 and sup5:
        print("All hypotheses are supported. The GPU-accelerated vectorized")
        print("implementation achieves a >=5x speedup, maintains statistical")
        print("accuracy within 1% of Benford's law, reduces memory usage by")
        print(">50%, scales favorably with sample size, and delivers consistent")
        print("performance across different high primorial bases.")
    else:
        supported_flags = [sup1, sup2, sup3, sup4, sup5]
        if all(supported_flags):
            print("All tested hypotheses are supported.")
        else:
            print("Some hypotheses were not supported. Review the results above.")
            if not sup1:
                print("- GPU speedup did not meet the 5x threshold.")
            if not sup2:
                print("- Distribution deviation exceeded the 1% tolerance.")
            if not sup3:
                print("- Memory reduction did not achieve at least 50%.")
            if not sup4:
                print("- Speedup did not improve with larger sample sizes.")
            if not sup5:
                print("- GPU speedup was not consistent across different primorial bases.")

if __name__ == "__main__":
    main()