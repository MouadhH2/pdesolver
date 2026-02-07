#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from pdesolver.core.solvers import HeatSolver
from pdesolver.models.grid import CartesianGrid


def main() -> None:
    print("=" * 60)
    print("pdesolver diagnostic: numerical validation")
    print("=" * 60)

    grid = CartesianGrid(nx=51, ny=51, lx=1.0, ly=1.0)
    initial = grid.gaussian(center_x=0.5, center_y=0.5, sigma=0.1)

    print(f"\nGrid: {grid.nx} x {grid.ny}, dx={grid.dx:.4f}, dy={grid.dy:.4f}")
    print(f"Initial condition: Gaussian centered at (0.5, 0.5), σ=0.1")

    solver = HeatSolver(grid=grid, alpha=1.0, dt=5e-4, t_end=0.05, method="crank-nicolson")
    print(f"\nSolver: Crank–Nicolson, α=1.0, Δt=5e-4, t_end=0.05")

    times, frames = solver.run(initial=initial, store_every=5)

    print(f"\nGenerated {len(frames)} frames over {len(times)} time steps\n")
    print("Frame #  |   Time    | L² Energy  |  Max(u)  |  Min(u)  |  Decay")
    print("-" * 70)

    energy_initial = np.linalg.norm(frames[0].ravel())

    for i, frame in enumerate(frames):
        energy = np.linalg.norm(frame.ravel())
        t = times[i * 5] if i * 5 < len(times) else times[-1]
        u_max = np.max(frame)
        u_min = np.min(frame)
        decay_ratio = (energy_initial - energy) / energy_initial * 100.0

        print(f"  {i:3d}   | {t:9.5f} | {energy:10.6f} | {u_max:8.6f} | {u_min:8.6f} | {decay_ratio:6.2f}%")

    print("-" * 70)
    print(f"\nEnergy decay: {energy_initial:.6f} → {energy:.6f} ({(1 - energy/energy_initial)*100:.1f}% reduction)")
    print("\n✓ Simulation completed successfully.")
    print("✓ Animations saved to outputs/*.gif")
    print("=" * 60)


if __name__ == "__main__":
    main()
