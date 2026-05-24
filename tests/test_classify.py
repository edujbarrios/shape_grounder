import cv2
import numpy as np

from shapegrounder.classify import classify_shape
from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.contours import extract_contours
from shapegrounder.features import compute_features


def _donut(size: int, outer_r: int, inner_r: int) -> np.ndarray:
    image = np.zeros((size, size, 3), dtype=np.uint8)
    center = (size // 2, size // 2)
    cv2.circle(image, center, outer_r, (255, 255, 255), thickness=-1)
    cv2.circle(image, center, inner_r, (0, 0, 0), thickness=-1)
    return image


def _classify_from_image(image: np.ndarray) -> str:
    cfg = ShapeGrounderConfig(min_area=50.0)
    group = max(extract_contours(image, cfg), key=lambda g: cv2.contourArea(g.outer))
    features = compute_features(group, cfg)
    return classify_shape(features, cfg)


def test_thin_disc_detection() -> None:
    assert _classify_from_image(_donut(256, 80, 20)) == "thin_disc"


def test_annulus_detection() -> None:
    assert _classify_from_image(_donut(256, 80, 50)) == "annulus"


def test_ring_detection() -> None:
    assert _classify_from_image(_donut(256, 80, 72)) == "ring"


def test_rectangle_detection() -> None:
    image = np.zeros((256, 256, 3), dtype=np.uint8)
    cv2.rectangle(image, (60, 80), (200, 180), (255, 255, 255), thickness=-1)
    cfg = ShapeGrounderConfig(min_area=50.0)
    group = max(extract_contours(image, cfg), key=lambda g: cv2.contourArea(g.outer))
    features = compute_features(group, cfg)
    assert classify_shape(features, cfg) == "rectangle"
