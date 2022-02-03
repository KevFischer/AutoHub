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
    Delete token so no one can access account by accident \n
    :param token: Token to delete \n
    :param db: DB to browse \n
    :return: OK if success
    """
    if token is None:
        raise HTTPException(status_code=401, detail="No Token to log out.")
    delete_token(token, db)
    return {"response": "ok"}
