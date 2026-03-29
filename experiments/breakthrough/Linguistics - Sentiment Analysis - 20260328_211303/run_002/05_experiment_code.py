import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import random

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# SECTION 1: Synthetic Technical Corpus Generation
# ============================================================================

def generate_synthetic_technical_corpus(n_docs=200, min_words=30, max_words=120):
    """
    Generate synthetic technical documents with known sentiment scores.
    Technical terms will be embedded in neutral/positive/negative contexts.
    """
    # Domain-specific technical terms (positive, negative, neutral)
    positive_terms = ["optimized", "efficient", "robust", "scalable", "reliable", "high-performance", "enhanced"]
    negative_terms = ["buggy", "inefficient", "unstable", "flawed", "deprecated", "incompatible", "slow"]
    neutral_terms = ["parameter", "function", "module", "variable", "algorithm", "interface", "component"]
    
    # Modifiers (intensifiers/diminishers)
    intensifiers = ["very", "highly", "significantly", "extremely", "remarkably"]
    diminishers = ["slightly", "somewhat", "partially", "marginally", "barely"]
    
    # Technical negation patterns
    negation_words = ["not", "no", "never", "none", "neither", "nobody", "nothing"]
    
    documents = []
    ground_truth = []
    
    for _ in range(n_docs):
        # Randomly assign sentiment category: -1 (negative), 0 (neutral), +1 (positive)
        sentiment = random.choice([-1, 0, 1])
        
        # Document length
        n_words = random.randint(min_words, max_words)
        
        # Build document
        words = []
        
        # Ensure at least one sentiment-carrying term
        if sentiment != 0:
            target_term = random.choice(positive_terms if sentiment > 0 else negative_terms)
            # Add context with possible modifiers and negations
            if random.random() < 0.4:
                modifier = random.choice(intensifiers if sentiment > 0 else diminishers)
                words.append(modifier)
            if random.random() < 0.2:
                negation = random.choice(negation_words)
                words.append(negation)
            words.append(target_term)
        
        # Fill remaining words with technical terms
        while len(words) < n_words:
            r = random.random()
            if r < 0.25:
                words.append(random.choice(positive_terms))
            elif r < 0.5:
                words.append(random.choice(negative_terms))
            else:
                words.append(random.choice(neutral_terms))
        
        # Join and store
        doc = " ".join(words)
        documents.append(doc)
        ground_truth.append(sentiment)
    
    return documents, np.array(ground_truth)

# ============================================================================
# SECTION 2: Domain-Specific Lexicon Construction
# ============================================================================

def build_technical_lexicon():
    """
    Build a domain-specific lexicon for technical terms.
    Each entry: {term: (v_neg, v_neu, v_pos, v_compound)}
    VADER expects compound scores in [-4, 4], but we'll use [-1, 1] for simplicity.
    """
    # Technical term sentiment scores (positive/negative/neutral)
    technical_lexicon = {}
    
    # Positive technical terms
    for term in ["optimized", "efficient", "robust", "scalable", "reliable", "high-performance", "enhanced"]:
        technical_lexicon[term] = 0.0, 0.0, 1.0, 1.0
    
    # Negative technical terms
    for term in ["buggy", "inefficient", "unstable", "flawed", "deprecated", "incompatible", "slow"]:
        technical_lexicon[term] = 1.0, 0.0, 0.0, -1.0
    
    # Neutral technical terms
    for term in ["parameter", "function", "module", "variable", "algorithm", "interface", "component"]:
        technical_lexicon[term] = 0.0, 1.0, 0.0, 0.0
    
    # Add intensifiers and diminishers with appropriate weights
    for term in ["very", "highly", "significantly", "extremely", "remarkably"]:
        technical_lexicon[term] = 0.0, 0.0, 0.0, 0.5
    for term in ["slightly", "somewhat", "partially", "marginally", "barely"]:
        technical_lexicon[term] = 0.0, 0.0, 0.0, -0.3
    
    return technical_lexicon

# ============================================================================
# SECTION 3: VADER Implementation (Minimal Subset for Technical Use)
# ============================================================================

