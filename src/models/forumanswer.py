"""
Model of the ForumPostAnswer object.
"""
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from ..util.database import Base


class Forumpostanswer(Base):
    """
    Abstraction of the database table "forumpostanswer"
    """
    __tablename__ = "forumpostanswer"

    answerID = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    post = Column(Integer, ForeignKey("forumpost.postID"), primary_key=True)
    account = Column(String(128), ForeignKey("account.email"), primary_key=True)
    postedAt = Column(DateTime, default=now())
    content = Column(String(1024))
    upvotes = Column(Integer, default=0)

    answer_post_idx = relationship("Forumpost", foreign_keys="Forumpostanswer.post")
    answer_account_idx = relationship("Account", foreign_keys="Forumpostanswer.account")
