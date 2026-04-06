# Research Problem: Systems - Priority Queues

## Objective
Compare the average wait time of 'First-Come-First-Serve' vs 'Shortest Job First' under heavy-tail job distributions.

## Research Questions
1. What is the fundamental statistical distribution of the observed phenomena?
2. To what extent does the phenomena deviate from the expected baseline (null hypothesis)?
3. Can the results be generalized across different scales of observation?

## Methodology
1. **Data Generation**: Implement a simulation or generate a synthetic dataset representing the Priority Queues environment.
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
