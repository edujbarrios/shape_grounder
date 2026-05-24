from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from shapegrounder.config import ShapeGrounderConfig


@dataclass(frozen=True, slots=True)
class PreprocessedImage:
    bgr: np.ndarray
    gray: np.ndarray
    blurred: np.ndarray
    binary: np.ndarray
    edges: np.ndarray


def load_image(path: str) -> np.ndarray:
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read image at path: {path}")
    return image


def preprocess_image(image: np.ndarray, config: ShapeGrounderConfig) -> PreprocessedImage:
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Expected a BGR image with shape (H, W, 3)")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (config.blur_kernel, config.blur_kernel), 0)

    if config.threshold_method == "otsu":
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif config.threshold_method == "adaptive":
        binary = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )
    else:
        if config.manual_threshold is None:
            raise ValueError("manual_threshold is required when threshold_method='manual'")
        _, binary = cv2.threshold(blurred, config.manual_threshold, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(blurred, config.canny_low, config.canny_high)
    return PreprocessedImage(bgr=image, gray=gray, blurred=blurred, binary=binary, edges=edges)
