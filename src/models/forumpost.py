"""
Model of the ForumPost object.
"""
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from ..util.database import Base


class Forumpost(Base):
    """
    Abstraction of the database table "forumpost"
    """
    __tablename__ = "forumpost"

    postID = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    account = Column(String(128), ForeignKey("account.email"), primary_key=True)
    postedAt = Column(DateTime, default=now())
    topic = Column(String(64))
    content = Column(String(1024))

    post_account_idx = relationship("Account", foreign_keys="Forumpost.account")
