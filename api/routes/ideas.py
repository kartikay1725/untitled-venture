import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.idea import Idea
from ..schemas.idea import IdeaCreateRequest, IdeaResponse
from ..services.validation_service import ValidationService, ValidationError

router = APIRouter()

@router.post("/ideas", response_model=IdeaResponse, status_code=status.HTTP_201_CREATED)
def submit_idea(
    payload: IdeaCreateRequest,
    db: Session = Depends(get_db),
    validator: ValidationService = Depends(ValidationService),
):
    # Create Idea record (user_id would normally come from auth context)
    idea = Idea(
        user_id=uuid.uuid4(),
        description=payload.description,
        industry_tags=payload.industry_tags,
    )
    db.add(idea)
    db.commit()
    db.refresh(idea)

    # Validate using AI
    try:
        score, text, features = validator.validate_idea(payload.description, payload.industry_tags)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    # Persist validation results
    idea.validation_score = score
    idea.validation_text = text
    db.commit()
    db.refresh(idea)

    return IdeaResponse(
        ideaId=str(idea.id),
        validationScore=float(score),
        validationText=text,
        recommendedFeatures=features,
    )