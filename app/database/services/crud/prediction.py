from sqlmodel.ext.asyncio.session import AsyncSession
from lesson_2.app.models.task import MLTask
from lesson_2.app.schemas import TaskStatus
from datetime import datetime

class PredictionCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_task_status(
            self,
            task_id: str,
            status: TaskStatus,  # Используем Enum
            result: dict = None
    ) -> MLTask:
        task = await self.session.get(MLTask, task_id)
        if not task:
            return None

        task.status = status
        task.updated_at = datetime.utcnow()

        if result:
            task.result = result

        self.session.add(task)
        await self.session.commit()
        return task
