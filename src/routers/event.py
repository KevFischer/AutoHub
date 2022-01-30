"""
Router class for events, providing all features needed to create, view, join and delete events.
"""
from fastapi import *
from typing import List
from src.util.token import *
from src.util.database import init_db
from src.models.event import Event, AccountEvent
from src.schemas.event import *


router = APIRouter()


@router.get("/", response_model=List[RespondEvent])
def get_all(db: Session = Depends(init_db)):
    """
    Get all events registered in DB. \n
    :param db: DB do browse with \n
    :return: All events in DB
    """
    return db.query(Event).all()


@router.get("/{id}", response_model=RespondEvent)
def get_by_id(id: int, token:str = Header(None), db: Session = Depends(init_db)):
    """
    Get a specific event. \n
    :param id: Unique ID of the event \n
    :param db: DB to browse \n
    :return: Event identified by the ID
    """
    if db.query(Event).filter(Event.eventID == id).first() is None:
        raise HTTPException(status_code=404)
    ownership = False
    data = db.query(Event).filter(Event.eventID == id).first()
    if token is not None:
        user = read_token(token, db)
        if data.creator == user:
            ownership = True
    response = RespondEvent(
    eventID=data.eventID,
    creator=data.creator,
    eventname=data.eventname,
    location=data.location,
    appointment=data.appointment,
    maxAttendants=data.maxAttendants,
    ownership=ownership
    )
    return response


@router.post("/")
def add_event(request: RequestEvent, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Add an event to the DB. \n
    :param request: Request body to create event \n
    :param token: Token to identify logged in user \n
    :param db: DB to browse \n
    :return: OK if success
    """
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    new_event = Event(
        creator=read_token(token, db),
        eventname=request.eventname,
        location=request.location,
        appointment=request.appointment,
        maxAttendants=request.maxAttendants,
        description=request.description
    )
    db.add(new_event)
    db.commit()
    return {"response": "ok"}


@router.post("/join/{id}")
def join_event(id: int, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Enter a specific event identified by unique ID \n
    :param id: Unique event ID \n
    :param token: Token to identify user, check if logged in \n
    :param db: DB to browse \n
    :return: OK if success
    """
    if db.query(Event).filter(Event.eventID == str(id)).first() is None:
        raise HTTPException(status_code=404)
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    new_participant = AccountEvent(
        event=id,
        account=read_token(token, db)
    )
    db.add(new_participant)
    db.commit()
    return {"response": "ok"}


@router.get("/participants/{id}")
def get_participants(id: int, db: Session = Depends(init_db)):
    """
    Get joined users of a specific event \n
    :param id: Unique ID of event \n
    :param db: DB to browse \n
    :return: List of all joined accounts
    """
    if db.query(Event).filter(Event.eventID == str(id)).first() is None:
        raise HTTPException(status_code=404)
    return db.execute("select * from account where email in (select email from account_event where event = " + str(id) + ")").fetchall()


@router.delete("/{id}")
def delete_event(id: int, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Delete an event. \n
    You have to be logged in as the owner of the event for this. \n
    :param id: Unique ID of Event \n
    :param token: Token to identify user \n
    :param db: DB to browse \n
    :return: OK if success
    """
    user = read_token(token, db)
    if db.query(Event).filter(Event.eventID == str(id)).first() is None:
        raise HTTPException(status_code=404)
    if user is None:
        raise HTTPException(status_code=401)
    if user != db.query(Event.creator).filter(Event.eventID == str(id)).first()[0]:
        raise HTTPException(status_code=401)
    db.execute("DELETE FROM account_event WHERE event = " + str(id))
    db.commit()
    db.execute("DELETE FROM event WHERE eventID = " + str(id))
    db.commit()
    return {"response": "ok"}
