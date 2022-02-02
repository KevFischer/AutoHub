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
        raise HTTPException(status_code=404, detail="Event not found.")
    ownership = False
    joined = False
    data = db.query(Event).filter(Event.eventID == id).first()
    if token is not None:
        user = read_token(token, db)
        if user is not None:
            if data.creator == user:
                ownership = True
            if db.query(AccountEvent).filter(AccountEvent.event == id).filter(AccountEvent.account == user).first() is not None:
                joined = True
    response = RespondEvent(
        eventID=data.eventID,
        creator=data.creator,
        eventname=data.eventname,
        location=data.location,
        appointment=data.appointment,
        maxAttendants=data.maxAttendants,
        ownership=ownership,
        description=data.description,
        joined=joined
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
        raise HTTPException(status_code=401, detail="You can not create an event as a guest.")
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
        raise HTTPException(status_code=404, detail="Event not found.")
    if read_token(token, db) is None:
        raise HTTPException(status_code=401, detail="You can not join an event as a guest.")
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
        raise HTTPException(status_code=404, detail="Event not found.")
    return db.execute("select * from account where email in (select account from account_event where event = " + str(id) + ")").fetchall()


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
        raise HTTPException(status_code=404, detail="Event not found.")
    if user is None:
        raise HTTPException(status_code=401, detail="User can not be resolved by token.")
    if user != db.query(Event.creator).filter(Event.eventID == str(id)).first()[0]:
        raise HTTPException(status_code=401, detail="You are not the owner of the event.")
    db.execute("DELETE FROM account_event WHERE event = " + str(id))
    db.commit()
    db.execute("DELETE FROM event WHERE eventID = " + str(id))
    db.commit()
    return {"response": "ok"}


@router.get("/search/")
def search_event(search_str: Optional[str] = None, location: Optional[str] = None, db: Session = Depends(init_db)):
    """
    Search an event. \n
    :param search_str: String contained in either Topic or description \n
    :param location: Location of the event \n
    :param db: DB to browse \n
    :return: List of matching events
    """
    if search_str is None and location is None:
        return db.query(Event).all()
    default_str = ("SELECT * FROM event WHERE")
    query_str = default_str
    if search_str != None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (eventname LIKE '%{search_str}%'"
        query_str += f" OR description LIKE '%{search_str}%')"
    if location != None:
        if query_str != default_str:
            query_str += " AND"
        query_str += f" (location LIKE '%{location}%')"
    query_str += ";"
    return db.execute(query_str).all()


@router.get("/{id}/joined")
def is_joined(id: int, token: str = Header(None), db: Session = Depends(init_db)):
    if db.query(Event).filter(Event.eventID == id).first() is None:
        raise HTTPException(status_code=404, detail="Event not found.")
    user = read_token(token, db)
    response = False
    if user is None:
        raise HTTPException(status_code=401, detail="You have to be logged in to do that.")
    if db.query(AccountEvent).filter(AccountEvent.event == id).filter(AccountEvent.account == user).first() is not None:
        response = True
    return {
        "joined": response
    }
