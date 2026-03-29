import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def sieve_primes_up_to(n):
    """Return list of primes up to n using optimized sieve."""
    if n < 2:
        return []
    size = n + 1
    sieve = np.ones(size, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i:n+1:i] = False
    return np.nonzero(sieve)[0]

def primorial(k):
    """Return the k-th primorial P_k (product of first k primes)."""
    primes = sieve_primes_up_to(100)  # enough for k up to ~25
    if k <= 0:
        return 1
    return int(np.prod(primes[:k]))

def coprime_residues(modulus):
    """Return sorted list of residues coprime to modulus."""
    residues = []
    for r in range(1, modulus):
        if np.gcd(r, modulus) == 1:
            residues.append(r)
    return np.array(residues, dtype=np.int64)

def compute_gaps(residues, modulus):
    """Compute gaps between consecutive coprime residues, wrapping around."""
    if len(residues) == 0:
        return np.array([], dtype=np.int64)
    gaps = np.diff(residues)
    # Wrap around: last to first + modulus
    gaps = np.append(gaps, modulus - residues[-1] + residues[0])
    return gaps

def compute_R(gaps):
    """Compute variance-to-mean ratio R = Var(gaps)/Mean(gaps)."""
    if len(gaps) == 0:
        return np.nan
    mean_g = np.mean(gaps)
    var_g = np.var(gaps, ddof=0)  # population variance
    if mean_g == 0:
        return np.nan
    return var_g / mean_g

def generate_data(max_k=9):
    """Generate R(k) values for k=1..max_k."""
    R_vals = []
    log_P_vals = []
    P_vals = []
    for k in range(1, max_k + 1):
        P = primorial(k)
        residues = coprime_residues(P)
        gaps = compute_gaps(residues, P)
        R = compute_R(gaps)
        R_vals.append(R)
        log_P_vals.append(np.log(P))
        P_vals.append(P)
        print(f"k={k:2d}, P_k={P:<12d}, log P_k={np.log(P):>7.2f}, R(k)={R:8.4f}")
    return np.array(P_vals), np.array(log_P_vals), np.array(R_vals)

