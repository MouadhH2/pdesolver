from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from pdesolver.core.solvers import HeatSolver
from pdesolver.io.visualizer import HeatVisualizer
from pdesolver.models.grid import CartesianGrid

__all__ = ["build_parser", "run_cli"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="2D heat equation solver using sparse operators.")
    parser.add_argument("--nx", type=int, default=101, help="Number of grid points along x.")
    parser.add_argument("--ny", type=int, default=101, help="Number of grid points along y.")
    parser.add_argument("--lx", type=float, default=1.0, help="Domain length along x.")
    parser.add_argument("--ly", type=float, default=1.0, help="Domain length along y.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Thermal diffusivity.")
    parser.add_argument("--dt", type=float, default=1e-4, help="Time step.")
    parser.add_argument("--t-end", type=float, default=0.02, help="Final simulation time.")
    parser.add_argument(
        "--method",
        choices=["explicit", "crank-nicolson"],
        default="crank-nicolson",
        help="Time integration method.",
    )
    parser.add_argument("--store-every", type=int, default=10, help="Snapshot stride.")
    parser.add_argument("--fps", type=int, default=20, help="Animation framerate.")
    parser.add_argument("--output", type=str, default="outputs/heat.gif", help="Output file (.gif or .mp4).")
    parser.add_argument("--sigma", type=float, default=0.1, help="Gaussian width for initial condition.")
    parser.add_argument("--center-x", type=float, default=0.5, help="Gaussian center position in x as a ratio in [0, 1].")
    parser.add_argument("--center-y", type=float, default=0.5, help="Gaussian center position in y as a ratio in [0, 1].")
    return parser


def run_cli(argv: Sequence[str] | None = None) -> Path:
    args = build_parser().parse_args(list(argv) if argv is not None else None)

    grid = CartesianGrid(nx=args.nx, ny=args.ny, lx=args.lx, ly=args.ly)
    initial = grid.gaussian(center_x=args.center_x, center_y=args.center_y, sigma=args.sigma)

    solver = HeatSolver(
        grid=grid,
        alpha=args.alpha,
        dt=args.dt,
        t_end=args.t_end,
        method=args.method,
    )

    n_steps = int(args.t_end / args.dt) + int((args.t_end % args.dt) > 0)
    print(
        "Simulation setup: "
        f"grid={args.nx}x{args.ny}, method={args.method}, dt={args.dt:.3e}, "
        f"t_end={args.t_end:.3e}, steps≈{n_steps}"
    )
    if args.method == "explicit":
        print(f"Explicit stability limit: dt <= {solver.explicit_stability_limit:.3e}")

    _, frames = solver.run(initial=initial, store_every=args.store_every)

    visualizer = HeatVisualizer(grid=grid, fps=args.fps)
    saved_path = visualizer.animate(frames=frames, output_path=args.output)
    print(f"Animation saved to {saved_path}")
    return saved_path
