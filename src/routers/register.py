"""
Register route to create new account
"""
from fastapi import *
from src.util.password import encrypt, check_password
from src.util.database import init_db
from src.util.token import *
from src.models.account import Account
from src.schemas.account import *


router = APIRouter()


@router.post("/")
def register(request: RequestRegister, db: Session = Depends(init_db)):
    """
    Register function to register a new Account entity to the database. \n
    :param request: Request Body received by Frontend application \n
    :param db: Database to interact with
    """
    # Check if mandatory columns are available.
    if request.username and request.password and request.email is None:
        raise HTTPException(status_code=422, detail="Username, password and email can not be empty.")
    # Check if there is already an account registered to the e-mail address.
    if db.query(Account).filter(Account.email == request.email).first() is not None:
        raise HTTPException(status_code=409, detail="E-Mail already in use.")
    # Check if password is OK
    if not check_password(request.password):
        raise HTTPException(status_code=422, detail="Password does not match password policy.")
    # Check if email is an email.
    if "@" not in request.email:
        raise HTTPException(status_code=422, detail="Invalid E-Mail adress.")
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
    return RespondLogin(
        token=generate_token(request.email, db)
    )
