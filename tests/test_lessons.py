import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import sys

from fractal_lab import lessons


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