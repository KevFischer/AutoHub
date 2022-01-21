"""
JSON Body formats for requests and responses.
"""
from pydantic import *
from datetime import datetime


class RequestLogin(BaseModel):
    """
    Request body expected when attempting to log in.
    """
    email: str
    password: str

    class Config:
        orm_mode = True


class RequestRegister(BaseModel):
    """
    Request body expected when attempting to create
    new account.
    """
    username: str
    email: str
    phone: str
    password: str

    class Config:
        orm_mode = True


class RespondAccount(BaseModel):
    """
    Respond body of an account object.
    """
    id: str
    username: str
    email: str
    phone: str
    password: str
    member_since: datetime

    class Config:
        orm_mode = True


class RespondLogin(BaseModel):
    """
    Respond body when log in successful.
    """
    token: str

    class Config:
        orm_mode = True
