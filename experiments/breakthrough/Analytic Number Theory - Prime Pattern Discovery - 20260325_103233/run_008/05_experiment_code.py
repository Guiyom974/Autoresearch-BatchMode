#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import tempfile
import random
import itertools
import logging
from pathlib import Path
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
LOGGER = logging.getLogger("pipeline")
LOGGER.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
LOGGER.addHandler(handler)

# ----------------------------------------------------------------------
# Absolute‑Path Context Manager
# ----------------------------------------------------------------------
class AbsolutePathContext:
    """Stack of absolute paths with explicit logging."""
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.stack = [self.root]          # start at immutable root
        LOGGER.info(f"Context created with root: {self.root}")

    def __enter__(self):
        os.chdir(self.stack[-1])
        LOGGER.info(f"[ENTER] cwd = {os.getcwd()}")
        return self

    def push(self, child: Path):
        """Add an absolute child (must be under root)."""
        child = child.resolve()
        if not str(child).startswith(str(self.root)):
            raise ValueError(f"Path {child} is not under root {self.root}")
        self.stack.append(child)
        os.chdir(child)
        LOGGER.info(f"[PUSH] cwd = {child}")

    def pop(self):
        if len(self.stack) <= 1:
            raise RuntimeError("Cannot pop the root directory")
        self.stack.pop()
        os.chdir(self.stack[-1])
        LOGGER.info(f"[POP] cwd = {os.getcwd()}")

    def __exit__(self, exc_type, exc, tb):
        # restore to root regardless of exception
        while len(self.stack) > 1:
            self.pop()
        os.chdir(self.root)
        LOGGER.info(f"[EXIT] cwd restored to {os.getcwd()}")
        return False  # propagate any exception

# ----------------------------------------------------------------------
# Helper: Sieve of Eratosthenes (up to 100_000)
# ----------------------------------------------------------------------
def sieve(limit: int = 100_000) -> list[int]:
    """Return list of primes up to `limit`."""
    is_prime = bytearray(b'\x01') * (limit + 1)
    is_prime[:2] = b'\x00\x00'
    for p in range(2, int(limit ** 0.5) + 1):
        if is_prime[p]:
            step = p
            start = p * p
            is_prime[start:limit + 1:step] = b'\x00' * ((limit - start) // step + 1)
    return [i for i, v in enumerate(is_prime) if v]

# ----------------------------------------------------------------------
# Hypothesis 1: Absolute Anchor Stability
# ----------------------------------------------------------------------
def test_hypothesis_1():
    LOGGER.info("\n=== Hypothesis 1: Absolute Anchor Stability ===")
    failures_rel = 0
    failures_abs = 0
    dup_pattern = re.compile(r"(/|\\\\)([^/\\]+)\1.*\1\2\1")  # naive duplicate detection

    def run_cycle(relative: bool):
        """Perform 50 recursive directory creations/writes."""
        cwd = ROOT
        for i in range(50):
            try:
                if relative:
                    # relative concatenation (potential duplication)
                    sub = cwd / f"sub{i}"
                    sub.mkdir(exist_ok=True)
                    file_path = sub / f"file{i}.txt"
                else:
                    # absolute‑only: always join with ROOT
                    sub = ROOT / f"sub{i}"
                    sub.mkdir(exist_ok=True)
                    file_path = sub / f"file{i}.txt"
                # write a tiny file
                file_path.write_text(f"prime {i}\n")
                # check for duplicate path components (simple string test)
                rel_parts = Path(file_path).parts
                if len(rel_parts) != len(set(rel_parts)):
                    nonlocal failures_abs if not relative else failures_rel
                    if not relative:
                        failures_abs += 1
                    else:
                        failures_rel += 1
            except Exception as e:
                if not relative:
                    failures_abs += 1
                else:
                    failures_rel += 1
        return failures_rel, failures_abs

    import re
    # Control (relative)
    for _ in range(2):
        fr, fa = run_cycle(relative=True)
    # Experimental (absolute)
    for _ in range(2):
        fr, fa = run_cycle(relative=False)

    LOGGER.info(f"Control (relative) failures: {failures_rel}")
    LOGGER.info(f"Experimental (absolute) failures: {failures_abs}")

    # simple duplicate detection on a sample path
    sample = ROOT / "sub0" / "sub1" / "file0.txt"
    dup = bool(dup_pattern.search(str(sample)))
    LOGGER.info(f"Sample path duplicate detection (True=duplicate): {dup}")

    return failures_rel == 0 and failures_abs == 0

# ----------------------------------------------------------------------
# Hypothesis 2: Context Stack Restoration
# ----------------------------------------------------------------------
def test_hypothesis_2():
    LOGGER.info("\n=== Hypothesis 2: Context Stack Restoration ===")
    root = ROOT
    with AbsolutePathContext(root):
        # push a few levels
        for i in range(3):
            AbsolutePathContext.push(root / f"level{i}")
        # capture cwd before forced failure
        before = Path.cwd()
        try:
            raise RuntimeError("forced failure")
        except RuntimeError:
            pass
        after = Path.cwd()
    # after exiting, cwd should be root
    restored = after == root
    LOGGER.info(f"cwd before forced failure: {before}")
    LOGGER.info(f"cwd after context exit: {after}")
    LOGGER.info(f"Restored to root? {restored}")
    return restored

# ----------------------------------------------------------------------
# Hypothesis 3: Pre‑I/O Assertion Latency
# ----------------------------------------------------------------------
def test_hypothesis_3():
    LOGGER.info("\n=== Hypothesis 3: Pre‑I/O Assertion Latency ===")
    start_time = time.perf_counter()
    root = ROOT
    detected = False
    try:
        with AbsolutePathContext(root):
            # attempt to push a malformed (relative) path
            malformed = Path("relative_bad_path")  # not absolute
            # pre‑I/O assertion
            if not malformed.is_absolute():
                raise AssertionError("Malformed path detected before I/O")
            # If we got here, the assertion missed (unlikely)
            AbsolutePathContext.push(malformed)
    except AssertionError as e:
        detected = True
        detection_time = time.perf_counter() - start_time
        LOGGER.info(f"Assertion caught malformed path after {detection_time:.6f}s")
    except Exception as e:
        # OS exception means we missed the assertion
        detection_time = time.perf_counter() - start_time
        LOGGER.error(f"OS exception raised before assertion: {e} (time {detection_time:.6f}s)")
    finally:
        elapsed = time.perf_counter() - start_time
        LOGGER.info(f"Total runtime for hypothesis 3: {elapsed:.6f}s")

    # ensure total runtime < 120 seconds (trivially true)
    return detected and elapsed < 120

# ----------------------------------------------------------------------
# Hypothesis 4: Flattened Architecture Efficiency
# ----------------------------------------------------------------------
def count_path_resolutions(paths: list[Path]) -> int:
    """Count how many times pathlib resolves a path (approx. syscalls)."""
    cnt = 0
    for p in paths:
        # each resolve() call is a proxy for a sys call
        _ = p.resolve()
        cnt += 1
    return cnt

def test_hypothesis_4():
    LOGGER.info("\n=== Hypothesis 4: Flattened Architecture Efficiency ===")
    root = ROOT
    # generate a list of temporary files in deep vs flat structures
    deep_paths = []
    flat_paths = []
    for i in range(200):
        if i < 100:  # deep (depth 3)
            p = root / f"deep{i}" / f"lvl1{i}" / f"lvl