from __future__ import annotations

from typing import Final

import scipy.sparse as sp

SparseMatrix = sp.csr_matrix

__all__ = ["laplacian_1d", "laplacian_2d"]


def _validate_positive_int(value: int, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be > 0, got {value}.")


def _validate_positive_float(value: float, name: str) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0, got {value}.")


def laplacian_1d(n: int, dx: float) -> SparseMatrix:
    _validate_positive_int(n, "n")
    _validate_positive_float(dx, "dx")

    inv_dx2: Final[float] = 1.0 / (dx * dx)
    main = -2.0 * inv_dx2
    off = 1.0 * inv_dx2

    matrix = sp.diags(
        diagonals=[off, main, off],
        offsets=[-1, 0, 1],
        shape=(n, n),
        format="csr",
    )
    return matrix


def laplacian_2d(nx: int, ny: int, dx: float, dy: float) -> SparseMatrix:
    _validate_positive_int(nx, "nx")
    _validate_positive_int(ny, "ny")
    _validate_positive_float(dx, "dx")
    _validate_positive_float(dy, "dy")

    lx = laplacian_1d(nx, dx)
    ly = laplacian_1d(ny, dy)

    ix = sp.eye(nx, format="csr")
    iy = sp.eye(ny, format="csr")

    matrix = sp.kron(iy, lx, format="csr") + sp.kron(ly, ix, format="csr")
    return matrix
