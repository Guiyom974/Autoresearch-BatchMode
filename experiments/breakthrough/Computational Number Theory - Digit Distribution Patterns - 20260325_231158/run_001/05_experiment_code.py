import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import time

def sieve_of_eratosthenes(limit):
    """Generate prime numbers up to a given limit."""
    if limit < 2:
        return np.array([], dtype=int)
    sieve = np.ones(limit // 2, dtype=bool)
    for i in range(3, int(limit**0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = False
    primes = 2 * np.nonzero(sieve)[0] + 1
    return primes

def get_controls(limit):
    """Generate odd numbers not divisible by 5 up to limit."""
    nums = np.arange(3, limit, 2)
    return nums[nums % 5 != 0]

def count_transitions(nums):
    """Count adjacent digit transitions in an array of numbers."""
    transitions = np.zeros((10, 10), dtype=int)
    for n in nums:
        s = str(n)
        for i in range(len(s) - 1):
            transitions[int(s[i]), int(s[i+1])] += 1
    return transitions

def test_hypothesis_1():
    print("Testing Hypothesis 1: Non-Uniform Digit Transition Bias Within Prime Numbers (Base-10)")
    limit = 2000000  # 2 million
    
    t0 = time.time()
    primes = sieve_of_eratosthenes(limit)
    # Remove single digit primes as they have no transitions
    primes = primes[primes >= 10]
    
    controls = get_controls(limit)
    controls = controls[controls >= 10]
    
    print(f"Generated {len(primes)} primes and {len(controls)} control numbers up to {limit}.")
    
    prime_trans = count_transitions(primes)
    control_trans = count_transitions(controls)
    
    # Normalize to probabilities
    prime_prob = prime_trans / prime_trans.sum()
    control_prob = control_trans / control_trans.sum()
    
    # Chi-square test
    # We compare the observed frequencies in primes vs controls
    # To do a proper test, we can use the raw counts
    obs = np.array([prime_trans.flatten(), control_trans.flatten()])
    # Remove columns where both are 0 to avoid division by zero in chi2
    valid_cols = np.sum(obs, axis=0) > 0
    obs = obs[:, valid_cols]
    
    chi2, p, dof, ex = chi2_contingency(obs)
    
    print(f"Chi-square statistic: {chi2:.2f}")
    print(f"p-value: {p:.2e}")
    
    # Plotting
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    im1 = axes[0].imshow(prime_prob, cmap='viridis')
    axes[0].set_title('Prime Digit Transitions')
    axes[0].set_xlabel('Next Digit')
    axes[0].set_ylabel('Current Digit')
    fig.colorbar(im1, ax=axes[0])
    
    im2 = axes[1].imshow(control_prob, cmap='viridis')
    axes[1].set_title('Control Digit Transitions')
    axes[1].set_xlabel('Next Digit')
    axes[1].set_ylabel('Current Digit')
    fig.colorbar(im2, ax=axes[1])
    
    diff = prime_prob - control_prob
    im3 = axes[2].imshow(diff, cmap='coolwarm', vmin=-np.max(np.abs(diff)), vmax=np.max(np.abs(diff)))
    axes[2].set_title('Difference (Primes - Controls)')
    axes[2].set_xlabel('Next Digit')
    axes[2].set_ylabel('Current Digit')
    fig.colorbar(im3, ax=axes[2])
    
    plt.tight_layout()
    plt.savefig('digit_transitions.png')
    plt.close()
    
    print(f"Test completed in {time.time() - t0:.2f} seconds.")
    print("-" * 50)
    
    return p

def main():
    print("Starting Digit Sequencing and Base-N Distribution Patterns Analysis\n")
    p_val = test_hypothesis_1()
    
    print("\nCONCLUSIONS:")
    print("1. Digit Transition Probabilities (Base-10):")
    if p_val < 0.05:
        print("   The adjacent-digit transition probability matrix for prime numbers differs significantly ")
        print("   from the control group of odd numbers not divisible by 5 (p < 0.05).")
        print("   This suggests there is a localized bias in the digit sequences of primes beyond simple ")
        print("   divisibility rules.")
    else:
        print("   No significant difference was found in the digit transition probabilities between primes ")
        print("   and the control group. The apparent patterns are likely artifacts of the uniform ")
        print("   distribution of numbers ending in 1, 3, 7, 9.")
    print("\nPlots have been saved to 'digit_transitions.png'.")

if __name__ == "__main__":
    main()