from typing import List
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models import Task as TaskModel, User as UserModel


class EntityDoesNotExist(Exception):
    pass

class BaseRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session
    

class TaskRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session)

    async def get_tasks(self, filters: dict={}) -> List[TaskModel]:
        conditions = []
        conditions.extend([getattr(TaskModel, attr) == value for attr, value in filters.items()])
        stmt = select(TaskModel).where(and_(*conditions)).order_by(TaskModel.created_at)
        tasks = await self._db_session.execute(stmt)
        return tasks.scalars().all()
    async def get_task(self, filters: dict={}) -> List[TaskModel]:
        conditions = []
        conditions.extend([getattr(TaskModel, attr) == value for attr, value in filters.items()])
        stmt = select(TaskModel).where(and_(*conditions))
        tasks = await self._db_session.execute(stmt)
        return tasks.scalars().first()

    async def create_task(self, title: str, user_id: UUID) -> TaskModel:
        task = TaskModel(title=title, user_id=user_id)
        self._db_session.add(task)
        await self._db_session.commit()
        await self._db_session.refresh(task)
        return task
    async def delete_task(self, task_id: UUID) -> TaskModel:
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        task_exc = await self._db_session.execute(stmt)
        task = task_exc.scalars().first()
        if task:
            await self._db_session.delete(task)
            await self._db_session.commit()
            return task
        raise EntityDoesNotExist(f"task with id {str(task_id)} does not exist")
    
    async def toggle_completed(self, task: TaskModel) -> TaskModel:
        task.is_completed = not task.is_completed
        self._db_session.add(task)
        await self._db_session.commit()
        await self._db_session.refresh(task)
        return task
    
    # async def get_datasources_by_observation_id(
    #     self, observation_id: UUID
    # ) -> List[DatasourceModel]:
    #     stmt = select(DatasourceModel)\
    #             .where(DatasourceModel.observation_id==observation_id,
    #                 DatasourceModel.deleted==False)
    #     datasources = await self._db_session.execute(stmt)
    #     return datasources.scalars().all()

    # async def get_datasource_by_id(
    #     self, datasource_id: UUID
    # ) -> DatasourceModel:
    #     stmt = select(DatasourceModel)\
    #             .where(
    #                 DatasourceModel.id==datasource_id,
    #                 DatasourceModel.deleted==False)
    #     datasource_exc = await self._db_session.execute(stmt)
    #     datasource = datasource_exc.scalars().first()
    #     if datasource:
    #         return datasource
    #     raise EntityDoesNotExist(f"datasource with id {str(datasource_id)} does not exist")

    # async def update_datasource(
    #     self, datasouce_update: DatasourceInUpdate, db_datasource: DatasourceModel
    # ) -> DatasourceModel:
    #     db_datasource.storage_quota = datasouce_update.storage_quota
    #     db_datasource.retention = datasouce_update.retention
    #     db_datasource.enable = datasouce_update.enable
    #     self._db_session.add(db_datasource)
    #     await self._db_session.commit()
    #     await self._db_session.refresh(db_datasource)
    #     return await self.get_datasource_by_id(
    #         datasource_id=db_datasource.id
    #     )

    # async def delete_datasource(
    #     self, db_datasource: DatasourceModel
    # ) -> DatasourceModel:
    #     db_datasource.deleted = True
    #     self._db_session.add(db_datasource)
    #     await self._db_session.commit()

    #     return db_datasource

class UserRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession) -> None:   
        super().__init__(db_session)    

    async def create_user(self, username: str, password_hash: str) -> UserModel:
        user = UserModel(username=username, password_hash=password_hash)
        self._db_session.add(user)
        await self._db_session.commit()
        await self._db_session.refresh(user)
        return user
    
    async def get_user_by_id(self, user_id: UUID) -> UserModel:
        stmt = select(UserModel).where(UserModel.id == user_id)
        user_exc = await self._db_session.execute(stmt)
        user = user_exc.scalars().first()
        if user:
            return user
        raise EntityDoesNotExist(f"user with id {str(user_id)} does not exist")
    
    async def get_user_by_username(self, username: str) -> UserModel:
        stmt = select(UserModel).where(UserModel.username == username)
        user_exc = await self._db_session.execute(stmt)
        user = user_exc.scalars().first()
        if user:
            return user
        raise EntityDoesNotExist(f"user with username {username} does not exist")