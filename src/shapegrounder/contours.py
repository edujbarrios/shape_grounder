from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.image import preprocess_image


@dataclass(frozen=True, slots=True)
class ContourGroup:
    outer: np.ndarray
    inners: list[np.ndarray]


def _contour_area(contour: np.ndarray) -> float:
    return float(cv2.contourArea(contour))


def extract_contours(image: np.ndarray, config: ShapeGrounderConfig) -> list[ContourGroup]:
    pre = preprocess_image(image, config)
    contours, hierarchy = cv2.findContours(pre.edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    if hierarchy is None or len(contours) == 0:
        return []

    h = hierarchy[0]
    groups: list[ContourGroup] = []

    for idx, contour in enumerate(contours):
        parent_idx = int(h[idx][3])
        if parent_idx != -1:
            continue

        area = _contour_area(contour)
        if area < config.min_area:
            continue
        if config.max_area is not None and area > config.max_area:
            continue

        inners: list[np.ndarray] = []
        child_idx = int(h[idx][2])
        while child_idx != -1:
            child = contours[child_idx]
            if _contour_area(child) > 0.0:
                inners.append(child)
            child_idx = int(h[child_idx][0])

        groups.append(ContourGroup(outer=contour, inners=inners))

    return groups
