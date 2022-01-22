from sqlalchemy.orm.session import Session
from fastapi import *
from typing import List
from ..util.token import *
from ..util.database import init_db
from ..models.forumpost import Forumpost
from ..models.forumanswer import Forumpostanswer
from ..schemas.forumpost import *
from ..schemas.forumanswer import *


router = APIRouter()


@router.get("/", response_model=List[RespondPost])
def get_all(db: Session = Depends(init_db)):
    return db.query(Forumpost).all()


@router.get("/{id}", response_model=RespondPost)
def get_by_id(id: int, db: Session = Depends(init_db)):
    return db.query(Forumpost).filter(Forumpost.postID == id).first()


@router.post("/")
def add_post(request: RequestPost, token: str = Header(None), db: Session = Depends(init_db)):
    new_post = Forumpost(
        account=read_token(token, db),
        topic=request.topic,
        content=request.content
    )
    db.add(new_post)
    db.commit()


@router.delete("/{id}")
def delete_post(id:int, token:str = Header(None), db: Session = Depends(init_db)):
    if db.query(Forumpost.account).filter(Forumpost.postID == id).first()[0] is not read_token(token,db):
        raise HTTPException(status_code=401)
    db.execute("DELETE FROM forumpostanswer WHERE post = " + str(id))
    db.commit()
    db.execute("DELETE FROM forumpost WHERE postID = " + str(id))
    db.commit()


@router.get("/answers/{id}", response_model=List[RespondAnswer])
def get_answers(id: int, db: Session = Depends(init_db)):
    return db.query(Forumpostanswer).filter(Forumpostanswer.post == id).all()


@router.post("/answer/{id}")
def answer_post(request: RequestAnswer, id:int, token: str = Header(None), db: Session = Depends(init_db)):
    new_answer = Forumpostanswer(
        post=id,
        account=read_token(token, db),
        content=request.content
    )
    db.add(new_answer)
    db.commit()


@router.patch("/answer/upvote/{id}")
def upvote_answer(id:int, db: Session = Depends(init_db)):
    db.execute("UPDATE forumpostanswer SET upvotes = upvotes + 1 WHERE answerID = " + str(id))
    db.commit()


@router.delete("/answer/{id}")
def delete_answer(id: int, token: str = Header(None), db: Session = Depends(init_db)):
    print(db.query(Forumpostanswer.account).filter(Forumpostanswer.answerID == id).first()[0])
    print(read_token(token, db))
    if db.query(Forumpostanswer.account).filter(Forumpostanswer.answerID == id).first()[0] != read_token(token, db):
        raise HTTPException(status_code=401)
    db.execute("DELETE FROM forumpostanswer WHERE answerID = " + str(id))
    db.commit()
