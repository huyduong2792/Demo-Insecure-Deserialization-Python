# models.py
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped
from app.database import Base
import datetime
from typing import Optional
from sqlalchemy import func
from typing_extensions import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]

class DateTimeModelMixin(Base):
    __abstract__ = True
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp]
    deleted_at: Optional[Mapped[timestamp]]

class DBModelMixin(DateTimeModelMixin):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)
    deleted: Mapped[bool] = mapped_column(nullable=False, default=False)

class Task(DBModelMixin):
    __tablename__ = "task"

    title: str = Column(String(64))
    is_completed: bool = Column(Boolean, default=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)


class User(DBModelMixin):
    __tablename__ = "user"

    username: str = Column(String(64), unique=True, nullable=False)
    password_hash: str = Column(Text, nullable=False)