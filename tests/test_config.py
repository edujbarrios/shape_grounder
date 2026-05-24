import pytest

from shapegrounder.config import ShapeGrounderConfig


def test_config_requires_manual_threshold_for_manual_method() -> None:
    with pytest.raises(ValueError, match="manual_threshold is required"):
        ShapeGrounderConfig(threshold_method="manual", manual_threshold=None)


def test_config_rejects_even_blur_kernel() -> None:
    with pytest.raises(ValueError, match="blur_kernel must be odd"):
        ShapeGrounderConfig(blur_kernel=4)


def test_config_rejects_invalid_canny_range() -> None:
    with pytest.raises(ValueError, match="canny_low must be < canny_high"):
        ShapeGrounderConfig(canny_low=200, canny_high=100)
