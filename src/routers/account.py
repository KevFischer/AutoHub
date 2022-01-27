"""
Router object and all necessary routes
for account objects.
"""
from fastapi import *
from src.util.database import init_db
from src.util.token import *
from src.models.account import Account

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
    """
    Get a specific account
    :param email: Email to identify account
    :param db: DB to browse
    :return: Account matching to email
    """
    if db.query(Account).filter(Account.email == email).first() is None:
        raise HTTPException(status_code=404)
    return db.query(Account).filter(Account.email == email).first()
