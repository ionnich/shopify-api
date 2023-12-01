from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from dependencies import get_db, get_current_partner
from schemas.schemas import PartnerRead, PartnerCreate, PartnerResponse
from crud.crud import create_partner, get_partner_by_id
from models.models import Partner

router = APIRouter()


@router.post("/partners/", response_model=PartnerResponse)
async def post_partner(partner_data: PartnerCreate, db: Database = Depends(get_db)):
    response: PartnerResponse = create_partner(
        db=db, partner_data=partner_data)
    return response


@router.get("/partners/{partner_id}", response_model=PartnerRead)
async def get_partner(partner_id: str, db: Database = Depends(get_db), current_company: Partner = Depends(get_current_partner)):
    if partner_id != str(current_company.id):
        raise HTTPException(status_code=403, detail="Access forbidden")

    partner = get_partner_by_id(db=db, partner_id=partner_id)
    if partner is None:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner
