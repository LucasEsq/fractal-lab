"""Core fractal generators. Pure NumPy, no matplotlib, fully testable."""
from __future__ import annotations

import numpy as np


def mandelbrot(
    width: int = 400,
    height: int = 300,
    max_iter: int = 100,
    x_min: float = -2.5,
    x_max: float = 1.0,
    y_min: float = -1.25,
    y_max: float = 1.25,
) -> np.ndarray:
    """Return iteration counts for the Mandelbrot set on a pixel grid."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    Z = np.zeros_like(C)
    div = np.zeros(C.shape, dtype=int)

    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        if not mask.any():
            break
        Z[mask] = Z[mask] ** 2 + C[mask]
        div[mask] = i

    return div


def julia(
    c: complex,
    width: int = 400,
    height: int = 400,
    max_iter: int = 100,
    x_min: float = -2.0,
    x_max: float = 2.0,
    y_min: float = -2.0,
    y_max: float = 2.0,
) -> np.ndarray:
    """Return iteration counts for the Julia set with parameter c."""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    div = np.zeros(Z.shape, dtype=int)

    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        if not mask.any():
            break
        Z[mask] = Z[mask] ** 2 + c
        div[mask] = i

    return div


def koch_snowflake_points(order: int = 6) -> np.ndarray:
    """Return complex points tracing a Koch snowflake boundary."""
    angles = np.array([0.0, 2 * np.pi / 3, 4 * np.pi / 3, 0.0])
    points = [np.exp(1j * a) for a in angles]

    for _ in range(order):
        new_points = [points[0]]
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]
            d = (p2 - p1) / 3
            a = p1 + d
            b = p1 + 2 * d
            peak = a + d * np.exp(-1j * np.pi / 3)
            new_points.extend([a, peak, b, p2])
        points = new_points

    return np.array(points)


def box_counts(points: np.ndarray, n_scales: int = 8) -> tuple[np.ndarray, np.ndarray]:
    """Count occupied boxes at multiple scales. Returns (sizes, counts)."""
    x, y = points.real, points.imag
    span = max(x.max() - x.min(), y.max() - y.min())
    x0, y0 = x.min(), y.min()

    sizes = span / (2.0 ** np.arange(1, n_scales + 1))
    counts = np.empty(len(sizes), dtype=int)

    for k, s in enumerate(sizes):
        i = ((x - x0) / s).astype(np.int64)
        j = ((y - y0) / s).astype(np.int64)
        counts[k] = len(np.unique(i * (10**9) + j))  # cheap 2D uniqueness

    return sizes, counts


def estimate_dimension(sizes: np.ndarray, counts: np.ndarray) -> float:
    """Least-squares slope of log(counts) vs log(1/sizes)."""
    log_inv_s = np.log(1.0 / sizes)
    log_n = np.log(counts.astype(float))
    slope, _ = np.polyfit(log_inv_s, log_n, 1)
    return float(slope)

def mandelbrot_contains(c: complex, max_iter: int = 200,
                        escape_radius: float = 2.0) -> bool:
    """Is c in the Mandelbrot set? Critical orbit stays bounded iff yes."""
    z = 0j
    for _ in range(max_iter):
        z = z * z + c
        if abs(z) > escape_radius:
            return False
    return True