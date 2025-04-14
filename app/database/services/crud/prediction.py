from sqlmodel.ext.asyncio.session import AsyncSession
from lesson_2.app.database.models import MLTask


class PredictionCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, user_id: str, input_data: dict) -> MLTask:
        task = MLTask(
            user_id=user_id,
            input_data=input_data,
            status="pending"
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update_task_status(
            self,
            task_id: str,
            status: str,
            result: dict = None
    ) -> MLTask:
        task = await self.session.get(MLTask, task_id)
        if not task:
            return None

        task.status = status
        if result:
            task.result = result

        self.session.add(task)
        await self.session.commit()
        return task

    async def get_task(self, task_id: str) -> MLTask:
        return await self.session.get(MLTask, task_id)
