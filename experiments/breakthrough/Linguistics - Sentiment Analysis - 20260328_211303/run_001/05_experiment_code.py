import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from collections import defaultdict
import re

# ============================================================================
# SECTION 1: Synthetic Data Generation
# ============================================================================

def generate_synthetic_technical_documents(n_docs=200, seed=42):
    """
    Generate synthetic technical documents with controlled sentiment.
    Returns: list of (text, true_sentiment) where true_sentiment ∈ [-1, -0.5, 0, 0.5, 1]
    """
    np.random.seed(seed)
    
    # Technical vocabulary categories
    positive_terms = {
        'software': ['efficient', 'optimized', 'robust', 'scalable', 'reliable', 'well-documented', 'high-performing', 'seamless', 'intuitive', 'streamlined'],
        'hardware': ['high-speed', 'low-latency', 'high-capacity', 'energy-efficient', 'fault-tolerant', 'stable', 'precise', 'durable'],
        'math': ['exact', 'closed-form', 'convergent', 'stable', 'well-conditioned', 'optimal', 'efficient', 'accurate']
    }
    negative_terms = {
        'software': ['buggy', 'inefficient', 'unreliable', 'memory-leaking', 'crash-prone', 'poorly-documented', 'fragile', 'complex', 'convoluted'],
        'hardware': ['slow', 'unstable', 'overheating', 'power-hungry', 'fragile', 'inaccurate', 'unreliable'],
        'math': ['ill-conditioned', 'divergent', 'inaccurate', 'inefficient', 'approximate', 'numerically-unstable']
    }
    neutral_terms = {
        'software': ['function', 'variable', 'parameter', 'class', 'method', 'module', 'import', 'return', 'loop', 'condition'],
        'hardware': ['circuit', 'component', 'signal', 'voltage', 'current', 'frequency', 'bandwidth', 'resolution'],
        'math': ['variable', 'constant', 'function', 'derivative', 'integral', 'matrix', 'vector', 'equation']
    }
    
    # Technical templates
    templates = [
        "The {category} {term} is {sentiment_word} and {adj}.",
        "In this {category}, {term} provides {sentiment_word} {adj} performance.",
        "Our {category} approach using {term} achieves {sentiment_word} {adj} results.",
        "{term} demonstrates {sentiment_word} {adj} characteristics in practice.",
        "The {category} {term} shows {sentiment_word} {adj} behavior."
    ]
    
    # Sentiment mappings
    sentiment_map = {
        1: ('positive', 'excellent', 'high'),
        0.5: ('positive', 'good', 'moderate'),
        0: ('neutral', 'acceptable', 'standard'),
        -0.5: ('negative', 'poor', 'suboptimal'),
        -1: ('negative', 'severe', 'critical')
    }
    
    documents = []
    for _ in range(n_docs):
        sentiment = np.random.choice([1, 0.5, 0, -0.5, -1], p=[0.15, 0.2, 0.2, 0.2, 0.25])
        cat = np.random.choice(['software', 'hardware', 'math'])
        
        if sentiment > 0:
            term = np.random.choice(positive_terms[cat])
            sent_word, adj1, adj2 = sentiment_map[sentiment]
            sentiment_word = 'positive' if sentiment > 0 else 'neutral' if sentiment == 0 else 'negative'
        elif sentiment < 0:
            term = np.random.choice(negative_terms[cat])
            sent_word, adj1, adj2 = sentiment_map[sentiment]
        else:
            term = np.random.choice(neutral_terms[cat])
            sent_word, adj1, adj2 = 'neutral', 'standard', 'typical'
        
        # Build document with variable length
        n_sentences = np.random.randint(1, 4)
        doc_parts = []
        for _ in range(n_sentences):
            template = np.random.choice(templates)
            doc_parts.append(template.format(
                category=cat,
                term=term,
                sentiment_word=sent_word,
                adj=adj1 if np.random.random() > 0.5 else adj2
            ))
        
        # Add some technical jargon to increase realism
        if np.random.random() > 0.5:
            doc_parts.append(f"This implementation uses {np.random.choice(['O(n log n)', 'O(n^2)', 'O(log n)', 'O(n)'])} complexity.")
        
        text = " ".join(doc_parts)
        documents.append((text, sentiment))
    
    return documents

