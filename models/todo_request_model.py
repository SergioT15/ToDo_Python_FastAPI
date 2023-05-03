from pydantic import BaseModel

class Todo_request(BaseModel):
    id: int
    text: str
    completed: bool
    class Config:
        orm_mode = True



