"""
Database connection setup.
"""
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json


CONFIG = "cfg/db.json"


def read_config():
    """
    Read the cfg/db.json file to configure the database connection.
    :return: Connection URL
    """
    with open(CONFIG) as f:
        data = json.load(f)
    return data["server"] + "://" + data["user"] + ":" + data["password"] + "@" + \
        data["host"] + ":" + data["port"] + "/" + data["database"]


engine = create_engine(read_config())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """
    Create a database session.
    :return: -
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
