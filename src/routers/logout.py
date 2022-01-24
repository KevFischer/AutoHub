from fastapi import *
from ..util.database import init_db
from src.util.token import *


router = APIRouter()


@router.post("/")
def logout(token: str = Header(None), db: Session = Depends(init_db)):
    delete_token(token, db)