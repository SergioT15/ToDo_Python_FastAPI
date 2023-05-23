from pydantic import BaseModel


class Todo_update(BaseModel):
    text: str
    completed: bool = False
