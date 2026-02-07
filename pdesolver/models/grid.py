from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt

BoundaryKind = Literal["dirichlet", "neumann"]
Array2D = npt.NDArray[np.float64]


@dataclass(frozen=True)
class BoundaryCondition:
    kind: BoundaryKind
    value: float = 0.0


@dataclass(frozen=True)
class BoundarySet:
    left: BoundaryCondition = BoundaryCondition("dirichlet", 0.0)
    right: BoundaryCondition = BoundaryCondition("dirichlet", 0.0)
    bottom: BoundaryCondition = BoundaryCondition("dirichlet", 0.0)
    top: BoundaryCondition = BoundaryCondition("dirichlet", 0.0)


@dataclass(frozen=True)
class CartesianGrid:
    nx: int
    ny: int
    lx: float = 1.0
    ly: float = 1.0
    boundaries: BoundarySet = BoundarySet()

    def __post_init__(self) -> None:
        if self.nx < 3:
            raise ValueError(f"nx must be >= 3, got {self.nx}.")
        if self.ny < 3:
            raise ValueError(f"ny must be >= 3, got {self.ny}.")
        if self.lx <= 0.0:
            raise ValueError(f"lx must be > 0, got {self.lx}.")
        if self.ly <= 0.0:
            raise ValueError(f"ly must be > 0, got {self.ly}.")

    @property
    def dx(self) -> float:
        return self.lx / (self.nx - 1)

    @property
    def dy(self) -> float:
        return self.ly / (self.ny - 1)

    @property
    def x(self) -> npt.NDArray[np.float64]:
        return np.linspace(0.0, self.lx, self.nx, dtype=np.float64)

    @property
    def y(self) -> npt.NDArray[np.float64]:
        return np.linspace(0.0, self.ly, self.ny, dtype=np.float64)

    def zeros(self) -> Array2D:
        return np.zeros((self.ny, self.nx), dtype=np.float64)

    def gaussian(self, center_x: float = 0.5, center_y: float = 0.5, sigma: float = 0.1) -> Array2D:
        if sigma <= 0.0:
            raise ValueError(f"sigma must be > 0, got {sigma}.")

        x = self.x
        y = self.y
        x0 = center_x * self.lx
        y0 = center_y * self.ly

        xx, yy = np.meshgrid(x, y, indexing="xy")
        rr2 = (xx - x0) ** 2 + (yy - y0) ** 2
        field = np.exp(-rr2 / (2.0 * sigma * sigma), dtype=np.float64)
        self.apply_boundaries(field)
        return field

    def apply_boundaries(self, u: Array2D) -> None:
        if u.shape != (self.ny, self.nx):
            raise ValueError(f"u shape must be {(self.ny, self.nx)}, got {u.shape}.")

        self._apply_vertical_boundary(u, side="left", bc=self.boundaries.left)
        self._apply_vertical_boundary(u, side="right", bc=self.boundaries.right)
        self._apply_horizontal_boundary(u, side="bottom", bc=self.boundaries.bottom)
        self._apply_horizontal_boundary(u, side="top", bc=self.boundaries.top)

    def interior_flat(self, u: Array2D) -> npt.NDArray[np.float64]:
        if u.shape != (self.ny, self.nx):
            raise ValueError(f"u shape must be {(self.ny, self.nx)}, got {u.shape}.")
        return np.ascontiguousarray(u[1:-1, 1:-1].ravel(order="C"), dtype=np.float64)

    def inject_interior(self, interior: npt.NDArray[np.float64], out: Array2D | None = None) -> Array2D:
        expected_size = (self.nx - 2) * (self.ny - 2)
        if interior.size != expected_size:
            raise ValueError(f"interior size must be {expected_size}, got {interior.size}.")

        u = self.zeros() if out is None else out
        if u.shape != (self.ny, self.nx):
            raise ValueError(f"out shape must be {(self.ny, self.nx)}, got {u.shape}.")

        u[1:-1, 1:-1] = interior.reshape((self.ny - 2, self.nx - 2), order="C")
        self.apply_boundaries(u)
        return u

    def _apply_vertical_boundary(self, u: Array2D, side: Literal["left", "right"], bc: BoundaryCondition) -> None:
        if side == "left":
            boundary_column = 0
            neighbor_column = 1
            normal_sign = -1.0
        else:
            boundary_column = self.nx - 1
            neighbor_column = self.nx - 2
            normal_sign = 1.0

        if bc.kind == "dirichlet":
            u[:, boundary_column] = bc.value
            return

        gradient = bc.value
        u[:, boundary_column] = u[:, neighbor_column] + normal_sign * self.dx * gradient

    def _apply_horizontal_boundary(self, u: Array2D, side: Literal["bottom", "top"], bc: BoundaryCondition) -> None:
        if side == "bottom":
            boundary_row = 0
            neighbor_row = 1
            normal_sign = -1.0
        else:
            boundary_row = self.ny - 1
            neighbor_row = self.ny - 2
            normal_sign = 1.0

        if bc.kind == "dirichlet":
            u[boundary_row, :] = bc.value
            return

        gradient = bc.value
        u[boundary_row, :] = u[neighbor_row, :] + normal_sign * self.dy * gradient
