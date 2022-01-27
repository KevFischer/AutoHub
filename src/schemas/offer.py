from pydantic import *
from typing import Optional
from datetime import datetime


class RequestOffer(BaseModel):
    brand: str
    model: str
    price: float
    firstRegistration: Optional[datetime]
    mileage: int
    fuelType: str
    location: str
    roadworthy: str
    description: Optional[str]

    class Config:
        orm_mode = True


class RespondOffer(BaseModel):
    offerID: int
    account: str
    brand: str
    model: str
    price: float
    dateAdded: datetime
    firstRegistration: Optional[datetime]
    mileage: int
    fuelType: str
    location: str
    roadworthy: str
    description: Optional[str]
    ownership: Optional[bool]

    class Config:
        orm_mode = True
