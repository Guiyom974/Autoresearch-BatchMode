#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import uuid
import tempfile
import shutil
from pathlib import Path
from contextlib import contextmanager

# matplotlib is optional – we try to import it for the bar‑chart
try:
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except Exception:  # pragma: no cover
    _HAS_MPL = False

# -