"""
Message routes using the pusher library
"""
from fastapi import *
from typing import List
from src.util.token import *
from src.util.database import init_db
from src.schemas.message import *
from src.models.message import Message
from src.models.offer import Offer
import smtplib
import pusher


router = APIRouter()
CONFIG_PUSHER = "cfg/pusher.json"
CONFIG_SMTP = "cfg/smtp.json"


with open(CONFIG_PUSHER) as f:
    data = json.load(f)


pusher_client = pusher.Pusher(
  app_id=data["app_id"],
  key=data["key"],
  secret=data["secret"],
  cluster=data["cluster"],
  ssl=bool(data["ssl"])
)


with open(CONFIG_SMTP) as f:
    data = json.load(f)


smtp_usr = data["user"]
smtp_pw = data["password"]
server = smtplib.SMTP("smtp.gmail.com:587")


@router.post("/")
def send_mail(request: RequestMessage, db: Session = Depends(init_db), token: str = Header(None)):
    """
    Send email to offer creator. \n
    :param request: Request body for email \n
    :param db: DB to browse \n
    :param token: Token to identify sender \n
    :return: OK if success
    """
    sender = read_token(token, db)
    if sender is None:
        raise HTTPException(status_code=401, detail="Sender can not be empty.")
    if db.query(Offer).filter(Offer.offerID == request.offer).first() is None:
        raise HTTPException(status_code=404, detail="Offer not found.")
    if request.content is None:
        raise HTTPException(status_code=422, detail="Content can not be empty.")
    offer = db.query(Offer).filter(Offer.offerID == request.offer).first()
    receiver = offer.account
    subj = f"{sender} is interested in your {offer.brand} {offer.model}!"
    mail_data = f"From:{sender}\nTo:{receiver}\nSubject:{subj}\n\n{request.content}"
    server.starttls()
    server.login(smtp_usr, smtp_pw)
    server.sendmail(sender, receiver, mail_data)
    server.quit()
    return {
        "response": "ok"
    }


@router.post("/pusher/")
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


@router.get("/pusher/setup", response_model=List[RespondMessage])
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
