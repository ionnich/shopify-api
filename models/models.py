from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Donator(BaseModel):
    id: Optional[int] = None
    name: str
    email: str


class Partner(BaseModel):
    id: Optional[int] = None
    name: str
    shopify_store_id: str


class Donation(BaseModel):
    id: Optional[str] = None
    donator: Donator
    partner: Partner
    amount: float
    timestamp: datetime = datetime.utcnow()
