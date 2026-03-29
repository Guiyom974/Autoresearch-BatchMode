#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import csv
import shutil
import logging
import pathlib
import tempfile
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Logging configuration (simple console output)
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

# ----------------------------------------------------------------------
# Helper: Sieve of Eratosthenes up to a given limit
# ----------------------------------------------------------------------
def sieve(limit: int) -> list[int]:
    """Return a list of all primes <= limit."""
    if limit < 2:
        return []
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0:2] = b"\x00\x00"
    for p in range(2, int(limit ** 0.5) + 1):
        if is_prime[p]:
            step = p
            start = p * p
            is_prime[start : limit + 1 : step] = b"\x00" * ((limit - start) // step + 1)
    return [i for i, prime in enumerate(is_prime) if prime]

# ----------------------------------------------------------------------
# Main execution
# ----------------------------------------------------------------------
def main() -> None:
    start_total = time.time()

    # Persistent output folder (outside the temporary directory)
    persistent_out = pathlib.Path.cwd() / "pipeline_output"
    persistent_out.mkdir(exist_ok=True)

    # ------------------------------------------------------------------
    # Hypothesis 1: Robust path resolution & error handling
    # ------------------------------------------------------------------
    try:
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            tmp_path = pathlib.Path(tmp_dir_name).resolve()
            logging.info(f"[H1] Temporary directory resolved to: {tmp_path}")

            # Sub‑directories for data and plots (absolute paths)
            data_dir = tmp_path / "data"
            plot_dir = tmp_path / "plots"
            data_dir.mkdir()
            plot_dir.mkdir()

            # ------------------------------------------------------------------
            # Prime generation (computation part – measured for H4)
            # ------------------------------------------------------------------
            start_compute = time.time()
            primes = sieve(100_000)
            compute_time = time.time() - start_compute

            # ------------------------------------------------------------------
            # Gap statistics
            # ------------------------------------------------------------------
            gaps = [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]
            mean_gap = sum(gaps) / len(gaps) if gaps else 0.0
            max_gap = max(gaps) if gaps else 0

            # ------------------------------------------------------------------
            # Artifact creation (CSV + PNG)
            # ------------------------------------------------------------------
            primes_path = data_dir / "primes.csv"
            gaps_path = data_dir / "gaps.csv"
            plot_path = plot_dir / "prime_gaps_hist.png"

            # Write primes CSV
            try:
                with open(primes_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["prime"])
                    writer.writerows([[p] for p in primes])
            except (OSError, FileNotFoundError) as e:
                logging.error(f"Failed to write {primes_path}: {e}")
                raise

            # Write gaps CSV
            try:
                with open(gaps_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["gap"])
                    writer.writerows([[g] for g in gaps])
            except (OSError, FileNotFoundError) as e:
                logging.error(f"Failed to write {gaps_path}: {e}")
                raise

            # Plot histogram of gaps
            try:
                plt.figure(figsize=(8, 5))
                plt.hist(gaps, bins=50, edgecolor="black", color="#4c72b0")
                plt.title("Prime Gaps up to 100,000")
                plt.xlabel("Gap")
                plt.ylabel("Frequency")
                plt.tight_layout()
                plt.savefig(plot_path, dpi=150)
                plt.close()
            except (OSError, FileNotFoundError) as e:
                logging.error(f"Failed