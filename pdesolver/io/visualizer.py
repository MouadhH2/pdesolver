from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

from pdesolver.models.grid import Array2D, CartesianGrid


class HeatVisualizer:
    def __init__(self, grid: CartesianGrid, fps: int = 20, cmap: str = "inferno") -> None:
        if fps <= 0:
            raise ValueError(f"fps must be > 0, got {fps}.")
        self.grid = grid
        self.fps = fps
        self.cmap = cmap

    def animate(
        self,
        frames: list[Array2D],
        output_path: str,
        title: str = "2D Heat Equation",
    ) -> Path:
        if not frames:
            raise ValueError("frames cannot be empty.")

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        vmin = float(np.min(frames[0]))
        vmax = float(np.max(frames[0]))

        fig, ax = plt.subplots(figsize=(7, 5), dpi=120)
        image = ax.imshow(
            frames[0],
            origin="lower",
            extent=[0.0, self.grid.lx, 0.0, self.grid.ly],
            cmap=self.cmap,
            vmin=vmin,
            vmax=vmax,
            animated=True,
            interpolation="bilinear",
            aspect="auto",
        )
        cbar = fig.colorbar(image, ax=ax)
        cbar.set_label("Temperature")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)

        def update(index: int) -> tuple:
            image.set_array(frames[index])
            ax.set_title(f"{title} · frame {index + 1}/{len(frames)}")
            return (image,)

        animation = FuncAnimation(
            fig,
            update,
            frames=len(frames),
            interval=int(1000 / self.fps),
            blit=True,
        )

        extension = path.suffix.lower()
        if extension == ".gif":
            animation.save(path, writer=PillowWriter(fps=self.fps))
        elif extension == ".mp4":
            animation.save(path, writer="ffmpeg", fps=self.fps)
        else:
            raise ValueError("output_path must end with .gif or .mp4")

        plt.close(fig)
        return path
