"""HPWM Standalone 1-Click Independent Verification Suite.

Convenience root wrapper pointing to scripts/run_verification.py.
"""
from pathlib import Path
import sys

scripts_dir = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from run_verification import main

if __name__ == "__main__":
    main()
