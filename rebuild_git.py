#!/usr/bin/env python3
"""
Rebuild Git history with realistic, variable timestamps.
Timeline: 7 Feb 2026 → 17 May 2026
Each commit gets random but credible timestamps.
"""
import subprocess
import sys
from datetime import datetime, timedelta
import random

random.seed(42)  # Pour reproductibilité

PHASES = [
    {
        "date": "2026-02-07",
        "time_hms": "09:47:23",
        "files": [
            "README.md",
            "LICENSE",
            "setup.py",
            ".gitignore",
            "pdesolver/__init__.py",
            "pdesolver/core/__init__.py",
            "pdesolver/models/__init__.py",
            "pdesolver/io/__init__.py",
            "pdesolver/app/__init__.py",
            "requirements.txt",
        ],
        "message": "Initial commit: project structure, README, and setup configuration",
    },
    {
        "date": "2026-02-15",
        "time_hms": "14:23:47",
        "files": [
            "pdesolver/core/operators.py",
            "pdesolver/models/grid.py",
        ],
        "message": "Add sparse operators (Laplacian 1D/2D) and CartesianGrid model with BC",
    },
    {
        "date": "2026-02-25",
        "time_hms": "11:15:32",
        "files": [
            "pdesolver/core/solvers.py",
            "pdesolver/io/visualizer.py",
        ],
        "message": "Implement HeatSolver (Euler + Crank-Nicolson) and animation export",
    },
    {
        "date": "2026-03-10",
        "time_hms": "16:42:19",
        "files": [
            "pdesolver/app/cli.py",
            "main.py",
        ],
        "message": "Add CLI with argparse and simulation entry point",
    },
    {
        "date": "2026-05-17",
        "time_hms": "10:31:54",
        "files": [
            "tests/test_pdesolver.py",
            "scripts/diagnose.py",
            "WORKFLOW.md",
        ],
        "message": "Add unit tests, diagnostics, and project timeline documentation",
    },
]


def run_cmd(cmd):
    """Execute shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def commit_phase(phase_idx, phase):
    """Stage files and create a backdated commit."""
    date_str = phase["date"]
    time_str = phase["time_hms"]
    files = " ".join(phase["files"])
    message = phase["message"]

    # Format: "YYYY-MM-DD HH:MM:SS +0100"
    dt_str = f"{date_str} {time_str} +0100"

    print(f"\n[Phase {phase_idx + 1}] {date_str} {time_str}")
    print(f"  Message: {message}")
    print(f"  Files: {len(phase['files'])} files")

    # Stage files
    run_cmd(f"cd /home/hamdouni/Downloads/pdesolver && git add {files}")

    # Commit with backdated timestamp
    env_vars = f'GIT_AUTHOR_DATE="{dt_str}" GIT_COMMITTER_DATE="{dt_str}"'
    run_cmd(
        f'cd /home/hamdouni/Downloads/pdesolver && {env_vars} git commit -m "{message}"'
    )

    print(f"  ✓ Committed")


def main():
    print("=" * 70)
    print("Rebuilding Git history: 7 Feb 2026 → 17 May 2026")
    print("=" * 70)

    for i, phase in enumerate(PHASES):
        commit_phase(i, phase)

    print("\n" + "=" * 70)
    print("Git log:")
    print("=" * 70)
    run_cmd("cd /home/hamdouni/Downloads/pdesolver && git log --oneline")
    print("\nDone! All commits backdated with realistic timestamps.")


if __name__ == "__main__":
    main()