# ============================================================================
# SECTION 2: VADER Sentiment Analysis (Simplified Implementation)
# ============================================================================

class SimpleVADER:
    """Simplified VADER-like sentiment analyzer for technical text"""
    
    def __init__(self):
        # Basic lexicon (simplified from original VADER)
        self.lexicon = {
            # Positive words
            'excellent': 3.2, 'good': 2.0, 'positive': 1.8, 'efficient': 2.5,
            'robust': 2.3, 'reliable': 2.1, 'scalable': 2.4, 'optimized': 2.6,
            'high-performing': 2.8, 'seamless': 2.2, 'intuitive': 2.0,
            'streamlined': 2.3, 'well-documented': 2.1, 'excellent': 3.2,
            'accurate': 2.4, 'optimal': 2.5, 'stable': 2.2, 'precise': 2.3,
            'durable': 2.1, 'energy-efficient': 2.7, 'fault-tolerant': 2.4,
            'high-speed': 2.6, 'low-latency': 2.5, 'high-capacity': 2.4,
            'closed-form': 2.3, 'convergent': 2.2, 'exact': 2.4,
            
            # Negative words
            'buggy': -3.0, 'inefficient': -2.7, 'unreliable': -2.8,
            'memory-leaking': -2.9, 'crash-prone': -3.1, 'poorly-documented': -2.6,
            'fragile': -2.5, 'complex': -1.8, 'convoluted': -2.2,
            'slow': -2.4, 'unstable': -2.9, 'overheating': -2.7,
            'power-hungry': -2.6, 'inaccurate': -2.5, 'approximate': -1.9,
            'numerically-unstable': -3.0, 'ill-conditioned': -2.8,
            'divergent': -2.3, 'inaccurate': -2.5, 'poor': -2.6,
            'severe': -2.4, 'critical': -2.7, 'suboptimal': -2.3,
            
            # Neutral words
            'function': 0.0, 'variable': 0.0, 'parameter': 0.0, 'class': 0.0,
            'method': 0.0, 'module': 0.0, 'import': 0.0, 'return': 0.0,
            'loop': 0.0, 'condition': 0.0, 'circuit': 0.0, 'component': 0.0,
            'signal': 0.0, 'voltage': 0.0, 'current': 0.0, 'frequency': 0.0,
            'bandwidth': 0.0, 'resolution': 0.0, 'derivative': 0.0,
            'integral': 0.0, 'matrix': 0.0, 'vector': 0.0, 'equation': 0.0,
            
            # Modifiers (simplified)
            'very': 1.5, 'highly': 1.5, 'extremely': 1.8, 'slightly': 0.7,
            'not': -1.0, 'very-not': -1.5
        }
    
    def polarity_scores(self, text):
        """Compute sentiment score for text"""
        words = re.findall(r'\b\w+(?:-\w+)*\b', text.lower())
        
        if not words:
            return {'compound': 0.0}
        
        scores = []
        for i, word in enumerate(words):
            # Check for compound words first
            compound = word
            if i > 0:
                prev = words[i-1]
                if prev in ['very', 'highly', 'extremely']:
                    compound = f"{prev}-{word}"
                elif prev == 'not':
                    compound = f"not-{word}"
            
            if compound in self.lexicon:
                scores.append(self.lexicon[compound])
            elif word in self.lexicon:
                scores.append(self.lexicon[word])
        
        if not scores:
            return {'compound': 0.0}
        
        # Normalize to [-1, 1] using sigmoid-like scaling
        avg_score = np.mean(scores)
        compound = np.tanh(avg_score / 2.0)  # Maps roughly [-4, 4] to [-1, 1]
        
        return {'compound': float(compound)}

# ============================================================================
# SECTION 3: Custom Keyword-Summation Sentiment Analyzer
# ============================================================================

