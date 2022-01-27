from pydantic import *
from typing import Optional
from datetime import datetime


class RequestPost(BaseModel):
    topic: str
    content: str

    class Config:
        orm_mode = True


class RespondPost(BaseModel):
    postID: int
    account: str
    postedAt: datetime
    topic: str
    content: str
    ownership: Optional[bool]

    class Config:
        orm_mode = True
