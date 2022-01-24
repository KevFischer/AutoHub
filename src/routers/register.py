from fastapi import *
from ..util.password import encrypt
from ..util.database import init_db
from src.util.token import *
from ..models.account import Account
from ..schemas.account import *


router = APIRouter()


@router.post("/")
def register(request: RequestRegister, db: Session = Depends(init_db)):
    """
    Register function to register a new Account entity to the database.
    :param request: Request Body received by Frontend application
    :param db: Database to interact with
    """
    # Check if mandatory columns are available.
    if request.username and request.password and request.email is None:
        raise HTTPException(status_code=422)
    # Check if there is already an account registered to the e-mail address.
    if db.query(Account).filter(Account.email == request.email).first() is not None:
        raise HTTPException(status_code=422)
    # Create new Account-object with values from the request.
    new_account = Account(
        username=request.username,
        email=request.email,
        phone=request.phone,
        password=encrypt(request.password)
    )
    # Finally, add the new account to the database and commit the changes.
    db.add(new_account)
    db.commit()