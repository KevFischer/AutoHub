"""
Message routes using the pusher library
"""
from fastapi import *
from typing import List
import pusher
from src.util.token import *
from src.util.database import init_db
from src.schemas.message import *
from src.models.message import Message


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
    """
    Setup pusher client \n
    :param request: Request body of the message \n
    :param db: DB to browse \n
    :param token: Token to identify user \n
    :return: No respons, due to pusher mechanics
    """
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
    """
    Get chat history \n
    :param receiver: Receiver of the messages \n
    :param db: DB to browse \n
    :param token: Token to identify user \n
    :return: Return List of all messages between 2 persons.
    """
    query_str = "SELECT * FROM message WHERE "\
        "(sender LIKE '" + read_token(token, db) + "' AND receiver LIKE '" + receiver + "') "\
        "OR (sender LIKE '" + receiver + "' AND receiver LIKE '" + read_token(token, db) + "')"
    return db.execute(query_str).all()