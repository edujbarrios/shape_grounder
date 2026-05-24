# shapegrounder

Geometry-first vision library that detects object shapes in images and converts them into:

- Structured `ShapeAnalysis` JSON
- Deterministic natural-language descriptions (templates only)

The MVP is **fully deterministic and rule-based**: it does **not** use any LLMs, local models, or external AI APIs.

## Why geometry-first (and no LLM in the MVP)

This project starts from contours and geometric features (area, perimeter, circularity, aspect ratio, holes, symmetry)
to provide transparent, debuggable shape recognition and descriptions.

An optional future "LLM rewriter" can be added later, but it must only rewrite from structured JSON and must never
invent attributes not present in `ShapeAnalysis`.

## Install (editable)

Python 3.10+

```bash
pip install -e .
```

For development (tests + Ruff):

```bash
pip install -e ".[dev]"
```

## CLI

Analyze an image:

```bash
shapegrounder analyze image.jpg
shapegrounder analyze disc.jpg --output both
shapegrounder analyze object.png --language es
shapegrounder analyze image.jpg --threshold-method adaptive
```

Useful options:

- `--threshold-method` (`otsu|adaptive|manual`)
- `--manual-threshold`
- `--blur-kernel`
- `--canny-low` / `--canny-high`
- `--min-area` / `--max-area`
- `--hole-detection/--no-hole-detection`
- `--symmetry-detection/--no-symmetry-detection`
- `--language` (`en|es`)
- `--output` (`json|text|both`)
- `--pretty` (pretty JSON)

## Python API

```python
from shapegrounder import ShapeGrounderConfig, analyze_image

config = ShapeGrounderConfig(language="en", min_area=200.0)
analysis = analyze_image("disc.jpg", config=config)

print(analysis.shape)
print(analysis.features.circularity)
print(analysis.description)
```

Public APIs:

- `analyze_image(path: str, config: ShapeGrounderConfig | None = None) -> ShapeAnalysis`
- `extract_contours(image, config)`
- `compute_features(contour, config)`
- `classify_shape(features, config)`
- `describe_shape(analysis, config)`

## Configuration

Configuration is a typed Pydantic model: `ShapeGrounderConfig` in `src/shapegrounder/config.py`.

It controls preprocessing and thresholds, including:

- `threshold_method`, `manual_threshold`
- `blur_kernel`, `canny_low`, `canny_high`
- `min_area`, `max_area`
- `circularity_threshold`, `ellipse_ratio_threshold`
- `rectangle_epsilon`, `polygon_epsilon`
- `hole_detection`, `symmetry_detection`
- `language`, `output_format`

## Optical disc example

For a thin circular disc with a centered hole (e.g., optical media), the analysis looks like:

```json
{
  "shape": "thin_disc",
  "features": {
    "outer_contour": "circle",
    "inner_contours": ["circle"],
    "has_hole": true,
    "symmetry": "radial",
    "circularity": 0.96
  }
}
```

Description (deterministic):

> A thin circular disc with a small circular hole in the center.

## Roadmap

- SAM segmentation backend
- YOLO proposals
- Rust geometry core
- WebAssembly demo
- Optional LLM rewriter (rewrite-only from `ShapeAnalysis`)
- More multilingual templates
- Industrial object analysis
