from sqlmodel import Session, select
from typing import List, Optional
from database.models import MLModel
from schemas import MLModelCreate, MLModelUpdate

class MLModelCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, model_data: MLModelCreate) -> MLModel:
        db_model = MLModel(**model_data.dict())
        self.session.add(db_model)
        self.session.commit()
        self.session.refresh(db_model)
        return db_model

    def get(self, model_id: int) -> Optional[MLModel]:
        return self.session.get(MLModel, model_id)

    def get_all(self) -> List[MLModel]:
        result = self.session.exec(select(MLModel))
        return result.all()

    def update(self, model_id: int, model_data: MLModelUpdate) -> Optional[MLModel]:
        db_model = self.get(model_id)
        if not db_model:
            return None
        update_data = model_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_model, key, value)
        self.session.add(db_model)
        self.session.commit()
        self.session.refresh(db_model)
        return db_model

    def delete(self, model_id: int) -> bool:
        db_model = self.get(model_id)
        if not db_model:
            return False
        self.session.delete(db_model)
        self.session.commit()
        return True
