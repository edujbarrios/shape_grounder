from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

ShapeLabel = Literal[
    "circle",
    "ellipse",
    "rectangle",
    "polygon",
    "ring",
    "annulus",
    "thin_disc",
    "irregular",
]

SymmetryLabel = Literal["radial", "bilateral", "none", "unknown"]


class BoundingBox(BaseModel):
    x: int
    y: int
    w: int
    h: int


class Point2D(BaseModel):
    x: float
    y: float


class ShapeFeatures(BaseModel):
    area: float
    perimeter: float
    aspect_ratio: float
    circularity: float
    approx_vertices: int
    is_convex: bool
    centroid: Point2D
    bounding_box: BoundingBox
    symmetry: SymmetryLabel = "unknown"
    outer_contour: str = "unknown"
    inner_contours: list[str] = Field(default_factory=list)
    has_hole: bool = False
    hole_area_ratio: float | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class ShapeAnalysis(BaseModel):
    shape: ShapeLabel
    features: ShapeFeatures
    description: str
    language: Literal["en", "es"] = "en"
    image_path: str | None = None
