import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import ttest_ind

# Constants
L = 1361.0  # Solar constant (W/m^2)
a0 = 0.3    # Global mean albedo (reference)
a_ice = 0.6 # Albedo of ice
a_ocean = 0.06 # Albedo of open ocean
sigma = 5.670374419e-8  # Stefan-Boltzmann constant (W/m^2/K^4)
C = 2.08e7  # Effective heat capacity (J/m^2/K)
T0 = 275.0  # Reference equilibrium temperature (K) adjusted for balance
dT_ref = 1.0  # Reference temperature change for scaling

def power_law(x, alpha, k):
    """Power-law function: y = k * x^alpha"""
    return k * np.power(x, alpha)

def compute_albedo(T, T_melt=273.15, T_min=250.0, T_max=290.0):
    """
    Compute surface albedo as a function of temperature.
    Linear transition between fully ice-covered (cold) and ice-free (warm).
    """
    # Fraction of ice cover: 1 at T <= T_min, 0 at T >= T_max
    frac_ice = np.clip((T_max - T) / (T_max - T_min), 0.0, 1.0)
    return a_ice * frac_ice + a_ocean * (1.0 - frac_ice)

def compute_cloud_fraction(T, SLP=1013.25, base_cloud=0.4, max_cloud=0.9):
    """
    Simplified cloud fraction parameterization.
    Cloud fraction increases with temperature due to increased evaporation.
    """
    # Use a smooth logistic function
    cloud_frac = base_cloud + (max_cloud - base_cloud) / (1.0 + np.exp(-0.03 * (T - 275.0)))
    return np.clip(cloud_frac, 0.0, 1.0)

def cloud_radiative_effect(cloud_frac, T):
    """
    Compute net cloud radiative effect (NCRE).
    Clouds cool via albedo (shortwave) and warm via greenhouse (longwave).
    For simplicity, assume net cooling effect that weakens as temperature rises.
    """
    # Net cloud forcing: more clouds → more reflection (cooling)
    # But warming reduces the net cooling effect (positive feedback on warming)
    # Simplified: net cooling = A * cloud_frac * (1 - B * (T - T0))
    A = 25.0  # Cloud albedo forcing (W/m^2)
    B = 0.02  # Temperature dependence
    net_cooling = A * cloud_frac * (1.0 - B * (T - T0))
    return np.clip(net_cooling, -50.0, 20.0)

def solve_energy_balance(T, dT, albedo_func, cloud_func, include_clouds=True, forcing=0.0):
    """
    Solve the energy balance equation for a given temperature perturbation.
    Returns the net radiative imbalance (W/m^2).
    Positive = warming required to restore balance.
    """
    T_full = T0 + dT
    albedo = albedo_func(T_full)
    
    # Solar absorption
    SW_in = (L / 4.0) * (1.0 - albedo)
    
    # Outgoing longwave radiation (Stefan-Boltzmann)
    LW_out = sigma * T_full**4
    
    # Cloud effect
    if include_clouds:
        cloud_frac = cloud_func(T_full)
        cloud_forcing = cloud_radiative_effect(cloud_frac, T_full)
        SW_in += cloud_forcing  # Add net cloud effect to solar absorption
    
    # Net radiation
    net_radiation = SW_in - LW_out + forcing
    
    return net_radiation

def find_equilibrium_dT(albedo_func, cloud_func, include_clouds=True, forcing=0.0):
    """
    Find the equilibrium temperature change given a forcing.
    Uses a simple root-finding approach.
    """
    dT = 0.0
    for _ in range(50):
        imbalance = solve_energy_balance(T0, dT, albedo_func, cloud_func, include_clouds, forcing)
        # Use a small perturbation for derivative estimate
        d_imbalance = solve_energy_balance(T0, dT + 0.01, albedo_func, cloud_func, include_clouds, forcing) - imbalance
        if abs(d_imbalance) < 1e-12:
            break
        dT -= imbalance / (d_imbalance / 0.01)
        dT = np.clip(dT, -50.0, 50.0)
    return dT

