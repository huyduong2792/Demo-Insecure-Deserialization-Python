# main.py
import uvicorn
import pickle, base64
from uuid import UUID
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi import Depends, HTTPException, Form
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import ExpiringDict, get_repository, get_user_authenticated, get_task_from_path, get_expiring_dict
from app.database import sessionmanager
from app.repositories import TaskRepository, UserRepository
from app.config import settings
from app.schema import User
from app.models import Task as TaskModel, User as UserModel
from app.ultis import RequiresLoginException, gen_login_session, make_password_hash

templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


def get_app() -> FastAPI:

    app = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_app()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return RedirectResponse(url=f"{settings.base_url}/login")

@app.get("/")
async def root():
    return {"message": "KTLTAT service"}

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def read_tasks(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=RedirectResponse)
async def post_register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    user_repo: UserRepository = Depends(get_repository(UserRepository))):
    try:
        esixting_user = await user_repo.get_user_by_username(username)
        if esixting_user:
            raise HTTPException(status_code=400, detail="Username already exists")
    except:
        pass
    password_hash = make_password_hash(password)
    await user_repo.create_user(username=username, password_hash=password_hash)
    raise RequiresLoginException
    

@app.post("/login", response_class=HTMLResponse)
async def post_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    cache: ExpiringDict = Depends(get_expiring_dict)):

    user = await user_repo.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password_hash == make_password_hash(password):
        session = gen_login_session(user.id, username, user.password_hash)
        response = RedirectResponse(f"{settings.base_url}/tasks/", status_code=302)
        cache.ttl(
            key=session, 
            value="1",
            ttl=settings.cookie_session_timeout)
        response.set_cookie(key="session", value=session, domain=settings.base_domain, max_age=settings.cookie_session_timeout)
        return response

    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/tasks/", response_class=HTMLResponse)
async def get_tasks(
    request: Request, 
    current_user: User = Depends(get_user_authenticated),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository))):
    results = await task_repo.get_tasks(filters={"user_id": current_user.id})
    return templates.TemplateResponse("index.html", {"request": request, "tasks": results})

@app.post("/tasks/", response_class=RedirectResponse, status_code=302)
async def create_task(
    request: Request,
    task_title: str = Form(...),
    current_user: User = Depends(get_user_authenticated),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository))):
    await task_repo.create_task(title=task_title, user_id=current_user.id)
    return f"{settings.base_url}/tasks/"

@app.delete("/tasks/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    db_task: TaskModel = Depends(get_task_from_path),
    current_user: User = Depends(get_user_authenticated),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
):
    return await task_repo.delete_task(db_task.id)

@app.get("/tasks/{task_id}/toggle-completion", status_code=status.HTTP_200_OK)
async def toggle_completion(
    db_task: TaskModel = Depends(get_task_from_path),
    current_user: User = Depends(get_user_authenticated),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
):
    return await task_repo.toggle_completed(db_task)

@app.get("/logout", response_class=RedirectResponse, status_code=302)
async def logout(request: Request):
    response = RedirectResponse(url=f"{settings.base_url}/login")
    response.delete_cookie(key="session", domain=settings.base_domain)
    return response

@app.post("/users/")
async def create_user(user: User, user_repo: UserRepository = Depends(get_repository(UserRepository))) -> User:
    return await user_repo.create_user(user.username)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=9000)