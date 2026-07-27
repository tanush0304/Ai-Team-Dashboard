from fastapi import APIRouter, HTTPException

from models.update import UpdateCreate, UpdateUpdate
from services.supabase import supabase

router = APIRouter(
    prefix="/updates",
    tags=["Updates"]
)


@router.get("/")
def get_updates():

    response = (
        supabase
        .table("daily_updates")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


@router.get("/{update_id}")
def get_update(update_id: int):

    response = (
        supabase
        .table("daily_updates")
        .select("*")
        .eq("id", update_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Update not found"
        )

    return response.data[0]


@router.post("/")
def create_update(update: UpdateCreate):

    response = (
        supabase
        .table("daily_updates")
        .insert(update.model_dump(mode="json"))
        .execute()
    )

    return response.data


@router.put("/{update_id}")
def update_update(update_id: int, update: UpdateUpdate):

    update_data = update.model_dump(
    exclude_none=True,
    mode="json"
    )

    response = (
        supabase
        .table("daily_updates")
        .update(update_data)
        .eq("id", update_id)
        .execute()
    )

    return response.data


@router.delete("/{update_id}")
def delete_update(update_id: int):

    response = (
        supabase
        .table("daily_updates")
        .delete()
        .eq("id", update_id)
        .execute()
    )

    return {
        "message": "Update deleted successfully",
        "data": response.data
    }