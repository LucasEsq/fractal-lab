# The Mandelbrot set is a map of c: pick a point and see its Julia set.
from __future__ import annotations

import os
import matplotlib.pyplot as plt

from ..render import mandelbrot, julia, mandelbrot_contains
from ..palettes import MANDELBROT_CMAP, JULIA_CMAP

M_EXTENT = [-2.5, 1.0, -1.25, 1.25]

# (c, label) pairs used by the static fallback and the notebook.
SAMPLE_POINTS = [
    (complex(-0.122561, 0.744862), "Douady rabbit"),
    (complex(-1.0, 0.0), "Basilica"),
    (complex(0.285, 0.01), "Dendrite"),
    (complex(0.4, 0.4), "Outside: dust"),
]


def _draw_map(ax, m, c):
    ax.imshow(m, cmap=MANDELBROT_CMAP, extent=M_EXTENT, origin="lower")
    ax.plot([c.real], [c.imag], marker="o", color="white",
            markeredgecolor="black", markersize=8)
    ax.set_title("Mandelbrot set (the space of c)", fontsize=11)
    ax.axis("off")


def mandelbrot_map(resolution=300, max_iter=80, force_static=False):
    # Side-by-side Mandelbrot map and Julia set. Falls back to a static figure.
    force_static = force_static or bool(os.environ.get("FRACTAL_LAB_STATIC"))
    if force_static:
        return _static_fallback(resolution, max_iter)

    try:
        import ipywidgets as widgets
    except ImportError:
        return _static_fallback(resolution, max_iter)

    m = mandelbrot(width=resolution, height=int(resolution * 0.714),
                   max_iter=max_iter)
    out = widgets.Output()

    def render(real, imag):
        with out:
            out.clear_output(wait=True)
            c = complex(real, imag)
            div = julia(c, width=resolution, height=resolution, max_iter=max_iter)

            fig, (ax_m, ax_j) = plt.subplots(1, 2, figsize=(11, 5))
            _draw_map(ax_m, m, c)
            ax_j.imshow(div, cmap=JULIA_CMAP, extent=[-2, 2, -2, 2], origin="lower")
            inside = mandelbrot_contains(c, max_iter=200)
            ax_j.set_title(
                f"Julia set, c = {real:+.3f} {imag:+.3f}i "
                f"({'connected' if inside else 'dust'})",
                fontsize=11,
            )
            ax_j.axis("off")
            fig.tight_layout()

            from IPython.display import display
            display(fig)
            plt.close(fig)

    real_slider = widgets.FloatSlider(
        value=-0.12, min=-2.0, max=1.0, step=0.005,
        description="Re(c)", continuous_update=False,
    )
    imag_slider = widgets.FloatSlider(
        value=0.74, min=-1.25, max=1.25, step=0.005,
        description="Im(c)", continuous_update=False,
    )

    def on_change(_):
        render(real_slider.value, imag_slider.value)

    real_slider.observe(on_change, names="value")
    imag_slider.observe(on_change, names="value")
    render(real_slider.value, imag_slider.value)

    return widgets.VBox([widgets.HBox([real_slider, imag_slider]), out])


def _static_fallback(resolution, max_iter):
    # Non-Jupyter fallback: the map with sample points, and their Julia sets.
    m = mandelbrot(width=resolution, height=int(resolution * 0.714),
                   max_iter=max_iter)
    fig = plt.figure(figsize=(12, 7))
    gs = fig.add_gridspec(2, len(SAMPLE_POINTS), height_ratios=[1.3, 1])

    ax_m = fig.add_subplot(gs[0, :])
    ax_m.imshow(m, cmap=MANDELBROT_CMAP, extent=M_EXTENT, origin="lower")
    for k, (c, _) in enumerate(SAMPLE_POINTS, start=1):
        ax_m.plot([c.real], [c.imag], "o", color="white",
                  markeredgecolor="black", markersize=8)
        ax_m.annotate(str(k), (c.real, c.imag), xytext=(6, 6),
                      textcoords="offset points", color="white", fontsize=11)
    ax_m.set_title("Mandelbrot set: each point is a choice of c", fontsize=12)
    ax_m.axis("off")

    for k, (c, name) in enumerate(SAMPLE_POINTS):
        ax = fig.add_subplot(gs[1, k])
        div = julia(c, width=resolution, height=resolution, max_iter=max_iter)
        ax.imshow(div, cmap=JULIA_CMAP, extent=[-2, 2, -2, 2], origin="lower")
        ax.set_title(f"{k + 1}. {name}\nc = {c.real:+.3f} {c.imag:+.3f}i",
                     fontsize=10)
        ax.axis("off")
    fig.tight_layout()
    return fig
