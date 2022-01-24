"""
Router object and all necessary routes
for account objects.
"""
from fastapi import *
from ..util.database import init_db
from src.util.token import *
from ..models.account import Account

router = APIRouter()


@router.get("/")
def get_all(db: Session = Depends(init_db)):
    """
    Get all accounts registered in the database.
    :param db: Database to interact with
    :return:
    """
    return db.query(Account).all()


@router.get("/{email}")
def get_by_id(email: str, db: Session = Depends(init_db)):
    return db.query(Account).filter(Account.email == email).first()
