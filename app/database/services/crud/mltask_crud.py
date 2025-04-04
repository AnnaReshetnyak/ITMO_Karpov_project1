from sqlmodel import Session, select
from typing import List, Optional
from app.models.MLSegment import MLTask
from app.schemas import MLTaskCreate, MLTaskUpdate

class MLTaskCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, task_data: MLTaskCreate) -> MLTask:
        db_task = MLTask(**task_data.dict())
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def get(self, task_id: int) -> Optional[MLTask]:
        return self.session.get(MLTask, task_id)

    def get_by_model(self, model_id: int) -> List[MLTask]:
        statement = select(MLTask).where(MLTask.model_id == model_id)
        return self.session.exec(statement).all()

    def update_status(self, task_id: int, status: str) -> Optional[MLTask]:
        db_task = self.get(task_id)
        if not db_task:
            return None
        db_task.status = status
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task
