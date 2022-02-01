"""
Login route to get access to authorized paths
"""
from fastapi import *
from src.util.password import encrypt
from src.util.database import init_db
from src.util.token import *
from src.models.account import Account
from src.schemas.account import *


router = APIRouter()


@router.post("/", response_model=RespondLogin)
def login(request: RequestLogin, db: Session = Depends(init_db)):
    """
    Function to log in into an account. \n
    :param request: Login request body \n
    :param db: Database to interact with \n
    :return: JWT token for user privileges
    """
    if request.email == "" or request.password == "":
        raise HTTPException(status_code=422)
    if request.email is None or request.password is None:
        raise HTTPException(status_code=422)
    if db.query(Account).filter(Account.email == request.email).first() is None:
        raise HTTPException(status_code=404)
    if db.query(Account.password).filter(Account.email == request.email).first()[0] != encrypt(request.password):
        raise HTTPException(status_code=404)
    return RespondLogin(
        token=generate_token(request.email, db)
    )
