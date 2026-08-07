from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from ..services.validation_service import ValidationService
from ..schemas.idea import IdeaCreate, IdeaResponse
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger()

@router.post("/", response_model=IdeaResponse, status_code=status.HTTP_201_CREATED)
async def create_idea(payload: IdeaCreate, service: ValidationService = Depends()):
    logger.info(f"Received idea submission from user {payload.user_id}")
    try:
        result = await service.validate_idea(payload)
        return result
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise HTTPException(status_code=500, detail="Validation service error")