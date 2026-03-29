!@#$
import numpy as np
import matplotlib.pyplot as plt
import sys
import time

# --- Configuration & Constants ---
MAX_X = 10**6
MODULO = 210
TARGET_A = 11  # Quadratic Non-Residue
TARGET_B = 1   # Principal Residue
CHECKPOINTS = [10**3, 10**4, 10**5, 10**6]

def run_prime_race_experiment():
    """
    Executes the optimized sieve and calculates statistics for the hypotheses.
    """
    print("--- Starting Algorithmic Optimization & Micro-Bound Validation ---\n")

    # --- Hypothesis 1: Algorithmic Efficiency (Performance Benchmark) ---
    print("[Hypothesis 1: Algorithmic Efficiency]")
    start_time = time.time()

    # Sieve of Eratosthenes using bytearray for memory efficiency
    # Initialize array with 1 (True) for all numbers up to MAX_X
    is_prime = bytearray(b'\x01') * (MAX_X + 1)
    is_prime[0:2] = b'\x00\x00'  # 0 and 1 are not prime

    # Optimization: Only check odd numbers for the sieve limit
    limit = int(MAX_X ** 0.5)
    for i in range(2, limit + 1):
        if is_prime[i]:
            # Start marking from i*i, step i
            # Using slice assignment for speed
            is_prime[i*i : MAX_X+1 : i] = b'\x00' * ((MAX_X - i*i)//i + 1)

    # Time taken for sieve generation
    sieve_time = time.time() - start_time
    print(f"  > Sieve Execution Time: {sieve_time:.4f} seconds")
    print(f"  > Status: {'PASS' if sieve_time < 30.0 else 'FAIL'} (Target < 30s)\n")

    # --- Hypothesis 2: Micro-Bound Dominance ---
    print("[Hypothesis 2: Micro-Bound Dominance]")
    
    count_A = 0
    count_B = 0
    
    log_density_A = 0.0
    log_density_B = 0.0
    
    history_x = []
    history_diff = []
    
    for x in range(2, MAX_X + 1):
        if is_prime[x]:
            rem = x % MODULO
            if rem == TARGET_A:
                count_A += 1
                log_density_A += 1.0 / x
            elif rem == TARGET_B:
                count_B += 1
                log_density_B += 1.0 / x
                
        if x in CHECKPOINTS:
            print(f"  > Checkpoint x={x}: Pi(x, {MODULO}, {TARGET_A}) = {count_A}, Pi(x, {MODULO}, {TARGET_B}) = {count_B}")
            print(f"    Log Density {TARGET_A}: {log_density_A:.6f}, Log Density {TARGET_B}: {log_density_B:.6f}")
            
        if x % 1000 == 0:
            history_x.append(x)
            history_diff.append(count_A - count_B)
            
    plt.figure(figsize=(10, 6))
    plt.plot(history_x, history_diff, label=f'Count Diff (a={TARGET_A} - a={TARGET_B})')
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel('x')
    plt.ylabel('Difference')
    plt.title(f'Prime Race Modulo {MODULO}: {TARGET_A} vs {TARGET_