class CustomKeywordSentiment:
    """Custom sentiment analyzer with technical vocabulary support"""
    
    def __init__(self):
        # Technical-specific lexicon with domain-weighted terms
        self.lexicon = {
            # Software-specific positive terms (higher weight)
            'efficient': 3.0, 'optimized': 3.2, 'robust': 2.8, 'scalable': 3.0,
            'reliable': 2.6, 'well-documented': 2.4, 'high-performing': 3.1,
            'seamless': 2.5, 'intuitive': 2.3, 'streamlined': 2.7,
            'accurate': 2.9, 'optimal': 3.0, 'stable': 2.7, 'precise': 2.8,
            
            # Hardware-specific positive terms
            'energy-efficient': 3.1, 'fault-tolerant': 2.9, 'high-speed': 3.0,
            'low-latency': 2.9, 'high-capacity': 2.8, 'durable': 2.6,
            
            # Math-specific positive terms
            'closed-form': 2.8, 'convergent': 2.7, 'exact': 3.0,
            
            # Software-specific negative terms (higher weight)
            'buggy': -3.2, 'inefficient': -3.0, 'unreliable': -3.1,
            'memory-leaking': -3.3, 'crash-prone': -3.4, 'poorly-documented': -2.9,
            'fragile': -2.8, 'complex': -2.2, 'convoluted': -2.6,
            
            # Hardware-specific negative terms
            'slow': -2.6, 'unstable': -3.2, 'overheating': -3.0,
            'power-hungry': -2.8, 'inaccurate': -2.7, 'approximate': -2.1,
            'numerically-unstable': -3.4,
            
            # Math-specific negative terms
            'ill-conditioned': -3.1, 'divergent': -2.8, 'inaccurate': -2.7,
            
            # Neutral terms (lower weight)
            'function': 0.1, 'variable': 0.1, 'parameter': 0.1, 'class': 0.1,
            'method': 0.1, 'module': 0.1, 'import': 0.1, 'return': 0.1,
            'loop': 0.1, 'condition': 0.1, 'circuit': 0.1, 'component': 0.1,
            'signal': 0.1, 'voltage': 0.1, 'current': 0.1, 'frequency': 0.1,
            'bandwidth': 0.1, 'resolution': 0.1, 'derivative': 0.1,
            'integral': 0.1, 'matrix': 0.1, 'vector': 0.1, 'equation': 0.1,
            
            # Modifiers
            'very': 1.3, 'highly': 1.3, 'extremely': 1.5, 'slightly': 0.8,
            'not': -1.0
        }
        
        # Domain weights for technical categories
        self.domain_weights = {
            'software': {'pos': 1.2, 'neg': 1.1},
            'hardware': {'pos': 1.1, 'neg': 1.2},
            'math': {'pos': 1.3, 'neg': 1.3}
        }
    
    def _detect_domain(self, text):
        """Detect technical domain from text content"""
        text_lower = text.lower()
        counts = {'software': 0, 'hardware': 0, 'math': 0}
        for word in ['function', 'variable', 'class', 'method', 'import', 'return', 'bug', 'code', 'algorithm', 'implementation']:
            if word in text_lower:
                counts['software'] += 1
        for word in ['circuit', 'component', 'signal', 'voltage', 'current', 'frequency', 'bandwidth', 'resolution']:
            if word in text_lower:
                counts['hardware'] += 1
        for word in ['derivative', 'integral', 'matrix', 'vector', 'equation', 'convergent', 'divergent']:
            if word in text_lower:
                counts['math'] += 1
        
        if not counts:
            return 'software'  # default
        
        return max(counts, key=counts.get)
    
    def polarity_scores(self, text):
        """Compute sentiment score with domain adaptation"""
        words = re.findall(r'\b\w+(?:-\w+)*\b', text.lower())
        domain = self._detect_domain(text)
        
        if not words:
            return {'compound': 0.0}
        
        scores = []
        for i, word in enumerate(words):
            compound = word
            if i > 0:
                prev = words[i-1]
                if prev in ['very', 'highly', 'extremely']:
                    compound = f"{prev}-{word}"
                elif prev == 'not':
                    compound = f"not-{word}"
            
            if compound in self.lexicon:
                scores.append(self.lexicon[compound])
            elif word in self.lexicon:
                scores.append(self.lexicon[word])
        
        if not scores:
            return {'compound': 0.0}
        
        # Apply domain-specific adjustment
        domain_adj = self.domain_weights[domain]
        pos_scores = [s for s in scores if s > 0]
        neg_scores = [s for s in scores if s < 0]
        
        if pos_scores:
            pos_sum = np.sum(pos_scores) * domain_adj['pos']
        else:
            pos_sum = 0.0
        if neg_scores:
            neg_sum = np.sum(neg_scores) * domain_adj['neg']
        else:
            neg_sum = 0.0
        
        # Combine and normalize
        combined = pos_sum + neg_sum
        compound = np.tanh(combined / 10.0)  # Scale for [-1, 1]
        
        return {'compound': float(compound)}

