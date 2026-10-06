import numpy as np
import pytest

from fractal_lab.render import julia, mandelbrot_contains


def test_julia_returns_correct_shape():
    div = julia(complex(-0.7, 0.27), width=64, height=64, max_iter=40)
    assert div.shape == (64, 64)


def test_julia_dtype_is_integer():
    div = julia(complex(-0.7, 0.27), width=32, height=32, max_iter=20)
    assert np.issubdtype(div.dtype, np.integer)


def test_julia_range_within_max_iter():
    max_iter = 50
    div = julia(complex(-0.4, 0.6), width=80, height=80, max_iter=max_iter)
    assert div.min() >= 0
    assert div.max() <= max_iter - 1


def test_julia_has_variation():
    # A non-degenerate Julia set should not produce a constant array.
    div = julia(complex(-0.7, 0.27), width=100, height=100, max_iter=60)
    assert np.unique(div).size > 1


def test_julia_different_c_gives_different_output():
    a = julia(complex(-0.7, 0.27), width=64, height=64, max_iter=40)
    b = julia(complex(-0.4, 0.6), width=64, height=64, max_iter=40)
    assert not np.array_equal(a, b)


def test_mandelbrot_contains_inside():
    assert mandelbrot_contains(0j) is True
    assert mandelbrot_contains(complex(-1.0, 0.0)) is True
    assert mandelbrot_contains(complex(-0.5, 0.0)) is True
    assert mandelbrot_contains(complex(-0.122561, 0.744862), max_iter=500) is True


def test_mandelbrot_contains_outside():
    # c = 1 escapes immediately (1 -> 2 -> 5 -> ...).
    assert mandelbrot_contains(complex(1.0, 0.0)) is False
    # Far outside the set.
    assert mandelbrot_contains(complex(-0.8, 0.8)) is False


def test_mandelbrot_contains_boundary_is_stable():
    # A point slightly off the boundary shouldn't flip on repeated calls.
    c = complex(-0.75, 0.1)
    first = mandelbrot_contains(c, max_iter=200)
    second = mandelbrot_contains(c, max_iter=200)
    assert first == second