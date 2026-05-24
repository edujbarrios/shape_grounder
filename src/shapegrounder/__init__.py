"""ShapeGrounder: deterministic, geometry-first shape analysis for images."""

from __future__ import annotations

from shapegrounder.api import analyze_image
from shapegrounder.classify import classify_shape
from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.contours import extract_contours
from shapegrounder.describe import describe_shape
from shapegrounder.features import compute_features
from shapegrounder.schemas import ShapeAnalysis

__all__ = [
    "__version__",
    "ShapeAnalysis",
    "ShapeGrounderConfig",
    "analyze_image",
    "classify_shape",
    "compute_features",
    "describe_shape",
    "extract_contours",
]

__version__ = "0.1.0"
