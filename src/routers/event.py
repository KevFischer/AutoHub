from fastapi import *
from typing import List
from src.util.token import *
from ..util.database import init_db
from ..models.event import Event, AccountEvent
from ..schemas.event import *

router = APIRouter()


@router.get("/", response_model=List[RespondEvent])
def get_all(db: Session = Depends(init_db)):
    return db.query(Event).all()


@router.get("/{id}", response_model=RespondEvent)
def get_by_id(id: int, db: Session = Depends(init_db)):
    return db.query(Event).filter(Event.eventID == id).first()


@router.post("/")
def add_event(request: RequestEvent, token: str = Header(None), db: Session = Depends(init_db)):
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    new_event = Event(
        creator=read_token(token, db),
        eventname=request.eventname,
        location=request.location,
        appointment=request.appointment,
        maxAttendants=request.maxAttendants
    )
    db.add(new_event)
    db.commit()


@router.post("/join/{id}")
def join_event(id: int, token: str = Header(None), db: Session = Depends(init_db)):
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    new_participant = AccountEvent(
        event=id,
        account=read_token(token, db)
    )
    db.add(new_participant)
    db.commit()


@router.get("/participants/{id}")
def get_participants(id: int, db: Session = Depends(init_db)):
    return db.execute("select * from account where email in (select email from account_event where event = " + str(id) + ")").fetchall()


@router.delete("/{id}")
def delete_event(id: int, db: Session = Depends(init_db)):
    db.execute("DELETE FROM account_event WHERE event = " + str(id))
    db.commit()
    db.execute("DELETE FROM event WHERE eventID = " + str(id))
    db.commit()
