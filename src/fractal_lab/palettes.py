"""Small palette helpers so lessons don't depend on user's matplotlib config."""
import numpy as np


def normalize(div: np.ndarray) -> np.ndarray:
    lo, hi = div.min(), div.max()
    if hi == lo:
        return np.zeros_like(div, dtype=float)
    return (div - lo) / (hi - lo)


MANDELBROT_CMAP = "twilight_shifted"
JULIA_CMAP = "magma"
KOCH_CMAP = "viridis"