from fastapi import *
from ..util.password import encrypt
from ..util.database import init_db
from src.util.token import *
from ..models.account import Account
from ..schemas.account import *


router = APIRouter()


@router.post("/", response_model=RespondLogin)
def login(request: RequestLogin, db: Session = Depends(init_db)):
    """
    Function to log in into an account.
    :param request: Login request body
    :param db: Database to interact with
    :return: JWT token for user privileges
    """
    if db.query(Account).filter(Account.email == request.email).\
            filter(Account.password == encrypt(request.password)) is not None:
        return RespondLogin(
            token=generate_token(request.email, db)
        )
    raise HTTPException(status_code=422)