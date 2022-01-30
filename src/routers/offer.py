"""
Router class for offers, providing all features needed to create, view, join and delete offers
"""
from fastapi import *
from typing import List
from src.util.token import *
from src.util.database import init_db
from src.models.offer import Offer
from src.schemas.offer import *

router = APIRouter()


@router.get("/", response_model=List[RespondOffer])
def get_all(db: Session = Depends(init_db)):
    """
    Get all offers from DB. \n
    :param db: DB to browse \n
    :return: List of offer objects
    """
    return db.query(Offer).all()


@router.get("/{id}", response_model=RespondOffer)
def get_by_id(id: int, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Get an offer identified by unique ID. \n
    :param id: ID of the offer \n
    :param token: Token to identify user \n
    :param db: DB to browse \n
    :return: Offer object if matching
    """
    if db.query(Offer).filter(Offer.offerID == id).first() is None:
        raise HTTPException(status_code=404)
    ownership = False
    data = db.query(Offer).filter(Offer.offerID == id).first()
    if token is not None:
        user = read_token(token, db)
        if data.account == user:
            ownership = True
    response = RespondOffer(
        offerID=data.offerID,
        account=data.account,
        brand=data.brand,
        model=data.model,
        price=data.price,
        dateAdded=data.dateAdded,
        firstRegistration=data.firstRegistration,
        mileage=data.mileage,
        fuelType=data.fuelType,
        location=data.location,
        roadworthy=data.roadworthy,
        description=data.description,
        ownership=ownership
    )
    return response


@router.post("/")
def add_offer(request: RequestOffer, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Add an offer to database. \n
    :param request: Request body with values to create offer \n
    :param token: Token to identify user \n
    :param db: DB to browse \n
    :return: OK if success
    """
    if request.roadworthy.lower() != "fahrtauglich" and request.roadworthy.lower() != "nicht fahrtauglich":
        raise HTTPException(status_code=422)
    new_offer = Offer(
        account=read_token(token, db),
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
    return {"response": "ok"}


@router.delete("/{id}")
def delete_offer(id: int, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Delete an offer if its matching to the token. \n
    :param id: ID of the offer \n
    :param token: Token to identify user \n
    :param db: DB to browse \n
    :return: OK if success
    """
    if db.query(Offer).filter(Offer.offerID == id).first() is None:
        raise HTTPException(status_code=404)
    if db.query(Offer).filter(Offer.offerID == id).first().account != read_token(token, db):
        raise HTTPException(status_code=401)
    db.execute("DELETE FROM message WHERE offer = " + str(id))
    db.commit()
    db.execute("DELETE FROM offer WHERE offerID = " + str(id))
    db.commit()
    return {"response": "ok"}


@router.get("/search/", response_model=List[RespondOffer])
def search_offer(db: Session = Depends(init_db), min_price: Optional[int] = None, max_price: Optional[int] = None, \
                 brand: Optional[str] = None, model: Optional[str] = None, \
                 min_first_registration: Optional[datetime] = None, max_first_registration: Optional[datetime] = None, \
                 min_mileage: Optional[int] = None, max_mileage: Optional[int] = None, fuel_type: Optional[str] = None, \
                 location: Optional[str] = None, roadworthy: Optional[str] = None):
    """
    Generate and execute a search string on a given DB. \n
    :param db: DB to search Items \n
    :param min_price: Lowest price the Item searched can have \n
    :param max_price: Highest price the Item searched can have \n
    :param brand: Brand of the searched Item \n
    :param model: Model of the searched Item \n
    :param min_first_registration: Oldest possible first registration \n
    :param max_first_registration: Youngest possible first registration \n
    :param min_mileage: Lowest mileage of an Item \n
    :param max_mileage: Highest mileage of an Item \n
    :param fuel_type: Fuel type of the vehicle \n
    :param location: Location where the Item is located \n
    :param roadworthy: Roadworthy \n
    :return: Result set matching the query parametes
    """
    if min_price is None and max_price is None and brand is None and model is None and min_first_registration is None \
            and max_first_registration is None and min_mileage is None and max_mileage is None and fuel_type is None \
            and location is None and roadworthy is None:
        return db.query(Offer).all()
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
