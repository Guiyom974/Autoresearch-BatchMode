#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import csv
import tempfile
import random
import itertools
import time
from pathlib import Path
import matplotlib.pyplot as plt

# Use non‑interactive backend for matplotlib
plt.switch_backend('Agg')


class PathValidationError(Exception):