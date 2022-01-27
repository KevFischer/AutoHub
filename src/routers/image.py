"""
Route for images e.g. Offer images
"""
from fastapi import *
from typing import List
from sqlalchemy.orm import *
from src.models.image import OfferImages
from src.models.offer import Offer
from src.util.token import read_token
from src.util.database import init_db
from src.schemas.image import RespondImage
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json


router = APIRouter()
CONFIG = "cfg/cloudinary.json"


with open(CONFIG) as f:
    data = json.load(f)
cloudinary.config(
    cloud_name=data["cloud_name"],
    api_key=data["api_key"],
    api_secret=data["api_secret"]
)


@router.get("/{id}",response_model=List[RespondImage])
def get_images(id:int, db: Session = Depends(init_db)):
    """
    Get images of an offer
    :param id: ID of the offer
    :param db: DB to browse
    :return: List of all imageURLs
    """
    if db.query(Offer).filter(Offer.offerID == id).first() is None:
        raise HTTPException(status_code=404)
    return db.query(OfferImages.url).filter(OfferImages.offer == id).all()


@router.get("/thumbnail/{id}")
def get_images(id: int, db: Session = Depends(init_db)):
    """
    EXPERIMENTAL
    :param id: ID of offer
    :param db: DB to browse
    :return: Thumbnail
    """
    if db.query(Offer).filter(Offer.offerID == id).first() is None:
        raise HTTPException(status_code=404)
    return db.query(OfferImages.url).filter(OfferImages.offer == id).first()


@router.post("/{id}")
async def upload_post(id: int, token:str = Header(None), file: UploadFile = File(...), db: Session = Depends(init_db)):
    """
    Upload an image for an offer
    :param id: ID of the offer
    :param token: Token to identify user
    :param file: File to upload
    :param db: DB to browse
    :return: OK if success
    """
    if read_token(token, db) is None:
        raise HTTPException(status_code=401)
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(status_code=422)
    if db.query(Offer).filter(Offer.offerID == id).first() is None:
        raise HTTPException(status_code=404)
    if db.query(Offer.account).filter(Offer.offerID == id).first()[0] != read_token(token, db):
        raise HTTPException(status_code=401)
    url = cloudinary.uploader.upload(file.file)["url"]
    new_image = OfferImages(
        offer=id,
        url=url
    )
    db.add(new_image)
    db.commit()
    return {"response": "ok"}
