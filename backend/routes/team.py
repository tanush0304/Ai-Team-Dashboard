from fastapi import APIRouter, HTTPException

from models.team_member import TeamMemberCreate, TeamMemberUpdate
from services.supabase import supabase

router = APIRouter(
    prefix="/team",
    tags=["Team Members"]
)


@router.get("/")
def get_team_members():

    response = (
        supabase
        .table("team_members")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


@router.get("/{member_id}")
def get_team_member(member_id: int):

    response = (
        supabase
        .table("team_members")
        .select("*")
        .eq("id", member_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Team member not found")

    return response.data[0]


@router.post("/")
def create_team_member(member: TeamMemberCreate):

    response = (
        supabase
        .table("team_members")
        .insert(member.model_dump())
        .execute()
    )

    return response.data


@router.put("/{member_id}")
def update_team_member(member_id: int, member: TeamMemberUpdate):

    update_data = member.model_dump(exclude_none=True)

    response = (
        supabase
        .table("team_members")
        .update(update_data)
        .eq("id", member_id)
        .execute()
    )

    return response.data


@router.delete("/{member_id}")
def delete_team_member(member_id: int):

    response = (
        supabase
        .table("team_members")
        .delete()
        .eq("id", member_id)
        .execute()
    )

    return {
        "message": "Team member deleted successfully",
        "data": response.data
    }