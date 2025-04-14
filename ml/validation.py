from pydantic import BaseModel, ValidationError
from typing import Optional
from fastapi import HTTPException

class TextInput(BaseModel):
    text: str
    max_length: Optional[int] = 512

def validate_prediction_input(data: dict):
    try:
        return TextInput(**data)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=e.errors()
        )