# ============================================================================
# SECTION 4: Evaluation Functions
# ============================================================================

def evaluate_sentiment_analyzer(analyzer, documents):
    """Evaluate sentiment analyzer against ground truth"""
    errors = []
    predictions = []
    
    for text, true_sentiment in documents:
        scores = analyzer.polarity_scores(text)
        pred = scores['compound']
        predictions.append(pred)
        errors.append(abs(pred - true_sentiment))
    
    # Calculate metrics
    mae = np.mean(errors)
    mse = np.mean([e**2 for e in errors])
    rmse = np.sqrt(mse)
    
    # Classification accuracy (using 0.25 threshold for 5-point scale)
    def classify(score):
        if score > 0.25:
            return 1
        elif score > 0.125:
            return 0.5
        elif score > -0.125:
            return 0
        elif score > -0.25:
            return -0.5
        else:
            return -1
    
    correct = sum(1 for pred, true in zip(predictions, [d[1] for d in documents]) 
                  if classify(pred) == true)
    accuracy = correct / len(documents)
    
    return {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'accuracy': accuracy,
        'predictions': predictions,
        'errors': errors
    }

def statistical_tests(vader_results, custom_results):
    """Perform statistical tests comparing two analyzers"""
    vader_errors = vader_results['errors']
    custom_errors = custom_results['errors']
    
    # Paired t-test (assuming normality)
    t_stat, p_value_t = stats.ttest_rel(vader_errors, custom_errors)
    
    # Wilcoxon signed-rank test (non-parametric)
    w_stat, p_value_w = stats.wilcoxon(vader_errors, custom_errors)
    
    # Effect size (Cohen's d for paired samples)
    diff = np.array(vader_errors) - np.array(custom_errors)
    mean_diff = np.mean(diff)
    std_diff = np.std(diff, ddof=1)
    cohens_d = mean_diff / std_diff if std_diff != 0 else 0
    
    return {
        't_stat': t_stat,
        'p_value_t': p_value_t,
        'w_stat': w_stat,
        'p_value_w': p_value_w,
        'cohens_d': cohens_d
    }

def distribution_analysis(vader_results, custom_results):
    """Analyze distribution properties of sentiment scores"""
    vader_errors = vader_results['errors']
    custom_errors = custom_results['errors']
    
    # Check for normality (Shapiro-Wilk test)
    _, p_vader_norm = stats.shapiro(vader_errors[:min(50, len(vader_errors))])
    _, p_custom_norm = stats.shapiro(custom_errors[:min(50, len(custom_errors))])
    
    # Calculate skewness and kurtosis
    vader_skew = stats.skew(vader_errors)
    custom_skew = stats.skew(custom_errors)
    vader_kurt = stats.kurtosis(vader_errors)
    custom_kurt = stats.kurtosis(custom_errors)
    
    return {
        'vader_shapiro_p': p_vader_norm,
        'custom_shapiro_p': p_custom_norm,
        'vader_skewness': vader_skew,
        'custom_skewness': custom_skew,
        'vader_kurtosis': vader_kurt,
        'custom_kurtosis': custom_kurt
    }

# ============================================================================
# SECTION 5: Visualization
# ============================================================================

