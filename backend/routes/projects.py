from fastapi import APIRouter, HTTPException

from models.project import ProjectCreate, ProjectUpdate
from services.supabase import supabase

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.get("/")
def get_projects():

    response = (
        supabase
        .table("projects")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


@router.get("/{project_id}")
def get_project(project_id: int):

    response = (
        supabase
        .table("projects")
        .select("*")
        .eq("id", project_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return response.data[0]


@router.post("/")
def create_project(project: ProjectCreate):

    response = (
        supabase
        .table("projects")
        .insert(project.model_dump())
        .execute()
    )

    return response.data


@router.put("/{project_id}")
def update_project(project_id: int, project: ProjectUpdate):

    update_data = project.model_dump(exclude_none=True)

    response = (
        supabase
        .table("projects")
        .update(update_data)
        .eq("id", project_id)
        .execute()
    )

    return response.data


@router.delete("/{project_id}")
def delete_project(project_id: int):

    response = (
        supabase
        .table("projects")
        .delete()
        .eq("id", project_id)
        .execute()
    )

    return {
        "message": "Project deleted successfully",
        "data": response.data
    }