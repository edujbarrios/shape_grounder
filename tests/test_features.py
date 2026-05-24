import math

import cv2
import numpy as np
import pytest

from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.contours import extract_contours
from shapegrounder.features import circularity, compute_features


def test_circularity_formula_for_perfect_circle() -> None:
    r = 10.0
    area = math.pi * r * r
    perimeter = 2.0 * math.pi * r
    assert circularity(area, perimeter) == pytest.approx(1.0, abs=1e-9)


def test_compute_features_sets_has_hole_for_donut_contour_group() -> None:
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.circle(image, (100, 100), 60, (255, 255, 255), thickness=-1)
    cv2.circle(image, (100, 100), 20, (0, 0, 0), thickness=-1)

    cfg = ShapeGrounderConfig(min_area=10.0)
    group = max(extract_contours(image, cfg), key=lambda g: cv2.contourArea(g.outer))
    features = compute_features(group, cfg)
    assert features.has_hole is True
    assert features.hole_area_ratio is not None
