
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.models import Partner
from dependencies import get_current_partner, get_db
from schemas.schemas import DonationRead
from crud.crud import get_donations_by_user

router = APIRouter()


@router.get("/users/{user_id}/donations/", response_model=list[DonationRead])
async def get_donations(user_id: int, db=Depends(get_db), current_partner: Partner = Depends(get_current_partner)):

    # Retrieve donations that match user_id and belong to the current partner's company
    if (current_partner is None):
        raise HTTPException(status_code=404, detail="Partner not found")

    donations = get_donations_by_user(
        db=db, user_id=user_id, shopify_id=current_partner.shopify_store_id)
    return donations
