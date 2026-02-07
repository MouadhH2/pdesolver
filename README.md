# pdesolver

`pdesolver` is a clean, modular Python package for solving and visualizing the 2D heat equation on Cartesian grids using sparse linear algebra.

## Architecture

- `pdesolver/core/`: sparse operators and time integrators
- `pdesolver/models/`: mesh and boundary condition model
- `pdesolver/io/`: animation and export
- `pdesolver/app/`: command-line application glue
- `main.py`: executable entrypoint

## Mathematical model

The simulated PDE is:

$$
\frac{\partial u}{\partial t} = \alpha \left(\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right)
$$

Space is discretized on a Cartesian mesh. The 2D Laplacian is assembled with Kronecker products:

$$
L_{2D} = I_y \otimes L_x + L_y \otimes I_x
$$

where $L_x$ and $L_y$ are 1D second-derivative sparse matrices.

Time integration methods:

- Explicit Euler:

$$
\mathbf{u}^{n+1} = \mathbf{u}^{n} + \Delta t\,\alpha\,(L\mathbf{u}^{n} + \mathbf{g})
$$

- Crank–Nicolson:

$$
(I - \tfrac{1}{2}\Delta t\,\alpha L)\mathbf{u}^{n+1} = (I + \tfrac{1}{2}\Delta t\,\alpha L)\mathbf{u}^{n} + \Delta t\,\alpha\,\mathbf{g}
$$

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python3 main.py --nx 101 --ny 101 --method crank-nicolson --dt 1e-4 --t-end 0.02 --output outputs/heat.gif
```

MP4 export is also supported:

```bash
python3 main.py --output outputs/heat.mp4
```

## CLI arguments (main)

- `--nx`, `--ny`: grid resolution
- `--lx`, `--ly`: physical domain lengths
- `--alpha`: diffusivity
- `--dt`, `--t-end`: temporal settings
- `--method`: `explicit` or `crank-nicolson`
- `--store-every`: frame stride
- `--fps`: animation framerate
- `--sigma`: Gaussian width for initial condition
- `--center-x`, `--center-y`: Gaussian center position in $[0, 1]$
- `--output`: destination `.gif` or `.mp4`

## Validation

The project includes lightweight unit tests to check:

- sparse operator dimensions,
- boundary condition enforcement,
- end-to-end solver output consistency.

Run tests with:

```bash
python3 -m pytest -q
```

## Why this project is strong for an applied math portfolio

- clean PDE-to-code mapping,
- sparse numerical linear algebra,
- two standard time integrators with different stability properties,
- reproducible CLI workflow and visual outputs.

## Notes

- Matrices are assembled in sparse CSR format.
- For explicit Euler, respect the CFL-like stability limit reported by the solver.
- MP4 export requires `ffmpeg` available on the system.
