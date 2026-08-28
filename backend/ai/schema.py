from typing import Any, Optional
from pydantic import BaseModel, Field

# --------------------------------------------------
# Team Member
# --------------------------------------------------
class TeamMemberContext(BaseModel):
    id: Optional[int] = None
    full_name: str
    email: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None

# --------------------------------------------------
# Project
# --------------------------------------------------
class ProjectContext(BaseModel):
    id: Optional[int] = None
    project_name: str
    status: Optional[str] = None
    description: Optional[str] = None

# --------------------------------------------------
# Daily Update
# --------------------------------------------------
class DailyUpdateContext(BaseModel):
    id: Optional[int] = None
    member_id: Optional[int] = None
    project_id: Optional[int] = None
    update_date: Optional[str] = None
    task_completed: Optional[str] = None
    blockers: Optional[str] = None
    hours_worked: Optional[float] = None
    status: Optional[str] = None

# --------------------------------------------------
# RAG Context
# --------------------------------------------------
class RAGContext(BaseModel):
    team_members: list[TeamMemberContext] = Field(
        default_factory=list
    )

    projects: list[ProjectContext] = Field(
        default_factory=list
    )

    updates: list[DailyUpdateContext] = Field(
        default_factory=list
    )

# --------------------------------------------------
# AI Response
# --------------------------------------------------
class AIResponse(BaseModel):
    response: str
    generated_sql: Optional[str] = None
    rows: list[Any] = Field(
        default_factory=list
    )