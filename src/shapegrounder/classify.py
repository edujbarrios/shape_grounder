from __future__ import annotations

from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.schemas import ShapeFeatures, ShapeLabel


def classify_shape(features: ShapeFeatures, config: ShapeGrounderConfig) -> ShapeLabel:
    outer = features.outer_contour

    if features.has_hole and config.hole_detection and outer == "circle":
        ratio = features.hole_area_ratio or 0.0
        if features.symmetry == "radial":
            if ratio >= 0.75:
                return "ring"
            if ratio >= 0.3:
                return "annulus"
            return "thin_disc"
        if ratio >= 0.5:
            return "ring"
        return "annulus"

    if outer == "circle":
        return "circle"
    if outer == "ellipse":
        return "ellipse"
    if outer == "rectangle":
        return "rectangle"
    if outer == "polygon":
        return "polygon"
    return "irregular"
