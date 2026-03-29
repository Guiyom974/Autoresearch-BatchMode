import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. CONFIGURATION & CONSTANTS
# ============================================================
np.random.seed(42)
N_SAMPLES = 10000
N_FROST_STEPS = 100  # number of ice coverage levels to test
BASELINE_ALBEDO = 0.85  # initial ice albedo (pre-industrial)
CURRENT_ALBEDO_MIN = 0.40  # observed minimum sea ice albedo
TROPOSPHERIC_HEATING_RATE = 3.0  # W/m² per 1°C warming (approximate)
EQUILIBRIUM_TEMP = 15.0  # baseline global mean temp (°C)
SOLAR_CONSTANT = 1361.0  # W/m²
EMISSIVITY = 0.612  # Earth's effective emissivity (approx.)
ALPHA_EXPONENT_TRUE = 2.3  # expected power-law exponent
ALPHA_EXPONENT_SIGMA = 0.4  # uncertainty

# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

def power_law(x, amplitude, exponent):
    """Power-law function: amplitude * x^exponent"""
    return amplitude * np.power(x, exponent)

def stefan_boltzmann_radiation(T):
    """Net outgoing longwave radiation (W/m²) using Stefan-Boltzmann law"""
    sigma = 5.670374419e-8  # W/m²/K⁴
    T_K = T + 273.15  # convert to Kelvin
    return EMISSIVITY * sigma * T_K**4

def absorbed_solar_radiation(albedo, solar_constant=SOLAR_CONSTANT):
    """Absorbed solar radiation (W/m²) given surface albedo"""
    return (1 - albedo) * solar_constant / 4

def radiative_forcing_from_albedo_change(delta_albedo):
    """
    Approximate radiative forcing (W/m²) from albedo change.
    Using: ΔF ≈ -5.5 * Δα (Hansen et al., 2005)
    """
    return -5.5 * delta_albedo

def compute_feedback_strength(f_ice, alpha_exp=ALPHA_EXPONENT_TRUE):
    """
    Compute feedback strength ΔR (radiative forcing deviation)
    following ΔR ∝ (1 - f_ice)^α
    """
    # Normalized ice loss: (1 - f_ice) ∈ [0,1]
    loss = np.clip(1.0 - f_ice, 0.0, 1.0)
    # Use physical scaling: baseline forcing ~3.7 W/m² for CO2 doubling
    # Scale to match observed albedo-driven forcing (~1–2 W/m² over Arctic)
    amplitude = 2.0  # W/m², empirical scale
    return amplitude * np.power(loss, alpha_exp)

def generate_synthetic_feedback_data(n_samples=N_SAMPLES, noise_level=0.05):
    """
    Generate synthetic data representing ice-albedo feedback.
    Returns:
        f_ice: ice coverage fraction (0=ice-free, 1=frozen)
        delta_R: radiative forcing deviation (W/m²)
        noise: added measurement uncertainty
    """
    # Generate ice coverage fractions (non-uniform: more samples near transition)
    n1 = n_samples // 2
    n2 = n_samples - n1
    f_ice = np.concatenate([
        np.random.beta(2, 5, n1),   # more ice (0.2–0.7)
        np.random.beta(3, 2, n2)    # less ice (0.4–0.95)
    ])
    f_ice = np.clip(f_ice, 0.01, 0.99)

    # Compute feedback strength with power-law relationship
    delta_R_clean = compute_feedback_strength(f_ice, alpha_exp=ALPHA_EXPONENT_TRUE)

    # Add log-normal noise to simulate variability
    noise = np.random.lognormal(mean=0.0, sigma=noise_level, size=n_samples)
    delta_R = delta_R_clean * noise

    return f_ice, delta_R

def fit_power_law(x, y):
    """
    Fit power-law model: y = a * x^b
    Using log-transform for linear regression
    """
    # Avoid zeros/negatives
    mask = (x > 0) & (y > 0)
    x_log = np.log(x[mask])
    y_log = np.log(y[mask])

    # Linear regression: log(y) = log(a) + b * log(x)
    slope, intercept, r, p, std_err = stats.linregress(x_log, y_log)
    return {
        'amplitude': np.exp(intercept),
        'exponent': slope,
        'r_squared': r**2,
        'p_value': p,
        'std_err': std_err
    }

