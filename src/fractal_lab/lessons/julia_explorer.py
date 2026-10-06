# Drag two sliders to morph the Julia set — see how c controls everything.
from __future__ import annotations

import os
import matplotlib.pyplot as plt

from ..render import julia, mandelbrot_contains
from ..palettes import JULIA_CMAP


def julia_explorer(resolution=300, max_iter=80, force_static=False):
    # Interactive Julia set explorer. Works in Jupyter; falls back to static.
    force_static = force_static or bool(os.environ.get("FRACTAL_LAB_STATIC"))
    if force_static:
        return _static_fallback(resolution, max_iter)

    try:
        import ipywidgets as widgets
    except ImportError:
        return _static_fallback(resolution, max_iter)

    out = widgets.Output()

    def render(real, imag):
        with out:
            out.clear_output(wait=True)

            c = complex(real, imag)
            div = julia(c, width=resolution, height=resolution, max_iter=max_iter)

            fig, ax = plt.subplots(figsize=(6, 6))
            ax.imshow(div, cmap=JULIA_CMAP, extent=[-2, 2, -2, 2], origin="lower")
            ax.axis("off")

            inside = mandelbrot_contains(c, max_iter=200)
            status = "connected (c in M)" if inside else "dust (c not in M)"
            ax.set_title(
                f"c = {real:+.4f} {imag:+.4f}i   -   {status}",
                fontsize=11,
            )

            from IPython.display import display
            display(fig)
            plt.close(fig)

    real_slider = widgets.FloatSlider(
        value=-0.7, min=-2.0, max=2.0, step=0.005,
        description="Re(c)", continuous_update=True,
    )
    imag_slider = widgets.FloatSlider(
        value=0.27, min=-2.0, max=2.0, step=0.005,
        description="Im(c)", continuous_update=True,
    )

    def on_change(_):
        render(real_slider.value, imag_slider.value)

    real_slider.observe(on_change, names="value")
    imag_slider.observe(on_change, names="value")

    render(real_slider.value, imag_slider.value)

    return widgets.VBox([
        widgets.HBox([real_slider, imag_slider]),
        out,
    ])


def _static_fallback(resolution, max_iter):
    # Non-Jupyter fallback: 6 named examples in a 2x3 grid.
    cs = [
        (complex(-0.122561, 0.744862), "Douady rabbit"),
        (complex( 0.285,   0.01),  "Dendrite"),
        (complex(-0.8,     0.156), "Dragon"),
        (complex(-0.4,     0.6),   "Siegel disk"),
        (complex(-1.75488, 0.0),   "Airplane"),
        (complex( 0.0,     0.0),   "Unit circle"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    for ax, (c, name) in zip(axes.ravel(), cs):
        div = julia(c, width=resolution, height=resolution, max_iter=max_iter)
        ax.imshow(div, cmap=JULIA_CMAP, extent=[-2, 2, -2, 2], origin="lower")
        ax.set_title(f"{name}\nc = {c.real:+.4f} {c.imag:+.4f}i", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    return fig