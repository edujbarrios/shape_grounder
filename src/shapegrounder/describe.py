from __future__ import annotations

from typing import Literal

from shapegrounder.config import ShapeGrounderConfig
from shapegrounder.schemas import ShapeAnalysis


def describe_shape(
    analysis: ShapeAnalysis,
    config: ShapeGrounderConfig,
    *,
    mode: Literal["templates", "llm"] = "templates",
) -> str:
    if mode != "templates":
        raise NotImplementedError(
            "LLM rewriting is not available in the MVP. Use mode='templates' only."
        )

    shape = analysis.shape
    f = analysis.features
    lang = config.language

    if lang == "es":
        if shape == "thin_disc" and f.has_hole:
            return "Un disco circular delgado con un pequeño orificio circular en el centro."
        if shape == "annulus" and f.has_hole:
            return "Un anillo circular con un orificio circular."
        if shape == "ring" and f.has_hole:
            return "Un anillo muy delgado con un orificio circular grande."
        if shape == "circle":
            return "Una forma circular."
        if shape == "ellipse":
            return "Una forma elíptica."
        if shape == "rectangle":
            return "Una forma rectangular."
        if shape == "polygon":
            sides = f.approx_vertices
            return f"Una forma poligonal con aproximadamente {sides} lados."
        return "Una forma irregular."

    if shape == "thin_disc" and f.has_hole:
        return "A thin circular disc with a small circular hole in the center."
    if shape == "annulus" and f.has_hole:
        return "A circular annulus with a circular hole."
    if shape == "ring" and f.has_hole:
        return "A thin circular ring with a large circular hole."
    if shape == "circle":
        return "A circular shape."
    if shape == "ellipse":
        return "An elliptical shape."
    if shape == "rectangle":
        return "A rectangular shape."
    if shape == "polygon":
        sides = f.approx_vertices
        return f"A polygonal shape with approximately {sides} sides."
    return "An irregular shape."
