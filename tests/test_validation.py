from app.services.validation import IdeaValidationService

def test_validation_score():
    score = IdeaValidationService.validate("This is a marketable idea with profit potential")
    assert score >= 70