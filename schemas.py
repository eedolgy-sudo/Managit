from pydantic import (BaseModel, Field, EmailStr, SecretStr, StringConstraints)
from typing import Annotated
from datetime import datetime, timezone


class Notification(BaseModel):
    description: str= Field(default='')
    date: datetime= Field(default_factory=lambda: datetime.now(timezone.utc))


class Task(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    date_created: datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    description: str= Field(default='')
    due_date: datetime | None = Field(default=None)
    subtasks: list["Task"]=Field(default_factory=list)
    notifications: list[Notification] = Field(default_factory=list)


class User(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    surname: str= Field(default='')
    email: EmailStr
    password: SecretStr