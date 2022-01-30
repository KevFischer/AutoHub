"""
Model of the account object.
"""
from sqlalchemy import *
from sqlalchemy.sql.functions import now
from ..util.database import Base


class Account(Base):
    """
    Abstraction of the database table "account"
    """
    __tablename__ = "account"

    email = Column(String(255), unique=True, primary_key=True, index=True)
    username = Column(String(255))
    password = Column(String(255))
    phone = Column(String(255))
    member_since = Column(DateTime, default=now())
    image_url = Column(String(512), default="https://res.cloudinary.com/autohubstorage/image/upload/v1643560393/blank-profile-picture-973460_960_720_dmzcen.webp")
