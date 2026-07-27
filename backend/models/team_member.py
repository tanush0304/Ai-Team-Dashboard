from pydantic import BaseModel, EmailStr
from typing import Optional


class TeamMemberCreate(BaseModel):
    full_name: str
    email: EmailStr
    role: str
    department: Optional[str] = None


class TeamMemberUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None