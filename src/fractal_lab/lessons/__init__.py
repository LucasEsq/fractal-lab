"""Each lesson is a single function call that opens an interactive demo."""
from .julia_explorer import julia_explorer
from .mandelbrot_map import mandelbrot_map

__all__ = ["julia_explorer", "mandelbrot_map", "list"]


def list() -> list[str]:
    """Names of available lessons."""
    return ["julia_explorer", "mandelbrot_map"]
