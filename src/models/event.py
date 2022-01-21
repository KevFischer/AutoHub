"""
Model of the event object.
"""
from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..util.database import Base


class Event(Base):
    """
    Abstraction of the database table "event"
    """
    __tablename__ = "event"

    eventID = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    creator = Column(String(255), ForeignKey("account.email"), primary_key=True)
    eventname = Column(String(255))
    location = Column(String(255))
    appointment = Column(DateTime)
    maxAttendants = Column(Integer)

    event_account_idx = relationship("Account", foreign_keys="Event.creator")


class AccountEvent(Base):
    """
    Abstraction of the database table "account_event"
    """
    __tablename__ = "account_event"
    event = Column(Integer, ForeignKey("event.eventID"), primary_key=True)
    account = Column(String(255), ForeignKey("account.email"), primary_key=True)

    participant_event_idx = relationship("Account", foreign_keys="AccountEvent.account")
    event_participants_idx = relationship("Event", foreign_keys="AccountEvent.event")