class MinimalVADER:
    """
    Minimal VADER implementation with only core functionality needed for this test.
    Uses rule-based heuristics and a lexicon.
    """
    def __init__(self, domain_lexicon=None):
        # Default VADER-like lexicon (simplified)
        self.lexicon = {
            "good": (0.0, 0.0, 1.0, 1.0),
            "great": (0.0, 0.0, 1.0, 1.5),
            "bad": (1.0, 0.0, 0.0, -1.0),
            "terrible": (1.0, 0.0, 0.0, -1.5),
            "excellent": (0.0, 0.0, 1.0, 1.5),
            "poor": (0.5, 0.0, 0.0, -0.5),
            "amazing": (0.0, 0.0, 1.0, 1.5),
            "awful": (1.0, 0.0, 0.0, -1.5),
            "ok": (0.0, 1.0, 0.0, 0.0),
            "fine": (0.0, 1.0, 0.0, 0.0),
            "not": (1.0, 0.0, 0.0, -0.5),  # Negation word
            "no": (1.0, 0.0, 0.0, -0.5),
            "never": (1.0, 0.0, 0.0, -0.5),
        }
        
        # Add domain-specific lexicon if provided
        if domain_lexicon:
            self.lexicon.update(domain_lexicon)
        
        # Negation words
        self.negation_words = {"not", "no", "never", "none", "neither", "nobody", "nothing"}
        
        # Intensifiers and diminishers
        self.intensifiers = {"very", "highly", "significantly", "extremely", "remarkably"}
        self.diminishers = {"slightly", "somewhat", "partially", "marginally", "barely"}
    
    def analyze(self, text):
        """
        Analyze sentiment of text and return compound score in [-1, 1].
        """
        words = text.lower().split()
        compound = 0.0
        i = 0
        
        while i < len(words):
            word = words[i]
            score = self.lexicon.get(word, (0.0, 0.0, 0.0, 0.0))[3]  # compound score
            
            # Check for negation in previous 3 words
            negated = False
            start = max(0, i - 3)
            for j in range(start, i):
                if words[j] in self.negation_words:
                    negated = True
                    break
            
            # Check for intensifiers/diminishers in previous 2 words
            modifier = 1.0
            start = max(0, i - 2)
            for j in range(start, i):
                if words[j] in self.intensifiers:
                    modifier = 1.5
                elif words[j] in self.diminishers:
                    modifier = 0.7
            
            # Apply modifiers and negation
            if negated:
                score = -score
            score *= modifier
            
            compound += score
            i += 1
        
        # Normalize compound score to [-1, 1]
        if compound > 0:
            compound = min(compound / 4.0, 1.0)
        elif compound < 0:
            compound = max(compound / 4.0, -1.0)
        
        return compound


# ============================================================================
# SECTION 4: Evaluation Metrics
# ============================================================================

def compute_mae(predictions, ground_truth):
    """Compute Mean Absolute Error."""
    return np.mean(np.abs(predictions - ground_truth))

def compute_mae_reduction(baseline_mae, hybrid_mae):
    """Compute percentage reduction in MAE."""
    if baseline_mae == 0:
        return 0.0
    return ((baseline_mae - hybrid_mae) / baseline_mae) * 100

def t_test_dependent(sample1, sample2):
    """Perform paired t-test."""
    # Compute differences
    diff = np.array(sample1) - np.array(sample2)
    # Paired t-test
    t_stat, p_value = stats.ttest_rel(sample1, sample2)
    return t_stat, p_value

# ============================================================================
# SECTION 5: Main Experiment
# ============================================================================

