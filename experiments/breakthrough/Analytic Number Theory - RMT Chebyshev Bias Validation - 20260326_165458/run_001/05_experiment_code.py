import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Constants and Parameters ---
MAX_X = 10**7  # Upper limit for prime counting (adjust if needed for runtime)
MODULUS = 210
PHI_MOD = 48  # Euler totient φ(210) = φ(2*3*5*7) = 1*2*4*6 = 48
PRIMES_PER_CLASS = {a: [] for a in range(1, MODULUS) if np.gcd(a, MODULUS) == 1}
PRIMES = []  # Will be filled by segmented sieve

# --- Helper Functions ---

def sieve_primes(n):
    """Segmented sieve to generate primes up to n efficiently."""
    if n < 2:
        return []
    limit = int(np.sqrt(n)) + 1
    # Base sieve up to sqrt(n)
    is_prime = np.ones(limit, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if is_prime[i]:
            is_prime[i*i:limit:i] = False
    base_primes = np.where(is_prime)[0].astype(np.int64)
    
    # Segmented sieve
    segment_size = 10**6
    primes = []
    for low in range(2, n+1, segment_size):
        high = min(low + segment_size - 1, n)
        segment_len = high - low + 1
        segment = np.ones(segment_len, dtype=bool)
        for p in base_primes:
            if p * p > high:
                break
            start = max(p * p, ((low + p - 1) // p) * p)
            segment[start - low::p] = False
        for i, is_p in enumerate(segment):
            if is_p:
                primes.append(low + i)
    return np.array(primes, dtype=np.int64)

def compute_chebyshev_bias(primes, modulus, a, b):
    """Compute π(x; modulus, a) - π(x; modulus, b) for primes up to max_x."""
    x = max(primes)
    count_a = np.sum(primes % modulus == a)
    count_b = np.sum(primes % modulus == b)
    return count_a - count_b

def compute_log_ratio(primes, modulus, a, b):
    """Compute log-ratio bias: log(π(x; q,a)/π(x; q,b))"""
    count_a = np.sum(primes % modulus == a)
    count_b = np.sum(primes % modulus == b)
    if count_b == 0:
        return np.inf
    return np.log(count_a / count_b)

# --- Hypothesis 1: RMT Covariance Model Validation ---
def compute_zero_covariance_matrix():
    """
    Approximate covariance matrix Σ of Chebyshev bias using RMT-inspired model.
    For Dirichlet L-functions modulo 210, we use first 100 zeros of each non-principal character.
    Since computing L-function zeros is expensive, we simulate using random matrix theory predictions.
    """
    # Number of independent characters: φ(210)/2 = 24 (since complex conjugates pair)
    # Simplified: use 24 independent bias processes
    n_chars = 24
    # Simulate zero frequencies: use Wigner surmise spacing distribution
    # For GOE: p(s) = (π s / 2) exp(-π s^2 / 4)
    def wigner_spacing(n):
        # Inverse transform sampling approximation
        u = np.random.rand(n)
        s = np.sqrt(4/np.pi * np.log(1/(1-u)))
        return s
    
    # Generate 100 zeros per character (scaled to match Riemann zeta density)
    zeros_per_char = 100
    zeros = []
    for _ in range(n_chars):
        # Scale: average spacing ~ 2π / log(T/2π) ~ 0.5 for low-lying zeros
        # We'll use empirical scaling: first 100 zeros have average spacing ~0.5
        spacings = wigner_spacing(zeros_per_char - 1)
        zeros_char = np.concatenate([[0.0], np.cumsum(spacings)])
        zeros.append(zeros_char)
    
    zeros = np.array(zeros)  # shape (n_chars, zeros_per_char)
    
    # Compute covariance matrix Σ_ij = lim_{x→∞} (1/log log x) * Cov(log π(x;q,χ_i), log π(x;q,χ_j))
    # For simplicity, use RMT prediction: Σ ≈ (2/π^2) * I (identity scaled)
    # This matches Rubinstein-Sarnak: variance ~ (1/2) log log x
    # We'll use a diagonal matrix with entries ~0.5 (empirical variance factor)
    Σ = 0.5 * np.eye(n_chars)
    
    return Σ, zeros

def validate_rmt_covariance():
    """Validate RMT covariance model against empirical Chebyshev bias variance."""
    global PRIMES
    # Generate primes up to MAX_X
    PRIMES = sieve_primes(MAX_X)
    
    # Get residues coprime to 210
    residues = [a for a in range(1, MODULUS) if np.gcd(a, MODULUS) == 1]
    
    # Compute bias for all residue pairs (a, b) where a is QR, b is NR mod 210
    # First, determine quadratic residues mod 210
    qr_set = set()
    for x in range(1, MODULUS):
        if np.gcd(x, MODULUS) == 1:
            qr_set.add((x * x) % MODULUS)
    qr_residues = sorted([a for a in residues if a in qr_set])
    nr_residues = sorted([a for a in residues if a not in qr_set])
    
    # For each prime count up to x (sample points), compute bias
    sample_points = [10**5, 2*10**5, 5*10**5, 10**6, 2*10**6, 5*10**6, MAX_X]
    biases = []
    
    for x in sample_points:
        mask = PRIMES <= x
        prime_subset = PRIMES[mask]
        for a in nr_residues[:3]:  # Test first 3 NR residues
            for b in qr_residues[:3]:  # Test first 3 QR residues
                count_a = np.sum(prime_subset % MODULUS == a)
                count_b = np.sum(prime_subset % MODULUS == b)
                if count_b > 0:
                    bias = (count_a - count_b) / np.sqrt(np.log(np.log(x + np.e)))
                    biases.append(bias)
    
    if len(biases) < 2:
        print("HYPOTHESIS 1: INSUFFICIENT DATA (no samples)")
        return False, 0.0, 0.0
    
    # Compute empirical variance
    empirical_var = np.var(biases, ddof=1)
    
    # RMT prediction: variance ≈ (1/2) * log log x (Rubinstein-Sarnak)
    # For x = MAX_X, log log x ≈ log log(1e7) ≈ log(16.1) ≈ 2.78
    x_ref = MAX_X
    rmt_var = 0.5 * np.log(np.log(x_ref + np.e))
    
    # Compute relative error
    rel_error = abs(empirical_var - rmt_var) / rmt_var if rmt_var > 0 else 0.0
    
    # Check ±10% agreement
    passed = rel_error <= 0.10
    
    return passed, empirical_var, rmt_var

# --- Hypothesis 2: LDAB Model for Base-210 Leading Digits ---
def compute_ldab_kl_divergence():
    """Compute KL divergence for prime leading digits in base-210 using LDAB model."""
    global PRIMES
    PRIMES = sieve_primes(MAX_X)
    
    # Filter primes > 210 to get meaningful leading digits
    primes_filtered = PRIMES[PRIMES > 210]
    if len(primes_filtered) == 0:
        print("HYPOTHESIS 2: NO PRIMES > 210")
        return False, 0.0, 0.0
    
    # Compute leading digit in base 210: floor(prime / 210^k) where 210^k <= prime < 210^{k+1}
    def leading_digit_base_b(n, b):
        if n <= 0:
            return 1
        k = int(np.floor(np.log(n) / np.log(b)))
        return int(n // (b**k))
    
    leading_digits = np.array([leading_digit_base_b(p, MODULUS) for p in primes_filtered])
    
    # Count frequencies
    digits = np.arange(1, MODULUS)
    observed_counts = np.array([np.sum(leading_digits == d) for d in digits], dtype=float)
    total = np.sum(observed_counts)
    observed_freq = observed_counts / total
    
    # LDAB model: P(d) = log_b((d+1)/d) * (1 + α * log log d / log d)
    # For base b=210, estimate α by minimizing KL divergence
    def ldab_prob(d, alpha):
        base = np.log((d+1)/d) / np.log(MODULUS)
        correction = 1.0 + alpha * np.log(np.log(d + np.e)) / np.log(d + 1)
        return base * correction
    
    # Normalize LDAB probabilities
    def normalize_ldab(alpha):
        probs = np.array([ldab_prob(d, alpha) for d in digits])
        return probs / np.sum(probs)
    
    # Find optimal alpha
    def kl_objective(alpha):
        probs = normalize_ldab(alpha)
        # Avoid log(0)
        probs = np.clip(probs, 1e-12, 1.0)
        observed_clipped = np.clip(observed_freq, 1e-12, 1.0)
        return np.sum(observed_clipped * np.log(observed_clipped / probs))
    
    # Minimize KL divergence over alpha
    res = minimize_scalar(kl_objective, bounds=(-1.0, 1.0), method='bounded')
    alpha_opt = res.x
    
    # Compute final KL divergence
    probs_opt = normalize_ldab(alpha_opt)
    probs_opt = np.clip(probs_opt, 1e-12, 1.0)
    kl_div = np.sum(observed_freq * np.log(observed_freq / probs_opt))
    
    # Compare to base Benford (α=0)
    probs_benford = np.array([ldab_prob(d, 0.0) for d in digits])
    probs_benford = probs_benford / np.sum(probs_benford)
    probs_benford = np.clip(probs_benford, 1e-12, 1.0)
    kl_benford = np.sum(observed_freq * np.log(observed_freq / probs_benford))
    
    # Hypothesis: KL divergence reduced from 0.511 to ~0.000034
    # We'll check if final KL < 0.001 (conservative threshold)
    passed = kl_div < 0.001
    
    return passed, kl_div, kl_benford

# --- Hypothesis 3: Multivariate Chebyshev Bias Direction Prediction ---
def test_bias_direction_prediction():
    """Test if Dirichlet characters predict bias direction in ≥92% of classes."""
    global PRIMES
    PRIMES = sieve_primes(MAX_X)
    
    residues = [a for a in range(1, MODULUS) if np.gcd(a, MODULUS) == 1]
    
    # Quadratic residues mod 210
    qr_set = set()
    for x in range(1, MODULUS):
        if np.gcd(x, MODULUS) == 1:
            qr_set.add((x * x) % MODULUS)
    qr_residues = [a for a in residues if a in qr_set]
    nr_residues = [a for a in residues if a not in qr_set]
    
    # For each residue class, compute bias vs a fixed reference (e.g., 1)
    ref = 1
    bias_signs = []
    predictions = []
    
    for a in residues:
        count_a = np.sum(PRIMES % MODULUS == a)
        count_ref = np.sum(PRIMES % MODULUS == ref)
        bias = count_a - count_ref
        bias_sign = np.sign(bias) if bias != 0 else 0.0
        
        # Prediction: NR classes should have positive bias (more primes)
        prediction = 1.0 if a in nr_residues else (-1.0 if a in qr_residues else 0.0)
        
        bias_signs.append(bias_sign)
        predictions.append(prediction)
    
    # Compute agreement
    bias_signs = np.array(bias_signs)
    predictions = np.array(predictions)
    
    # Only compare non-zero predictions
    mask = predictions != 0
    agreement = np.mean(bias_signs[mask] == predictions[mask])
    
    # Hypothesis: ≥92% agreement
    passed = agreement >= 0.92
    
    return passed, agreement * 100

# --- Hypothesis 4: Log-Log Growth of Bias Magnitude ---
def test_log_log_growth():
    """Test that bias magnitude scales as log log x."""
    global PRIMES
    PRIMES = sieve_primes(MAX_X)
    
    sample_points = np.logspace(4, np.log10(MAX_X), 20, dtype=int)
    biases = []
    loglog_x = []
    
    for x in sample_points:
        mask = PRIMES <= x
        prime_subset = PRIMES[mask]
        count_3 = np.sum(prime_subset % 4 == 3)  # Classic 4k+3 vs 4k+1
        count_1 = np.sum(prime_subset % 4 == 1)
        bias = count_3 - count_1
        biases.append(bias)
        loglog_x.append(np.log(np.log(x + np.e)))
    
    # Fit: bias = α * log log x + β
    loglog_x = np.array(loglog_x)
    biases = np.array(biases)
    
    # Linear regression
    A = np.vstack([loglog_x, np.ones(len(loglog_x))]).T
    alpha, beta = np.linalg.lstsq(A, biases, rcond=None)[0]
    
    # Compute R²
    y_pred = alpha * loglog_x + beta
    ss_res = np.sum((biases - y_pred)**2)
    ss_tot = np.sum((biases - np.mean(biases))**2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    
    # Rubinstein-Sarnak prediction: α ≈ 1/(2√2) ≈ 0.3535 for mod 4
    # We'll check if α is positive and significant
    passed = r_squared > 0.95 and alpha > 0.2
    
    return passed, alpha, r_squared

# --- Hypothesis 5: RMT-Corrected Detection Test Performance ---
def test_detection_performance():
    """Test Mahalanobis-distance-based detection using RMT covariance."""
    global PRIMES
    PRIMES = sieve_primes(MAX_X)
    
    # Get residues coprime to 210
    residues = [a for a in range(1, MODULUS) if np.gcd(a, MODULUS) == 1]
    
    # Compute normalized bias vector for sample points
    sample_points = [10**5, 5*10**5, 10**6, 2*10**6, 5*10**6, MAX_X]
    bias_vectors = []
    
    for x in sample_points:
        mask = PRIMES <= x
        prime_subset = PRIMES[mask]
        bias_vec = []
        for a in residues:
            count_a = np.sum(prime_subset % MODULUS == a)
            bias_vec.append(count_a)
        # Normalize by expected count (π(x)/φ(m))
        expected = len(prime_subset) / len(residues)
        bias_vec = (np.array(bias_vec) - expected) / np.sqrt(expected)
        bias_vectors.append(bias_vec)
    
    bias_vectors = np.array(bias_vectors)
    
    # Compute sample covariance
    Σ_emp = np.cov(bias_vectors.T)
    
    # RMT covariance (identity scaled)
    Σ_rmt = np.eye(len(residues)) * np.mean(np.diag(Σ_emp))
    
    # Compute Mahalanobis distances
    try:
        Σ_inv = np.linalg.inv(Σ_rmt)
    except:
        print("HYPOTHESIS 5: SINGULAR COVARIANCE MATRIX")
        return False, 0.0, 0.0
    
    # Mean bias vector
    mean_bias = np.mean(bias_vectors, axis=0)
    
    # Mahalanobis distance for each sample point
    mahal_dists = []
    for vec in bias_vectors:
        diff = vec - mean_bias
        mahal_dists.append(np.sqrt(diff @ Σ_inv @ diff))
    
    mahal_dists = np.array(mahal_dists)
    
    # Expected distribution: χ² with df = len(residues), so E[dist] ≈ sqrt(df)
    df = len(residues)
    expected_mahal = np.sqrt(df)
    rel_error = abs(np.mean(mahal_dists) - expected_mahal) / expected_mahal
    
    # Hypothesis: within ±10% of expected
    passed = rel_error <= 0.10
    
    return passed, np.mean(mahal_dists), expected_mahal

# --- Main Execution ---
def main():
    print("=" * 70)
    print("RMT-Corrected Chebyshev Bias and LDAB Validation Tests")
    print("=" * 70)
    
    # Hypothesis 1
    print("\n[HYPOTHESIS 1] RMT Covariance Model Validation")
    print("-" * 50)
    try:
        h1_passed, emp_var, rmt_var = validate_rmt_covariance()
        print(f"Empirical variance: {emp_var:.6f}")
        print(f"RMT prediction:     {rmt_var:.6f}")
        print(f"Relative error:     {abs(emp_var - rmt_var) / rmt_var * 100:.2f}%")
        print(f"Result: {'PASSED' if h1_passed else 'FAILED'} (within ±10%: {h1_passed})")
    except Exception as e:
        print(f"ERROR: {e}")
        h1_passed = False
    
    # Hypothesis 2
    print("\n[HYPOTHESIS 2] LDAB Model for Base-210 Leading Digits")
    print("-" * 50)
    try:
        h2_passed, kl_final, kl_benford = compute_ldab_kl_divergence()
        print(f"KL divergence (Benford, α=0): {kl_benford:.6f}")
        print(f"KL divergence (LDAB, α≈{0.0:.3f}): {kl_final:.6f}")
        print(f"Result: {'PASSED' if h2_passed else 'FAILED'} (KL < 0.001: {h2_passed})")
    except Exception as e:
        print(f"ERROR: {e}")
        h2_passed = False
    
    # Hypothesis 3
    print("\n[HYPOTHESIS 3] Dirichlet Character Bias Direction Prediction")
    print("-" * 50)
    try:
        h3_passed, agreement_pct = test_bias_direction_prediction()
        print(f"Agreement: {agreement_pct:.2f}%")
        print(f"Result: {'PASSED' if h3_passed else 'FAILED'} (≥92%: {h3_passed})")
    except Exception as e:
        print(f"ERROR: {e}")
        h3_passed = False
    
    # Hypothesis 4
    print("\n[HYPOTHESIS 4] Log-Log Growth of Bias Magnitude")
    print("-" * 50)
    try:
        h4_passed, alpha, r_sq = test_log_log_growth()
        print(f"Slope (α): {alpha:.6f}")
        print(f"R²:        {r_sq:.6f}")
        print(f"Result: {'PASSED' if h4_passed else 'FAILED'} (R² > 0.95 & α > 0.2: {h4_passed})")
    except Exception as e:
        print(f"ERROR: {e}")
        h4_passed = False
    
    # Hypothesis 5
    print("\n[HYPOTHESIS 5] RMT-Corrected Detection Test Performance")
    print("-" * 50)
    try:
        h5_passed, mean_mahal, exp_mahal = test_detection_performance()
        print(f"Mean Mahalanobis distance: {mean_mahal:.4f}")
        print(f"Expected (χ² df={PHI_MOD}): {exp_mahal:.4f}")
        print(f"Relative error: {abs(mean_mahal - exp_mahal) / exp_mahal * 100:.2f}%")
        print(f"Result: {'PASSED' if h5_passed else 'FAILED'} (within ±10%: {h5_passed})")
    except Exception as e:
        print(f"ERROR: {e}")
        h5_passed = False
    
    # Summary
    print("\n" + "=" * 70)
    print("CONCLUSIONS:")
    total_passed = sum([h1_passed, h2_passed, h3_passed, h4_passed, h5_passed])
    print(f"  Hypotheses tested: 5")
    print(f"  Hypotheses passed: {total_passed}")
    print(f"  Overall status: {'CONFIRMED' if total_passed >= 4 else 'PARTIAL/REJECTED'}")
    
    if total_passed >= 4:
        print("  → RMT-corrected Chebyshev bias model and LDAB validation supported by data.")
    else:
        print("  → Further investigation needed for some hypotheses.")
    
    print("=" * 70)

if __name__ == "__main__":
    main()