import os

output_dir = r"d:\LocalProjects\Python apps\AutoResearch\math problems"
os.makedirs(output_dir, exist_ok=True)

problems = [
    ("Prime Numbers", "Goldbach's Conjecture", "Investigate the distribution of representations of even numbers as the sum of two primes up to 10^7."),
    ("Prime Numbers", "Twin Primes", "Investigate the density of twin primes (p, p+2) up to 10^7 and compare with the Hardy-Littlewood conjecture."),
    ("Prime Numbers", "Cousin Primes", "Investigate the density of cousin primes (p, p+4) up to 10^7 and analyze the distribution compared to twin primes."),
    ("Prime Numbers", "Sexy Primes", "Investigate the density of sexy primes (p, p+6) up to 10^7 and analyze their occurrence frequency."),
    ("Prime Numbers", "Sophie Germain Primes", "Investigate the density of Sophie Germain primes (p, 2p+1) up to 10^7 and estimate their asymptotic growth."),
    ("Prime Numbers", "Safe Primes", "Investigate the density of Safe primes (2p+1) up to 10^7 and estimate their asymptotic growth."),
    ("Prime Numbers", "Mersenne Primes", "Investigate the deterministic distribution and divisibility properties of Mersenne numbers (2^p - 1) up to p=10^4."),
    ("Prime Numbers", "Fermat Primes", "Investigate the deterministic distribution and divisibility properties of generalized Fermat numbers up to n=10^4."),
    ("Prime Numbers", "Pierpont Primes", "Investigate the density and distribution of Pierpont primes (2^u * 3^v + 1) up to 10^7."),
    ("Prime Numbers", "Wagstaff Primes", "Investigate the density and distribution of Wagstaff primes ((2^p + 1)/3) up to p=10^4."),
    ("Prime Numbers", "Cullen Primes", "Investigate the density of Cullen primes (n*2^n + 1) for n up to 10^4."),
    ("Prime Numbers", "Woodall Primes", "Investigate the density of Woodall primes (n*2^n - 1) for n up to 10^4."),
    ("Prime Numbers", "Carol Primes", "Investigate the density of Carol primes ((2^n - 1)^2 - 2) for n up to 10^4."),
    ("Prime Numbers", "Kynea Primes", "Investigate the density of Kynea primes ((2^n + 1)^2 - 2) for n up to 10^4."),
    ("Prime Numbers", "Wieferich Primes", "Investigate the occurrence and modular properties related to Wieferich condition (p^2 divides 2^(p-1) - 1) up to 10^6."),
    ("Prime Numbers", "Wilson Primes", "Investigate the occurrence and modular properties related to Wilson condition (p^2 divides (p-1)! + 1) up to 10^5."),
    ("Prime Numbers", "Wall-Sun-Sun Primes", "Investigate the modular properties of the Fibonacci sequence related to Wall-Sun-Sun primes up to 10^6."),
    ("Prime Numbers", "Wolstenholme Primes", "Investigate the modular properties of harmonic numbers up to 10^5."),
    ("Prime Numbers", "Proth Primes", "Investigate the density of Proth primes (k*2^n + 1) for fixed k and varying n."),
    ("Prime Numbers", "Palindromic Primes", "Investigate the density and base-dependent properties of Palindromic primes up to 10^7 in different bases."),
    ("Prime Numbers", "Repunit Primes", "Investigate the properties and pseudo-primality of Repunits (111...1) up to 10^4 digits."),
    ("Prime Numbers", "Prime Gaps", "Investigate the statistical distribution of gaps between consecutive prime numbers up to 10^7."),
    ("Prime Numbers", "Legendre's Conjecture", "Investigate the number of primes situated between n^2 and (n+1)^2 for n up to 10^4."),
    ("Prime Numbers", "Brocard's Conjecture", "Investigate the number of primes situated between (p_n)^2 and (p_{n+1})^2 for initial sequence of primes."),
    ("Prime Numbers", "Andrica's Conjecture", "Investigate the maximum value of sqrt(p_{n+1}) - sqrt(p_n) up to p_n = 10^7."),

    ("Number Theory", "Collatz Conjecture", "Investigate the statistical distribution of stopping times for the Collatz (3n+1) sequence up to 10^6."),
    ("Number Theory", "Perfect Numbers", "Investigate the properties of the sum of proper divisors and abundance index for integers up to 10^6."),
    ("Number Theory", "Amicable Numbers", "Investigate the distribution and pair distances of amicable numbers up to 10^6."),
    ("Number Theory", "Sociable Numbers", "Investigate the detection and length of aliquot cycles for integers up to 10^5."),
    ("Number Theory", "Abundant Numbers", "Investigate the fractional density of abundant numbers in intervals up to 10^6."),
    ("Number Theory", "Deficient Numbers", "Investigate the fractional density of deficient numbers in intervals up to 10^6."),
    ("Number Theory", "Weird Numbers", "Investigate the scarcity and distribution of weird numbers (abundant but not semiperfect) up to 10^5."),
    ("Number Theory", "Lychrel Numbers", "Investigate the iterative palindrome generation process and non-terminating candidates (196 problem) up to 10^5."),
    ("Number Theory", "Happy Numbers", "Investigate the density and clustering of Happy Numbers (sum of squared digits reaching 1) up to 10^6."),
    ("Number Theory", "Narcissistic Numbers", "Investigate the search space and distribution of Armstrong numbers across different bases."),
    ("Number Theory", "Harshad Numbers", "Investigate the density of Harshad numbers (divisible by sum of digits) in base 10 up to 10^6."),
    ("Number Theory", "Ulam Numbers", "Investigate the asymptotic density of Ulam numbers up to 10^6."),
    ("Number Theory", "Carmichael Numbers", "Investigate the frequency of Carmichael numbers relative to prime numbers up to 10^6."),
    ("Number Theory", "Zeisel Numbers", "Investigate the generative properties and distribution of Zeisel numbers."),
    ("Number Theory", "Poulet Numbers", "Investigate the occurrence of Fermat pseudoprimes to base 2 up to 10^6."),
    ("Number Theory", "Hardy-Ramanujan Numbers", "Investigate algorithms to find Taxi-cab numbers (sum of two cubes in n ways)."),
    ("Number Theory", "Kaprekar Constants", "Investigate the convergence network of Kaprekar's routine for 3, 4, 5, and 6-digit numbers."),
    ("Number Theory", "Kaprekar Numbers", "Investigate the density of Kaprekar numbers up to 10^6."),
    ("Number Theory", "Untouchable Numbers", "Investigate numbers that cannot be expressed as the sum of proper divisors of any integer up to 10^5."),
    ("Number Theory", "Practical Numbers", "Investigate the distribution of practical numbers up to 10^6 and compare to prime numbers."),
    ("Number Theory", "Erdős-Woods Numbers", "Investigate the occurrence and gap lengths associated with Erdős-Woods numbers up to 10^5."),
    ("Number Theory", "Catalan Numbers", "Investigate the modular distribution properties (parity and congruences) of Catalan numbers."),
    ("Number Theory", "Bell Numbers", "Investigate the prime modulus properties (Touchard's congruence) of Bell numbers."),
    ("Number Theory", "Motzkin Numbers", "Investigate the modular and asymptotic properties of Motzkin numbers."),
    ("Number Theory", "Fibonacci Sequence", "Investigate the distribution of Pisano periods for primes up to 10^5."),

    ("Constants", "Pi Digits - Frequency", "Investigate the uniformity (Normality) of digits 0-9 in the first 10^6 digits of Pi."),
    ("Constants", "Pi Digits - Consecutive", "Investigate the statistical distribution of consecutive identical digits in the first 10^6 digits of Pi."),
    ("Constants", "Pi Digits - Pairs", "Investigate the frequency of digit pairs (00 to 99) in the first 10^6 digits of Pi."),
    ("Constants", "Pi Digits - Triplets", "Investigate the frequency of digit triplets (000 to 999) in the first 10^6 digits of Pi."),
    ("Constants", "Pi Digits - Random Walk", "Investigate the 2D random walk generated by assigning directions to Pi digits (0-3 mod 4) for 10^5 steps."),
    ("Constants", "Pi Digits - Spectral", "Investigate the Fourier/spectral properties of the digit sequence of Pi to detect any hidden periodicities."),
    ("Constants", "Pi Digits - Benford", "Investigate the applicability of Benford's Law on sequences derived from subsets of Pi's digits."),
    ("Constants", "Pi Digits - Gap Distances", "Investigate the gap distances between occurrences of identical digits in Pi's expansion."),
    ("Constants", "Pi Digits - String Matching", "Investigate the probabilities and occurrences of arbitrary short strings in the first 10^6 digits of Pi."),
    ("Constants", "Pi Digits - Entropy", "Investigate the Shannon entropy measurements of sliding windows over Pi's digits to evaluate randomness."),
    ("Constants", "e Digits - Frequency", "Investigate the uniformity of digits 0-9 in the first 10^6 digits of Euler's number e."),
    ("Constants", "e Digits - Consecutive", "Investigate the statistical distribution of consecutive identical digits in the first 10^6 digits of e."),
    ("Constants", "e Digits - Random Walk", "Investigate the 2D random walk generated by the digits of e mapped to Cartesian directions."),
    ("Constants", "Golden Ratio - Digits", "Investigate the digit distribution (Normality tests) in the first 10^6 digits of Phi."),
    ("Constants", "Sqrt(2) - Digits", "Investigate the digit frequency and randomness tests on the first 10^6 digits of the Square Root of 2."),
    ("Constants", "Sqrt(3) - Digits", "Investigate the digit frequency and randomness tests on the first 10^6 digits of the Square Root of 3."),
    ("Constants", "Euler-Mascheroni Constant", "Investigate the statistical randomness properties of the digits of the Euler-Mascheroni constant."),
    ("Constants", "Apery's Constant", "Investigate the statistical randomness properties of the digits of Apery's constant."),
    ("Constants", "Champernowne Constant", "Investigate the structural anomalies and predictable patterns in the string of Champernowne's constant."),
    ("Constants", "Copeland-Erdős Constant", "Investigate the statistical properties of the Copeland-Erdős constant generated from prime numbers."),
    ("Constants", "Khinchin's Constant", "Investigate the digit distribution and mathematical properties related to Khinchin's constant."),
    ("Constants", "Chaitin's Constant", "Investigate statistical properties of algorithmic approximations representing Chaitin's constant Omega."),
    ("Constants", "Pi - Continued Fractions", "Investigate the statistical distribution of elements in the continued fraction expansion of Pi."),
    ("Constants", "e - Continued Fractions", "Investigate the deterministic patterns (and their bounds) in the continued fraction expansion of e."),
    ("Constants", "Golden Ratio - Continued Fractions", "Investigate the simple repetitive continued fraction elements of Phi and compute bounding approximations."),

    ("Fractals", "Mandelbrot Set - Boundary", "Investigate the box-counting dimension and roughness of the Mandelbrot set boundary."),
    ("Fractals", "Menger Sponge - Volume", "Investigate the volume and surface area scaling ratios of a Menger sponge construction up to 10 iterations."),
    ("Fractals", "Julia Sets - Basins", "Investigate the distribution of basin of attraction sizes for varying parameters c in Julia sets."),
    ("Fractals", "Burning Ship Fractal", "Investigate the geometric properties and local fractal dimensions within the Burning Ship fractal."),
    ("Fractals", "Logistic Map - Bifurcations", "Investigate the distribution and spacing of bifurcation points in the chaotic regime of the logistic map."),
    ("Fractals", "Logistic Map - Feigenbaum", "Investigate the empirical numerical estimation of the Feigenbaum constant from logistic map bifurcations."),
    ("Fractals", "Lorenz Attractor - Dimension", "Investigate the correlation dimension characterizing the Lorenz strange attractor."),
    ("Fractals", "Rössler Attractor - Lyapunov", "Investigate the stability of the largest Lyapunov exponent across parameter spaces of the Rössler attractor."),
    ("Fractals", "Barnsley Fern - IFS Density", "Investigate the spatial probability density distribution generated by the Barnsley fern Iterated Function System."),
    ("Fractals", "Sierpinski Triangle - Cellular Automata", "Investigate the statistical equivalence and entropy matching between Rule 90 cellular automata and the Sierpinski Triangle."),
    ("Fractals", "Sierpinski Carpet - Random Walk", "Investigate the escape time and diffusion metrics for a random walk constrained within a Sierpinski Carpet lattice."),
    ("Fractals", "Koch Snowflake - Perimeter", "Investigate the perimeter length vs resolution scaling behavior representing the Koch curve dimension."),
    ("Fractals", "Cantor Set - Measure Zero", "Investigate numerical approximations of Lebesgue measure approaching zero for standard and generalized Cantor sets."),
    ("Fractals", "Hénon Map - Strange Attractor", "Investigate the structural properties (correlation dimension) of the Hénon map strange attractor."),
    ("Fractals", "Mandelbrot - Area Estimation", "Investigate the convergence rate of Monte Carlo methods used for estimating the area of the Mandelbrot set."),
    ("Fractals", "Ikeda Map - Trajectories", "Investigate the fractal dimension and chaos boundaries of trajectory clouds in the Ikeda map."),
    ("Fractals", "Standard Map - Chaos Onset", "Investigate the critical parameter K marking the breakdown of the last KAM torus in the Chirikov standard map."),
    ("Fractals", "Tent Map - Iteration", "Investigate the invariant density and deterministic diffusion properties within the chaotic regime of the Tent map."),
    ("Fractals", "Arnold's Cat Map - Mixing", "Investigate the mixing times and recurrence periodicity of Arnold's Cat Map on discrete uniform grids."),
    ("Fractals", "Enigma Fractal", "Investigate the pseudo-random walk boundaries equivalent to fractal patterns within cryptographic permutations like the Enigma."),
    ("Fractals", "Tinkerbell Map", "Investigate the bounding parameters defining the attractor region vs escaping orbits in the Tinkerbell map."),
    ("Fractals", "Clifford Attractor", "Investigate the point density distribution and parameter sensitivity within the Clifford chaotic attractor."),
    ("Fractals", "Peter de Jong Attractor", "Investigate the structural symmetry variations and correlation dimensions in Peter de Jong attractors."),
    ("Fractals", "Hofstadter's Butterfly", "Investigate the energy spectrum gaps structured as a fractal pattern in Hofstadter's Butterfly model."),
    ("Fractals", "Collatz Fractal", "Investigate the complex-plane continuous extension convergence boundaries creating the Collatz fractal.")
]

template = """# Research Problem: {category} - {topic}

## Objective
{objective}

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

for category, topic, obj in problems:
    # safe filename
    filename = f"{category} - {topic} - problem.md".replace(":", " ").replace("/", " ").replace("\\", " ")
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(template.format(category=category, topic=topic, objective=obj))

print(f"Generated {len(problems)} markdown files.")
