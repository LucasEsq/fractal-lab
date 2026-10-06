# Notebooks

Interactive lessons. **Previews render directly on GitHub** — click any
`.ipynb` file to see the executed output without cloning anything.

| # | Lesson | Preview | Run it |
|---|--------|---------|--------|
| 1 | What does `c` actually do? | [📓](01_julia_explorer.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/YOURNAME/fractal-lab/main?labpath=notebooks/01_julia_explorer.ipynb) |

## Regenerating

Notebooks are built from jupytext `.py` sources. Edit the `.py`, then:

```bash
python notebooks/_build/build.py