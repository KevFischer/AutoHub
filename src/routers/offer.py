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
        fuelType=request.fuelType,
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


@router.get("/search/", response_model=List[RespondOffer])
def search_offer(db: Session = Depends(init_db), min_price: Optional[int] = None, max_price: Optional[int] = None,\
                 brand: Optional[str] = None, model: Optional[str] = None,\
                 min_first_registration: Optional[datetime] = None, max_first_registration: Optional[datetime] = None,\
                 min_mileage: Optional[int] = None, max_mileage: Optional[int] = None, fuel_type: Optional[str] = None,\
                 location: Optional[str] = None, roadworthy: Optional[str] = None):
    default_str = "SELECT * FROM offer WHERE"
    query_str = default_str
    if min_price is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (price >= '{min_price}')"
    if max_price is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (price <= '{max_price}')"
    if brand is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (brand LIKE '%{brand}%')"
    if model is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (model LIKE '%{model}%')"
    if min_first_registration is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (firstRegistration > STR_TO_DATE('{min_first_registration}', '%Y-%m-%d %H:%i:%s'))"
    if max_first_registration is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (firstRegistration < STR_TO_DATE('{max_first_registration}', '%Y-%m-%d %H:%i:%s'))"
    if min_mileage is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (mileage >= '{min_mileage}')"
    if max_mileage is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (mileage <= '{max_mileage}')"
    if fuel_type is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (fuelType LIKE '%{fuel_type}%')"
    if location is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (location LIKE '%{location}%')"
    if roadworthy is not None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (roadworthy LIKE '%{roadworthy}%')"
    query_str += ";"
    return db.execute(query_str).all()
