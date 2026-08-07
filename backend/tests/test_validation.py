import pytest
from ..api.services.validation_service import ValidationService
from ..api.schemas.idea import IdeaCreate

@pytest.mark.asyncio
async def test_validate_idea():
    service = ValidationService()
    payload = IdeaCreate(user_id="user-123", description="Test idea", industry_tags=["tech"])
    result = await service.validate_idea(payload)
    assert result.validation_score == 0.75
    assert len(result.recommended_features) == 3