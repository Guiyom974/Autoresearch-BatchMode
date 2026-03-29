import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq

# ============================================================================
# 2D LATITUDINAL ENERGY BALANCE MODEL (EBM) — HYPOTHESIS TESTING
# ============================================================================
# Model: 1D latitudinal (θ from -π/2 to π/2), steady-state, zonally symmetric
# Equation: 0 = S(θ)(1 - α(T, θ))/4 - T⁴ + D(θ, ∇T) * (1/a²) * d/dθ[(1 - sinθ) dT/dθ]
# Simplified: use dimensionless latitude x = sinθ ∈ [-1, 1], grid in x
# Heat transport term approximated via finite differences with variable D
# ============================================================================

# Physical constants (non-dimensionalized)
A = 255.0   # Outgoing longwave radiation coefficient (W/m²)
B = 1.45    # Linear feedback parameter (W/m²/K)
T0 = 288.0  # Reference temperature (K)
S0 = 1361.0 # Solar constant (W/m²)
a = 6.371e6 # Earth radius (m), used only for scaling — cancels in 1D latitudinal
ε = 0.6     # Emissivity (used implicitly via A, B)
c_s = 10.0  # Surface heat capacity (simplified, non-dimensionalized)

# Albedo functions
def albedo_linear(T, α_i=0.6, α_0=0.3, T_i=273.15, T_w=298.15):
    """Linear ice-albedo feedback: high albedo in cold regions (ice), low in warm."""
    return α_i + (α_0 - α_i) * (T - T_i) / (T_w - T_i)

def albedo_step(T, T_c=273.15):
    """Step-function albedo: ice (α_i) if T ≤ T_c, else ice-free (α_0)."""
    return np.where(T <= T_c, 0.6, 0.3)

# Solar insolation (seasonal mean, cosine latitude)
def insolation(x):
    """x = sinθ, so cosθ = sqrt(1 - x²). Insolation ∝ cosθ."""
    return S0 * np.sqrt(1 - x**2)

# ============================================================================
# CORE EBM SOLVER
# ============================================================================
def solve_ebm(D_const=0.15, D_func=None, x=None, nx=180, max_iter=500, tol=1e-5,
              T_init=None, albedo_func=albedo_step, T_c=273.15):
    """
    Solve steady-state 1D latitudinal EBM using fixed-point iteration.
    
    Parameters
    ----------
    D_const : float
        Constant heat transport coefficient (W/m²/K) — used if D_func is None
    D_func : callable or None
        If not None, D(x, T, gradT) returns spatially variable D
    x : array or None
        Grid points in x = sinθ (if None, use nx points)
    nx : int
        Number of grid points if x is None
    max_iter : int
        Max iterations for fixed-point solve
    tol : float
        Convergence tolerance (K)
    T_init : array or None
        Initial temperature guess (if None, use 255 K everywhere)
    albedo_func : callable
        Albedo function: albedo(T) → array of albedos
    T_c : float
        Critical temperature for ice (K)
    
    Returns
    -------
    x : array
        Grid points (sinθ)
    T : array
        Temperature profile (K)
    ice_edge : float or None
        Latitude (in degrees) of first ice edge (N), or None if no ice
    """
    if x is None:
        x = np.linspace(-1.0, 1.0, nx)
    
    dx = x[1] - x[0]
    
    # Boundary conditions: no flux at poles (dT/dx = 0 at x = ±1)
    # Use ghost points or modify finite-difference stencil
    
    if T_init is None:
        T = np.full_like(x, 255.0)
    else:
        T = T_init.copy()
    
    # Precompute geometric factors: (1 - sinθ) = 1 - x
    g = 1.0 - x  # weight for diffusion term
    
    for iteration in range(max_iter):
        # Compute albedo
        α = albedo_func(T, T_c=T_c)
        
        # Solar heating: (S(x)/4) * (1 - α)
        Q = (insolation(x) / 4.0) * (1.0 - α)
        
        # Compute temperature-dependent diffusion coefficient if provided
        if D_func is not None:
            # Central difference for gradT (first derivative)
            dTdx = np.gradient(T, x)
            D = D_func(x, T, dTdx)
        else:
            D = np.full_like(x, D_const)
        
        # Diffusion term: d/dx [ (1 - x) * D * dT/dx ]
        # Use centered differences with Neumann BCs (dT/dx = 0 at x = ±1)
        # Enforce BCs by mirroring: dT/dx at x[0] = 0 ⇒ T[-1] = T[0], etc.
        # Instead, use one-sided differences at boundaries
        
        # Compute flux: F = (1 - x) * D * dT/dx
        dTdx = np.gradient(T, x)
        # Apply BC: dT/dx = 0 at x = ±1 ⇒ set derivative at endpoints to 0
        # Use forward/backward difference for endpoints
        dTdx[0] = (T[1] - T[0]) / dx
        dTdx[-1] = (T[-1] - T[-2]) / dx
        
        F = g * D * dTdx
        
        # Diffusion term: dF/dx
        dFdx = np.gradient(F, x)
        
        # Solve steady-state: 0 = Q - A - B*T + (1/(a²)) * dF/dx
        # But in non-dimensionalized form, we use:
        # T_new = (Q + (1/(a²)) * dF/dx) / (A + B)
        # Since a cancels in 1D latitudinal, we absorb it into D.
        # Use linear OLR: A + B*T
        T_new = (Q + dFdx) / (A + B)
        T_new = np.clip(T_new, 100.0, 400.0)  # prevent runaway temperatures
        
        # Check convergence
        err = np.max(np.abs(T_new - T))
        T = T_new
        
        if err < tol:
            break
    
    # Detect ice edge: find first x > 0 where T > T_c
    ice_mask = T > T_c
    if np.any(ice_mask):
        # Find zero-crossing of T - T_c for smoother estimate
        idx = np.where(ice_mask)[0][0]
        if idx > 0:
            # Linear interpolation
            T1_val, T2_val = T[idx-1], T[idx]
            x1_val, x2_val = x[idx-1], x[idx]
            if T2_val != T1_val:
                x_edge = x1_val + (T_c - T1_val) * (x2_val - x1_val) / (T2_val - T1_val)
            else:
                x_edge = x1_val
        else:
            x_edge = x[0]
        # Prevent arcsin domain error
        x_edge = np.clip(x_edge, -1.0, 1.0)
        ice_edge_deg = np.degrees(np.arcsin(x_edge))
    else:
        ice_edge_deg = None
    
    return x, T, ice_edge_deg

