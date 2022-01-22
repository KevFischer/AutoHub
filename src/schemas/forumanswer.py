from pydantic import *
from typing import Optional
from datetime import datetime


class RequestAnswer(BaseModel):
    content: str

    class Config:
        orm_mode = True


class RespondAnswer(BaseModel):
    answerID: int
    post: int
    account: str
    postedAt: datetime
    content: str
    upvotes: Optional[int]

    class Config:
        orm_mode = True