def create_visualizations(vader_results, custom_results, output_prefix='sentiment_analysis'):
    """Create and save visualization plots"""
    
    # Plot 1: Error distributions
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Histogram of errors
    axes[0].hist(vader_results['errors'], bins=20, alpha=0.7, label='VADER', edgecolor='black')
    axes[0].hist(custom_results['errors'], bins=20, alpha=0.7, label='Custom Keyword', edgecolor='black')
    axes[0].set_xlabel('Absolute Error')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Error Distribution Comparison')
    axes[0].legend()
    
    # Q-Q plot for VADER
    stats.probplot(vader_results['errors'], dist="norm", plot=axes[1])
    axes[1].set_title('Q-Q Plot: VADER Errors')
    
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_error_dist.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Plot 2: True vs Predicted sentiment
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # VADER scatter
    true_vals = [d[1] for d in documents]
    axes[0].scatter(true_vals, vader_results['predictions'], alpha=0.6, label='VADER')
    axes[0].plot([-1, 1], [-1, 1], 'r--', label='Perfect')
    axes[0].set_xlabel('True Sentiment')
    axes[0].set_ylabel('Predicted Sentiment')
    axes[0].set_title('VADER: True vs Predicted')
    axes[0].legend()
    
    # Custom scatter
    axes[1].scatter(true_vals, custom_results['predictions'], alpha=0.6, color='orange', label='Custom')
    axes[1].plot([-1, 1], [-1, 1], 'r--', label='Perfect')
    axes[1].set_xlabel('True Sentiment')
    axes[1].set_ylabel('Predicted Sentiment')
    axes[1].set_title('Custom Keyword: True vs Predicted')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_scatter.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Plot 3: Box plot of error distributions
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.boxplot([vader_results['errors'], custom_results['errors']], 
               labels=['VADER', 'Custom Keyword'])
    ax.set_ylabel('Absolute Error')
    ax.set_title('Error Distribution Comparison (Box Plot)')
    ax.grid(True, alpha=0.3)
    plt.savefig(f'{output_prefix}_boxplot.png', dpi=150, bbox_inches='tight')
    plt.close()

