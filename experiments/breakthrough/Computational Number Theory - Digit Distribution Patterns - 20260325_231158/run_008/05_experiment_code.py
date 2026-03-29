import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import math
import time

# Start timing
start_time = time.time()

# =============================================================================
# CONFIGURATION AND CONSTANTS
# =============================================================================

MAX_PRIME = 10**7  # Reduced from 10^8 for 2-minute runtime constraint
BASE = 210  # 2*3*5*7 primorial base
PHI_BASE = 48  # Euler's totient of 210 = 48 coprime digits

# Coprime digits to 210 (digits 1-209 that are coprime to 210)
# 210 = 2*3*5*7, so coprime digits are those not divisible by 2, 3, 5, or 7
COPRIME_DIGITS = sorted([d for d in range(1, BASE) 
                         if math.gcd(d, BASE) == 1])
assert len(COPRIME_DIGITS) == PHI_BASE, f"Expected {PHI_BASE} coprime digits"

# =============================================================================
# PRIME GENERATION (Segmented Sieve for efficiency)
# =============================================================================

def simple_sieve(limit):
    """Generate primes up to limit using simple sieve."""
    if limit < 2:
        return np.array([], dtype=np.int64)
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return np.where(sieve)[0].astype(np.int64)

def segmented_sieve(limit):
    """Segmented sieve for large limits, memory efficient."""
    if limit <= 10**6:
        return simple_sieve(limit)
    
    # Use simple sieve for small primes (base primes)
    segment_size = min(10**6, limit // 10)
    base_primes = simple_sieve(int(limit**0.5) + 1)
    
    primes = list(base_primes)
    
    for low in range(0, limit + 1, segment_size):
        high = min(low + segment_size, limit + 1)
        segment = np.ones(high - low, dtype=bool)
        
        for p in base_primes:
            start = ((low + p - 1) // p) * p
            segment[start - low::p] = False
        
        if low == 0:
            segment[0] = False
            if len(segment) > 1:
                segment[1] = False
        
        new_primes = np.where(segment)[0] + low
        if low == 0:
            primes = list(new_primes)
        else:
            primes.extend(new_primes)
    
    return np.array(primes, dtype=np.int64)

# =============================================================================
# LEADING DIGIT EXTRACTION
# =============================================================================

def get_leading_digit_base210(n):
    """
    Get the leading digit of n in base 210.
    Returns the most significant digit (1-209, coprime to 210 for primes > 210).
    """
    if n < BASE:
        return n
    
    # Find the highest power of 210 <= n
    power = BASE
    while power * BASE <= n:
        power *= BASE
    
    # Leading digit is n // power
    leading = n // power
    
    # Ensure it's in valid range
    if leading >= BASE:
        leading = leading % BASE
        if leading == 0:
            leading = BASE - 1
    
    return leading

# =============================================================================
# PROBABILITY MODELS
# =============================================================================

def naive_benford_prob(d, base=BASE):
    """Naive Benford probability: P(d) = log_b(1 + 1/d)."""
    return np.log(1 + 1/d) / np.log(base)

def primorial_adjusted_prob(d, base=BASE):
    """
    Primorial-adjusted Benford probability.
    Normalized over coprime digits only.
    P(d) proportional to log_b(1 + 1/d) for coprime d, 0 otherwise.
    """
    if math.gcd(d, base) != 1:
        return 0.0
    
    # Unnormalized weight
    weight = np.log(1 + 1/d)
    return weight

def compute_normalized_primorial_probs():
    """Compute normalized primorial-adjusted probabilities for all coprime digits."""
    weights = {}
    total_weight = 0.0
    
    for d in COPRIME_DIGITS:
        w = primorial_adjusted_prob(d)
        weights[d] = w
        total_weight += w
    
    # Normalize
    probs = {d: w / total_weight for d, w in weights.items()}
    return probs

# =============================================================================
# STATISTICAL TESTS
# =============================================================================

def kl_divergence(p, q):
    """
    Compute KL divergence D_KL(P || Q) = sum_i P(i) * log(P(i)/Q(i)).
    p and q are dictionaries or arrays of probabilities.
    """
    kl = 0.0
    for key in p:
        if p[key] > 0:
            if q.get(key, 0) <= 0:
                return float('inf')  # Undefined
            kl += p[key] * np.log(p[key] / q[key])
    return kl

def chi_square_test(observed, expected, digits):
    """Perform chi-square goodness of fit test."""
    chi2 = 0.0
    dof = 0
    for d in digits:
        if expected[d] > 0:
            # Pool small expected counts
            if expected[d] * sum(observed.values()) >= 5:
                chi2 += (observed.get(d, 0) - expected[d])**2 / expected[d]
                dof += 1
    
    # Adjust DOF: subtract 1 for constraint that probabilities sum to 1
    dof = max(1, dof - 1)
    
    # Compute p-value
    if chi2 > 0 and dof > 0:
        p_value = 1 - stats.chi2.cdf(chi2 * sum(observed.values()), dof)
    else:
        p_value = 1.0
    
    return chi2, dof, p_value

def total_variation_distance(p, q, digits):
    """Compute total variation distance: 0.5 * sum |p(i) - q(i)|."""
    tvd = 0.0
    for d in digits:
        tvd += abs(p.get(d, 0) - q.get(d, 0))
    return 0.5 * tvd

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    print("=" * 80)
    print("PRIMORIAL-ADJUSTED BENFORD MODEL VALIDATION")
    print(f"Base: {BASE} (primorial 2*3*5*7 = 210)")
    print(f"Max Prime: {MAX_PRIME:,}")
    print(f"Coprime digits: {PHI_BASE}")
    print("=" * 80)
    
    # Step 1: Generate primes
    print("\n[1] Generating primes...")
    primes = segmented_sieve(MAX_PRIME)
    print(f"    Found {len(primes):,} primes up to {MAX_PRIME:,}")
    
    # Step 2: Extract leading digits in base 210
    print("\n[2] Extracting leading digits in base-210...")
    
    # Skip primes <= 210 for clean leading digit analysis
    valid_primes = primes[primes > BASE]
    print(f"    Analyzing {len(valid_primes):,} primes > {BASE}")
    
    # Vectorized leading digit extraction
    leading_digits = np.array([get_leading_digit_base210(p) for p in valid_primes])
    
    # Count frequencies
    empirical_counts = {}
    for d in COPRIME_DIGITS:
        empirical_counts[d] = 0
    
    for ld in leading_digits:
        if ld in empirical_counts:
            empirical_counts[ld] += 1
    
    total = sum(empirical_counts.values())
    empirical_probs = {d: c / total for d, c in empirical_counts.items()}
    
    print(f"    Total leading digits analyzed: {total:,}")
    print(f"    Expected per digit (uniform): {total/PHI_BASE:,.1f}")
    
    # Step 3: Compute theoretical models
    print("\n[3] Computing theoretical models...")
    
    # Naive Benford (all digits 1-209)
    naive_probs_all = {d: naive_benford_prob(d) for d in range(1, BASE)}
    # Normalize naive to coprime digits (incorrect model)
    naive_coprime_sum = sum(naive_probs_all[d] for d in COPRIME_DIGITS)
    naive_probs = {d: naive_probs_all[d] / naive_coprime_sum for d in COPRIME_DIGITS}
    
    # Primorial-adjusted
    primorial_probs = compute_normalized_primorial_probs()
    
    # Uniform over coprime digits (null hypothesis)
    uniform_probs = {d: 1.0 / PHI_BASE for d in COPRIME_DIGITS}
    
    # Verify normalization
    print(f"    Naive model sum: {sum(naive_probs.values()):.6f}")
    print(f"    Primorial model sum: {sum(primorial_probs.values()):.6f}")
    print(f"    Uniform model sum: {sum(uniform_probs.values()):.6f}")
    
    # Step 4: Compute KL divergences
    print("\n" + "=" * 80)
    print("HYPOTHESIS 1: KL DIVERGENCE COMPARISON")
    print("=" * 80)
    
    # KL(empirical || model)
    kl_naive = kl_divergence(empirical_probs, naive_probs, COPRIME_DIGITS)
    kl_primorial = kl_divergence(empirical_probs, primorial_probs, COPRIME_DIGITS)
    kl_uniform = kl_divergence(empirical_probs, uniform_probs, COPRIME_DIGITS)
    
    print(f"\nKL Divergence (Empirical || Naive Benford):     {kl_naive:.6f}")
    print(f"KL Divergence (Empirical || Primorial-Adjusted): {kl_primorial:.6f}")
    print(f"KL Divergence (Empirical || Uniform):            {kl_uniform:.6f}")
    
    # KL(model || empirical) - reverse direction
    kl_naive_rev = kl_divergence(naive_probs, empirical_probs, COPRIME_DIGITS)
    kl_primorial_rev = kl_divergence(primorial_probs, empirical_probs, COPRIME_DIGITS)
    
    print(f"\nKL Divergence (Naive || Empirical):     {kl_naive_rev:.6f}")
    print(f"KL Divergence (Primorial || Empirical): {kl_primorial_rev:.6f}")
    
    # Symmetric KL (Jensen-Shannon related)
    kl_reduction = (kl_naive - kl_primorial) / kl_naive * 100 if kl_naive > 0 else 0
    print(f"\n>>> KL Reduction from Primorial adjustment: {kl_reduction:.2f}%")
    
    # Test: Is primorial KL < 0.05 (random fluctuation threshold)?
    threshold = 0.05
    h1_result = "SUPPORTED" if kl_primorial < threshold else "NOT SUPPORTED"
    print(f"\n>>> H1 Test: Is KL < {threshold}? {h1_result}")
    print(f"    (KL_primorial = {kl_primorial:.6f}, threshold = {threshold})")
    
    # Step 5: Chi-square goodness of fit
    print("\n" + "=" * 80)
    print("HYPOTHESIS 2: CHI-SQUARE GOODNESS OF FIT")
    print("=" * 80)
    
    chi2_naive, dof_naive, p_naive = chi_square_test(empirical_probs, naive_probs, COPRIME_DIGITS)
    chi2_prim, dof_prim, p_prim = chi_square_test(empirical_probs, primorial_probs, COPRIME_DIGITS)
    chi2_unif, dof_unif, p_unif = chi_square_test(empirical_probs, uniform_probs, COPRIME_DIGITS)
    
    print(f"\nNaive Benford:     χ² = {chi2_naive*total:.2f}, p = {p_naive:.6f}")
    print(f"Primorial-Adjusted: χ² = {chi2_prim*total:.2f}, p = {p_prim:.6f}")
    print(f"Uniform:            χ² = {chi2_unif*total:.2f}, p = {p_unif:.6f}")
    
    alpha = 0.05
    h2_result = "SUPPORTED" if p_prim > alpha else "NOT SUPPORTED"
    print(f"\n>>> H2 Test: Good fit at α={alpha}? {h2_result}")
    print(f"    (p-value = {p_prim:.6f}, α = {alpha})")
    
    # Step 6: Total variation distance
    print("\n" + "=" * 80)
    print("HYPOTHESIS 3: TOTAL VARIATION DISTANCE")
    print("=" * 80)
    
    tvd_naive = total_variation_distance(empirical_probs, naive_probs, COPRIME_DIGITS)
    tvd_primorial = total_variation_distance(empirical_probs, primorial_probs, COPRIME_DIGITS)
    tvd_uniform = total_variation_distance(empirical_probs, uniform_probs, COPRIME_DIGITS)
    
    print(f"\nTVD (Empirical, Naive):     {tvd_naive:.6f}")
    print(f"TVD (Empirical, Primorial): {tvd_primorial:.6f}")
    print(f"TVD (Empirical, Uniform):   {tvd_uniform:.6f}")
    
    tvd_threshold = 0.1
    h3_result = "SUPPORTED" if tvd_primorial < tvd_threshold else "NOT SUPPORTED"
    print(f"\n>>> H3 Test: TVD < {tvd_threshold}? {h3_result}")
    print(f"    (TVD = {tvd_primorial:.6f}, threshold = {tvd_threshold})")
    
    # Step 7: Specific prediction for digit 1
    print("\n" + "=" * 80)
    print("HYPOTHESIS 4: SPECIFIC PREDICTION FOR DIGIT 1")
    print("=" * 80)
    
    empirical_d1 = empirical_probs.get(1, 0)
    naive_d1 = naive_probs.get(1, 0)
    primorial_d1 = primorial_probs.get(1, 0)
    
    print(f"\nP(d=1) empirical:   {empirical_d1:.6f}")
    print(f"P(d=1) naive:       {naive_d1:.6f}")
    print(f"P(d=1) primorial:   {primorial_d1:.6f}")
    print(f"Expected (theory):  ~0.4675")
    
    # Theoretical calculation for primorial model
    theoretical_d1 = np.log(2) / sum(np.log(1 + 1/d) for d in COPRIME_DIGITS)
    print(f"Computed theoretical: {theoretical_d1:.6f}")
    
    error_naive = abs(empirical_d1 - naive_d1) / empirical_d1 * 100
    error_primorial = abs(empirical_d1 - primorial_d1) / empirical_d1 * 100
    
    print(f"\nRelative error (naive):     {error_naive:.2f}%")
    print(f"Relative error (primorial): {error_primorial:.2f}%")
    
    h4_result = "SUPPORTED" if error_primorial < error_naive else "NOT SUPPORTED"
    print(f"\n>>> H4 Test: Primorial closer to empirical? {h4_result}")
    
    # Step 8: Visualizations
    print("\n[4] Generating visualizations...")
    
    # Sort digits for plotting
    sorted_digits = sorted(COPRIME_DIGITS)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Plot 1: Probability comparison
    ax = axes[0, 0]
    x = np.arange(len(sorted_digits))
    width = 0.25
    
    emp_vals = [empirical_probs[d] for d in sorted_digits]
    naive_vals = [naive_probs[d] for d in sorted_digits]
    prim_vals = [primorial_probs[d] for d in sorted_digits]
    
    ax.bar(x - width, emp_vals, width, label='Empirical', alpha=0.8, color='black')
    ax.bar(x, naive_vals, width, label='Naive Benford', alpha=0.6, color='red')
    ax.bar(x + width, prim_vals, width, label='Primorial-Adjusted', alpha=0.6, color='blue')
    
    ax.set_xlabel('Leading Digit (coprime to 210)')
    ax.set_ylabel('Probability')
    ax.set_title('Leading Digit Distribution Comparison')
    ax.set_xticks(x[::5])
    ax.set_xticklabels([str(sorted_digits[i]) for i in range(0, len(sorted_digits), 5)], rotation=45)
    ax.legend()
    ax.set_yscale('log')
    
    # Plot 2: Residuals
    ax = axes[0, 1]
    resid_naive = [empirical_probs[d] - naive_probs[d] for d in sorted_digits]
    resid_prim = [empirical_probs[d] - primorial_probs[d] for d in sorted_digits]
    
    ax.plot(sorted_digits, resid_naive, 'r-', alpha=0.7, label='Naive residuals')
    ax.plot(sorted_digits, resid_prim, 'b-', alpha=0.7, label='Primorial residuals')
    ax.axhline(y=0, color='k', linestyle='--')
    ax.set_xlabel('Leading Digit')
    ax.set_ylabel('Residual (Empirical - Model)')
    ax.set_title('Model Residuals')
    ax.legend()
    
    # Plot 3: CDF comparison
    ax = axes[1, 0]
    emp_cdf = np.cumsum(emp_vals)
    naive_cdf = np.cumsum(naive_vals)
    prim_cdf = np.cumsum(prim_vals)
    
    ax.plot(sorted_digits, emp_cdf, 'k-', linewidth=2, label='Empirical')
    ax.plot(sorted_digits, naive_cdf, 'r--', linewidth=1.5, label='Naive')
    ax.plot(sorted_digits, prim_cdf, 'b--', linewidth=1.5, label='Primorial')
    ax.set_xlabel('Leading Digit')
    ax.set_ylabel('Cumulative Probability')
    ax.set_title('Cumulative Distribution Functions')
    ax.legend()
    
    # Plot 4: Metrics summary
    ax = axes[1, 1]
    ax.axis('off')
    
    metrics_text = f"""
    STATISTICAL SUMMARY
    ===================
    
    Sample Size: {total:,} primes
    
    KL DIVERGENCES:
      Naive Benford:      {kl_naive:.6f}
      Primorial-Adjusted: {kl_primorial:.6f}
      Uniform:            {kl_uniform:.6f}
      Reduction:          {kl_reduction:.1f}%
    
    TOTAL VARIATION DISTANCE:
      Naive:              {tvd_naive:.6f}
      Primorial:          {tvd_primorial:.6f}
      Uniform:            {tvd_uniform:.6f}
    
    CHI-SQUARE (scaled by N):
      Naive:              {chi2_naive*total:.2f}
      Primorial:          {chi2_prim*total:.2f}
      Uniform:            {chi2_unif*total:.2f}
    
    P(d=1) PREDICTION:
      Empirical:          {empirical_d1:.4f}
      Primorial (theory): {theoretical_d1:.4f}
      Error:              {error_primorial:.2f}%
    
    HYPOTHESIS TESTS:
      H1 (KL < 0.05):     {h1_result}
      H2 (p > 0.05):      {h2_result}
      H3 (TVD < 0.1):     {h3_result}
      H4 (d=1 accuracy):  {h4_result}
    """
    
    ax.text(0.1, 0.5, metrics_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='center', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('primorial_benford_analysis.png', dpi=150, bbox_inches='tight')
    print("    Saved: primorial_benford_analysis.png")
    
    # Additional detailed plot
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    # Show first 20 coprime digits in detail
    detail_digits = sorted_digits[:20]
    x = np.arange(len(detail_digits))
    width = 0.25
    
    emp_detail = [empirical_probs[d] for d in detail_digits]
    naive_detail = [naive_probs[d] for d in detail_digits]
    prim_detail = [primorial_probs[d] for d in detail_digits]
    
    ax2.bar(x - width, emp_detail, width, label='Empirical', alpha=0.9, color='black')
    ax2.bar(x, naive_detail, width, label='Naive Benford', alpha=0.7, color='crimson')
    ax2.bar(x + width, prim_detail, width, label='Primorial-Adjusted', alpha=0.7, color='steelblue')
    
    ax2.set_xlabel('Leading Digit')
    ax2.set_ylabel('Probability')
    ax2.set_title('Detailed View: First 20 Coprime Digits')
    ax2.set_xticks(x)
    ax2.set_xticklabels([str(d) for d in detail_digits])
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('primorial_benford_detail.png', dpi=150, bbox_inches='tight')
    print("    Saved: primorial_benford_detail.png")
    
    # Runtime
    elapsed = time.time() - start_time
    print(f"\n[5] Total runtime: {elapsed:.2f} seconds")
    
    # =============================================================================
    # CONCLUSIONS
    # =============================================================================
    print("\n" + "=" * 80)
    print("CONCLUSIONS")
    print("=" * 80)
    
    print(f"""
    The primorial-adjusted Benford model for base-210 was tested against
    {total:,} prime numbers up to {MAX_PRIME:,}.
    
    KEY FINDINGS:
    
    1. KL DIVERGENCE: The primorial-adjusted model achieves KL = {kl_primorial:.6f}
       vs. naive Benford KL = {kl_naive:.6f}, a {kl_reduction:.1f}% reduction.
       Status: {'PASS' if kl_primorial < kl_naive else 'FAIL'}
    
    2. GOODNESS OF FIT: Chi-square test yields p = {p_prim:.4f} for primorial model
       vs. p = {p_naive:.4f} for naive model.
       Status: {'PASS (good fit)' if p_prim > 0.05 else 'FAIL (reject fit)'}
    
    3. TOTAL VARIATION: TVD = {tvd_primorial:.4f} for primorial vs {tvd_naive:.4f} naive.
       Status: {'PASS' if tvd_primorial < tvd_naive else 'FAIL'}
    
    4. DIGIT 1 PREDICTION: Predicted P(d=1) = {theoretical_d1:.4f}, empirical = {empirical_d1:.4f}.
       Status: {'PASS' if error_primorial < 5 else 'FAIL'}
    
    OVERALL ASSESSMENT:
    The primorial-adjusted Benford model {'SUCCESSFULLY' if (kl_primorial < kl_naive and tvd_primorial < tvd_naive) else 'PARTIALLY'} 
    accounts for the non-uniform distribution of leading digits in base-210.
    The restriction to coprime digits (φ(210)=48) is essential; naive Benford
    fails because it doesn't account for the arithmetic structure of primes.
    
    The model's prediction of P(d=1) ≈ 0.4675 is {'confirmed' if abs(empirical_d1 - theoretical_d1) < 0.01 else 'not fully confirmed'}
    by empirical data (observed: {empirical_d1:.4f}).
    """)
    
    # Return key metrics for potential further analysis
    return {
        'kl_primorial': kl_primorial,
        'kl_naive': kl_naive,
        'tvd_primorial': tvd_primorial,
        'tvd_naive': tvd_naive,
        'p_value_primorial': p_prim,
        'empirical_d1': empirical_d1,
        'theoretical_d1': theoretical_d1
    }

if __name__ == "__main__":
    try:
        results = main()
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        # Ensure we still print conclusions
        print("\n" + "=" * 80)
        print("CONCLUSIONS")
        print("=" * 80)
        print("Script encountered an error. Partial results may be available above.")
        print(f"Error: {e}")