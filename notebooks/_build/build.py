# Regenerate executed .ipynb files from jupytext .py sources.
# Run: python notebooks/_build/build.py
from __future__ import annotations

import base64
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]  # notebooks/
GALLERY = ROOT.parent / "docs" / "gallery"


def find_sources():
    return sorted(p for p in ROOT.glob("[0-9]*.py"))


def convert_to_notebook(src):
    # Convert jupytext .py source to .ipynb using the current interpreter.
    out = src.with_suffix(".ipynb")
    subprocess.run(
        [
            sys.executable, "-m", "jupytext",
            "--to", "notebook",
            "--output", str(out),
            str(src),
        ],
        check=True,
    )
    return out


def execute(nb):
    # Execute the notebook in place, forcing the static fallback.
    env = {**os.environ, "FRACTAL_LAB_STATIC": "1"}
    subprocess.run(
        [
            sys.executable, "-m", "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute", "--inplace",
            "--ExecutePreprocessor.timeout=180",
            "--ExecutePreprocessor.kernel_name=fractal-lab",
            str(nb),
        ],
        check=True,
        env=env,
    )


def extract_first_figure(nb):
    # Save the notebook's first PNG output to docs/gallery/.
    import nbformat

    GALLERY.mkdir(parents=True, exist_ok=True)
    node = nbformat.read(nb, as_version=4)

    for cell in node.cells:
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            if "image/png" in data:
                out = GALLERY / f"{nb.stem}.png"
                out.write_bytes(base64.b64decode(data["image/png"]))
                print(f"  -> {out.relative_to(ROOT.parent)}")
                return

    print(f"  (no PNG output found in {nb.name})")


def main():
    sources = find_sources()
    if not sources:
        print("No notebooks found.", file=sys.stderr)
        return 1

    for src in sources:
        print(f"Building {src.name} ...")
        nb = convert_to_notebook(src)
        execute(nb)
        extract_first_figure(nb)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())