from shapegrounder.schemas import ShapeAnalysis


def test_shapeanalysis_json_schema_is_available() -> None:
    schema = ShapeAnalysis.model_json_schema()
    assert schema["title"] == "ShapeAnalysis"


def test_shapeanalysis_dump_roundtrips() -> None:
    # Minimal round-trip validation of the JSON-compatible payload.
    payload = {
        "shape": "circle",
        "features": {
            "area": 1.0,
            "perimeter": 1.0,
            "aspect_ratio": 1.0,
            "circularity": 1.0,
            "approx_vertices": 8,
            "is_convex": True,
            "centroid": {"x": 0.0, "y": 0.0},
            "bounding_box": {"x": 0, "y": 0, "w": 1, "h": 1},
            "symmetry": "radial",
            "outer_contour": "circle",
            "inner_contours": [],
            "has_hole": False,
            "hole_area_ratio": None,
            "extra": {},
        },
        "description": "A circular shape.",
        "language": "en",
        "image_path": None,
    }
    ShapeAnalysis.model_validate(payload)
