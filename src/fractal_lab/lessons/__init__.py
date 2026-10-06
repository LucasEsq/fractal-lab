"""Each lesson is a single function call that opens an interactive demo."""
from .julia_explorer import julia_explorer

__all__ = ["julia_explorer", "list"]


def list() -> list[str]:
    """Names of available lessons."""
    return ["julia_explorer"]