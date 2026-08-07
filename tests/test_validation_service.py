import pytest
from unittest.mock import patch, MagicMock
from api.services.validation_service import ValidationService, ValidationError

@pytest.fixture
def validator():
    return ValidationService(openai_api_key="test-key")

def test_validate_idea_success(validator):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='{"score": 85, "text": "Valid idea", "features": ["Feature1", "Feature2", "Feature3"]}'))]
    with patch("openai.ChatCompletion.create", return_value=mock_response):
        score, text, features = validator.validate_idea("Test idea", ["Tech"])
        assert score == 85
        assert text == "Valid idea"
        assert features == ["Feature1", "Feature2", "Feature3"]

def test_validate_idea_invalid_json(validator):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='Invalid JSON'))]
    with patch("openai.ChatCompletion.create", return_value=mock_response):
        with pytest.raises(ValidationError):
            validator.validate_idea("Test", ["Tech"])

def test_validate_idea_missing_keys(validator):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='{"score": 85, "text": "Valid"}'))]
    with patch("openai.ChatCompletion.create", return_value=mock_response):
        with pytest.raises(ValidationError):
            validator.validate_idea("Test", ["Tech"])