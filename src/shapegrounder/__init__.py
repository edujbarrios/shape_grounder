"""ShapeGrounder: deterministic, geometry-first shape analysis for images."""

from __future__ import annotations

from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.schemas import ShapeAnalysis

__all__ = [
    "__version__",
    "ShapeAnalysis",
    "ShapeGrounderConfig",
]

__version__ = "0.1.0"
