from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, field_validator, model_validator


class ShapeGrounderConfig(BaseModel):
    threshold_method: Literal["otsu", "adaptive", "manual"] = "otsu"
    manual_threshold: int | None = None
    blur_kernel: int = 5
    canny_low: int = 50
    canny_high: int = 150
    min_area: float = 100.0
    max_area: float | None = None
    circularity_threshold: float = 0.85
    ellipse_ratio_threshold: float = 1.2
    rectangle_epsilon: float = 0.02
    polygon_epsilon: float = 0.02
    hole_detection: bool = True
    symmetry_detection: bool = True
    describe_material: bool = False
    language: Literal["en", "es"] = "en"
    output_format: Literal["json", "text", "both"] = "both"

    @field_validator("manual_threshold")
    @classmethod
    def _validate_manual_threshold(cls, value: int | None) -> int | None:
        if value is None:
            return None
        if not (0 <= value <= 255):
            raise ValueError("manual_threshold must be between 0 and 255")
        return value

    @field_validator("blur_kernel")
    @classmethod
    def _validate_blur_kernel(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("blur_kernel must be > 0")
        if value % 2 == 0:
            raise ValueError("blur_kernel must be odd")
        return value

    @field_validator("canny_low", "canny_high")
    @classmethod
    def _validate_canny_thresholds(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("canny thresholds must be > 0")
        return value

    @field_validator("min_area")
    @classmethod
    def _validate_min_area(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("min_area must be > 0")
        return value

    @field_validator("max_area")
    @classmethod
    def _validate_max_area(cls, value: float | None) -> float | None:
        if value is None:
            return None
        if value <= 0:
            raise ValueError("max_area must be > 0")
        return value

    @field_validator("circularity_threshold", "ellipse_ratio_threshold")
    @classmethod
    def _validate_positive_float(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("threshold must be > 0")
        return value

    @field_validator("rectangle_epsilon", "polygon_epsilon")
    @classmethod
    def _validate_epsilon(cls, value: float) -> float:
        if not (0 < value < 0.25):
            raise ValueError("epsilon must be in (0, 0.25)")
        return value

    @model_validator(mode="after")
    def _validate_cross_fields(self) -> ShapeGrounderConfig:
        if self.threshold_method == "manual" and self.manual_threshold is None:
            raise ValueError("manual_threshold is required when threshold_method='manual'")
        if self.canny_low >= self.canny_high:
            raise ValueError("canny_low must be < canny_high")
        if self.max_area is not None and self.min_area >= self.max_area:
            raise ValueError("min_area must be < max_area when max_area is set")
        return self


DEFAULT_CONFIG = ShapeGrounderConfig()
