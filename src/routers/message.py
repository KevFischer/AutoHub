from fastapi import *
from typing import List
import pusher
from src.util.token import *
from ..util.database import init_db
from ..schemas.message import *
from ..models.message import Message


router = APIRouter()
CONFIG = "cfg/pusher.json"


with open(CONFIG) as f:
    data = json.load(f)


pusher_client = pusher.Pusher(
  app_id=data["app_id"],
  key=data["key"],
  secret=data["secret"],
  cluster=data["cluster"],
  ssl=bool(data["ssl"])
)


@router.post("/")
async def push(request: RequestMessage, db: Session = Depends(init_db), token: str = Header(None)):
    new_message = Message(
        sender=read_token(token, db),
        offer=request.offer,
        receiver=request.receiver,
        testDrive=request.testDrive,
        content=request.content
    )
    db.add(new_message)
    db.commit()
    set = db.query(Message).filter(Message.sender == read_token(token, db)).filter(Message.receiver == request.receiver).first()
    set_json = {
        "id": set.id,
        "senderID": set.senderID,
        "receiverID": set.receiverID,
        "content": set.content
    }
    pusher_client.trigger('contact', 'contact', set_json)


@router.get("/", response_model=List[RespondMessage])
async def setup(receiver: str, db: Session = Depends(init_db), token: str = Header(None)):
    query_str = "SELECT * FROM message WHERE "\
        "(sender LIKE '" + read_token(token, db) + "' AND receiver LIKE '" + receiver + "') "\
        "OR (sender LIKE '" + receiver + "' AND receiver LIKE '" + read_token(token, db) + "')"
    return db.execute(query_str).all()