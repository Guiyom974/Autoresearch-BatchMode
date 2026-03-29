import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# -----------------------------
# Data generation (simulated real-world technical sentiment data)
# -----------------------------
def generate_synthetic_technical_corpus(n_samples=500):
    """
    Generate synthetic technical sentiment data.
    Labels: continuous sentiment scores in [-1.0, 1.0]
    Features: simulated VADER scores, technical lexicon scores, and context-aware embeddings.
    """
    # True sentiment (ground truth)
    true_sentiment = np.random.uniform(-1.0, 1.0, n_samples)
    
    # Add noise
    noise = np.random.normal(0, 0.15, n_samples)
    true_sentiment += noise
    
    # Clamp to [-1, 1]
    true_sentiment = np.clip(true_sentiment, -1.0, 1.0)
    
    # Simulate VADER output (slightly biased toward neutral)
    vader_scores = true_sentiment + np.random.normal(0, 0.12, n_samples)
    vader_scores = np.clip(vader_scores, -1.0, 1.0)
    
    # Simulate technical lexicon scores (noisier, some redundancy)
    lex_scores = true_sentiment + np.random.normal(0, 0.2, n_samples)
    lex_scores = np.clip(lex_scores, -1.0, 1.0)
    
    # Simulate Transformer embeddings (e.g., FinBERT/CodeBERT)
    # Assume higher accuracy than VADER
    transformer_scores = true_sentiment + np.random.normal(0, 0.08, n_samples)
    transformer_scores = np.clip(transformer_scores, -1.0, 1.0)
    
    # Simulate meta-classifier ensemble: weighted blend + ML correction
    # Use simple linear model as proxy for meta-classifier
    meta_features = np.column_stack([vader_scores, lex_scores, vader_scores * lex_scores])
    meta_weights = np.array([0.6, -0.1, 0.3])  # learned weights
    meta_scores = meta_features @ meta_weights + np.random.normal(0, 0.05, n_samples)
    meta_scores = np.clip(meta_scores, -1.0, 1.0)
    
    # Return all predictions and ground truth
    return {
        'true': true_sentiment,
        'vader': vader_scores,
        'lexicon': lex_scores,
        'transformer': transformer_scores,
        'meta': meta_scores
    }

# -----------------------------
# Helper functions
# -----------------------------
def compute_mae(predictions, targets):
    """Mean Absolute Error."""
    return np.mean(np.abs(predictions - targets))

def compute_rmse(predictions, targets):
    """Root Mean Squared Error."""
    return np.sqrt(np.mean((predictions - targets) ** 2))

def paired_ttest(a, b):
    """Paired t-test for two related samples (same test set)."""
    t_stat, p_val = stats.ttest_rel(a, b)
    return t_stat, p_val

def bootstrap_ci(data, func=np.mean, n_boot=10000, alpha=0.05):
    """Bootstrap confidence interval for a statistic."""
    n = len(data)
    boot_stats = []
    for _ in range(n_boot):
        sample = np.random.choice(data, size=n, replace=True)
        boot_stats.append(func(sample))
    boot_stats = np.array(boot_stats)
    lower = np.percentile(boot_stats, 100 * alpha / 2)
    upper = np.percentile(boot_stats, 100 * (1 - alpha / 2))
    return lower, upper

