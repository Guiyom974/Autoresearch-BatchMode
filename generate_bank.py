import os

PROBLEMS = [
    # 1. Number Theory
    ("Number Theory", "Twin Primes", "Investigate the density of twin primes (p, p+2) up to 10^9 and compare with the Hardy-Littlewood conjecture."),
    ("Number Theory", "Cousin Primes", "Analyze the distribution of cousin primes (p, p+4) across different modular residues to detect hidden asymmetries."),
    ("Number Theory", "Sexy Primes", "Examine the frequency and clustering of sexy primes (p, p+6) in large primorial bases."),
    ("Number Theory", "Palindromic Primes", "Investigate the leading and trailing digit distributions of palindromic primes in Base-10 and Base-2."),
    ("Number Theory", "Sophie Germain Primes", "Test the success of Sophie Germain primes in predicting safe prime gaps in cryptographic applications."),
    ("Number Theory", "Mersenne Primes", "Analyze the bit-structure of known Mersenne exponents for non-obvious binary patterns."),
    ("Number Theory", "Perfect Numbers", "Explore the relationship between digit sums of perfect numbers and their factors."),
    ("Number Theory", "Collatz Conjecture", "Analyze the 'flight length' of Collatz sequences for integers up to 10^7 to find periodicity in sequence peaks."),
    ("Number Theory", "Fibonacci Sequence", "Test Benford's Law on the first 10000 Fibonacci numbers across different prime bases."),
    ("Number Theory", "Goldbach Conjecture", "Test the 'Goldbach Comet' density for even numbers up to 10^8 and fit a power-law distribution."),

    # 2. Statistics & Paradoxes
    ("Statistics", "Simpson's Paradox", "Simulate a multi-variable dataset where the aggregate trend reverses in all sub-groups; detect the threshold of 'hidden variable' impact."),
    ("Statistics", "Birthday Paradox", "Generalize the Birthday Paradox to non-uniform birth distributions and measure the deviation from the classic formula."),
    ("Statistics", "Benford's Law", "Analyze the leading digits of the first 10^6 factorials and identify where the law fails due to truncation."),
    ("Statistics", "Monty Hall", "Extend the Monty Hall problem to N doors and K goats, simulating the optimal strategy under 'partial disclosure' rules."),
    ("Statistics", "Central Limit Theorem", "Detect the sample size N required for heavily skewed distributions (e.g., Pareto) to satisfy normality tests within 1% error."),
    ("Statistics", "Law of Large Numbers", "Measure the 'convergence speed' of the average for different probability distributions (Cauchy vs Gaussian)."),
    ("Statistics", "Bayesian Inference", "Test the sensitivity of posterior probability to increasingly 'wrong' priors in a biased coin experiment."),
    ("Statistics", "Null Hypothesis Testing", "Simulate a 'P-hacking' environment to measure how many false positives are generated across 10,000 random correlation tests."),
    ("Statistics", "Regression to Mean", "Test the 'Sophomore Slump' effect in simulated sports data using multi-linear regression."),
    ("Statistics", "Information Entropy", "Measure the Shannon entropy of various human-generated vs computer-generated random sequences."),

    # 3. Financial & Economic Modeling
    ("Financial", "Geometric Brownian Motion", "Test the accuracy of GBM in predicting price paths for high-volatility assets vs stable assets."),
    ("Financial", "Black-Scholes Model", "Measure the sensitivity of the 'Greeks' (Delta/Gamma) under non-normal (fat-tailed) volatility distributions."),
    ("Financial", "Efficient Market Hypothesis", "Test various technical analysis indicators (RSI/MACD) on 10^5 random walk price paths to find false positive signals."),
    ("Financial", "Fractal Market Hypothesis", "Measure the Hurst exponent of various global indices over 50 years to detect long-memory correlations."),
    ("Financial", "Volatility Clustering", "Simulate GARCH(1,1) processes and compare their volatility clustering with actual historical crypto data."),
    ("Financial", "Arbitrage Detection", "Simulate a multi-exchange triangular arbitrage environment and detect the 'decay rate' of profit opportunities."),
    ("Financial", "Portfolio Optimization", "Test the Sharpe ratio of a 'Markowitz' optimized portfolio against a simple 'naive' 1/N allocation under stress."),
    ("Financial", "Market Microstructure", "Analyze the distribution of bid-ask spreads in simulated high-frequency environments with 'iceberg' orders."),
    ("Financial", "Economic Bubbles", "Model the 'herding' behavior in asset prices using a self-exciting point process (Hawkes process)."),
    ("Financial", "Inflation Patterns", "Analyze the correlation between commodity price peaks and currency devaluation using multi-lag analysis."),

    # 4. Network Theory & Connectivity
    ("Network Theory", "Small World Networks", "Measure the average path length and clustering coefficient as a function of the 're-wiring' probability p in a Watts-Strogatz model."),
    ("Network Theory", "Scale-Free Networks", "Test the robustness of Barabasi-Albert networks against random node failure vs targeted 'hub' attacks."),
    ("Network Theory", "Social Contagion", "Model the spread of information on a network using the 'Simple' vs 'Complex' contagion threshold rules."),
    ("Network Theory", "PageRank Algorithm", "Analyze how the PageRank of nodes changes in a 'dynamic' network where nodes are added and removed daily."),
    ("Network Theory", "Community Detection", "Compare the modularity of Louvain vs Girvan-Newman algorithms on large synthetic datasets."),
    ("Network Theory", "Network Resilience", "Measure the critical threshold of connectivity where a random graph transitions from many components to a Giant Component."),
    ("Network Theory", "Traffic Congestion", "Model Braess's Paradox: show how adding a road to a network can increase total travel time."),
    ("Network Theory", "Neural Connectivity", "Simulate a simple recurrent neural network and measure how 'synaptic' pruning affects signal transmission efficiency."),
    ("Network Theory", "Supply Chain Robustness", "Model the 'Bullwhip Effect' in a multi-tier supply chain network and detect propagation delays."),
    ("Network Theory", "Degree Correlations", "Analyze assortativity (rich-club effect) in networks and its impact on the epidemic threshold."),

    # 5. Physics, Chaos & Dynamical Systems
    ("Physics", "Lorenz Attractor", "Measure the 'Butterfly Effect': how quickly do two starting points diverge as a function of the initial epsilon delta?"),
    ("Physics", "Double Pendulum", "Analyze the transitions from periodic to chaotic motion by mapping the Lyapunov exponent across the energy phase space."),
    ("Physics", "Fluid Dynamics", "Simulate a simple Navier-Stokes environment (Lattice Boltzmann) and detect the transition from laminar to turbulent flow."),
    ("Physics", "Orbital Mechanics", "Test the 'Kessler Syndrome' stability: simulate satellite collision cascades in Low Earth Orbit (LEO)."),
    ("Physics", "Schrodinger's Cat", "Simulated 'quantum' state collapse: model the effects of decoherence rate on the probability of 'state survival'."),
    ("Physics", "Diffusion-Limited Aggregation", "Analyze the fractal dimension of DLA clusters generated under various 'sticking' probability rules."),
    ("Physics", "Oscillator Synchronization", "Test the Kuramoto model: find the critical 'coupling strength' where N oscillators reach full phase sync."),
    ("Physics", "Entropy Increase", "Model N particles in a box and measure the time to reach maximum entropy starting from a localized cluster."),
    ("Physics", "Ising Model", "Simulate a 2D ferromagnetic Ising model and detect the 'Curie Temperature' where magnetization vanishes."),
    ("Physics", "Brownian Motion", "Model the 'Random Walk' of particles and calculate the diffusion coefficient for different environment temperatures."),

    # 6. Linguistics & Information Theory
    ("Linguistics", "Zipf's Law", "Analyze the word frequency distribution of 100 classic texts to detect deviations from the power-law exponent."),
    ("Linguistics", "Heaps' Law", "Measure the growth of vocabulary (V) as a function of total words (N) in large corpora and fit the Heaps exponent."),
    ("Linguistics", "Semantic Drift", "Compare the word-vector distances of 'neutral' words in literature from different centuries (e.g., 1800 vs 2000)."),
    ("Linguistics", "Sentiment Analysis", "Test the sensitivity of VADER vs custom keyword-summation for sentiment detection in technical language."),
    ("Linguistics", "Language Complexity", "Measure the average 'Readability' (Flesch-Kincaid) of medical abstracts vs pop-science articles over 50 years."),
    ("Linguistics", "Phonetic Similarity", "Measure the 'Levenshtein Distance' between common words in different Indo-European languages to map proximity."),
    ("Linguistics", "Grammatical Evolution", "Model the decay rate of irregular verbs in English over time using a simple reinforcement learning model."),
    ("Linguistics", "Text Compression", "Compare the LZW vs Huffman compression efficiency for various natural vs artificial languages."),
    ("Linguistics", "Named Entity Recognition", "Test the recall of simple REGEX-based entity detection vs pre-trained Spacy models for industrial terminology."),
    ("Linguistics", "Translation Entropy", "Measure the entropy 'loss' when a text is translated back and forth through multiple languages (e.g., En -> Fr -> Ge -> En)."),

    # 7. Optimization & Algorithms
    ("Optimization", "Genetic Algorithms", "Test the 'mutation rate' versus 'convergence speed' tradeoff for finding extremes in multimodal functions."),
    ("Optimization", "Traveling Salesman Problem", "Benchmark the Ant Colony Optimization (ACO) algorithm against Nearest Neighbor (NN) for N > 100 nodes."),
    ("Optimization", "Simulated Annealing", "Determine the optimal 'cooling schedule' (Linear vs Exponential) for solving a complex Scheduling Problem."),
    ("Optimization", "Knapsack Problem", "Compare the results of 'Greedy' approach vs 'Dynamic Programming' for large datasets with varying capacity ratios."),
    ("Optimization", "Particle Swarm Optimization", "Test the 'Global' vs 'Local' swarm topology for escaping local minima in the Rastrigin function."),
    ("Optimization", "Linear Programming", "Optimize a factory's multi-resource production schedule using the Simplex method and sensitivity analysis."),
    ("Optimization", "Pathfinding Efficiency", "Compare the 'A*' algorithm vs Dijkstra for pathfinding on a dynamic grid with moving obstacles."),
    ("Optimization", "Constraint Satisfaction", "Model the 'Sudoku Solver' as a backtracking problem and measure the time-complexity across puzzle difficulty levels."),
    ("Optimization", "Hash Function Collision", "Compare the collision rates of different hash functions (MD5 vs SHA-256 vs CRC32) for large string datasets."),
    ("Optimization", "Sorting Algorithm Performance", "Benchmark QuickSort vs MergeSort across 'nearly sorted' vs 'completely random' large datasets."),

    # 8. Ecology & Population Dynamics
    ("Ecology", "Lotka-Volterra Model", "Model Predator-Prey dynamics and identify the parameter range that causes 'extinction cascades' in the prey."),
    ("Ecology", "Island Biogeography", "Model the 'Species-Area' relationship: measure how species richness scales with the size and isolation of simulated ecological islands."),
    ("Ecology", "Carbon Cycle Modeling", "Model the 'feedback loops' between ocean carbon absorption and global temperature increases."),
    ("Ecology", "Forest Fire Spread", "Model the spread of fire on a grid using cellular automata and detect the 'percolation threshold' of tree density."),
    ("Ecology", "Genetic Drift", "Simulate the 'Founder Effect': how quickly do small isolated populations lose genetic diversity compared to larger ones?"),
    ("Ecology", "Invasive Species", "Model the spread of an invasive plant on a landscape and test the effectiveness of 'barrier' vs 'random' removal."),
    ("Ecology", "Resource Depletion", "Simulate the 'Tragedy of the Commons' in a fishery and find the 'maximum sustainable yield' before collapse."),
    ("Ecology", "Epidemic Spread", "Model the SIR model phases based on the 'Contact Rate' and find the threshold for 'herd immunity' coverage."),
    ("Ecology", "Pollination Networks", "Simulate the impact of 'specialist' vs 'generalist' pollinator extinction on overall flower diversity."),
    ("Ecology", "Climate Feedback", "Model the 'Albedo effect': how do melting polar ice caps accelerate global warming in a 1D energy balance model?"),

    # 9. Game Theory & Human Behavior
    ("Game Theory", "Prisoner's Dilemma", "Benchmark the 'Tit-for-Tat' strategy against 'Tit-for-Two-Tats' and 'Always Defect' in a 1000-round tournament."),
    ("Game Theory", "Nash Equilibrium", "Identify multiple equilibria in a 3-player non-zero-sum coordination game using iterative simulation."),
    ("Game Theory", "Public Goods Game", "Model the impact of 'social punishment' on the level of contribution in a community resource pool."),
    ("Game Theory", "Auction Theory", "Compare the final price and 'revenue' of First-Price vs Second-Price (Vickrey) auctions with 'Shill' bidders."),
    ("Game Theory", "Congestion Games", "Model traffic flow where each driver chooses the fastest path, finding the total social cost compared to a centrally planned optimum."),
    ("Game Theory", "Evolutionary Stable Strategy", "Simulate a population of 'Hawks' and 'Doves' and find the stable ratio under varying 'cost of injury' (C) parameters."),
    ("Game Theory", "Signaling Games", "Model the effectiveness of 'Costly Signaling' in a job market where candidates have hidden quality levels."),
    ("Game Theory", "Cooperative Games", "Calculate the Shapley value for a 5-player coalition game with varying player 'power' weights."),
    ("Game Theory", "Bargaining Models", "Model the Nash Bargaining Solution: find the split between two parties with different 'threat points' and patience levels."),
    ("Game Theory", "Zero-Sum Games", "Test the 'Minimax' strategy in an expanded Rock-Paper-Scissors-Lizard-Spock game with randomized strategies."),

    # 10. Systems & Queuing Theory
    ("Systems", "MM1 Queue Simulation", "Measure the relationship between 'utilization' (rho) and the average waiting time in a single-server system."),
    ("Systems", "Throughput Bottlenecks", "Model a multi-stage production line and detect how 'buffer' capacity in stage 2 affects overall system throughput."),
    ("Systems", "Parallel Processing", "Simulate Amdahl's Law: measure the speedup of a system as a function of the 'serial' vs 'parallel' proportion of code."),
    ("Systems", "Reliability Engineering", "Model a 'k-out-of-n' redundant system and calculate the overall MTBF (Mean Time Between Failures)."),
    ("Systems", "Inventory Management", "Simulate the Economic Order Quantity (EOQ) model under 'uncertain demand' and calculate the required 'safety stock' level."),
    ("Systems", "Priority Queues", "Compare the average wait time of 'First-Come-First-Serve' vs 'Shortest Job First' under heavy-tail job distributions."),
    ("Systems", "Network Latency", "Model the impact of 'packet loss' probability on the total file transfer time in a simulated TCP-like protocol."),
    ("Systems", "System Dynamics", "Model a simple 'Stock and Flow' system of a car dealership (Orders, Inventory, Sales) and detect oscillatory behaviors."),
    ("Systems", "Cybersecurity Resilience", "Simulate the 'DDoS' attack resilience of a load balancer for different request filtering strategies."),
    ("Systems", "Service Level Agreements", "Model the probability of 'SLA breach' for a cloud provider as a function of server 'uptime' and total customer load.")
]

