from fastapi import *
from sqlalchemy.orm.session import Session
from ..util.database import init_db
from uuid import uuid4
import os


router = APIRouter()


@router.post("/{id}")
async def upload_post(id: int, file: UploadFile = File(...)):
    print(file.file)
    directory = "files/"
    content = await file.read()
    filename = str(uuid4()) + os.path.splitext(file.filename)[1]
    if file.content_type.split("/")[0] == "image":
        print(f"{directory}" + filename)
        with open(f"{directory}" + filename, "wb") as f:
            f.write(content)
        return {"filename": filename}
    raise HTTPException(status_code=422)
