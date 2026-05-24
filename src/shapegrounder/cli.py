from __future__ import annotations

import json
from typing import Literal

import typer

from shapegrounder.api import analyze_image
from shapegrounder.config import ShapeGrounderConfig

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.callback()
def _main() -> None:
    """Geometry-first object shape analysis."""


@app.command()
def analyze(
    image_path: str,
    threshold_method: Literal["otsu", "adaptive", "manual"] = typer.Option(
        "otsu", "--threshold-method"
    ),
    manual_threshold: int | None = typer.Option(None, "--manual-threshold"),
    blur_kernel: int = typer.Option(5, "--blur-kernel"),
    canny_low: int = typer.Option(50, "--canny-low"),
    canny_high: int = typer.Option(150, "--canny-high"),
    min_area: float = typer.Option(100.0, "--min-area"),
    max_area: float | None = typer.Option(None, "--max-area"),
    circularity_threshold: float = typer.Option(0.85, "--circularity-threshold"),
    ellipse_ratio_threshold: float = typer.Option(1.2, "--ellipse-ratio-threshold"),
    rectangle_epsilon: float = typer.Option(0.02, "--rectangle-epsilon"),
    polygon_epsilon: float = typer.Option(0.02, "--polygon-epsilon"),
    hole_detection: bool = typer.Option(True, "--hole-detection/--no-hole-detection"),
    symmetry_detection: bool = typer.Option(True, "--symmetry-detection/--no-symmetry-detection"),
    describe_material: bool = typer.Option(False, "--describe-material/--no-describe-material"),
    language: Literal["en", "es"] = typer.Option("en", "--language"),
    output: Literal["json", "text", "both"] = typer.Option("both", "--output"),
    pretty: bool = typer.Option(False, "--pretty"),
) -> None:
    config = ShapeGrounderConfig(
        threshold_method=threshold_method,
        manual_threshold=manual_threshold,
        blur_kernel=blur_kernel,
        canny_low=canny_low,
        canny_high=canny_high,
        min_area=min_area,
        max_area=max_area,
        circularity_threshold=circularity_threshold,
        ellipse_ratio_threshold=ellipse_ratio_threshold,
        rectangle_epsilon=rectangle_epsilon,
        polygon_epsilon=polygon_epsilon,
        hole_detection=hole_detection,
        symmetry_detection=symmetry_detection,
        describe_material=describe_material,
        language=language,
        output_format=output,
    )

    analysis = analyze_image(image_path, config=config)

    if output in {"json", "both"}:
        payload = analysis.model_dump(mode="json")
        if pretty:
            typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            typer.echo(json.dumps(payload, separators=(",", ":"), ensure_ascii=False))

    if output in {"text", "both"}:
        typer.echo(analysis.description)
