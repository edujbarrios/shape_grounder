import json

import cv2
import numpy as np
from typer.testing import CliRunner

from shapegrounder.cli import app


def test_cli_analyze_outputs_json(tmp_path) -> None:
    image = np.zeros((256, 256, 3), dtype=np.uint8)
    cv2.circle(image, (128, 128), 80, (255, 255, 255), thickness=-1)
    cv2.circle(image, (128, 128), 20, (0, 0, 0), thickness=-1)

    path = tmp_path / "disc.png"
    assert cv2.imwrite(str(path), image)

    runner = CliRunner()
    result = runner.invoke(app, ["analyze", str(path), "--output", "json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["shape"] == "thin_disc"
    assert payload["features"]["has_hole"] is True


def test_cli_analyze_text_only(tmp_path) -> None:
    image = np.zeros((128, 128, 3), dtype=np.uint8)
    cv2.rectangle(image, (30, 40), (100, 90), (255, 255, 255), thickness=-1)
    path = tmp_path / "rect.png"
    assert cv2.imwrite(str(path), image)

    runner = CliRunner()
    result = runner.invoke(app, ["analyze", str(path), "--output", "text"])
    assert result.exit_code == 0, result.output
    assert "rectangular" in result.output.lower()