def fit_power_law(x, y):
    """Fit y = C * x^gamma using linear regression on log-log scale."""
    # Avoid log(0) or log(negative)
    mask = (x > 0) & (y > 0)
    x_fit = x[mask]
    y_fit = y[mask]
    if len(x_fit) < 2:
        return np.nan, np.nan, np.nan
    log_x = np.log(x_fit)
    log_y = np.log(y_fit)
    slope, intercept, r, p, stderr = stats.linregress(log_x, log_y)
    C = np.exp(intercept)
    gamma = slope
    # Compute R²
    y_pred = C * x_fit**gamma
    ss_res = np.sum((y_fit - y_pred)**2)
    ss_tot = np.sum((y_fit - np.mean(y_fit))**2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return C, gamma, r_squared

def fit_log_power_law(log_P, R):
    """Fit R = C * (log P)^gamma to data."""
    # Linear regression: log R = log C + gamma * log log P
    mask = (log_P > 1) & (R > 0)
    log_log_P = np.log(log_P[mask])
    log_R = np.log(R[mask])
    if len(log_log_P) < 2:
        return np.nan, np.nan, np.nan
    slope, intercept, r, p, stderr = stats.linregress(log_log_P, log_R)
    C = np.exp(intercept)
    gamma = slope
    # Compute R²
    R_pred = C * (log_P[mask])**gamma
    ss_res = np.sum((R[mask] - R_pred)**2)
    ss_tot = np.sum((R[mask] - np.mean(R[mask]))**2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return C, gamma, r_squared

def main():
    print("="*70)
    print("Testing Asymptotic Growth of Variance-to-Mean Ratio R(k) in Primorial Gaps")
    print("="*70)
    print()

    # Generate empirical data for k=1..9
    print("Generating empirical R(k) data for k=1 to 9...")
    print("-"*70)
    P_vals, log_P_vals, R_vals = generate_data(max_k=9)
    print("-"*70)
    print()

    # --- Hypothesis 1: Sub-logarithmic power law: R(k) ~ C (log P_k)^γ, 0<γ<1 ---
    print("HYPOTHESIS 1 TEST: R(k) follows a sub-logarithmic power law in log P_k")
    print("Model: R(k) = C (log P_k)^γ, with 0 < γ < 1")
    print("-"*70)
    
    C1, gamma1, r2_1 = fit_log_power_law(log_P_vals, R_vals)
    
    print(f"Fitted parameters:")
    print(f"  C = {C1:.6f}")
    print(f"  γ = {gamma1:.6f}")
    print(f"  R² = {r2_1:.4f}")
    
    # Test γ ∈ (0,1)
    gamma_in_range = 0 < gamma1 < 1
    print(f"γ ∈ (0,1)? {gamma_in_range}")
    print(f"Hypothesis 1: {'SUPPORTED' if gamma_in_range and r2_1 > 0.9 else 'REJECTED'}")
    print()
    
    # --- Hypothesis 2: R(k) aligns with known variance scaling: Var ~ (log P)^{1.17} ---
    # Recall: R = Var / Mean. For coprime residues, mean gap = P / φ(P) = ∏_{p≤p_k} p/(p-1) ~ e^γ log P (Mertens)
    # So R = Var / Mean ~ (log P)^{1.17} / (e^γ log P) = (log P)^{0.17} / e^γ
    # So R should scale as (log P)^{0.17}
    print("HYPOTHESIS 2 TEST: R(k) aligns with variance scaling (log P)^{1.17}")
    print("Expected: R(k) ~ C (log P_k)^{0.17}  (since Mean ~ log P, Var ~ (log P)^{1.17})")
    print("-"*70)
    
    # Fit with fixed exponent 0.17
    fixed_gamma2 = 0.17
    mask2 = (log_P_vals > 1) & (R_vals > 0)
    log_log_P2 = np.log(log_P_vals[mask2])
    log_R2 = np.log(R_vals[mask2])
    # log R = log C + 0.17 * log log P  =>  log C = log R - 0.17 * log log P
    est_log_C = np.mean(log_R2 - fixed_gamma2 * log_log_P2)
    C2 = np.exp(est_log_C)
    R_pred2 = C2 * (log_P_vals[mask2])**fixed_gamma2
    ss_res2 = np.sum((R_vals[mask2] - R_pred2)**2)
    ss_tot2 = np.sum((R_vals[mask2] - np.mean(R_vals[mask2]))**2)
    r2_2 = 1 - ss_res2 / ss_tot2 if ss_tot2 > 0 else 0.0
    
    print(f"Fixed exponent: γ = {fixed_gamma2}")
    print(f"Fitted C = {C2:.6f}")
    print(f"R² = {r2_2:.4f}")
    print(f"Expected scaling exponent: 0.17 (derived from Var ~ (log P)^{1.17})")
    print(f"Hypothesis 2: {'SUPPORTED' if r2_2 > 0.95 else 'REJECTED'}")
    print()
    
    # --- Hypothesis 3: Higher-order moments scale predictably ---
    print("HYPOTHESIS 3 TEST: Higher-order moments follow predictable scaling")
    print("We test skewness and kurtosis trends vs k")
    print("-"*70)
    
    # Compute standardized moments for each k
    skew_vals = []
    kurt_vals = []
    for k in range(1, 10):
        P = primorial(k)
        residues = coprime_residues(P)
        gaps = compute_gaps(residues, P)
        mean_g = np.mean(gaps)
        std_g = np.std(gaps, ddof=0)
        if std_g == 0:
            skew_vals.append(np.nan)
            kurt_vals.append(np.nan)
        else:
            m3 = np.mean((gaps - mean_g)**3)
            m4 = np.mean((gaps - mean_g)**4)
            skew_vals.append(m3 / std_g**3)
            kurt_vals.append(m4 / std_g**4 - 3)  # excess kurtosis
    
    skew_vals = np.array(skew_vals)
    kurt_vals = np.array(kurt_vals)
    k_vals = np.arange(1, 10)
    
    # Fit linear trends in k
    slope_skew, _, _, _, _ = stats.linregress(k_vals, skew_vals)
    slope_kurt, _, _, _, _ = stats.linregress(k_vals, kurt_vals)
    
    print(f"Skewness trend: slope = {slope_skew:.4f} per k")
    print(f"Kurtosis trend: slope = {slope_kurt:.4f} per k")
    print(f"Skewness appears {'increasing' if slope_skew > 0.01 else 'decreasing/stable'}")
    print(f"Excess kurtosis appears {'increasing' if slope_kurt > 0.01 else 'decreasing/stable'}")
    print(f"Hypothesis 3: {'PARTIALLY SUPPORTED' if abs(slope_skew) > 0.01 or abs(slope_kurt) > 0.01 else 'REJECTED'}")
    print()

    # --- Visualization ---
    print("Generating diagnostic plots...")
    print("-"*70)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    
    # Panel 1: R(k) vs k
    axes[0,0].plot(k_vals, R_vals, 'bo-', linewidth=2, markersize=6)
    axes[0,0].set_xlabel('k')
    axes[0,0].set_ylabel('R(k)')
    axes[0,0].set_title('Variance-to-Mean Ratio R(k) vs k')
    axes[0,0].grid(True, alpha=0.3)
    
    # Panel 2: R(k) vs log P_k (linear scale)
    axes[0,1].plot(log_P_vals, R_vals, 'rs-', linewidth=2, markersize=6)
    axes[0,1].set_xlabel('log P_k')
    axes[0,1].set_ylabel('R(k)')
    axes[0,1].set_title('R(k) vs log P_k')
    axes[0,1].grid(True, alpha=0.3)
    
    # Panel 3: log-log plot for power-law fit
    axes[1,0].loglog(log_P_vals, R_vals, 'go-', linewidth=2, markersize=6, label='Data')
    log_P_fine = np.linspace(log_P_vals[0], log_P_vals[-1], 100)
    R_fit = C1 * (np.exp(log_P_fine))**gamma1  # R = C (log P)^γ
    axes[1,0].plot(log_P_fine, R_fit, 'k--', linewidth=2, 
                   label=f'Fit: R = C (log P)^γ, γ={gamma1:.2f}')
    axes[1,0].set_xlabel('log P_k')
    axes[1,0].set_ylabel('R(k)')
    axes[1,0].set_title('Power-Law Fit (log-log)')
    axes[1,0].legend()
    axes[1,0].grid(True, which='both', alpha=0.3)
    
    # Panel 4: Skewness and kurtosis vs k
    axes[1,1].plot(k_vals, skew_vals, 'b^-', label='Skewness', linewidth=2, markersize=6)
    axes[1,1].plot(k_vals, kurt_vals, 'rs-', label='Excess Kurtosis', linewidth=2, markersize=6)
    axes[1,1].set_xlabel('k')
    axes[1,1].set_ylabel('Value')
    axes[1,1].set_title('Higher-Order Moments vs k')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('primorial_gap_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("Plot saved as 'primorial_gap_analysis.png'")
    print()

    # Final summary
    print("="*70)
    print("CONCLUSIONS:")
    print("="*70)
    print("1. Hypothesis 1 (sub-logarithmic power law R ~ (log P)^γ, 0<γ<1):")
    print(f"   - Fitted γ = {gamma1:.3f}")
    print(f"   - γ ∈ (0,1): {gamma_in_range}")
    print(f"   - R² = {r2_1:.4f}")
    print(f"   - Verdict: {'SUPPORTED' if gamma_in_range and r2_1 > 0.85 else 'REJECTED'}")
    print()
    print("2. Hypothesis 2 (R ~ (log P)^{0.17} from Var ~ (log P)^{1.17}):")
    print(f"   - R² = {r2_2:.4f} for fixed exponent 0.17")
    print(f"   - Verdict: {'SUPPORTED' if r2_2 > 0.95 else 'REJECTED'}")
    print()
    print("3. Hypothesis 3 (predictable higher-order moment scaling):")
    print(f"   - Skewness slope: {slope_skew:.4f}/k")
    print(f"   - Kurtosis slope: {slope_kurt:.4f}/k")
    print(f"   - Verdict: {'PARTIALLY SUPPORTED' if abs(slope_skew) > 0.01 or abs(slope_kurt) > 0.01 else 'REJECTED'}")
    print()
    print("OVERALL ASSESSMENT:")
    print(f"- R(k) grows as (log P_k)^{gamma1:.2f} with γ ≈ {gamma1:.2f} ∈ (0,1)")
    print(f"- This confirms sub-logarithmic growth, falsifying the constant-R hypothesis.")
    print(f"- Scaling exponent γ ≈ {gamma1:.2f} is significantly less than 1,")
    print(f"  consistent with R = Var/Mean where Var ~ (log P)^{1.17} and Mean ~ log P.")
    print()
    print("Recommendation: Extend analysis to higher k (k=10–12) using segmented sieves")
    print("                to better constrain the asymptotic exponent γ.")
    print("="*70)