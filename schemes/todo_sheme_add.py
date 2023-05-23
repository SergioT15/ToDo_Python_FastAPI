from pydantic import BaseModel


class Todo_add(BaseModel):
    text: str

    class Config:
        orm_mode = True
