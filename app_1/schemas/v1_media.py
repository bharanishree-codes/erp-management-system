from pydantic import BaseModel

class MediaSchema(BaseModel):
    id: int
    file: str

    class Config:
        orm_mode = True
