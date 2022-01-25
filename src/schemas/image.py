from pydantic import *


class RespondImage(BaseModel):
    url: str

    class Config:
        orm_mode = True
