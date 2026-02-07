from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve

from pdesolver.core.operators import laplacian_2d
from pdesolver.models.grid import Array2D, CartesianGrid

TimeMethod = Literal["explicit", "crank-nicolson"]

__all__ = ["HeatSolver"]


@dataclass
class HeatSolver:
    grid: CartesianGrid
    alpha: float
    dt: float
    t_end: float
    method: TimeMethod = "explicit"

    def __post_init__(self) -> None:
        if self.alpha <= 0.0:
            raise ValueError(f"alpha must be > 0, got {self.alpha}.")
        if self.dt <= 0.0:
            raise ValueError(f"dt must be > 0, got {self.dt}.")
        if self.t_end <= 0.0:
            raise ValueError(f"t_end must be > 0, got {self.t_end}.")

        self._nx_i = self.grid.nx - 2
        self._ny_i = self.grid.ny - 2
        self._lap = laplacian_2d(self._nx_i, self._ny_i, self.grid.dx, self.grid.dy)
        self._identity = sp.eye(self._lap.shape[0], format="csr")

        theta = 0.5 * self.alpha * self.dt
        self._cn_left = (self._identity - theta * self._lap).tocsr()
        self._cn_right = (self._identity + theta * self._lap).tocsr()

    @property
    def explicit_stability_limit(self) -> float:
        inv_dx2 = 1.0 / (self.grid.dx * self.grid.dx)
        inv_dy2 = 1.0 / (self.grid.dy * self.grid.dy)
        return 1.0 / (2.0 * self.alpha * (inv_dx2 + inv_dy2))

    def run(
        self,
        initial: Array2D,
        store_every: int = 1,
    ) -> tuple[npt.NDArray[np.float64], list[Array2D]]:
        if store_every <= 0:
            raise ValueError(f"store_every must be > 0, got {store_every}.")

        if self.method == "explicit" and self.dt > self.explicit_stability_limit:
            raise ValueError(
                "Explicit Euler unstable with current dt. "
                f"Use dt <= {self.explicit_stability_limit:.6e} or switch to crank-nicolson."
            )

        u = np.array(initial, dtype=np.float64, copy=True)
        if u.shape != (self.grid.ny, self.grid.nx):
            raise ValueError(f"initial shape must be {(self.grid.ny, self.grid.nx)}, got {u.shape}.")

        self.grid.apply_boundaries(u)

        n_steps = int(np.ceil(self.t_end / self.dt))
        times = np.linspace(0.0, n_steps * self.dt, n_steps + 1, dtype=np.float64)

        frames: list[Array2D] = [u.copy()]
        interior = self.grid.interior_flat(u)

        for step in range(1, n_steps + 1):
            if self.method == "explicit":
                interior = self._step_explicit(interior)
            else:
                interior = self._step_crank_nicolson(interior)

            u = self.grid.inject_interior(interior, out=u)
            if step % store_every == 0 or step == n_steps:
                frames.append(u.copy())

        return times, frames

    def _step_explicit(self, interior: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        u_full = self.grid.inject_interior(interior)
        source = self._boundary_source(u_full)
        rhs = self._lap @ interior + source
        return interior + self.dt * self.alpha * rhs

    def _step_crank_nicolson(self, interior: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        u_full = self.grid.inject_interior(interior)
        source = self._boundary_source(u_full)

        rhs = self._cn_right @ interior + self.alpha * self.dt * source
        next_interior = spsolve(self._cn_left, rhs)
        return np.asarray(next_interior, dtype=np.float64)

    def _boundary_source(self, u: Array2D) -> npt.NDArray[np.float64]:
        g = np.zeros((self._ny_i, self._nx_i), dtype=np.float64)

        inv_dx2 = 1.0 / (self.grid.dx * self.grid.dx)
        inv_dy2 = 1.0 / (self.grid.dy * self.grid.dy)

        g[:, 0] += inv_dx2 * u[1:-1, 0]
        g[:, -1] += inv_dx2 * u[1:-1, -1]
        g[0, :] += inv_dy2 * u[0, 1:-1]
        g[-1, :] += inv_dy2 * u[-1, 1:-1]

        return np.ascontiguousarray(g.ravel(order="C"), dtype=np.float64)
