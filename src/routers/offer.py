from fastapi import *
from typing import List
from src.util.token import *
from ..util.database import init_db
from ..models.offer import Offer
from ..schemas.offer import *


router = APIRouter()


@router.get("/", response_model=List[RespondOffer])
def get_all(db: Session = Depends(init_db)):
    return db.query(Offer).all()


@router.get("/{id}", response_model=RespondOffer)
def get_by_id(id: int, db: Session = Depends(init_db)):
    return db.query(Offer).filter(Offer.offerID == id).first()


@router.post("/")
def add_offer(request: RequestOffer, token: str = Header(None), db: Session = Depends(init_db)):
    new_offer = Offer(
        account=read_token(token,db),
        brand=request.brand,
        model=request.model,
        price=request.price,
        firstRegistration=request.firstRegistration,
        mileage=request.mileage,
        fuelType=request.mileage,
        location=request.location,
        roadworthy=request.roadworthy,
        description=request.description
    )
    db.add(new_offer)
    db.commit()


@router.delete("/{id}")
def delete_offer(id: int, db: Session = Depends(init_db)):
    db.execute("DELETE FROM message WHERE offer = " + str(id))
    db.commit()
    db.execute("DELETE FROM offer WHERE offerID = " + str(id))
    db.commit()
