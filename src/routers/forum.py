"""
Router class for forum posts/answers,
providing all features needed to create, view, join and delete forum posts/answers.
"""
from fastapi import *
from typing import List
from src.util.token import *
from src.util.database import init_db
from src.models.forumpost import Forumpost
from src.models.forumanswer import Forumpostanswer
from src.schemas.forumpost import *
from src.schemas.forumanswer import *


router = APIRouter()


@router.get("/", response_model=List[RespondPost])
def get_all(db: Session = Depends(init_db)):
    """
    Get a list of all form posts \n
    :param db: DB to browse \n
    :return: List of all posts from DB
    """
    return db.query(Forumpost).all()


@router.get("/{id}", response_model=RespondPost)
def get_by_id(id: int, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Get a specific ForumPost identified by ID \n
    :param id: Id to identify post \n
    :param token: Token to identify user \n
    :param db: DB to browse \n
    :return: Matching forumpost object
    """
    if db.query(Forumpost).filter(Forumpost.postID == id).first() is None:
        raise HTTPException(status_code=404)
    ownership = False
    data = db.query(Forumpost).filter(Forumpost.postID == id).first()
    if token is not None:
        user = read_token(token, db)
        if data.account == user:
            ownership = True
    response = RespondPost(
        postID=data.postID,
        account=data.account,
        postedAt=data.postedAt,
        topic=data.topic,
        content=data.content,
        ownership=ownership
    )
    return response


@router.post("/")
def add_post(request: RequestPost, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Add a post to the DB \n
    :param request: Request body with all values to create Post onject \n
    :param token: Token to identify user \n
    :param db: DB to browse \n
    :return: OK if success
    """
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    new_post = Forumpost(
        account=read_token(token, db),
        topic=request.topic,
        content=request.content
    )
    db.add(new_post)
    db.commit()
    return {"response": "ok"}


@router.delete("/{id}")
def delete_post(id:int, token:str = Header(None), db: Session = Depends(init_db)):
    """
    Delete a complete forum posts with all its answers of owned by token owner \n
    :param id: ID to identify ForumPost \n
    :param token: Token to identify user \n
    :param db: DB to browse \n
    :return: OK if success
    """
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    if db.query(Forumpost).filter(Forumpost.postID == id).first() is None:
        raise HTTPException(status_code=404)
    if db.query(Forumpost.account).filter(Forumpost.postID == id).first()[0] != read_token(token, db):
        raise HTTPException(status_code=401)
    db.execute("DELETE FROM forumpostanswer WHERE post = " + str(id))
    db.commit()
    db.execute("DELETE FROM forumpost WHERE postID = " + str(id))
    db.commit()
    return {"response": "ok"}


@router.get("/answers/{id}", response_model=List[RespondAnswer])
def get_answers(id: int, db: Session = Depends(init_db)):
    """
    Get a list of all answeres from a specific ForumPost \n
    :param id: ID of the ForumPost \n
    :param db: DB to browse \n
    :return: List of Answers
    """
    if db.query(Forumpost).filter(Forumpost.postID == id).first() is None:
        raise HTTPException(status_code=404)
    return db.query(Forumpostanswer).filter(Forumpostanswer.post == id).all()


@router.post("/answer/{id}")
def answer_post(request: RequestAnswer, id: int, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Answer to a forum post \n
    :param request: Request body with values for the answer object \n
    :param id: ID of the post \n
    :param token: Token to identify user \n
    :param db: DB to browse \n
    :return: OK if success
    """
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    if db.query(Forumpost).filter(Forumpost.postID == id).first() is None:
        raise HTTPException(status_code=404)
    new_answer = Forumpostanswer(
        post=id,
        account=read_token(token, db),
        content=request.content
    )
    db.add(new_answer)
    db.commit()
    return {"response": "ok"}


@router.patch("/answer/upvote/{id}")
def upvote_answer(id:int, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Increment upvote column of ForumPostAnswer \n
    :param id: ID of the answer \n
    :param token: Token to identify user \n
    :param db: DB to Browse \n
    :return: OK if success
    """
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    if db.query(Forumpostanswer).filter(Forumpostanswer.answerID == id).first() is None:
        raise HTTPException(status_code=404)
    db.execute("UPDATE forumpostanswer SET upvotes = upvotes + 1 WHERE answerID = " + str(id))
    db.commit()
    return {"response": "ok"}


@router.delete("/answer/{id}")
def delete_answer(id: int, token: str = Header(None), db: Session = Depends(init_db)):
    """
    Delete a specific answer. \n
    :param id: ID of the answer \n
    :param token: Token to identify user \n
    :param db: DB to browse \n
    :return: OK if success
    """
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    if db.query(Forumpostanswer.account).filter(Forumpostanswer.answerID == id).first()[0] != read_token(token, db):
        raise HTTPException(status_code=401)
    db.execute("DELETE FROM forumpostanswer WHERE answerID = " + str(id))
    db.commit()
    return {"response": "ok"}


@router.get("/search/", response_model=List[RespondPost])
def search_post(search_str: Optional[str] = None, db: Session = Depends(init_db)):
    """
    Search for a string in topic column \n
    :param search_str: String to search in topic \n
    :param db: DB to browse \n
    :return: List of matching posts
    """
    return db.execute("SELECT * FROM forumpost WHERE topic LIKE '%" + search_str + "%'").all()