def main():
    print("="*70)
    print("HYBRID VADER + DOMAIN LEXICON SENTIMENT ANALYSIS TEST")
    print("="*70)
    
    # Generate synthetic technical corpus
    print("\n[1/5] Generating synthetic technical corpus...")
    documents, ground_truth = generate_synthetic_technical_corpus(n_docs=200)
    print(f"    Generated {len(documents)} technical documents.")
    
    # Build domain-specific lexicon
    print("\n[2/5] Building domain-specific technical lexicon...")
    domain_lexicon = build_technical_lexicon()
    print(f"    Lexicon contains {len(domain_lexicon)} technical terms.")
    
    # Initialize models
    print("\n[3/5] Initializing VADER models...")
    vader_baseline = MinimalVADER()
    vader_hybrid = MinimalVADER(domain_lexicon=domain_lexicon)
    print("    Baseline VADER and Hybrid VADER initialized.")
    
    # Analyze documents with both models
    print("\n[4/5] Analyzing documents...")
    baseline_scores = []
    hybrid_scores = []
    
    for doc in documents:
        baseline_scores.append(vader_baseline.analyze(doc))
        hybrid_scores.append(vader_hybrid.analyze(doc))
    
    baseline_scores = np.array(baseline_scores)
    hybrid_scores = np.array(hybrid_scores)
    
    # Compute MAE for both models
    baseline_mae = compute_mae(baseline_scores, ground_truth)
    hybrid_mae = compute_mae(hybrid_scores, ground_truth)
    
    print(f"    Baseline VADER MAE: {baseline_mae:.4f}")
    print(f"    Hybrid VADER MAE:   {hybrid_mae:.4f}")
    
    # Compute MAE reduction
    mae_reduction_pct = compute_mae_reduction(baseline_mae, hybrid_mae)
    print(f"    MAE Reduction:      {mae_reduction_pct:.2f}%")
    
    # Statistical test
    print("\n[5/5] Performing statistical analysis...")
    t_stat, p_value = t_test_dependent(baseline_scores, hybrid_scores)
    print(f"    Paired t-test: t = {t_stat:.4f}, p = {p_value:.6f}")
    
    # ============================================================================
    # HYPOTHESIS TESTING
    # ============================================================================
    
    print("\n" + "="*70)
    print("HYPOTHESIS TESTING RESULTS")
    print("="*70)
    
    # Hypothesis 1: MAE Reduction >= 10%
    print("\nHYPOTHESIS 1: MAE Reduction >= 10%")
    print("-" * 40)
    print(f"Observed MAE reduction: {mae_reduction_pct:.2f}%")
    print(f"Threshold: 10%")
    
    if mae_reduction_pct >= 10:
        print("Result: ✅ SUPPORTED (reduction >= 10%)")
    else:
        print("Result: ❌ NOT SUPPORTED (reduction < 10%)")
    
    # Additional analysis: significance
    alpha = 0.05
    if p_value < alpha:
        print(f"Statistical significance: ✅ p = {p_value:.6f} < {alpha}")
    else:
        print(f"Statistical significance: ❌ p = {p_value:.6f} >= {alpha}")
    
    # ============================================================================
    # HYPOTHESIS 2: Technical Negation Handling
    # ============================================================================
    
    print("\nHYPOTHESIS 2: Improved Technical Negation Handling")
    print("-" * 40)
    
    # Extract documents with negation patterns
    negation_docs = []
    negation_ground_truth = []
    for i, doc in enumerate(documents):
        if any(neg in doc.lower() for neg in ["not ", "no ", "never "]):
            negation_docs.append(doc)
            negation_ground_truth.append(ground_truth[i])
    
    if len(negation_docs) > 0:
        baseline_neg_scores = np.array([vader_baseline.analyze(doc) for doc in negation_docs])
        hybrid_neg_scores = np.array([vader_hybrid.analyze(doc) for doc in negation_docs])
        
        baseline_neg_mae = compute_mae(baseline_neg_scores, negation_ground_truth)
        hybrid_neg_mae = compute_mae(hybrid_neg_scores, negation_ground_truth)
        
        print(f"Baseline MAE on negation docs: {baseline_neg_mae:.4f}")
        print(f"Hybrid MAE on negation docs:   {hybrid_neg_mae:.4f}")
        print(f"Negation MAE reduction: {compute_mae_reduction(baseline_neg_mae, hybrid_neg_mae):.2f}%")
        
        if compute_mae_reduction(baseline_neg_mae, hybrid_neg_mae) > 0:
            print("Result: ✅ SUPPORTED (negation handling improved)")
        else:
            print("Result: ❌ NOT SUPPORTED (no improvement)")
    else:
        print("No negation documents found.")
    
    # ============================================================================
    # HYPOTHESIS 3: Domain-Specific Jargon Handling
    # ============================================================================
    
    print("\nHYPOTHESIS 3: Domain-Specific Jargon Handling")
    print("-" * 40)
    
    # Extract documents with domain-specific terms
    positive_terms = ["optimized", "efficient", "robust", "scalable", "reliable", "high-performance", "enhanced"]
    negative_terms = ["buggy", "inefficient", "unstable", "flawed", "deprecated", "incompatible", "slow"]
    
    jargon_docs = []
    jargon_ground_truth = []
    for i, doc in enumerate(documents):
        words = doc.lower().split()
        if any(term in words for term in positive_terms + negative_terms):
            jargon_docs.append(doc)
            jargon_ground_truth.append(ground_truth[i])
    
    if len(jargon_docs) > 0:
        baseline_jargon_scores = np.array([vader_baseline.analyze(doc) for doc in jargon_docs])
        hybrid_jargon_scores = np.array([vader_hybrid.analyze(doc) for doc in jargon_docs])
        
        baseline_jargon_mae = compute_mae(baseline_jargon_scores, jargon_ground_truth)
        hybrid_jargon_mae = compute_mae(hybrid_jargon_scores, jargon_ground_truth)
        
        print(f"Baseline MAE on jargon docs: {baseline_jargon_mae:.4f}")
        print(f"Hybrid MAE on jargon docs:   {hybrid_jargon_mae:.4f}")
        print(f"Jargon MAE reduction: {compute_mae_reduction(baseline_jargon_mae, hybrid_jargon_mae):.2f}%")
        
        if compute_mae_reduction(baseline_jargon_mae, hybrid_jargon_mae) > 10:
            print("Result: ✅ SUPPORTED (significant jargon improvement)")
        elif compute_mae_reduction(baseline_jargon_mae, hybrid_jargon_mae) > 0:
            print("Result: ⚠️ PARTIALLY SUPPORTED (modest improvement)")
        else:
            print("Result: ❌ NOT SUPPORTED")
    else:
        print("No jargon documents found.")
    
    # ============================================================================
    # HYPOTHESIS 4: Context-Dependent Modifiers
    # ============================================================================
    
    print("\nHYPOTHESIS 4: Context-Dependent Modifiers Handling")
    print("-" * 40)
    
    # Extract documents with modifiers
    intensifiers = ["very", "highly", "significantly", "extremely", "remarkably"]
    diminishers = ["slightly", "somewhat", "partially", "marginally", "barely"]
    
    modifier_docs = []
    modifier_ground_truth = []
    for i, doc in enumerate(documents):
        words = doc.lower().split()
        if any(term in words for term in intensifiers + diminishers):
            modifier_docs.append(doc)
            modifier_ground_truth.append(ground_truth[i])
    
    if len(modifier_docs) > 0:
        baseline_mod_scores = np.array([vader_baseline.analyze(doc) for doc in modifier_docs])
        hybrid_mod_scores = np.array([vader_hybrid.analyze(doc) for doc in modifier_docs])
        
        baseline_mod_mae = compute_mae(baseline_mod_scores, modifier_ground_truth)
        hybrid_mod_mae = compute_mae(hybrid_mod_scores, modifier_ground_truth)
        
        print(f"Baseline MAE on modifier docs: {baseline_mod_mae:.4f}")
        print(f"Hybrid MAE on modifier docs:   {hybrid_mod_mae:.4f}")
        print(f"Modifier MAE reduction: {compute_mae_reduction(baseline_mod_mae, hybrid_mod_mae):.2f}%")
        
        if compute_mae_reduction(baseline_mod_mae, hybrid_mod_mae) > 5:
            print("Result: ✅ SUPPORTED (modifier handling improved)")
        else:
            print("Result: ❌ NOT SUPPORTED (no significant improvement)")
    else:
        print("No modifier documents found.")
    
    # ============================================================================
    # HYPOTHESIS 5: Overall Performance Improvement
    # ============================================================================
    
    print("\nHYPOTHESIS 5: Overall Performance Improvement")
    print("-" * 40)
    
    # Compute accuracy (correct sign prediction)
    baseline_correct = np.sum(np.sign(baseline_scores) == np.sign(ground_truth))
    hybrid_correct = np.sum(np.sign(hybrid_scores) == np.sign(ground_truth))
    
    baseline_acc = baseline_correct / len(documents) * 100
    hybrid_acc = hybrid_correct / len(documents) * 100
    
    print(f"Baseline accuracy: {baseline_acc:.2f}%")
    print(f"Hybrid accuracy:   {hybrid_acc:.2f}%")
    print(f"Accuracy improvement: {hybrid_acc - baseline_acc:.2f}%")
    
    if hybrid_acc > baseline_acc:
        print("Result: ✅ SUPPORTED (overall accuracy improved)")
    else:
        print("Result: ❌ NOT SUPPORTED")
    
    # ============================================================================
    # VISUALIZATION
    # ============================================================================
    
    print("\n[Generating visualization...]")
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: MAE comparison
    mae_labels = ['Baseline', 'Hybrid']
    mae_values = [baseline_mae, hybrid_mae]
    colors = ['#ff9999', '#66b3ff']
    
    axes[0].bar(mae_labels, mae_values, color=colors, edgecolor='black')
    axes[0].set_ylabel('Mean Absolute Error (MAE)', fontsize=12)
    axes[0].set_title('MAE Comparison: Baseline vs Hybrid VADER', fontsize=14)
    axes[0].set_ylim(0, max(mae_values) * 1.2)
    
    # Add value labels on bars
    for i, v in enumerate(mae_values):
        axes[0].text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom', fontsize=12)
    
    # Plot 2: Accuracy comparison
    acc_labels = ['Baseline', 'Hybrid']
    acc_values = [baseline_acc, hybrid_acc]
    
    axes[1].bar(acc_labels, acc_values, color=colors, edgecolor='black')
    axes[1].set_ylabel('Accuracy (%)', fontsize=12)
    axes[1].set_title('Sentiment Classification Accuracy', fontsize=14)
    axes[1].set_ylim(0, 100)
    
    # Add value labels on bars
    for i, v in enumerate(acc_values):
        axes[1].text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('sentiment_analysis_results.png', dpi=150, bbox_inches='tight')
    print("    Visualization saved to 'sentiment_analysis_results.png'")
    
    # ============================================================================
    # CONCLUSIONS
    # ============================================================================
    
    print("\n" + "="*70)
    print("CONCLUSIONS")
    print("="*70)
    
    print(f"\n1. Hypothesis 1 (MAE Reduction ≥ 10%): {'✅ SUPPORTED' if mae_reduction_pct >= 10 else '❌ NOT SUPPORTED'}")
    print(f"   - Observed MAE reduction: {mae_reduction_pct:.2f}%")
    print(f"   - Statistical significance: {'p < 0.05' if p_value < 0.05 else 'p ≥ 0.05'}")
    
    print(f"\n2. Hypothesis 2 (Negation Handling): {'✅ SUPPORTED' if 'negation' in locals() and compute_mae_reduction(baseline_neg_mae, hybrid_neg_mae) > 0 else '❌ NOT SUPPORTED'}")
    print(f"   - Negation-specific MAE reduction: {'N/A' if 'negation' not in locals() else f'{compute_mae_reduction(baseline_neg_mae, hybrid_neg_mae):.2f}%'}")
    
    print(f"\n3. Hypothesis 3 (Domain Jargon): {'✅ SUPPORTED' if 'jargon' in locals() and compute_mae_reduction(baseline_jargon_mae, hybrid_jargon_mae) > 10 else '⚠️ PARTIALLY SUPPORTED' if 'jargon' in locals() and compute_mae_reduction(baseline_jargon_mae, hybrid_jargon_mae) > 0 else '❌ NOT SUPPORTED'}")
    print(f"   - Jargon MAE reduction: {'N/A' if 'jargon' not in locals() else f'{compute_mae_reduction(baseline_jargon_mae, hybrid_jargon_mae):.2f}%'}")
    
    print(f"\n4. Hypothesis 4 (Context Modifiers): {'✅ SUPPORTED' if 'modifier' in locals() and compute_mae_reduction(baseline_mod_mae, hybrid_mod_mae) > 5 else '❌ NOT SUPPORTED'}")
    print(f"   - Modifier MAE reduction: {'N/A' if 'modifier' not in locals() else f'{compute_mae_reduction(baseline_mod_mae, hybrid_mod_mae):.2f}%'}")
    
    print(f"\n5. Hypothesis 5 (Overall Accuracy): {'✅ SUPPORTED' if hybrid_acc > baseline_acc else '❌ NOT SUPPORTED'}")
    print(f"   - Accuracy improvement: {hybrid_acc - baseline_acc:.2f}%")
    
    print("\nSUMMARY:")
    print("--------")
    total_hypotheses = 5
    supported = sum([
        mae_reduction_pct >= 10,
        'negation' in locals() and compute_mae_reduction(baseline_neg_mae, hybrid_neg_mae) > 0,
        'jargon' in locals() and compute_mae_reduction(baseline_jargon_mae, hybrid_jargon_mae) > 10,
        'modifier' in locals() and compute_mae_reduction(baseline_mod_mae, hybrid_mod_mae) > 5,
        hybrid_acc > baseline_acc
    ])
    
    print(f"Overall: {supported}/{total_hypotheses} hypotheses supported.")
    
    if supported >= 4:
        print("\n✅ The hybrid VADER + domain lexicon approach shows strong promise")
        print("   for improving sentiment analysis in technical domains.")
    elif supported >= 2:
        print("\n⚠️ Mixed results suggest context-dependent effectiveness.")
        print("   Further refinement of the domain lexicon is recommended.")
    else:
        print("\n❌ The hybrid approach did not significantly improve performance.")
        print("   Consider re-evaluating the domain lexicon construction strategy.")
    
    print("\n" + "="*70)
    print("END OF EXPERIMENT")
    print("="*70)

if __name__ == "__main__":
    main()