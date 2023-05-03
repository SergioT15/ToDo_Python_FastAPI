from pydantic import BaseModel

class Todo_request(BaseModel):
    text: str
    completed: bool