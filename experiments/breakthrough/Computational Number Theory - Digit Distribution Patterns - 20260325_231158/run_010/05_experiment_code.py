import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import rel_entr
import math

def sieve(n):
    """Simple sieve of Eratosthenes to find primes up to n."""
    flags = np.ones(n + 1, dtype=bool)
    flags[0:2] = False
    for i in range(2, int(n**0.5) + 1):
        if flags[i]:
            flags[i*i::i] = False
    return np.nonzero(flags)[0]

def get_leading_digits_base(primes, base):
    """Extract leading digits of an array of numbers in a given base."""
    # Filter out primes less than base to ensure they have a valid leading digit
    primes = primes[primes >= base]
    # Calculate leading digit: floor(p / base^floor(log_base(p)))
    # To avoid floating point inaccuracies with large numbers, we can use a vectorized approach
    # For primes < 5,000,000 and base 210, max power is 210^3 = 9,261,000
    powers = np.floor(np.log(primes) / np.log(base)).astype(int)
    leading_digits = np.floor(primes / (base ** powers)).astype(int)
    return leading_digits

def coprime_weight(d, base):
    """Calculate a hypothetical coprime weight for a digit."""
    return 1.0 if math.gcd(d, base) == 1 else 0.5

def test_hypothesis_1():
    print("Testing Hypothesis 1: Normalization Overcorrection via Coprime Filtering")
    base = 210
    limit = 5000000
    primes = sieve(limit)
    
    leading_digits = get_leading_digits_base(primes, base)
    
    # Empirical distribution
    counts = np.bincount(leading_digits, minlength=base)[1:base]
    empirical_prob = counts / counts.sum()
    
    # Benford distribution
    digits = np.arange(1, base)
    benford_prob = np.log10(1 + 1/digits) / np.log10(base)
    benford_prob = benford_prob / benford_prob.sum()
    
    # Calculate coprime weights
    weights = np.array([coprime_weight(d, base) for d in digits])
    
    alphas = np.linspace(0, 2, 21)
    kl_divergences = []
    
    for alpha in alphas:
        # Theoretical model with varying coprime adjustment strength
        adj_prob = benford_prob * (weights ** alpha)
        adj_prob = adj_prob / adj_prob.sum()
        
        # Calculate KL Divergence: sum(Empirical * log(Empirical / Theoretical))
        # Add small epsilon to avoid log(0)
        eps = 1e-10
        emp_safe = empirical_prob + eps
        adj_safe = adj_prob + eps
        kl_div = np.sum(rel_entr(emp_safe, adj_safe))
        kl_divergences.append(kl_div)
        
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(alphas, kl_divergences, marker='o', linestyle='-', color='b')
    plt.title('KL Divergence vs. Coprime Weighting Exponent ($\\alpha$)')
    plt.xlabel('Coprime Weighting Exponent $\\alpha$')
    plt.ylabel('KL Divergence (Empirical || Theoretical)')
    plt.grid(True)
    plt.savefig('hypothesis1_kl_divergence.png')
    plt.close()
    
    best_alpha = alphas[np.argmin(kl_divergences)]
    print(f"Minimum KL divergence achieved at alpha = {best_alpha:.2f}")
    print("KL Divergence at alpha=0 (Standard Benford): {:.6f}".format(kl_divergences[0]))
    print("KL Divergence at alpha=1 (Original Model): {:.6f}".format(kl_divergences[10]))
    print(f"KL Divergence at optimal alpha={best_alpha:.2f}: {min(kl_divergences):.6f}")
    print("-" * 50)

if __name__ == "__main__":
    test_hypothesis_1()
    
    print("\nCONCLUSIONS:")
    print("1. We tested the effect of varying the coprime weighting exponent on the KL divergence between the empirical distribution of prime leading digits in Base-210 and the adjusted Benford model.")
    print("2. The results show how adjusting the strength of the coprime filtering correction impacts the accuracy of the theoretical model.")
    print("3. If the optimal alpha is less than 1 (or close to 0), it confirms the hypothesis that the original model applied an excessive weighting correction, and a reduced (or zero) coprime adjustment yields a distribution closer to the empirical data.")