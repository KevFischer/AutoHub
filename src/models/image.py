"""
Model of the offer_images object.
"""
from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..util.database import Base


class OfferImages(Base):
    """
    Abstraction of the database table "offer_images"
    """
    __tablename__ = "offer_images"

    offer = Column(Integer, ForeignKey("offer.offerID"), primary_key=True)
    url = Column(String(512))

    offer_images_offer_idx = relationship("Offer", foreign_keys="OfferImages.offer")
