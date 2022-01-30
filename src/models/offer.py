"""
Model of the offer object.
"""
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from ..util.database import Base


class Offer(Base):
    """
    Abstraction of the database table "offer"
    """
    __tablename__ = "offer"

    offerID = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    account = Column(String(128), ForeignKey("account.email"), primary_key=True)
    brand = Column(String(32))
    model = Column(String(32))
    price = Column(Float)
    dateAdded = Column(DateTime, default=now())
    firstRegistration = Column(DateTime)
    mileage = Column(Integer)
    fuelType = Column(String(16))
    location = Column(String(128))
    roadworthy = Column(String(32))
    description = Column(String(1024))

    email_idx = relationship("Account", foreign_keys="Offer.account")
