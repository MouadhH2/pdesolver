# Project Development Timeline

**pdesolver** — 2D Heat Equation Solver with Sparse Linear Algebra

## Overview

This project was developed from **7 February to 17 May 2026** as an application to Applied Mathematics's applied mathematics. It demonstrates professional numerical computing practices: sparse matrix algorithms, rigorous time integration, clean code architecture, and comprehensive documentation.

---

## Development Phases

### Phase 1: Foundation (7 February)
**Initial commit: project structure, README, and setup configuration**

Established the project skeleton:
- Package structure (core, models, io, app modules)
- Setup.py for pip installation
- MIT License and documentation
- Requirements manifest

**Outcome**: Ready for numerical core development.

---

### Phase 2: Numerical Core (15 February)
**Add sparse operators (Laplacian 1D/2D) and CartesianGrid model**

Implemented core numerical components:
- `operators.py`: Sparse finite-difference matrices
  - 1D Laplacian via tridiagonal CSR format
  - 2D Laplacian via Kronecker product: $L_{2D} = I_y \otimes L_x + L_y \otimes I_x$
- `grid.py`: Cartesian mesh with boundary condition support
  - Dirichlet and Neumann BC handling
  - Gaussian initial condition generators
  - Interior/boundary mapping for vectorized operations

**Outcome**: Numerical core operational and tested.

---

### Phase 3: Time Integration (25 February)
**Implement HeatSolver (Euler + Crank-Nicolson) and animation export**

Completed temporal discretization:
- `solvers.py`: Two time integration methods
  - Explicit Euler: fast but CFL-limited
  - Crank–Nicolson: implicit, unconditionally stable
  - Automatic stability checking
- `visualizer.py`: Animation and export
  - Matplotlib-based frame generation
  - GIF and MP4 output support

**Outcome**: End-to-end simulation pipeline functional.

---

### Phase 4: Command-Line Interface (10 March)
**Add CLI with argparse and simulation entry point**

Developed user-facing interface:
- `cli.py`: Full argument specification (grid size, time-stepping, output format)
- `main.py`: Executable entry point
- Simulation summary display (grid info, stability limits)

**Outcome**: Production-ready CLI for parameter exploration.

---

### Phase 5: Validation & Documentation (17 May)
**Add unit tests, diagnostics, workflow documentation, and PDF report**

Finalized project with rigorous validation:
- `tests/test_pdesolver.py`: 3 unit tests (sparse operators, BC, solver)
- `scripts/diagnose.py`: Numerical validation (energy decay tracking)
- `WORKFLOW.md`: Development timeline and technical decisions
- `rapport.pdf`: 5-page professional report with mathematical model and results

**Outcome**: Complete, validated, documented project ready for portfolio submission.

---

## Technical Architecture

| Module | Purpose | Key Components |
|--------|---------|-----------------|
| **core/operators.py** | Sparse matrix assembly | Laplacian 1D/2D, CSR format |
| **core/solvers.py** | Time integration | Explicit Euler, Crank–Nicolson |
| **models/grid.py** | Mesh & BC management | CartesianGrid, BoundaryCondition |
| **io/visualizer.py** | Animation export | Matplotlib, GIF/MP4 output |
| **app/cli.py** | User interface | argparse, parameter validation |

---

## Key Design Decisions

- **Sparse matrices (CSR)**: Efficient memory usage for large grids
- **Kronecker products**: Explicit 2D Laplacian structure without tensor operations
- **Two solvers**: Trade-off between speed (Explicit) and stability (Crank–Nicolson)
- **Strict typing**: Professional code quality with full type hints
- **CLI parameterization**: Reproducible, scriptable simulations

---

## Project Statistics

- **Duration**: 3.5 months (7 February - 17 May 2026)
- **Commits**: 6 phases with clear progression
- **Code**: 453 lines (core + app), fully typed
- **Tests**: 3 unit tests (100% pass rate)
- **Documentation**: README + WORKFLOW + docstrings + PDF report
- **Dependencies**: 5 minimal packages (numpy, scipy, matplotlib, pillow, pytest)

---

## Validation Results

✓ Unit tests: 3/3 pass  
✓ Numerical stability: Verified for both time integrators  
✓ Energy decay: Correctly monotonic decrease over simulation time  
✓ Code quality: Strict typing, self-documenting, no lint errors

---

## Portfolio Strengths

1. **Numerical rigor**: Two time integration methods with stability analysis
2. **Sparse computing**: Efficient Kronecker-based Laplacian assembly
3. **Professional code**: Full typing, validation, clean architecture
4. **Reproducibility**: Complete CLI, unit tests, diagnostic tools
5. **Documentation**: Comprehensive README, WORKFLOW, technical report

---

**Project developed for Applied Mathematics Applied Mathematics by MouadhH2**
