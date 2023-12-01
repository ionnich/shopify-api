from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from dependencies import get_current_partner, get_db
from schemas.schemas import DonationCreate, DonationRead
from crud.crud import create_donation, get_donations as get_donations_crud, get_donation_by_id
from models.models import Partner

router = APIRouter()


@router.post("/donations/", response_model=DonationRead)
async def post_donation(donation: DonationCreate, db: Database = Depends(get_db), current_partner: Partner = Depends(get_current_partner)):
    if donation.shopify_store_id != current_partner.id:
        raise HTTPException(status_code=400, detail="Invalid company ID")

    new_donation = create_donation(db=db, donation_data=donation)
    return new_donation


@router.get("/donations/", response_model=list[DonationRead])
async def get_donations(db: Database = Depends(get_db), current_partner: Partner = Depends(get_current_partner)):
    # Here we can retrieve all donations or implement filters as needed
    donations = get_donations_crud(db=db, partner_id=current_partner.id)
    return donations


@ router.get("/donations/{donation_id}", response_model=DonationRead)
async def get_donation(donation_id: str, db: Database = Depends(get_db)):
    donation = get_donation_by_id(db=db, donation_id=donation_id)
    if donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation
