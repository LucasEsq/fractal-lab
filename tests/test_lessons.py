import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import sys

from fractal_lab import lessons
from fractal_lab.lessons.mandelbrot_map import SAMPLE_POINTS


def test_lessons_registry():
    assert "julia_explorer" in lessons.list()


def test_julia_lesson_returns_figure_in_static_mode(monkeypatch):
    # Force the static fallback so we can inspect the returned figure
    # without needing ipywidgets.
    monkeypatch.setenv("FRACTAL_LAB_STATIC", "1")
    result = lessons.julia_explorer(resolution=80, max_iter=20)
    assert result is not None
    # matplotlib Figure
    assert hasattr(result, "savefig")
    assert len(result.axes) == 6
    plt.close("all")

def test_registry_lists_both_lessons():
    assert lessons.list() == ["julia_explorer", "mandelbrot_map"]


def test_mandelbrot_map_returns_figure_in_static_mode(monkeypatch):
    monkeypatch.setenv("FRACTAL_LAB_STATIC", "1")
    result = lessons.mandelbrot_map(resolution=80, max_iter=20)
    assert hasattr(result, "savefig")
    # One Mandelbrot map plus one Julia set per sample point.
    assert len(result.axes) == 1 + len(SAMPLE_POINTS)
    plt.close("all")
