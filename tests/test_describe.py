from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.describe import describe_shape
from shapegrounder.schemas import BoundingBox, Point2D, ShapeAnalysis, ShapeFeatures


def test_describe_thin_disc_en() -> None:
    cfg = ShapeGrounderConfig(language="en")
    features = ShapeFeatures(
        area=1.0,
        perimeter=1.0,
        aspect_ratio=1.0,
        circularity=0.95,
        approx_vertices=32,
        is_convex=True,
        centroid=Point2D(x=0.0, y=0.0),
        bounding_box=BoundingBox(x=0, y=0, w=1, h=1),
        symmetry="radial",
        outer_contour="circle",
        inner_contours=["circle"],
        has_hole=True,
        hole_area_ratio=0.05,
    )
    analysis = ShapeAnalysis(shape="thin_disc", features=features, description="", language="en")
    assert (
        describe_shape(analysis, cfg)
        == "A thin circular disc with a small circular hole in the center."
    )


def test_describe_thin_disc_es() -> None:
    cfg = ShapeGrounderConfig(language="es")
    features = ShapeFeatures(
        area=1.0,
        perimeter=1.0,
        aspect_ratio=1.0,
        circularity=0.95,
        approx_vertices=32,
        is_convex=True,
        centroid=Point2D(x=0.0, y=0.0),
        bounding_box=BoundingBox(x=0, y=0, w=1, h=1),
        symmetry="radial",
        outer_contour="circle",
        inner_contours=["circle"],
        has_hole=True,
        hole_area_ratio=0.05,
    )
    analysis = ShapeAnalysis(shape="thin_disc", features=features, description="", language="es")
    assert (
        describe_shape(analysis, cfg)
        == "Un disco circular delgado con un pequeño orificio circular en el centro."
    )
