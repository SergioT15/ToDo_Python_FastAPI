from pydantic import BaseModel

class Todo_model(BaseModel):
    id: str
    text: str
    completed: bool
    filter: str