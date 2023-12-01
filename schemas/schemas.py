from pydantic import BaseModel
from datetime import datetime


class DonationCreate(BaseModel):
    user_id: int
    shopify_store_id: int
    email: str
    company_name: str
    amount: float


class DonationRead(BaseModel):
    id: int
    user_id: int
    shopify_store_id: int
    company_name: str
    amount: float
    timestamp: datetime


class PartnerCreate(BaseModel):
    name: str
    shopify_store_id: str


class PartnerRead(PartnerCreate):
    id: str

class PartnerResponse(BaseModel):
    partner: PartnerRead
    secret_key: str
