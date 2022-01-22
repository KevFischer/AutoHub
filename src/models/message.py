"""
Model of the Message object.
"""
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from ..util.database import Base


class Message(Base):
    """
    Abstraction of the database table "Message"
    """
    __tablename__ = "message"

    messageID = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    sender = Column(String(255), ForeignKey("account.email"), primary_key=True)
    receiver = Column(String(255), ForeignKey("account.email"), primary_key=True)
    offer = Column(Integer, ForeignKey("offer.offerID"), primary_key=True)
    testDrive = Column(DateTime, default=now())
    content = Column(String(512))

    msg_sender_idx = relationship("Account", foreign_keys="Message.sender")
    msg_receiver_idx = relationship("Account", foreign_keys="Message.receiver")
    msg_offer_idx = relationship("Offer", foreign_keys="Message.offer")
