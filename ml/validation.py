from pydantic import BaseModel, ValidationError, validator, Field
from typing import Optional, Dict, Any
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class TextInput(BaseModel):
    """
    Схема для валидации входных данных ML модели
    """
    text: str = Field(..., min_length=1, max_length=2048, example="I love machine learning!")
    max_length: Optional[int] = Field(512, ge=16, le=2048, description="Максимальная длина токенизированного текста")
    temperature: Optional[float] = Field(1.0, ge=0.1, le=2.0)
    top_k: Optional[int] = Field(50, ge=1, le=100)
    top_p: Optional[float] = Field(0.95, ge=0.1, le=1.0)
    num_return_sequences: Optional[int] = Field(1, ge=1, le=5)

    class Config:
        schema_extra = {
            "example": {
                "text": "Artificial intelligence will revolutionize",
                "max_length": 100,
                "temperature": 0.7,
                "top_k": 30,
                "top_p": 0.9,
                "num_return_sequences": 3
            }
        }

    @validator('text')
    def validate_text_content(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Text cannot be empty")
        if len(v) > 2048:
            logger.warning(f"Input text too long: {len(v)} characters")
        return v

    @validator('max_length')
    def validate_max_length(cls, v, values):
        if 'text' in values and v < len(values['text']):
            logger.warning(f"Truncating text from {len(values['text'])} to {v} characters")
        return v

def validate_prediction_input(data: Dict[str, Any], model_config: Dict[str, Any] = None) -> TextInput:
    """
    Валидация входных данных с учетом конфигурации модели
    """
    try:
        validated = TextInput(**data)
        
        # Дополнительная проверка параметров модели
        if model_config:
            if validated.max_length > model_config.get('max_length', 512):
                raise ValueError(f"Max length exceeds model limit ({model_config['max_length']})")
            
            if validated.num_return_sequences > model_config.get('max_sequences', 5):
                raise ValueError("Too many return sequences requested")

        return validated
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=422,
            detail=[{"loc": err["loc"], "msg": err["msg"], "type": err["type"]} for err in e.errors()]
        )
    except ValueError as e:
        logger.error(f"Custom validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={"message": str(e)}
        )
