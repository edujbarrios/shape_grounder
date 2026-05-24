from __future__ import annotations

from shapegrounder.classify import classify_shape
from shapegrounder.config import DEFAULT_CONFIG, ShapeGrounderConfig
from shapegrounder.contours import extract_contours
from shapegrounder.describe import describe_shape
from shapegrounder.features import compute_features
from shapegrounder.image import load_image
from shapegrounder.schemas import ShapeAnalysis


def analyze_image(path: str, config: ShapeGrounderConfig | None = None) -> ShapeAnalysis:
    cfg = config or DEFAULT_CONFIG
    image = load_image(path)

    groups = extract_contours(image, cfg)
    if not groups:
        raise ValueError(
            "No contours found after preprocessing; try adjusting thresholds/min_area."
        )

    largest = max(groups, key=lambda g: float(compute_features(g, cfg).area))
    features = compute_features(largest, cfg)
    shape = classify_shape(features, cfg)
    analysis = ShapeAnalysis(
        shape=shape, features=features, description="", language=cfg.language, image_path=path
    )
    analysis.description = describe_shape(analysis, cfg)
    return analysis
