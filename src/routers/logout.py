"""
Logout route
"""
from fastapi import *
from src.util.database import init_db
from src.util.token import *


router = APIRouter()


@router.post("/")
def logout(token: str = Header(None), db: Session = Depends(init_db)):
    """
    Delete token so no one can access account by accident
    :param token: Token to delete
    :param db: DB to browse
    :return: OK if success
    """
    delete_token(token, db)
    return {"response": "ok"}
