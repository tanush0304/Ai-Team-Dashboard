from pydantic import BaseModel


class ProjectCreate(BaseModel):
    project_name: str
    description: str
    status: str


class ProjectUpdate(BaseModel):
    project_name: str | None = None
    description: str | None = None
    status: str | None = None