from __future__ import annotations

import numpy as np

from pdesolver.core.operators import laplacian_2d
from pdesolver.core.solvers import HeatSolver
from pdesolver.models.grid import CartesianGrid


def test_laplacian_2d_shape() -> None:
    matrix = laplacian_2d(nx=4, ny=3, dx=0.1, dy=0.2)
    assert matrix.shape == (12, 12)


def test_grid_dirichlet_boundaries_are_applied() -> None:
    grid = CartesianGrid(nx=7, ny=6)
    field = grid.gaussian(sigma=0.2)

    assert np.allclose(field[:, 0], 0.0)
    assert np.allclose(field[:, -1], 0.0)
    assert np.allclose(field[0, :], 0.0)
    assert np.allclose(field[-1, :], 0.0)


def test_heat_solver_crank_nicolson_outputs_expected_shapes() -> None:
    grid = CartesianGrid(nx=15, ny=15)
    initial = grid.gaussian(sigma=0.12)

    solver = HeatSolver(grid=grid, alpha=1.0, dt=1e-3, t_end=5e-3, method="crank-nicolson")
    times, frames = solver.run(initial=initial, store_every=2)

    assert times.ndim == 1
    assert frames[0].shape == (15, 15)
    assert frames[-1].shape == (15, 15)
    assert len(frames) >= 2
