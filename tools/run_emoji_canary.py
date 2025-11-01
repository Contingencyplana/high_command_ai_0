"""Wrapper script to run the Level-0 translator canary.

Intended for cron/systemd timers. Executes the dispatcher against the sample
chains and exits non-zero if translation fails, allowing scheduling systems
to alert or retry.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "golf_00" / "delta_00" / "alfa_04" / "dispatch_sample_chains.py"
    result = subprocess.run([sys.executable, str(script)], cwd=repo_root)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
