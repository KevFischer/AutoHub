"""
Router object and all necessary routes
for account objects.
"""
from fastapi import *
from typing import List
from src.util.database import init_db
from src.util.token import *
from src.models.account import Account
from src.models.forumpost import Forumpost
from src.models.offer import Offer
from src.models.event import Event
from src.schemas.forumpost import RespondPost
from src.schemas.offer import RespondOffer
from src.schemas.event import RespondEvent

router = APIRouter()


@router.get("/")
def get_all(db: Session = Depends(init_db)):
    """
    Get all accounts registered in the database. \n
    :param db: Database to interact with \n
    :return: List of all accounts
    """
    return db.query(Account).all()


@router.get("/{email}")
def get_by_id(email: str, db: Session = Depends(init_db)):
    """
    Get a specific account. \n
    :param email: Email to identify account \n
    :param db: DB to browse \n
    :return: Account matching to email
    """
    if db.query(Account).filter(Account.email == email).first() is None:
        raise HTTPException(status_code=404)
    return db.query(Account).filter(Account.email == email).first()


@router.get("/{email}/posts", response_model=List[RespondPost])
def get_forum_posts(email: str, db: Session = Depends(init_db)):
    """
    Get all forum posts of a user. \n
    :param email: E-Mail of the user \n
    :param db: DB to browse \n
    :return: List of all posts of the user
    """
    if db.query(Account).filter(Account.email == email).first() is None:
        raise HTTPException(status_code=404)
    return db.query(Forumpost).filter(Forumpost.account == email).all()


@router.get("/{email}/offers", response_model=List[RespondOffer])
def get_offers(email: str, db: Session = Depends(init_db)):
    """
    Get all forum offers of a user. \n
    :param email: E-Mail of the user \n
    :param db: DB to browse \n
    :return: List of all offers of the user
    """
    if db.query(Account).filter(Account.email == email).first() is None:
        raise HTTPException(status_code=404)
    return db.query(Offer).filter(Offer.account == email).all()


@router.get("/{email}/events", response_model=List[RespondEvent])
def get_events(email: str, db: Session = Depends(init_db)):
    """
    Get all events offers of a user. \n
    :param email: E-Mail of the user \n
    :param db: DB to browse \n
    :return: List of all events of the user
    """
    if db.query(Account).filter(Account.email == email).first() is None:
        raise HTTPException(status_code=404)
    return db.query(Event).filter(Event.creator == email).all()
