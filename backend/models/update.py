from datetime import date
from pydantic import BaseModel


class UpdateCreate(BaseModel):
    member_id: int
    project_id: int
    update_date: date
    task_completed: str
    blockers: str
    hours_worked: float
    status: str


class UpdateUpdate(BaseModel):
    member_id: int | None = None
    project_id: int | None = None
    update_date: date | None = None
    task_completed: str | None = None
    blockers: str | None = None
    hours_worked: float | None = None
    status: str | None = None