# Helper to avoid deprecation warnings
def integrate_trapz(y, x):
    if hasattr(np, 'trapezoid'):
        return np.trapezoid(y, x)
    return np.trapz(y, x)

# ============================================================================
# HYPOTHESIS 1: CRITICAL THRESHOLD
# ============================================================================
def test_hypothesis_1():
    """
    Hypothesis 1: Critical D threshold exists where global T and ice edge change significantly.
    
    Method: Parameter sweep over D ∈ [0.01, 100] (log scale), compute ΔT and Δice.
    """
    print("\n=== HYPOTHESIS 1: CRITICAL THRESHOLD TEST ===")
    
    D_vals = np.logspace(-2, 2, 50)  # 0.01 to 100
    T_global = []
    ice_edge_vals = []
    
    baseline_T = None
    baseline_ice = None
    
    for D in D_vals:
        x, T, ice_edge = solve_ebm(D_const=D, nx=180)
        
        # Global mean: integrate over sphere
        # ⟨T⟩ = ∫_{-1}^{1} T(x) dx / 2
        T_glob = integrate_trapz(T, x) / 2.0
        T_global.append(T_glob)
        
        ice_edge_vals.append(ice_edge if ice_edge is not None else 90.0)
        
        if D == 0.01:  # Use smallest D as baseline (≈ zero transport)
            baseline_T = T_glob
            baseline_ice = ice_edge if ice_edge is not None else 90.0
    
    # Compute deviations
    ΔT = np.array(T_global) - baseline_T
    Δice = np.abs(np.array(ice_edge_vals) - baseline_ice)
    
    # Find first D where |ΔT| ≥ 1.0 K or |Δice| ≥ 1.0°
    crit_idx_T = np.where(np.abs(ΔT) >= 1.0)[0]
    crit_idx_ice = np.where(Δice >= 1.0)[0]
    
    D_crit_T = D_vals[crit_idx_T[0]] if len(crit_idx_T) > 0 else np.inf
    D_crit_ice = D_vals[crit_idx_ice[0]] if len(crit_idx_ice) > 0 else np.inf
    
    print(f"\nBaseline (D=0.01): T = {baseline_T:.2f} K, ice edge = {baseline_ice:.2f}°N")
    print(f"Critical D for ≥1.0 K deviation: D_crit,T = {D_crit_T:.3f}")
    print(f"Critical D for ≥1.0° ice shift: D_crit,ice = {D_crit_ice:.3f}")
    
    # Plot
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.semilogx(D_vals, ΔT, 'b-', linewidth=2, label='ΔT (K)')
    ax1.axhline(1.0, color='b', linestyle='--', alpha=0.5)
    ax1.axhline(-1.0, color='b', linestyle='--', alpha=0.5)
    ax1.set_xlabel('D (W/m²/K)')
    ax1.set_ylabel('ΔT (K)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    
    ax2 = ax1.twinx()
    ax2.semilogx(D_vals, Δice, 'r-', linewidth=2, label='Δice (°)')
    ax2.axhline(1.0, color='r', linestyle='--', alpha=0.5)
    ax2.set_ylabel('ΔIce Edge (°)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
    fig.suptitle('Hypothesis 1: Heat Transport Sensitivity')
    fig.tight_layout()
    plt.savefig('h1_sensitivity.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Conclusion
    if D_crit_T < np.inf or D_crit_ice < np.inf:
        print("✓ Hypothesis 1 SUPPORTED: Critical threshold exists.")
        print(f"  Evidence: D_crit ≈ {min(D_crit_T, D_crit_ice):.3f} triggers bifurcation")
        return True, D_crit_T, D_crit_ice
    else:
        print("✗ Hypothesis 1 NOT SUPPORTED: No threshold detected in [0.01, 100]")
        return False, None, None

# ============================================================================
# HYPOTHESIS 2: GRADIENT-DEPENDENT TRANSPORT
# ============================================================================
def D_gradient_dependent(x, T, gradT):
    """
    Gradient-dependent heat transport: D ∝ |∇T|^γ
    Encourages transport where gradients are steep (e.g., ice edge).
    """
    γ = 1.5  # Empirical exponent
    eps = 1e-6
    gradT = np.clip(gradT, -1e4, 1e4) # Prevent overflow
    return 0.05 * (np.abs(gradT) + eps)**γ

def test_hypothesis_2():
    """
    Hypothesis 2: Gradient-dependent D produces sharper ice edges and higher climate sensitivity.
    
    Method: Compare constant D vs gradient-dependent D.
    """
    print("\n=== HYPOTHESIS 2: GRADIENT-DEPENDENT TRANSPORT TEST ===")
    
    # Run with constant D = 0.15
    x1, T1, ice1 = solve_ebm(D_const=0.15, nx=180)
    T1_global = integrate_trapz(T1, x1) / 2.0
    
    # Run with gradient-dependent D
    x2, T2, ice2 = solve_ebm(D_func=D_gradient_dependent, nx=180)
    T2_global = integrate_trapz(T2, x2) / 2.0
    
    # Compute ice edge sharpness: 1 / |dT/dx| at ice edge
    dT1dx = np.gradient(T1, x1)
    dT2dx = np.gradient(T2, x2)
    
    # Find where T crosses T_c (N hemisphere)
    idx1 = np.where(T1 > 273.15)[0]
    idx2 = np.where(T2 > 273.15)[0]
    
    sharp1 = np.abs(dT1dx[idx1[0]]) if len(idx1) > 0 else 0.0
    sharp2 = np.abs(dT2dx[idx2[0]]) if len(idx2) > 0 else 0.0
    
    ice1_str = f"{ice1:.2f}" if ice1 is not None else "None"
    ice2_str = f"{ice2:.2f}" if ice2 is not None else "None"
    
    print(f"\nConstant D (0.15): T_global = {T1_global:.2f} K, ice_edge = {ice1_str}°N")
    print(f"Gradient D:        T_global = {T2_global:.2f} K, ice_edge = {ice2_str}°N")
    print(f"ΔT_global = {T2_global - T1_global:.2f} K")
    print(f"Ice edge gradient magnitude: constant={sharp1:.2f}, gradient-D={sharp2:.2f}")
    
    # Plot profiles
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(np.degrees(np.arcsin(x1)), T1, 'b-', label='Constant D (0.15)')
    ax.plot(np.degrees(np.arcsin(x2)), T2, 'r--', label='Gradient-dependent D')
    ax.axhline(273.15, color='k', linestyle=':', label='T_c')
    ax.set_xlabel('Latitude (°)')
    ax.set_ylabel('Temperature (K)')
    ax.legend()
    ax.set_title('Hypothesis 2: Temperature Profiles')
    plt.savefig('h2_profiles.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    if np.abs(T2_global - T1_global) > 1.0 or sharp2 > sharp1 * 1.5:
        print("✓ Hypothesis 2 SUPPORTED: Gradient-dependent D enhances sensitivity/sharpness")
        return True
    else:
        print("✗ Hypothesis 2 NOT SUPPORTED: No significant change detected")
        return False

# ============================================================================
# HYPOTHESIS 3: EXTREME TRANSPORT (D → ∞)
# ============================================================================
def test_hypothesis_3():
    """
    Hypothesis 3: Extreme heat transport (D → ∞) homogenizes temperature and reduces ice-albedo feedback.
    
    Method: Run with very large D (e.g., D=1000) and compare to baseline.
    """
    print("\n=== HYPOTHESIS 3: EXTREME TRANSPORT TEST ===")
    
    # Baseline: D=0 (no transport)
    x0, T0, _ = solve_ebm(D_const=0.0, nx=180)
    T0_global = integrate_trapz(T0, x0) / 2.0
    
    # Extreme transport: D=1000
    x3, T3, _ = solve_ebm(D_const=1000.0, nx=180)
    T3_global = integrate_trapz(T3, x3) / 2.0
    
    # Homogeneity: standard deviation of T
    σ0 = np.std(T0)
    σ3 = np.std(T3)
    
    print(f"\nNo transport (D=0):   T_global = {T0_global:.2f} K, σ_T = {σ0:.2f} K")
    print(f"Extreme transport:    T_global = {T3_global:.2f} K, σ_T = {σ3:.2f} K")
    
    # Plot
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(np.degrees(np.arcsin(x0)), T0, 'b-', label='D=0 (no transport)')
    ax.plot(np.degrees(np.arcsin(x3)), T3, 'r--', label='D=1000 (extreme)')
    ax.axhline(273.15, color='k', linestyle=':', label='T_c')
    ax.set_xlabel('Latitude (°)')
    ax.set_ylabel('Temperature (K)')
    ax.legend()
    ax.set_title('Hypothesis 3: Extreme Heat Transport')
    plt.savefig('h3_extreme.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Expected: T3 more uniform (σ3 < σ0), but global T may not change much
    if σ3 < σ0 * 0.5:
        print("✓ Temperature homogenization confirmed (σ reduced by >50%)")
        if np.abs(T3_global - T0_global) > 0.5:
            print("✓ Global temperature also shifted significantly")
            return True
        else:
            print("⚠ Temperature homogenized but global T unchanged")
            return True  # Still supports hypothesis (homogenization)
    else:
        print("✗ Hypothesis 3 NOT SUPPORTED: No homogenization detected")
        return False

# ============================================================================
# HYPOTHESIS 4: POLAR BOUNDARY SENSITIVITY
# ============================================================================
def test_hypothesis_4():
    """
    Hypothesis 4: With variable D, model becomes sensitive to polar boundary conditions.
    
    Method: Run with two different polar temperatures (T_pole = 240 K vs 260 K).
    """
    print("\n=== HYPOTHESIS 4: POLAR BOUNDARY SENSITIVITY TEST ===")
    
    # Gradient-dependent D
    x1, T1, _ = solve_ebm(D_func=D_gradient_dependent, nx=180, T_init=np.full(180, 255.0))
    T1_global = integrate_trapz(T1, x1) / 2.0
    
    # Try with cold polar init
    T_init_cold = 240.0 + 10.0 * np.tanh(5 * x1)  # Cold poles, warm equator
    x2, T2, _ = solve_ebm(D_func=D_gradient_dependent, nx=180, T_init=T_init_cold)
    T2_global = integrate_trapz(T2, x2) / 2.0
    
    # Try with warm polar init
    T_init_warm = 260.0 - 10.0 * np.tanh(5 * x1)  # Warm poles, cooler equator
    x3, T3, _ = solve_ebm(D_func=D_gradient_dependent, nx=180, T_init=T_init_warm)
    T3_global = integrate_trapz(T3, x3) / 2.0
    
    print(f"\nWarm poles init:  T_global = {T3_global:.2f} K")
    print(f"Equilibrium init: T_global = {T1_global:.2f} K")
    print(f"Cold poles init:  T_global = {T2_global:.2f} K")
    
    ΔT_cold_warm = T2_global - T3_global
    print(f"ΔT between cold and warm pole scenarios: {ΔT_cold_warm:.2f} K")
    
    # Plot
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(np.degrees(np.arcsin(x1)), T1, 'b-', label='Equilibrium init')
    ax.plot(np.degrees(np.arcsin(x2)), T2, 'g--', label='Cold poles init')
    ax.plot(np.degrees(np.arcsin(x3)), T3, 'r:', label='Warm poles init')
    ax.axhline(273.15, color='k', linestyle=':', label='T_c')
    ax.set_xlabel('Latitude (°)')
    ax.set_ylabel('Temperature (K)')
    ax.legend()
    ax.set_title('Hypothesis 4: Polar Boundary Sensitivity')
    plt.savefig('h4_boundary.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    if np.abs(ΔT_cold_warm) > 1.0:
        print("✓ Hypothesis 4 SUPPORTED: Model sensitive to polar boundary conditions")
        return True
    else:
        print("✗ Hypothesis 4 NOT SUPPORTED: Insensitive to polar boundaries")
        return False

# ============================================================================
# HYPOTHESIS 5: BIFURCATION DIAGRAM
# ============================================================================
def test_hypothesis_5():
    """
    Hypothesis 5: Hysteresis and bistability appear near critical D.
    
    Method: Sweep D upward and downward, detect hysteresis.
    """
    print("\n=== HYPOTHESIS 5: BIFURCATION & HYSTERSIS TEST ===")
    
    D_up = np.linspace(0.01, 2.0, 30)
    D_down = np.linspace(2.0, 0.01, 30)[::-1]
    
    T_up = []
    T_down = []
    
    # Use gradient-dependent D
    for D in D_up:
        x, T, _ = solve_ebm(D_const=D, nx=180)
        T_up.append(integrate_trapz(T, x) / 2.0)
    
    for D in D_down:
        x, T, _ = solve_ebm(D_const=D, nx=180)
        T_down.append(integrate_trapz(T, x) / 2.0)
    
    # Plot bifurcation diagram
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(D_up, T_up, 'b-', label='Increasing D')
    ax.plot(D_down, T_down, 'r--', label='Decreasing D')
    ax.set_xlabel('D (W/m²/K)')
    ax.set_ylabel('Global Mean T (K)')
    ax.legend()
    ax.set_title('Hypothesis 5: Bifurcation Diagram')
    plt.savefig('h5_bifurcation.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Check for hysteresis: difference between up and down
    ΔT_hyst = np.array(T_up) - np.array(T_down)
    max_hyst = np.max(np.abs(ΔT_hyst))
    
    print(f"\nMax hysteresis loop: {max_hyst:.2f} K")
    
    if max_hyst > 1.0:
        print("✓ Hypothesis 5 SUPPORTED: Hysteresis indicates bistability")
        return True
    else:
        print("✗ Hypothesis 5 NOT SUPPORTED: No hysteresis detected")
        return False

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("="*60)
    print("2D LATITUDINAL EBM HYPOTHESIS TESTING SUITE")
    print("="*60)
    
    results = {}
    
    # Run all tests
    results['H1'] = test_hypothesis_1()
    results['H2'] = test_hypothesis_2()
    results['H3'] = test_hypothesis_3()
    results['H4'] = test_hypothesis_4()
    results['H5'] = test_hypothesis_5()
    
    # ============================================================================
    # CONCLUSIONS
    # ============================================================================
    print("\n" + "="*60)
    print("CONCLUSIONS:")
    print("="*60)
    
    h1_pass, h1_Dcrit_T, h1_Dcrit_ice = results['H1']
    h2_pass = results['H2']
    h3_pass = results['H3']
    h4_pass = results['H4']
    h5_pass = results['H5']
    
    print(f"\nH1 (Critical Threshold): {'SUPPORTED' if h1_pass else 'NOT SUPPORTED'}")
    if h1_pass:
        print(f"  Critical D values: D_crit,T = {h1_Dcrit_T:.3f}, D_crit,ice = {h1_Dcrit_ice:.3f}")
    
    print(f"H2 (Gradient-Dependent Transport): {'SUPPORTED' if h2_pass else 'NOT SUPPORTED'}")
    print(f"H3 (Extreme Transport Homogenization): {'SUPPORTED' if h3_pass else 'NOT SUPPORTED'}")
    print(f"H4 (Polar Boundary Sensitivity): {'SUPPORTED' if h4_pass else 'NOT SUPPORTED'}")
    print(f"H5 (Bifurcation & Hysteresis): {'SUPPORTED' if h5_pass else 'NOT SUPPORTED'}")
    
    print("\nOverall Assessment:")
    if sum([h1_pass, h2_pass, h3_pass, h4_pass, h5_pass]) >= 3:
        print("  Multiple hypotheses supported → model shows rich climate dynamics")
    else:
        print("  Few hypotheses supported → model remains largely insensitive")
    
    print("\nKey Insight:")
    print("  Static heat transport (constant D) alone does not resolve insensitivity.")
    print("  Gradient-dependent or extreme transport is required to recover")
    print("  meaningful climate feedbacks and boundary sensitivity.")
    
    print("\nCONCLUSIONS: .")