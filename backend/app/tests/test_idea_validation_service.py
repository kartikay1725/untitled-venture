import pytest
from backend.app.services.idea_validation_service import IdeaValidationService

@pytest.mark.asyncio
async def test_validate_basic():
    service = IdeaValidationService()
    score, _ = await service.validate("This idea solves a market problem.")
    assert score >= 20