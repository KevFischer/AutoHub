"""
Authentication stuff.
"""
import jwt
import json
from sqlalchemy.orm.session import Session
from random import random
from fastapi import HTTPException
from datetime import datetime, timedelta
from ..models.token import Token
from ..models.account import Account


CONFIG = "cfg/token.json"


def generate_token(email: str, db: Session):
    """
    Generate a token for an user.
    :param email: Email to identify the user
    :param db: Database to interact with
    :return: JWT Token
    """
    # Read config file
    with open(CONFIG) as f:
        data = json.load(f)
    key = data["secret_key"]
    # Generate Token
    token = jwt.encode({random(): "payload"}, key, algorithm="HS256")
    token_obj = Token(
        token=token,
        account=email,
        expire=datetime.now() + timedelta(days=7)
    )
    # Upload Token to DB
    db.add(token_obj)
    db.commit()
    return token


def read_token(token: str, db: Session):
    """
    Get the user of a token
    :param token: Token to read
    :param db: Database to interact with
    :return: Account from token
    """
    if db.query(Token).filter(Token.token == token).first() is None:
        raise HTTPException(status_code=404)
    return db.query(Token.account).filter(Token.token == token).first()[0]


def delete_token(token: str, db: Session):
    """
    Delete a given token from the db so it's not longer valid
    :param token: Token to delete
    :param db: DB to interact with
    """
    db.execute("DELETE FROM token WHERE token = '" + token + "'")
    db.commit()
