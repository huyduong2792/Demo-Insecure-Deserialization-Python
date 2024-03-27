from uuid import UUID
from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class User(BaseModel):
    id: Optional[UUID] = Field(None, title="User ID", nullable=True)
    username: str
