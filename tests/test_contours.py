import cv2
import numpy as np

from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.contours import extract_contours


def _donut_image(size: int = 256, outer_r: int = 80, inner_r: int = 25) -> np.ndarray:
    image = np.zeros((size, size, 3), dtype=np.uint8)
    center = (size // 2, size // 2)
    cv2.circle(image, center, outer_r, (255, 255, 255), thickness=-1)
    cv2.circle(image, center, inner_r, (0, 0, 0), thickness=-1)
    return image


def test_extract_contours_returns_outer_group() -> None:
    image = _donut_image()
    config = ShapeGrounderConfig(min_area=50.0)
    groups = extract_contours(image, config)
    assert len(groups) >= 1
    assert groups[0].outer is not None


def test_extract_contours_detects_inner_hole() -> None:
    image = _donut_image(inner_r=35)
    config = ShapeGrounderConfig(min_area=50.0)
    groups = extract_contours(image, config)
    assert len(groups) >= 1
    assert len(groups[0].inners) >= 1
