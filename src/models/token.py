from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..util.database import Base


class Token(Base):
    """
    Abstraction of the database table "token"
    """
    __tablename__ = "token"

    token = Column(String(512), unique=True, primary_key=True, index=True, )
    account = Column(String(128), ForeignKey("account.email"), primary_key=True)
    expire = Column(DateTime)

    email_idx = relationship("Account", foreign_keys="Token.account")