def run_coupled_model(include_clouds=True, dT_range=np.arange(0.5, 12.1, 0.5)):
    """
    Run the model over a range of external forcings mapped from dT_range.
    Returns dT and corresponding ice extent (or albedo change).
    """
    dT_vals = []
    ice_extent_vals = []
    
    # Map the target dT to an approximate forcing
    for F in np.linspace(0, 40, len(dT_range)):
        eq_dT = find_equilibrium_dT(compute_albedo, compute_cloud_fraction, include_clouds, forcing=F)
        if not np.isnan(eq_dT):
            dT_vals.append(eq_dT)
            # Compute ice fraction at equilibrium
            albedo_eq = compute_albedo(T0 + eq_dT)
            ice_frac = (a_ice - albedo_eq) / (a_ice - a_ocean)
            ice_extent_vals.append(np.clip(ice_frac, 0.0, 1.0))
    
    return np.array(dT_vals), np.array(ice_extent_vals)

def fit_power_law(x, y):
    """
    Fit y = k * x^alpha using log-log linear regression.
    Returns alpha and k.
    """
    # Remove zeros/negatives
    mask = (x > 0) & (y > 0)
    x_fit = x[mask]
    y_fit = y[mask]
    
    if len(np.unique(x_fit)) < 3:
        return np.nan, np.nan
    
    log_x = np.log(x_fit)
    log_y = np.log(y_fit)
    
    # Linear regression
    n = len(log_x)
    sum_x = np.sum(log_x)
    sum_y = np.sum(log_y)
    sum_xy = np.sum(log_x * log_y)
    sum_x2 = np.sum(log_x * log_x)
    
    denom = n * sum_x2 - sum_x**2
    if abs(denom) < 1e-12:
        return np.nan, np.nan
    
    alpha = (n * sum_xy - sum_x * sum_y) / denom
    k = np.exp((sum_y - alpha * sum_x) / n)
    
    return alpha, k

