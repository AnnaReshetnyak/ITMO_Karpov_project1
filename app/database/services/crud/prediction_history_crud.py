from sqlmodel import Session, select, desc
from typing import List, Optional, Dict, Any
from app.models.MLSegment import PredictionHistory
from app.schemas import PredictionHistoryCreate, PredictionHistoryUpdate


class PredictionHistoryCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, prediction_data: PredictionHistoryCreate) -> PredictionHistory:
        """Создание новой записи предсказания"""
        db_prediction = PredictionHistory(**prediction_data.dict())
        self.session.add(db_prediction)
        self.session.commit()
        self.session.refresh(db_prediction)
        return db_prediction

    def get(self, prediction_id: int) -> Optional[PredictionHistory]:
        """Получение предсказания по ID"""
        return self.session.get(PredictionHistory, prediction_id)

    def get_by_user(
            self,
            user_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[PredictionHistory]:
        """Получение истории предсказаний пользователя с пагинацией"""
        statement = select(PredictionHistory).where(
            PredictionHistory.user_id == user_id
        ).order_by(desc(PredictionHistory.created_at)).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_model(
            self,
            model_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[PredictionHistory]:
        """Получение истории предсказаний модели с пагинацией"""
        statement = select(PredictionHistory).where(
            PredictionHistory.model_id == model_id
        ).order_by(desc(PredictionHistory.created_at)).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(
            self,
            prediction_id: int,
            prediction_data: PredictionHistoryUpdate
    ) -> Optional[PredictionHistory]:
        """Обновление данных предсказания"""
        db_prediction = self.get(prediction_id)
        if not db_prediction:
            return None

        update_data = prediction_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_prediction, key, value)

        self.session.add(db_prediction)
        self.session.commit()
        self.session.refresh(db_prediction)
        return db_prediction

    def add_feedback(
            self,
            prediction_id: int,
            feedback_data: Dict[str, Any]
    ) -> Optional[PredictionHistory]:
        """Добавление обратной связи к предсказанию"""
        db_prediction = self.get(prediction_id)
        if not db_prediction:
            return None

        db_prediction.feedback = feedback_data
        self.session.add(db_prediction)
        self.session.commit()
        self.session.refresh(db_prediction)
        return db_prediction

    def delete(self, prediction_id: int) -> bool:
        """Удаление записи предсказания"""
        db_prediction = self.get(prediction_id)
        if not db_prediction:
            return False

        self.session.delete(db_prediction)
        self.session.commit()
        return True

    def get_latest_predictions(
            self,
            hours: int = 24,
            limit: int = 100
    ) -> List[PredictionHistory]:
        """Получение последних предсказаний за указанный период"""
        from datetime import datetime, timedelta
        time_threshold = datetime.utcnow() - timedelta(hours=hours)

        statement = select(PredictionHistory).where(
            PredictionHistory.created_at >= time_threshold
        ).order_by(desc(PredictionHistory.created_at)).limit(limit)

        return self.session.exec(statement).all()
