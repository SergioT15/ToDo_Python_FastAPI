
from fastapi import FastAPI

app = FastAPI()


@app.get("/todo{page}")
def get_todo():
    return "todos, count, pages"

@app.post("/todo")
def add_todo():
    return "Added Successfully"

@app.delete("/todo/{id}")
def delete_todo(id: str):
    return "Deleted Successfully"

@app.delete("/All")
def delete_all_todo():
    return "todos"

@app.patch("/completedAll")
def completed_all_todo():
    return "todos"

@app.patch("/todo/{id}")
def update_todo(id: str):
    return "Updated Successfully"