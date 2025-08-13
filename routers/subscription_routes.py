from fastapi import APIRouter

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.get("/plans")
def get_plans():
    return {"plans": ["Free", "Pro", "Premium"]}


