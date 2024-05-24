from pydantic import BaseModel


class UserFiles(BaseModel):
    file_id: int
    filename: str
