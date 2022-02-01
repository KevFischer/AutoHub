from pydantic import *
from typing import Optional
from datetime import datetime


class RequestMessage(BaseModel):
    offer: int
    testDrive: Optional[datetime]
    content: str

    class Config:
        orm_mode = True


class RespondMessage(BaseModel):
    messageID: int
    sender: str
    receiver: str
    offer: int
    testDrive: Optional[datetime]
    content: str

    class Config:
        orm_mode = True
