"""Unit tests for validation and MVP generation services."""

import pytest
from app.services.idea_validation_service import validate_idea
from app.services.mvp_generation_service import generate_mvp


def test_validate_short_description():
    score = validate_idea("Short")
    assert score == 40.0


def test_validate_keyword_score():
    desc = "This idea solves a market problem with a unique value proposition."
    score = validate_idea(desc)
    assert score >= 70.0


def test_generate_mvp_structure():
    blueprint = generate_mvp("test-idea-id")
    assert "wireframes" in blueprint
    assert "feature_list" in blueprint
    assert "tech_stack" in blueprint
    assert "timeline" in blueprint
    assert os.path.exists(blueprint["pdf_path"])