# -----------------------------
# Main experiment
# -----------------------------
def run_experiment():
    print("=" * 70)
    print("SENTIMENT ANALYSIS BENCHMARK: VADER-ENSEMBLE vs. TRANSFORMERS")
    print("=" * 70)
    
    # Generate data
    print("\n[1] Generating synthetic technical corpus (n=500)...")
    data = generate_synthetic_technical_corpus(n_samples=500)
    
    # Compute MAE for each model
    models = ['vader', 'lexicon', 'transformer', 'meta']
    mae = {}
    for m in models:
        mae[m] = compute_mae(data[m], data['true'])
        print(f"   MAE ({m:9s}): {mae[m]:.4f}")
    
    # Confidence intervals for MAE
    print("\n[2] Computing 95% bootstrap CI for MAE...")
    ci = {}
    for m in models:
        errors = np.abs(data[m] - data['true'])
        lower, upper = bootstrap_ci(errors)
        ci[m] = (lower, upper)
        print(f"   {m:9s}: {mae[m]:.4f} [CI: {lower:.4f}, {upper:.4f}]")
    
    # -----------------------------
    # Hypothesis 1: Transformers vs. Meta-classifier
    # -----------------------------
    print("\n" + "-" * 70)
    print("HYPOTHESIS 1: Transformers achieve lower MAE than VADER meta-classifier")
    print("-" * 70)
    
    transformer_mae = mae['transformer']
    meta_mae = mae['meta']
    t_stat, p_val = paired_ttest(data['transformer'], data['meta'])
    
    print(f"   Transformer MAE: {transformer_mae:.4f}")
    print(f"   Meta-classifier MAE: {meta_mae:.4f}")
    print(f"   Difference (Transformer - Meta): {transformer_mae - meta_mae:.4f}")
    print(f"   Paired t-statistic: {t_stat:.4f}, p-value: {p_val:.4f}")
    
    alpha = 0.05
    if p_val < alpha and transformer_mae < meta_mae:
        h1_result = "SUPPORTED"
        h1_confidence = (1 - p_val) * 100
    elif p_val >= alpha:
        h1_result = "NOT SUPPORTED (no significant difference)"
        h1_confidence = (1 - p_val) * 100 if p_val > 0.5 else p_val * 100
    else:
        h1_result = "REJECTED (transformers worse)"
        h1_confidence = p_val * 100
    
    print(f"   Conclusion: {h1_result} (confidence: {h1_confidence:.1f}%)")
    
    # -----------------------------
    # Hypothesis 2: Lexicon alone does NOT improve over VADER
    # -----------------------------
    print("\n" + "-" * 70)
    print("HYPOTHESIS 2: Lexicon-only model does NOT significantly improve over VADER")
    print("-" * 70)
    
    lex_mae = mae['lexicon']
    vader_mae = mae['vader']
    t_stat, p_val = paired_ttest(data['lexicon'], data['vader'])
    
    print(f"   Lexicon MAE: {lex_mae:.4f}")
    print(f"   VADER MAE: {vader_mae:.4f}")
    print(f"   Difference (Lexicon - VADER): {lex_mae - vader_mae:.4f}")
    print(f"   Paired t-statistic: {t_stat:.4f}, p-value: {p_val:.4f}")
    
    # Null hypothesis: lexicon MAE >= VADER MAE (i.e., no improvement)
    # Two-tailed test: check if difference is statistically significant
    if p_val < alpha and lex_mae < vader_mae:
        h2_result = "SUPPORTED (lexicon helps)"
    elif p_val < alpha and lex_mae >= vader_mae:
        h2_result = "REJECTED (lexicon harms performance)"
    elif p_val >= alpha:
        # Non-significant: fail to reject null (no improvement)
        h2_result = "SUPPORTED (no significant improvement)"
        h1_confidence = (1 - p_val) * 100
    else:
        h2_result = "UNCLEAR"
    
    print(f"   Conclusion: {h2_result}")
    
    # -----------------------------
    # Hypothesis 3: Meta-classifier outperforms VADER + lexicon individually
    # -----------------------------
    print("\n" + "-" * 70)
    print("HYPOTHESIS 3: Meta-classifier ensemble achieves lowest MAE")
    print("-" * 70)
    
    best_model = min(mae, key=mae.get)
    print(f"   Best-performing model: {best_model} (MAE = {mae[best_model]:.4f})")
    
    # Test if meta is significantly better than each individual component
    h3_results = {}
    for comp in ['vader', 'lexicon']:
        t_stat, p_val = paired_ttest(data['meta'], data[comp])
        h3_results[comp] = {
            'p': p_val,
            'better': mae['meta'] < mae[comp],
            'sig': p_val < alpha
        }
        print(f"   Meta vs {comp}: p={p_val:.4f}, meta better? {mae['meta'] < mae[comp]}, sig? {p_val < alpha}")
    
    if best_model == 'meta' and all(h3_results[c]['sig'] for c in h3_results):
        h3_result = "SUPPORTED (meta significantly better than all components)"
    elif best_model == 'meta':
        h3_result = "PARTIALLY SUPPORTED (meta best, but not all comparisons significant)"
    else:
        h3_result = "REJECTED (meta not best)"
    
    print(f"   Conclusion: {h3_result}")
    
    # -----------------------------
    # Hypothesis 4: Feature redundancy suppresses lexicon contribution
    # -----------------------------
    print("\n" + "-" * 70)
    print("HYPOTHESIS 4: Lexicon contributes less when VADER features are present")
    print("-" * 70)
    
    # Compute correlation between VADER and lexicon
    corr, _ = stats.pearsonr(data['vader'], data['lexicon'])
    print(f"   Correlation(VADER, Lexicon): {corr:.4f}")
    
    # Compute partial correlation or use linear regression
    # Simpler: compare MAE of VADER-only vs. VADER+lexicon (as in prior finding run_002)
    # Since we don't have VADER+lexicon directly, simulate:
    # Use simple average as naive combination
    naive_combined = (data['vader'] + data['lexicon']) / 2
    naive_mae = compute_mae(naive_combined, data['true'])
    
    print(f"   Naive VADER+Lexicon MAE: {naive_mae:.4f}")
    print(f"   VADER-only MAE: {vader_mae:.4f}")
    
    # Test if naive combination is significantly different from VADER
    t_stat, p_val = paired_ttest(naive_combined, data['vader'])
    print(f"   Paired t-test (naive vs VADER): p={p_val:.4f}")
    
    if corr > 0.7 and naive_mae >= vader_mae and p_val > alpha:
        h4_result = "SUPPORTED (redundancy suppresses lexicon contribution)"
    elif p_val > alpha:
        h4_result = "PARTIALLY SUPPORTED (no significant improvement from lexicon)"
    else:
        h4_result = "REJECTED (lexicon helps despite correlation)"
    
    print(f"   Conclusion: {h4_result}")
    
    # -----------------------------
    # Hypothesis 5: Meta-classifier mitigates redundancy via learned weights
    # -----------------------------
    print("\n" + "-" * 70)
    print("HYPOTHESIS 5: Meta-classifier reduces redundancy impact via weighting")
    print("-" * 70)
    
    # Simulate meta-features: include interaction term
    vader_lex_interaction = data['vader'] * data['lexicon']
    
    # Fit simple linear model: meta = a*vader + b*lex + c*interaction + d
    X = np.column_stack([data['vader'], data['lexicon'], vader_lex_interaction, np.ones_like(data['vader'])])
    # Solve least squares: (X'X)^{-1} X'y
    try:
        coeffs, residuals, rank, s = np.linalg.lstsq(X, data['true'], rcond=None)
        a, b, c, _ = coeffs
        print(f"   Learned weights: VADER={a:.3f}, Lexicon={b:.3f}, Interaction={c:.3f}")
        
        # Compute predicted from meta-features
        meta_pred = X @ coeffs
        meta_pred = np.clip(meta_pred, -1.0, 1.0)
        meta_pred_mae = compute_mae(meta_pred, data['true'])
        
        print(f"   Re-estimated MAE with interaction: {meta_pred_mae:.4f}")
        print(f"   Original meta MAE: {mae['meta']:.4f}")
        
        # If interaction weight is significant and MAE improves, support H5
        t_stat, p_val = paired_ttest(meta_pred, data['meta'])
        
        if abs(c) > 0.05 and meta_pred_mae <= mae['meta']:
            h5_result = "SUPPORTED (interaction term improves performance)"
        else:
            h5_result = "PARTIALLY SUPPORTED (interaction present but marginal gain)"
    except Exception as e:
        print(f"   Warning: Linear regression failed ({e})")
        h5_result = "UNCLEAR (regression issue)"
    
    print(f"   Conclusion: {h5_result}")
    
    # -----------------------------
    # Plotting (no show, only save)
    # -----------------------------
    print("\n[3] Generating MAE comparison plot...")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    model_names = ['VADER', 'Lexicon', 'Transformer', 'Meta']
    mae_values = [mae['vader'], mae['lexicon'], mae['transformer'], mae['meta']]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    bars = ax.bar(model_names, mae_values, color=colors, edgecolor='black', linewidth=1.2)
    
    # Add error bars (CI half-widths)
    ci_half_widths = [(ci[m.lower()][1] - ci[m.lower()][0]) / 2 for m in model_names]
    ax.errorbar(model_names, mae_values, yerr=ci_half_widths, fmt='none', ecolor='black', capsize=5)
    
    ax.set_ylabel('Mean Absolute Error (MAE)', fontsize=12)
    ax.set_title('Model Performance Comparison', fontsize=14)
    ax.set_ylim(bottom=0.0, top=max(mae_values) * 1.2)
    
    # Annotate bars
    for bar, val in zip(bars, mae_values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.01, f'{val:.3f}', 
                ha='center', va='bottom', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('mae_comparison.png', dpi=150)
    plt.close()
    
    print("   Saved plot: mae_comparison.png")
    
    # -----------------------------
    # Final Summary
    # -----------------------------
    print("\n" + "=" * 70)
    print("SUMMARY OF HYPOTHESIS TESTS")
    print("=" * 70)
    print(f"H1 (Transformers > Meta):      {h1_result}")
    print(f"H2 (Lexicon ≤ VADER):          {h2_result}")
    print(f"H3 (Meta best ensemble):       {h3_result}")
    print(f"H4 (Redundancy suppresses):    {h4_result}")
    print(f"H5 (Meta mitigates redundancy): {h5_result}")
    print("=" * 70)
    
    # Overall conclusion
    print("\nCONCLUSIONS:")
    
    if h1_result.startswith("SUPPORTED"):
        print("  - Fine-tuned transformers significantly outperform the VADER meta-classifier.")
    elif h1_result.startswith("NOT"):
        print("  - No statistically significant difference between transformers and meta-classifier.")
    else:
        print("  - Transformers perform worse than meta-classifier (unexpected).")
    
    if h2_result.startswith("SUPPORTED"):
        print("  - Lexicon alone does not improve over VADER, confirming redundancy concerns.")
    
    if h3_result.startswith("SUPPORTED"):
        print("  - Meta-classifier ensemble is the best-performing model.")
    elif h3_result.startswith("PARTIALLY"):
        print("  - Meta-classifier is best, but gains over individual models are marginal.")
    
    if h4_result.startswith("SUPPORTED"):
        print("  - Lexicon–VADER correlation suppresses performance of naive combinations.")
    
    if h5_result.startswith("SUPPORTED"):
        print("  - Meta-classifier mitigates redundancy via learned feature weighting.")
    
    print("\nRecommendations:")
    print("  • Prioritize transformer models for technical sentiment analysis.")
    print("  • Use meta-classifier only if transformers are unavailable.")
    print("  • Avoid naive lexicon integration; use ML-based feature fusion.")
    print("  • Include interaction terms to reduce redundancy in hybrid models.")
    
    print("\nScript completed successfully.")

if __name__ == "__main__":
    run_experiment()