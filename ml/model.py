import json
import logging
from typing import Dict, Any
from datetime import datetime
from uuid import UUID
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

logger = logging.getLogger(__name__)


class MLModel:
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.model_name = model_name
        self._load_model()

    def _load_model(self):
        """Загрузка ML модели с Hugging Face Hub"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.classifier = pipeline(
                "text-classification",
                model=self.model,
                tokenizer=self.tokenizer
            )
            logger.info(f"Successfully loaded model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Валидация входных данных"""
        required_fields = {"text"}
        if not all(field in input_data for field in required_fields):
            return False
        if not isinstance(input_data["text"], str) or len(input_data["text"]) == 0:
            return False
        return True

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнение предсказания"""
        if not self.validate_input(input_data):
            raise ValueError("Invalid input data")

        try:
            result = self.classifier(input_data["text"])
            return {
                "prediction": result[0],
                "model_version": self.model_name,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise


# Инициализация модели при импорте
model = MLModel()