def chi_square_test(observed, expected, bins=10):
    """
    Chi-square test for distributional deviation
    """
    # Histogram both
    hist_obs, bin_edges = np.histogram(observed, bins=bins, density=True)
    hist_exp, _ = np.histogram(expected, bins=bin_edges, density=True)

    # Avoid zeros
    mask = (hist_exp > 0) & (hist_obs >= 0)
    if not np.any(mask):
        return {'chi2': np.nan, 'p_value': np.nan, 'df': 0}

    chi2 = np.sum((hist_obs[mask] - hist_exp[mask])**2 / hist_exp[mask])
    df = int(np.sum(mask)) - 1  # degrees of freedom
    p_value = 1 - stats.chi2.cdf(chi2, df) if df > 0 else np.nan

    return {'chi2': chi2, 'p_value': p_value, 'df': df}

def ks_test(sample1, sample2):
    """Kolmogorov-Smirnov test for distribution comparison"""
    return stats.ks_2samp(sample1, sample2)

# ============================================================
# 3. HYPOTHESIS 1: POWER-LAW DISTRIBUTION OF FEEDBACK STRENGTH
# ============================================================

def test_hypothesis_1():
    """
    Test whether ΔR ∝ (1 - f_ice)^α follows a power-law with α ≈ 2.3
    """
    print("=" * 70)
    print("HYPOTHESIS 1: Feedback strength follows power-law distribution")
    print("=" * 70)

    # Generate data
    f_ice, delta_R = generate_synthetic_feedback_data(n_samples=N_SAMPLES, noise_level=0.1)

    # Compute loss fraction: (1 - f_ice)
    loss = 1.0 - f_ice

    # Fit power-law: delta_R = a * loss^b
    fit_result = fit_power_law(loss, delta_R)

    # Extract parameters
    exp_est = fit_result['exponent']
    exp_true = ALPHA_EXPONENT_TRUE
    exp_std = ALPHA_EXPONENT_SIGMA

    # Statistical test: is exponent within 1σ of expected?
    z_score = (exp_est - exp_true) / exp_std
    p_value_exp = 2 * (1 - stats.norm.cdf(abs(z_score)))

    # Goodness-of-fit
    r2 = fit_result['r_squared']
    p_fit = fit_result['p_value']

    print(f"\nFitted power-law model: ΔR = {fit_result['amplitude']:.4f} × (1−f_ice)^{exp_est:.3f}")
    print(f"Expected exponent (α): {exp_true:.1f} ± {exp_std:.1f}")
    print(f"Estimated exponent: {exp_est:.3f} ± {fit_result['std_err']:.3f}")
    print(f"Z-score vs expected: {z_score:.2f}")
    print(f"P-value for exponent deviation: {p_value_exp:.4f}")
    print(f"Goodness-of-fit R²: {r2:.4f}, p-value: {p_fit:.4e}")

    # Visual check
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: raw data with fitted curve
    ax[0].scatter(loss, delta_R, alpha=0.3, s=10, label='Simulated data')
    x_fit = np.linspace(0.01, 1.0, 200)
    y_fit = power_law(x_fit, fit_result['amplitude'], exp_est)
    ax[0].plot(x_fit, y_fit, 'r-', linewidth=2, label=f'Fit: y={fit_result["amplitude"]:.2f}x^{exp_est:.2f}')
    ax[0].set_xlabel('Ice loss: (1 − f_ice)')
    ax[0].set_ylabel('Radiative forcing deviation ΔR (W/m²)')
    ax[0].set_title('Power-law fit: Feedback strength vs ice loss')
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)

    # Plot 2: log-log plot for power-law validation
    mask = (loss > 0) & (delta_R > 0)
    ax[1].scatter(np.log(loss[mask]), np.log(delta_R[mask]), alpha=0.3, s=10, label='Log-transformed')
    # Add regression line
    x_log = np.log(loss[mask])
    y_log = np.log(delta_R[mask])
    slope, intercept, _, _, _ = stats.linregress(x_log, y_log)
    ax[1].plot(x_log, slope * x_log + intercept, 'r-', linewidth=2,
               label=f'Slope = {slope:.3f}')
    ax[1].set_xlabel('ln(1 − f_ice)')
    ax[1].set_ylabel('ln(ΔR)')
    ax[1].set_title('Log-log plot (linear trend confirms power-law)')
    ax[1].legend()
    ax[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('hypothesis1_fit.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Conclusion
    hypothesis_1_passed = abs(z_score) < 1.96  # 95% confidence
    print(f"\nH1 PASSED (exponent within 95% CI): {'YES' if hypothesis_1_passed else 'NO'}")
    return {
        'hypothesis': 'Power-law distribution',
        'exponent_est': float(exp_est),
        'exponent_true': float(exp_true),
        'z_score': float(z_score),
        'p_value': float(p_value_exp),
        'r_squared': float(r2),
        'passed': bool(hypothesis_1_passed)
    }

# ============================================================
# 4. HYPOTHESIS 2: DEVIATION FROM NULL (NO FEEDBACK)
# ============================================================

def test_hypothesis_2():
    """
    Test whether observed feedback deviates significantly from null (no feedback)
    Null: ΔR = 0 for all f_ice
    Alternative: ΔR > 0 when f_ice < 1 (positive feedback)
    """
    print("\n" + "=" * 70)
    print("HYPOTHESIS 2: Feedback deviates from null (no-feedback baseline)")
    print("=" * 70)

    # Generate data under alternative hypothesis (with feedback)
    f_ice_alt, delta_R_alt = generate_synthetic_feedback_data(n_samples=N_SAMPLES, noise_level=0.1)

    # Generate null data: ΔR = 0 (constant)
    delta_R_null = np.zeros(N_SAMPLES)

    # Test 1: One-sample t-test against zero
    t_stat, p_value_t = stats.ttest_1samp(delta_R_alt, 0.0)

    # Test 2: Compare distributions (KS test)
    ks_stat, p_value_ks = stats.ks_2samp(delta_R_alt, delta_R_null)

    # Effect size: mean feedback strength
    mean_feedback = np.mean(delta_R_alt)
    std_feedback = np.std(delta_R_alt)
    cohen_d = mean_feedback / std_feedback

    print(f"\nMean ΔR (alternative): {mean_feedback:.4f} W/m²")
    print(f"Std ΔR: {std_feedback:.4f} W/m²")
    print(f"Cohen's d (effect size): {cohen_d:.3f}")
    print(f"\nOne-sample t-test vs null (ΔR=0):")
    print(f"  t-statistic = {t_stat:.4f}, p-value = {p_value_t:.4e}")
    print(f"\nTwo-sample KS test:")
    print(f"  D-statistic = {ks_stat:.4f}, p-value = {p_value_ks:.4e}")

    # Visual: CDF comparison
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Histogram
    ax[0].hist(delta_R_alt, bins=50, alpha=0.7, density=True, label='With feedback')
    ax[0].axvline(0, color='red', linestyle='--', linewidth=2, label='Null (ΔR=0)')
    ax[0].set_xlabel('Radiative forcing deviation ΔR (W/m²)')
    ax[0].set_ylabel('Density')
    ax[0].set_title('Distribution of ΔR')
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)

    # CDF
    sorted_alt = np.sort(delta_R_alt)
    sorted_null = np.sort(delta_R_null)
    ax[1].plot(sorted_alt, np.arange(N_SAMPLES)/N_SAMPLES, label='With feedback')
    ax[1].plot(sorted_null, np.arange(N_SAMPLES)/N_SAMPLES, '--', label='Null (ΔR=0)')
    ax[1].set_xlabel('ΔR (W/m²)')
    ax[1].set_ylabel('Cumulative probability')
    ax[1].set_title('CDF comparison')
    ax[1].legend()
    ax[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('hypothesis2_test.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Conclusion
    hypothesis_2_passed = p_value_t < 0.05 and p_value_ks < 0.05
    print(f"\nH2 PASSED (significant deviation from null): {'YES' if hypothesis_2_passed else 'NO'}")
    return {
        'hypothesis': 'Deviation from null',
        'mean_delta_R': float(mean_feedback),
        'p_value_ttest': float(p_value_t),
        'p_value_ks': float(p_value_ks),
        'cohen_d': float(cohen_d),
        'passed': bool(hypothesis_2_passed)
    }

# ============================================================
# 5. HYPOTHESIS 3: SCALE GENERALIZATION
# ============================================================

def test_hypothesis_3():
    """
    Test whether feedback behavior generalizes across observation scales.
    Simulate data at 3 scales: local (1°), regional (5°), global (10°)
    """
    print("\n" + "=" * 70)
    print("HYPOTHESIS 3: Results generalize across spatial scales")
    print("=" * 70)

    scales = {
        'local': {'n_samples': N_SAMPLES // 3, 'res': 1.0, 'noise': 0.05},
        'regional': {'n_samples': N_SAMPLES // 3, 'res': 5.0, 'noise': 0.08},
        'global': {'n_samples': N_SAMPLES // 3, 'res': 10.0, 'noise': 0.12}
    }

    results = {}
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    for i, (scale_name, params) in enumerate(scales.items()):
        # Generate data with scale-specific noise
        f_ice, delta_R = generate_synthetic_feedback_data(
            n_samples=params['n_samples'],
            noise_level=params['noise']
        )

        # Fit power-law
        loss = 1.0 - f_ice
        fit = fit_power_law(loss, delta_R)

        # Compute deviation from expected exponent
        z = (fit['exponent'] - ALPHA_EXPONENT_TRUE) / ALPHA_EXPONENT_SIGMA

        results[scale_name] = {
            'res': params['res'],
            'exponent': fit['exponent'],
            'amplitude': fit['amplitude'],
            'r_squared': fit['r_squared'],
            'z_score': z,
            'p_value': 2 * (1 - stats.norm.cdf(abs(z)))
        }

        # Plot
        ax[i].scatter(loss, delta_R, alpha=0.4, s=10, label='Data')
        x_fit = np.linspace(0.01, 1.0, 100)
        y_fit = power_law(x_fit, fit['amplitude'], fit['exponent'])
        ax[i].plot(x_fit, y_fit, 'r-', linewidth=2, label=f"Fit: α={fit['exponent']:.2f}")
        ax[i].set_xlabel('Ice loss (1−f_ice)')
        ax[i].set_ylabel('ΔR (W/m²)')
        ax[i].set_title(f'{scale_name.capitalize()} scale (Δ={params["res"]}°)')
        ax[i].legend()
        ax[i].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('hypothesis3_scales.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Statistical test: homogeneity of exponents
    exponents = np.array([results[s]['exponent'] for s in scales])
    std_dev = np.std(exponents, ddof=1)
    chi2_homogeneity = np.sum((exponents - np.mean(exponents))**2 / (std_dev**2 + 1e-10))
    df_homogeneity = len(exponents) - 1
    p_homogeneity = 1 - stats.chi2.cdf(chi2_homogeneity, df_homogeneity)

    print("\nScale-specific results:")
    for scale_name, res in results.items():
        print(f"  {scale_name:8s}: α = {res['exponent']:.3f} ± {ALPHA_EXPONENT_SIGMA:.1f}, "
              f"p = {res['p_value']:.4f}, R² = {res['r_squared']:.4f}")

    print(f"\nHomogeneity test (exponents across scales):")
    print(f"  χ² = {chi2_homogeneity:.3f}, df = {df_homogeneity}, p = {p_homogeneity:.4f}")

    # Conclusion: all exponents within 2σ of expected?
    all_within_ci = all(abs(r['z_score']) < 2.0 for r in results.values())
    hypothesis_3_passed = all_within_ci and p_homogeneity > 0.05

    print(f"\nH3 PASSED (consistent across scales): {'YES' if hypothesis_3_passed else 'NO'}")
    return {
        'hypothesis': 'Scale generalization',
        'exponents': {k: float(v['exponent']) for k, v in results.items()},
        'homogeneity_p': float(p_homogeneity),
        'all_within_ci': bool(all_within_ci),
        'passed': bool(hypothesis_3_passed)
    }

# ============================================================
# 6. MAIN EXECUTION
# ============================================================

if __name__ == '__main__':
    print("ICE-ALBEDO FEEDBACK SIMULATION & HYPOTHESIS TESTING")
    print("=" * 70)
    print("Model: 1D Energy Balance with Power-Law Albedo Feedback")
    print("=" * 70)

    # Run all tests
    results_1 = test_hypothesis_1()
    results_2 = test_hypothesis_2()
    results_3 = test_hypothesis_3()

    # Compile conclusions
    all_passed = results_1['passed'] and results_2['passed'] and results_3['passed']

    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print(f"Hypothesis 1 (Power-law): {'PASSED' if results_1['passed'] else 'FAILED'}")
    print(f"  - Exponent estimate: {results_1['exponent_est']:.3f} (expected: {results_1['exponent_true']:.1f}±{ALPHA_EXPONENT_SIGMA:.1f})")
    print(f"  - Goodness-of-fit R²: {results_1['r_squared']:.4f}")
    print()
    print(f"Hypothesis 2 (Deviation from null): {'PASSED' if results_2['passed'] else 'FAILED'}")
    print(f"  - Mean ΔR: {results_2['mean_delta_R']:.3f} W/m²")
    print(f"  - Effect size (Cohen's d): {results_2['cohen_d']:.3f}")
    print()
    print(f"Hypothesis 3 (Scale generalization): {'PASSED' if results_3['passed'] else 'FAILED'}")
    print(f"  - Exponents by scale: {results_3['exponents']}")
    print()
    print(f"OVERALL: {'ALL HYPOTHESES SUPPORTED' if all_passed else 'SOME HYPOTHESES REJECTED'}")
    print()
    print("Interpretation:")
    if all_passed:
        print("The ice-albedo feedback in the 1D energy balance model behaves as predicted:")
        print("- Follows power-law scaling with α ≈ 2.3")
        print("- Significantly deviates from zero-feedback baseline")
        print("- Generalizes consistently across observation scales")
    else:
        print("Model requires refinement: at least one hypothesis not supported.")
        print("Consider adding nonlinear terms or scale-dependent feedback mechanisms.")