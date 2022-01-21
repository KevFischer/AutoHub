from pydantic import *
from typing import Optional
from datetime import datetime


class RequestEvent(BaseModel):
    eventname: str
    location: str
    appointment: Optional[datetime]
    maxAttendants: Optional[int]

    class Config:
        orm_mode = True


class RespondEvent(BaseModel):
    eventID: int
    creator: str
    eventname: str
    location: str
    appointment: Optional[datetime]
    maxAttendants: Optional[int]

    class Config:
        orm_mode = True
