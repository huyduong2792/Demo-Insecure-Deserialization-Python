import pickle, base64
from uuid import UUID
from typing import Callable, Type
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from fastapi import Depends, Cookie, Path, HTTPException, status

from app.database import sessionmanager
from app.repositories import BaseRepository, UserRepository, TaskRepository
from app.models import User as UserModel, Task
from app.repositories import EntityDoesNotExist
from app.ultis import  RequiresLoginException

async def get_db_session():
    async with sessionmanager.session() as session:
        yield session

def get_repository(
    repo_type: Type[BaseRepository],
) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(
        db_session: AsyncSession = Depends(get_db_session),
    ) -> BaseRepository:
        return repo_type(db_session)

    return _get_repo

async def get_user_authenticated(
    cookie_session: str = Cookie(None, alias="session"),
    user_repo: UserRepository = Depends(get_repository(UserRepository))
) -> UserModel:
    if not cookie_session:
        raise RequiresLoginException
    
    current_user = pickle.loads(base64.b64decode(cookie_session))
    return await user_repo.get_user_by_username(current_user.username)

async def get_task_from_path(
    task_id: UUID = Path(title="ID của task muốn lấy thông tin"),
    current_user: UserModel = Depends(get_user_authenticated),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository))
) -> Task:
    try:
        return await task_repo.get_task({"id": task_id, "user_id": current_user.id})
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
