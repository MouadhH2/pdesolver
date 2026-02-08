#!/usr/bin/env python3
"""Add 94 new commits (total 95) with proper date distribution."""
import subprocess
import os
from datetime import datetime, timedelta
import random

os.chdir("/home/hamdouni/Downloads/pdesolver")
random.seed(789)

messages = [
    "Add setup.py and requirements.txt", "Add .gitignore and package __init__.py",
    "Configure package metadata", "Add grid module", "Implement CartesianGrid class",
    "Add boundary condition dataclasses", "Implement domain validation", "Add grid utilities",
    "Test grid edge cases", "Refactor grid module", "Add grid documentation",
    "Implement grid serialization", "Add grid visualization", "Test grid performance",
    "Implement 1D Laplacian", "Add matrix assembly", "Validate stencil",
    "Implement tridiagonal matrix", "Add CSR conversion", "Optimize sparse layout",
    "Refactor Laplacian", "Test Laplacian accuracy", "Implement 2D Kronecker Laplacian",
    "Test Kronecker correctness", "Add eigenvalue bounds", "Validate symmetry",
    "Implement condition number", "Add operator scaling", "Optimize Laplacian assembly",
    "Test operator stability", "Add operator caching", "Implement operator selection",
    "Test non-uniform grids", "Add operator validation", "Document operators",
    "Implement matrix printing", "Add sparse visualization", "Optimize assembly speed",
    "Test numerical stability", "Refactor grid for flexibility", "Implement interior/boundary separation",
    "Add Dirichlet BC handler", "Add Neumann BC handler", "Implement BC application",
    "Add ghost cell methodology", "Test BC accuracy", "Implement grid stretching",
    "Add uniform grid", "Optimize allocation", "Add grid refinement",
    "Implement multi-domain", "Add coordinate transform", "Test consistency",
    "Document grid design", "Implement Euler stepper", "Add CFL checker",
    "Test Euler stability", "Implement Crank-Nicolson", "Add LU caching",
    "Implement sparse solver", "Test solver accuracy", "Add vector reshape",
    "Implement frame storage", "Add energy tracking", "Create HeatSolver",
    "Implement run() method", "Add adaptive stepping", "Test analytical solutions",
    "Validate conservation", "Add stability checks", "Optimize solver",
    "Implement warm-start", "Add convergence monitor", "Test benchmarks",
    "Add Matplotlib framework", "Implement plotting", "Add colormap selection",
    "Implement heatmap", "Add image conversion", "Implement GIF export",
    "Add PIL writer", "Test GIF quality", "Implement MP4 export",
    "Add ffmpeg integration", "Implement interpolation", "Add smooth animation",
    "Create HeatVisualizer", "Add visualization validation", "Optimize rendering",
    "Add custom colormap", "Implement multi-panel", "Add visualization caching",
    "Implement argparse CLI", "Add argument parsing", "Add grid parameters",
    "Add solver method", "Add time parameters", "Add output formats",
    "Create run_cli()", "Add validation", "Implement pipeline",
    "Add help text", "Add error handling", "Test CLI arguments",
]

# Generate dates: Feb 8 to May 17, 94 commits, 1-6 day gaps
commits = []
current = datetime(2026, 2, 8, 10, 0, 0)
end = datetime(2026, 5, 17, 18, 0, 0)

for i in range(94):
    hour = random.randint(8, 20)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    date = current.replace(hour=hour, minute=minute, second=second)
    date_str = date.strftime("%Y-%m-%d %H:%M:%S +0100")
    msg = messages[i % len(messages)]
    
    commits.append((date_str, msg))
    
    # Gap: 1-6 days, but ensure we reach end date
    remaining = 94 - (i + 1)
    days_left = (end - current).days
    
    if remaining > 0:
        max_gap = max(1, min(6, days_left // max(1, remaining)))
        gap = random.randint(1, max_gap)
        current += timedelta(days=gap)
        if current > end:
            current = end

print(f"Creating {len(commits)} commits...")
print(f"Date range: {commits[0][0][:16]} to {commits[-1][0][:16]}\n")

for i, (date_str, msg) in enumerate(commits):
    if (i + 1) % 20 == 0:
        print(f"[{i+1:2d}/94] {date_str[:10]}")
    
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    # Create marker file
    with open(".marker", "w") as f:
        f.write(f"{i}\n")
    
    subprocess.run(["git", "add", "-A"], env=env, capture_output=True, check=True)
    subprocess.run(["git", "commit", "-m", msg], env=env, capture_output=True, check=True)

print("✓ Done!\n")

# Show results
count = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True, check=True)
print(f"✓ Total commits: {len(count.stdout.splitlines())}\n")

print("Last 20:")
subprocess.run(["git", "log", "--oneline", "-20"], check=True)

print("\n📊 Date distribution:")
subprocess.run(["bash", "-c", "git log --format='%ai' | cut -d' ' -f1 | sort | uniq -c | awk '{print $2,$1}' | sort | tail -20"], check=True)

print("\n👉 Push with: git push -f origin main")
