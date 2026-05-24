from __future__ import annotations

import math

import cv2
import numpy as np

from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.contours import ContourGroup
from shapegrounder.schemas import BoundingBox, Point2D, ShapeFeatures, SymmetryLabel


def _perimeter(contour: np.ndarray) -> float:
    return float(cv2.arcLength(contour, True))


def _area(contour: np.ndarray) -> float:
    return float(cv2.contourArea(contour))


def circularity(area: float, perimeter: float) -> float:
    if perimeter <= 0:
        return 0.0
    return float((4.0 * math.pi * area) / (perimeter * perimeter))


def _approx_vertices(contour: np.ndarray, epsilon_ratio: float) -> tuple[np.ndarray, int]:
    peri = _perimeter(contour)
    approx = cv2.approxPolyDP(contour, epsilon_ratio * peri, True)
    return approx, int(len(approx))


def _centroid(contour: np.ndarray) -> Point2D:
    moments = cv2.moments(contour)
    if moments["m00"] == 0:
        x, y, w, h = cv2.boundingRect(contour)
        return Point2D(x=float(x + w / 2.0), y=float(y + h / 2.0))
    return Point2D(
        x=float(moments["m10"] / moments["m00"]),
        y=float(moments["m01"] / moments["m00"]),
    )


def _contour_primitive_label(contour: np.ndarray, config: ShapeGrounderConfig) -> str:
    a = _area(contour)
    p = _perimeter(contour)
    c = circularity(a, p)
    x, y, w, h = cv2.boundingRect(contour)
    aspect = float(w / h) if h else 0.0

    approx, n = _approx_vertices(contour, config.polygon_epsilon)
    is_convex = bool(cv2.isContourConvex(approx))

    if c >= config.circularity_threshold and 0.8 <= aspect <= 1.25:
        return "circle"
    if is_convex and n == 4:
        return "rectangle"
    if is_convex and n >= 5:
        if 0.6 <= c < config.circularity_threshold:
            return "ellipse"
        return "polygon"
    return "irregular"


def _symmetry_label(
    circularity_value: float, aspect_ratio: float, approx_vertices: int, config: ShapeGrounderConfig
) -> SymmetryLabel:
    if circularity_value >= config.circularity_threshold and 0.8 <= aspect_ratio <= 1.25:
        return "radial"
    if approx_vertices in {4, 5, 6} and 0.5 <= aspect_ratio <= 2.0:
        return "bilateral"
    return "unknown"


def compute_features(
    contour: np.ndarray | ContourGroup, config: ShapeGrounderConfig
) -> ShapeFeatures:
    if isinstance(contour, ContourGroup):
        outer = contour.outer
        inners = contour.inners
    else:
        outer = contour
        inners = []

    a = _area(outer)
    p = _perimeter(outer)
    x, y, w, h = cv2.boundingRect(outer)
    aspect = float(w / h) if h else 0.0
    circ = circularity(a, p)
    approx, n_vertices = _approx_vertices(outer, config.polygon_epsilon)
    is_convex = bool(cv2.isContourConvex(approx))

    inner_labels: list[str] = []
    inner_area_sum = 0.0
    for inner in inners:
        inner_area = _area(inner)
        inner_area_sum += inner_area
        inner_labels.append(_contour_primitive_label(inner, config))

    hole_ratio = (inner_area_sum / a) if a > 0 else None
    has_hole = bool(
        config.hole_detection
        and inners
        and hole_ratio is not None
        and hole_ratio >= 0.01
        and any(label in {"circle", "ellipse", "polygon"} for label in inner_labels)
    )

    outer_label = _contour_primitive_label(outer, config)
    symmetry = (
        _symmetry_label(
            circularity_value=circ, aspect_ratio=aspect, approx_vertices=n_vertices, config=config
        )
        if config.symmetry_detection
        else "unknown"
    )

    return ShapeFeatures(
        area=a,
        perimeter=p,
        aspect_ratio=aspect,
        circularity=circ,
        approx_vertices=n_vertices,
        is_convex=is_convex,
        centroid=_centroid(outer),
        bounding_box=BoundingBox(x=int(x), y=int(y), w=int(w), h=int(h)),
        symmetry=symmetry,
        outer_contour=outer_label,
        inner_contours=inner_labels,
        has_hole=has_hole,
        hole_area_ratio=hole_ratio if has_hole else None,
    )