def run_hypothesis_tests():
    """
    Run all hypothesis tests and return results.
    """
    # Reference: isolated albedo feedback (no clouds)
    print("\n=== RUNNING HYPOTHESIS TESTS ===\n")
    
    # Generate data for isolated albedo feedback
    dT_iso, ice_iso = run_coupled_model(include_clouds=False)
    
    # Fit power law to isolated case
    alpha_iso, k_iso = fit_power_law(ice_iso, dT_iso)
    print(f"Isolated albedo feedback (no clouds):")
    print(f"  Ice extent vs. dT power-law fit: α = {alpha_iso:.3f}, k = {k_iso:.3f}")
    
    # Generate data for coupled case
    dT_coupled, ice_coupled = run_coupled_model(include_clouds=True)
    
    # Fit power law to coupled case
    alpha_coupled, k_coupled = fit_power_law(ice_coupled, dT_coupled)
    print(f"Coupled albedo + cloud feedback:")
    print(f"  Ice extent vs. dT power-law fit: α = {alpha_coupled:.3f}, k = {k_coupled:.3f}")
    
    # For hypothesis testing, we need to compare exponents statistically
    # We'll simulate uncertainty by perturbing the data slightly
    np.random.seed(42)
    n_sim = 1000
    alpha_iso_samples = []
    alpha_coupled_samples = []
    
    # Add small noise to simulate measurement uncertainty
    noise_std = 0.05
    
    for _ in range(n_sim):
        # Perturb dT values
        dT_iso_noise = dT_iso + np.random.normal(0, noise_std, len(dT_iso))
        dT_coupled_noise = dT_coupled + np.random.normal(0, noise_std, len(dT_coupled))
        
        # Re-fit
        alpha_iso_s, _ = fit_power_law(ice_iso, dT_iso_noise)
        alpha_coupled_s, _ = fit_power_law(ice_coupled, dT_coupled_noise)
        
        if not np.isnan(alpha_iso_s):
            alpha_iso_samples.append(alpha_iso_s)
        if not np.isnan(alpha_coupled_s):
            alpha_coupled_samples.append(alpha_coupled_s)
    
    alpha_iso_samples = np.array(alpha_iso_samples)
    alpha_coupled_samples = np.array(alpha_coupled_samples)
    
    # Hypothesis 1: Cloud feedback dampens exponent (α_coupled < 2.3, in range 1.6–2.0)
    print("\n--- HYPOTHESIS 1: Cloud Feedback Dampens Power-Law Exponent ---")
    print("Null hypothesis H0: α_coupled ≥ 2.3")
    print("Alternative H1: α_coupled < 2.3")
    
    if len(alpha_coupled_samples) > 1:
        # Compute sample mean and std
        alpha_coupled_mean = np.mean(alpha_coupled_samples)
        alpha_coupled_std = np.std(alpha_coupled_samples, ddof=1)
        alpha_coupled_se = alpha_coupled_std / np.sqrt(len(alpha_coupled_samples))
        
        # One-sample t-test against 2.3
        t_stat_1 = (alpha_coupled_mean - 2.3) / alpha_coupled_se
        from scipy import stats as scipy_stats
        p_val_1 = scipy_stats.t.cdf(t_stat_1, df=len(alpha_coupled_samples)-1)
        
        print(f"  α_coupled mean = {alpha_coupled_mean:.3f} ± {alpha_coupled_std:.3f}")
        print(f"  t-statistic vs. 2.30: {t_stat_1:.3f}")
        print(f"  One-tailed p-value: {p_val_1:.4f}")
        
        in_range = np.mean((alpha_coupled_samples >= 1.6) & (alpha_coupled_samples <= 2.0))
        print(f"  Probability α_coupled ∈ [1.6, 2.0]: {in_range:.3f}")
    else:
        p_val_1 = 1.0
        in_range = 0.0
    
    # Hypothesis 2: Cloud feedback reduces warming for same ice loss
    print("\n--- HYPOTHESIS 2: Cloud Feedback Reduces Warming for Fixed Ice Loss ---")
    ice_ref = 0.5
    dT_iso_ref = 0.0
    dT_coupled_ref = 0.0
    p_val_2 = 1.0
    if len(dT_iso) > 1 and len(dT_coupled) > 1:
        dT_iso_ref = np.interp(ice_ref, ice_iso[::-1], dT_iso[::-1])
        dT_coupled_ref = np.interp(ice_ref, ice_coupled[::-1], dT_coupled[::-1])
        
        print(f"  At fixed ice extent = {ice_ref:.2f}:")
        print(f"    dT (no clouds) = {dT_iso_ref:.2f} K")
        print(f"    dT (with clouds) = {dT_coupled_ref:.2f} K")
        print(f"    ΔdT = {dT_coupled_ref - dT_iso_ref:.2f} K")
        
        mask = (ice_iso > 0.1) & (ice_iso < 0.9)
        if np.sum(mask) > 1:
            t_stat_2, p_val_2 = ttest_ind(dT_iso[mask], dT_coupled[mask], equal_var=False)
            print(f"  Two-sample t-test: t = {t_stat_2:.3f}, p = {p_val_2:.4f}")
    
    # Hypothesis 3: Cloud feedback changes the sensitivity (d(dT)/d(ice))
    print("\n--- HYPOTHESIS 3: Cloud Feedback Alters Sensitivity (d(dT)/d(ice)) ---")
    sens_iso = 0.0
    sens_coupled = 0.0
    p_val_3 = 1.0
    if len(np.unique(ice_iso)) > 2 and len(np.unique(ice_coupled)) > 2:
        dt_iso_dice = np.gradient(dT_iso, ice_iso)
        dt_coupled_dice = np.gradient(dT_coupled, ice_coupled)
        
        sens_iso = np.mean(np.abs(dt_iso_dice))
        sens_coupled = np.mean(np.abs(dt_coupled_dice))
        
        print(f"  Average |dT/d(ice)| (no clouds): {sens_iso:.3f} K per unit ice")
        print(f"  Average |dT/d(ice)| (with clouds): {sens_coupled:.3f} K per unit ice")
        
        t_stat_3, p_val_3 = ttest_ind(dt_iso_dice, dt_coupled_dice, equal_var=False)
        print(f"  Two-sample t-test: t = {t_stat_3:.3f}, p = {p_val_3:.4f}")
    
    # Hypothesis 4: Cloud feedback introduces nonlinearity (breaks power law)
    print("\n--- HYPOTHESIS 4: Cloud Feedback Introduces Nonlinearity ---")
    def r_squared(x, y, alpha, k):
        if np.isnan(alpha) or np.isnan(k): return np.nan
        y_pred = k * x**alpha
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        return 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    
    r2_iso = r_squared(ice_iso, dT_iso, alpha_iso, k_iso)
    r2_coupled = r_squared(ice_coupled, dT_coupled, alpha_coupled, k_coupled)
    
    print(f"  R² (no clouds): {r2_iso:.4f}")
    print(f"  R² (with clouds): {r2_coupled:.4f}")
    
    def residual_sum_squares(x, y, order):
        mask = ~np.isnan(x) & ~np.isnan(y)
        x_clean, y_clean = x[mask], y[mask]
        if len(np.unique(x_clean)) <= order + 1:
            return np.nan
        coeffs = np.polyfit(x_clean, y_clean, order)
        y_pred = np.polyval(coeffs, x_clean)
        return np.sum((y_clean - y_pred)**2)
    
    ss1_iso = residual_sum_squares(ice_iso, dT_iso, 1)
    ss2_iso = residual_sum_squares(ice_iso, dT_iso, 2)
    ss1_coupled = residual_sum_squares(ice_coupled, dT_coupled, 1)
    ss2_coupled = residual_sum_squares(ice_coupled, dT_coupled, 2)
    
    n = len(ice_iso)
    p1, p2 = 2, 3
    p_coupled = 1.0
    if not np.isnan(ss1_iso) and not np.isnan(ss2_iso) and ss2_iso > 0:
        f_iso = ((ss1_iso - ss2_iso) / (p2 - p1)) / (ss2_iso / (n - p2))
        p_iso = 1 - scipy_stats.f.cdf(f_iso, p2 - p1, n - p2)
        print(f"    No clouds: F = {f_iso:.2f}, p = {p_iso:.4f}")
    
    if not np.isnan(ss1_coupled) and not np.isnan(ss2_coupled) and ss2_coupled > 0:
        f_coupled = ((ss1_coupled - ss2_coupled) / (p2 - p1)) / (ss2_coupled / (n - p2))
        p_coupled = 1 - scipy_stats.f.cdf(f_coupled, p2 - p1, n - p2)
        print(f"    With clouds: F = {f_coupled:.2f}, p = {p_coupled:.4f}")
    
    # Hypothesis 5: Cloud feedback creates threshold behavior
    print("\n--- HYPOTHESIS 5: Cloud Feedback Introduces Threshold Behavior ---")
    sign_changes_iso = 0
    sign_changes_coupled = 0
    monotonic_coupled = True
    if len(np.unique(ice_iso)) > 5:
        d2t_iso = np.gradient(np.gradient(dT_iso, ice_iso), ice_iso)
        d2t_coupled = np.gradient(np.gradient(dT_coupled, ice_coupled), ice_coupled)
        
        sign_changes_iso = np.sum(np.diff(np.sign(d2t_iso)) != 0)
        sign_changes_coupled = np.sum(np.diff(np.sign(d2t_coupled)) != 0)
        
        print(f"  Number of inflection points (no clouds): {sign_changes_iso}")
        print(f"  Number of inflection points (with clouds): {sign_changes_coupled}")
        
        monotonic_iso = np.all(np.diff(dT_iso) >= 0) or np.all(np.diff(dT_iso) <= 0)
        monotonic_coupled = np.all(np.diff(dT_coupled) >= 0) or np.all(np.diff(dT_coupled) <= 0)
        
        print(f"  Monotonic? (no clouds): {monotonic_iso}")
        print(f"  Monotonic? (with clouds): {monotonic_coupled}")
    
    # Generate plots
    print("\n--- GENERATING PLOTS ---")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(ice_iso, dT_iso, 'b-o', label='No cloud feedback (α = %.3f)' % (alpha_iso if not np.isnan(alpha_iso) else 0))
    ax.plot(ice_coupled, dT_coupled, 'r-s', label='With cloud feedback (α = %.3f)' % (alpha_coupled if not np.isnan(alpha_coupled) else 0))
    ax.set_xlabel('Ice Extent (fraction)')
    ax.set_ylabel('Temperature Change (K)')
    ax.set_title('Ice-Albedo Feedback with and without Cloud Coupling')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig_dT_vs_ice.png', dpi=150)
    plt.close()
    
    fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    if not np.isnan(alpha_iso) and not np.isnan(k_iso):
        y_pred_iso = k_iso * ice_iso**alpha_iso
        res_iso = dT_iso - y_pred_iso
        ax1.plot(ice_iso, res_iso, 'bo')
    ax1.axhline(0, color='k', linestyle='--')
    ax1.set_xlabel('Ice Extent')
    ax1.set_ylabel('Residual (dT - fit)')
    ax1.set_title('Residuals: No Cloud Feedback')
    ax1.grid(True, alpha=0.3)
    
    if not np.isnan(alpha_coupled) and not np.isnan(k_coupled):
        y_pred_coupled = k_coupled * ice_coupled**alpha_coupled
        res_coupled = dT_coupled - y_pred_coupled
        ax2.plot(ice_coupled, res_coupled, 'rs')
    ax2.axhline(0, color='k', linestyle='--')
    ax2.set_xlabel('Ice Extent')
    ax2.set_ylabel('Residual (dT - fit)')
    ax2.set_title('Residuals: With Cloud Feedback')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fig_residuals.png', dpi=150)
    plt.close()
    
    T_range = np.linspace(250, 290, 100)
    cloud_range = compute_cloud_fraction(T_range)
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    ax3.plot(T_range, cloud_range, 'g-', linewidth=2)
    ax3.set_xlabel('Temperature (K)')
    ax3.set_ylabel('Cloud Fraction')
    ax3.set_title('Cloud Fraction vs Temperature')
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig_cloud_temp.png', dpi=150)
    plt.close()
    
    print("  Plots saved: fig_dT_vs_ice.png, fig_residuals.png, fig_cloud_temp.png")
    
    print("\n" + "="*60)
    print("HYPOTHESIS TEST SUMMARY")
    print("="*60)
    
    print("\nH1 (Dampening):")
    print(f"  α_coupled = {alpha_coupled:.3f} vs. α_iso = {alpha_iso:.3f}")
    print(f"  Cloud feedback significantly reduces exponent? {'YES' if p_val_1 < 0.05 else 'NO'}")
    print(f"  Within predicted range [1.6, 2.0]? {'YES' if in_range > 0.5 else 'NO'}")
    
    print("\nH2 (Reduced warming):")
    print(f"  At fixed ice = 0.5, ΔdT = {dT_coupled_ref - dT_iso_ref:.2f} K")
    print(f"  Significant reduction? {'YES' if p_val_2 < 0.05 else 'NO'}")
    
    print("\nH3 (Sensitivity change):")
    print(f"  |dT/d(ice)| increased? {'YES' if sens_coupled > sens_iso else 'NO'}")
    print(f"  Significant? {'YES' if p_val_3 < 0.05 else 'NO'}")
    
    print("\nH4 (Nonlinearity):")
    print(f"  R² improved with clouds? {'YES' if (not np.isnan(r2_coupled) and not np.isnan(r2_iso) and r2_coupled > r2_iso) else 'NO'}")
    print(f"  Quadratic term significant? {'YES' if p_coupled < 0.05 else 'NO'}")
    
    print("\nH5 (Thresholds):")
    print(f"  More inflection points with clouds? {'YES' if sign_changes_coupled > sign_changes_iso else 'NO'}")
    print(f"  Loss of monotonicity? {'YES' if not monotonic_coupled else 'NO'}")
    
    print("\n" + "="*60)
    print("CONCLUSIONS:")
    print("="*60)
    
    conclusions = []
    if p_val_1 < 0.05 and alpha_coupled < 2.3:
        conclusions.append("✓ H1 supported: Cloud feedback significantly reduces the power-law exponent.")
    else:
        conclusions.append("✗ H1 not supported: Cloud feedback does not significantly reduce the exponent.")
    
    if p_val_2 < 0.05 and (dT_coupled_ref - dT_iso_ref) < 0:
        conclusions.append("✓ H2 supported: Cloud feedback reduces warming for a given ice loss.")
    else:
        conclusions.append("✗ H2 not supported: Cloud feedback does not significantly reduce warming.")
    
    if p_val_3 < 0.05:
        conclusions.append("✓ H3 supported: Cloud feedback significantly alters climate sensitivity.")
    else:
        conclusions.append("✗ H3 not supported: Cloud feedback does not significantly alter sensitivity.")
    
    if p_coupled < 0.05:
        conclusions.append("✓ H4 supported: Cloud feedback introduces significant nonlinearity.")
    else:
        conclusions.append("✗ H4 not supported: Power-law fit remains adequate with clouds.")
    
    if sign_changes_coupled > sign_changes_iso:
        conclusions.append("✓ H5 supported: Cloud feedback introduces additional threshold behavior.")
    else:
        conclusions.append("✗ H5 not supported: No evidence of new thresholds from cloud feedback.")
    
    for c in conclusions:
        print(c)
    
    print("\nNote: All tests use simulated data with measurement uncertainty (σ=0.05 K).")
    print("Model assumptions: Linear ice-albedo transition, logistic cloud formation.")
    print("="*60)

run_hypothesis_tests()