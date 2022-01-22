"""
Router object and all necessary routes
for account objects.
"""
from sqlalchemy.orm.session import Session
from fastapi import *
from ..util.password import encrypt
from ..util.database import init_db
from ..util.token import *
from ..models.account import Account
from ..schemas.account import *


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
