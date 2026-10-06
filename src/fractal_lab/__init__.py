"""fractal-lab: interactive fractal education for Jupyter."""
from . import lessons
from .render import mandelbrot, julia, koch_snowflake_points, box_counts
from .palettes import MANDELBROT_CMAP, JULIA_CMAP, KOCH_CMAP

__version__ = "0.1.0"
__all__ = [
    "lessons",
    "mandelbrot", "julia", "koch_snowflake_points", "box_counts",
    "MANDELBROT_CMAP", "JULIA_CMAP", "KOCH_CMAP",
]