TEMPLATE = """# Research Problem: {category} - {topic}

## Objective
{description}

## Research Questions
1. What is the fundamental statistical distribution of the observed phenomena?
2. To what extent does the phenomena deviate from the expected baseline (null hypothesis)?
3. Can the results be generalized across different scales of observation?

## Methodology
1. **Data Generation**: Implement a simulation or generate a synthetic dataset representing the {topic} environment.
2. **Feature Extraction**: Process the generated data to identify relevant metrics and patterns.
3. **Statistical Testing**: Apply appropriate tests (Chi-square, KL Divergence, P-values) to assess significance.
4. **Visualization**: Produce clear graphical representations of the findings.

## Success Criteria
- Identification of a statistically significant behavior or deviation ($p < 0.01$).
- The algorithm completes analysis of at least 10^5 data points within 2 minutes.
- Results are consistent across multiple independent runs.

## Constraints
- Python libraries only (numpy, scipy, matplotlib).
- No external data or API calls required for the core calculation.
- Memory usage must stay within standard limits.
"""

def main():
    bank_dir = "problem bank"
    if not os.path.exists(bank_dir):
        os.makedirs(bank_dir)

    for cat, topic, desc in PROBLEMS:
        filename = f"{cat} - {topic} - problem.md".replace("/", "-")
        filepath = os.path.join(bank_dir, filename)
        
        content = TEMPLATE.format(
            category=cat,
            topic=topic,
            description=desc
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
    print(f"Successfully generated {len(PROBLEMS)} problems in 'problem bank/'")

if __name__ == "__main__":
    main()
