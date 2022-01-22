from pydantic import *
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

    class Config:
        orm_mode = True
