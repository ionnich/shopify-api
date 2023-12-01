import secrets
from internal.keys import encrypt_secret_key

from bson import ObjectId
from models.models import Donation, Donator, Partner
from schemas.schemas import DonationCreate, DonationRead, PartnerResponse
from schemas.schemas import PartnerRead, PartnerCreate


def create_donation(db, donation_data: DonationCreate) -> DonationRead:
    donation_dict = donation_data.model_dump()
    donation: Donation = Donation(
        donator=Donator(
            email=donation_dict["email"],
            name=donation_dict["name"],
            id=donation_dict["user_id"]
        ), partner=Partner(
            name=donation_dict["company_name"],
            id=donation_dict["company_id"],
            shopify_store_id=donation_dict["shopify_store_id"]
        ),
        amount=donation_dict["amount"]
    )

    result = db.donations.insert_one(donation.model_dump())
    new_donation = db.donations.find_one({"_id": result.inserted_id})
    return DonationRead(**new_donation)


def get_donations(db, partner_id) -> list[DonationRead]:
    donations = []
    for donation in db.donations.find({"shopify_store_id": partner_id}):
        donations.append(DonationRead(**donation))
    return donations


def get_total_donations(db, partner_id) -> float:
    donations = db.donations.find({"shopify_store_id": partner_id})
    total = 0
    for donation in donations:
        total += donation["amount"]
    return total


def get_donation_by_id(db, donation_id: str) -> DonationRead | None:
    donation = db.donations.find_one({"_id": ObjectId(donation_id)})
    if donation:
        return DonationRead(**donation)
    return None


def create_partner(db, partner_data: PartnerCreate) -> PartnerResponse:
    secret_key = secrets.token_urlsafe()
    encrypted_key = encrypt_secret_key(
        secret_key, partner_data.shopify_store_id, partner_data.name)

    partner_dict = partner_data.model_dump()
    partner_dict['secret_key'] = encrypted_key

    result = db.partners.insert_one(partner_dict)
    new_partner = db.partners.find_one({"_id": result.inserted_id})

    new_partner.pop('secret_key')
    return PartnerResponse(
        partner=PartnerRead(**new_partner),
        secret_key=secret_key
    )


def get_partner_by_id(db, partner_id: str) -> PartnerRead | None:
    partner = db.partners.find_one({"_id": ObjectId(partner_id)})
    if partner:
        return PartnerRead(**partner)
    return None


def get_donations_by_user(db, user_id: int, shopify_id: str) -> list[DonationRead]:
    donations = []
    for donation in db.donations.find({"user_id": user_id, "shopify_id": shopify_id}):
        donations.append(DonationRead(**donation))
    return donations