# ============================================================================
# SECTION 6: Main Execution
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SENTIMENT ANALYSIS: VADER vs CUSTOM KEYWORD-SUMMATION")
    print("=" * 70)
    print()
    
    # Generate synthetic data
    print("Generating synthetic technical documents...")
    documents = generate_synthetic_technical_documents(n_docs=200, seed=42)
    print(f"Generated {len(documents)} documents")
    print()
    
    # Initialize analyzers
    print("Initializing analyzers...")
    vader = SimpleVADER()
    custom_analyzer = CustomKeywordSentiment()
    print("Analyzers initialized.")
    print()
    
    # Evaluate analyzers
    print("Evaluating VADER...")
    vader_results = evaluate_sentiment_analyzer(vader, documents)
    print(f"VADER MAE: {vader_results['mae']:.4f}")
    print(f"VADER RMSE: {vader_results['rmse']:.4f}")
    print(f"VADER Accuracy: {vader_results['accuracy']:.2%}")
    print()
    
    print("Evaluating Custom Keyword-Summation...")
    custom_results = evaluate_sentiment_analyzer(custom_analyzer, documents)
    print(f"Custom MAE: {custom_results['mae']:.4f}")
    print(f"Custom RMSE: {custom_results['rmse']:.4f}")
    print(f"Custom Accuracy: {custom_results['accuracy']:.2%}")
    print()
    
    # Statistical tests
    print("Running statistical tests...")
    stat_tests = statistical_tests(vader_results, custom_results)
    print(f"Paired t-test: t = {stat_tests['t_stat']:.4f}, p = {stat_tests['p_value_t']:.6f}")
    print(f"Wilcoxon signed-rank: W = {stat_tests['w_stat']:.4f}, p = {stat_tests['p_value_w']:.6f}")
    print(f"Cohen's d (effect size): {stat_tests['cohens_d']:.4f}")
    print()
    
    # Distribution analysis
    print("Analyzing error distributions...")
    dist_analysis = distribution_analysis(vader_results, custom_results)
    print(f"VADER normality (Shapiro p): {dist_analysis['vader_shapiro_p']:.4f}")
    print(f"Custom normality (Shapiro p): {dist_analysis['custom_shapiro_p']:.4f}")
    print(f"VADER skewness: {dist_analysis['vader_skewness']:.4f}")
    print(f"Custom skewness: {dist_analysis['custom_skewness']:.4f}")
    print()
    
    # Create visualizations
    print("Generating visualizations...")
    create_visualizations(vader_results, custom_results)
    print("Visualizations saved: sentiment_analysis_error_dist.png, sentiment_analysis_scatter.png, sentiment_analysis_boxplot.png")
    print()
    
    # Hypothesis testing summary
    print("=" * 70)
    print("HYPOTHESIS TESTING SUMMARY")
    print("=" * 70)
    print()
    
    # Hypothesis 1: VADER Underperforms Custom Keyword-Summation
    print("HYPOTHESIS 1: VADER Underperforms Custom Keyword-Summation on Technical Language")
    print("-" * 70)
    
    alpha = 0.05
    print(f"Significance level (α): {alpha}")
    print()
    
    # Check if custom has significantly lower error
    custom_mae = custom_results['mae']
    vader_mae = vader_results['mae']
    improvement_pct = (vader_mae - custom_mae) / vader_mae * 100
    
    print(f"VADER MAE: {vader_mae:.4f}")
    print(f"Custom MAE: {custom_mae:.4f}")
    print(f"Improvement: {improvement_pct:.2f}%")
    print()
    
    # Statistical significance
    if stat_tests['p_value_t'] < alpha and stat_tests['p_value_w'] < alpha:
        print("✓ Results are statistically significant (both tests)")
        print("✓ Reject null hypothesis: Custom keyword-summation significantly outperforms VADER")
    elif stat_tests['p_value_t'] < alpha or stat_tests['p_value_w'] < alpha:
        print("⚠ Results are significant in at least one test")
        if stat_tests['p_value_t'] < alpha:
            print("  - Paired t-test: significant")
        if stat_tests['p_value_w'] < alpha:
            print("  - Wilcoxon signed-rank: significant")
    else:
        print("✗ Results are not statistically significant")
        print("✗ Fail to reject null hypothesis: No significant difference between methods")
    
    # Effect size interpretation
    d = stat_tests['cohens_d']
    if abs(d) > 0.8:
        effect_size = "large"
    elif abs(d) > 0.5:
        effect_size = "medium"
    elif abs(d) > 0.2:
        effect_size = "small"
    else:
        effect_size = "negligible"
    
    print(f"Effect size (Cohen's d): {d:.4f} ({effect_size})")
    print()
    
    # Distribution analysis interpretation
    print("Distribution Analysis:")
    vader_norm = dist_analysis['vader_shapiro_p'] > 0.05
    custom_norm = dist_analysis['custom_shapiro_p'] > 0.05
    print(f"VADER errors normal: {vader_norm} (Shapiro p = {dist_analysis['vader_shapiro_p']:.4f})")
    print(f"Custom errors normal: {custom_norm} (Shapiro p = {dist_analysis['custom_shapiro_p']:.4f})")
    print()
    
    # Generalization consideration
    print("Generalizability Assessment:")
    n_docs = len(documents)
    n_categories = 3  # software, hardware, math
    print(f"Sample size: {n_docs} documents across {n_categories} technical domains")
    print("Cross-domain coverage suggests reasonable generalizability within technical contexts")
    print("Note: Synthetic data may not capture all real-world technical language variation")
    print()
    
    # Final conclusion
    print("=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    
    if stat_tests['p_value_t'] < alpha and stat_tests['p_value_w'] < alpha:
        print("✓ HYPOTHESIS 1 SUPPORTED: Custom keyword-summation significantly outperforms VADER")
        print("  on technical language sentiment analysis.")
        print()
        print("  Key findings:")
        print(f"  • MAE reduction: {improvement_pct:.2f}%")
        print(f"  • Statistical significance: p < {alpha} (both tests)")
        print(f"  • Effect size: {effect_size} (d = {d:.4f})")
        print()
        print("  Recommendation: Use domain-adapted sentiment analysis for technical documents")
        print("  where standard lexicons like VADER may misfit technical vocabulary.")
    else:
        print("✗ HYPOTHESIS 1 NOT SUPPORTED: No significant difference found")
        print("  between VADER and custom keyword-summation on technical language.")
    
    print()
    print("Limitations:")
    print("• Synthetic data may not fully capture real-world technical language")
    print("• Simplified VADER implementation may not reflect full original performance")
    print("• Limited to three technical domains (software, hardware, math)")
    print()
    print("=" * 70)