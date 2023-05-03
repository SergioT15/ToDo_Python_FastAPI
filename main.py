import math
from fastapi import FastAPI, status, HTTPException
from db import engine, session
from models.todo_model import Base, Todo
from models.todo_request_model import Todo_request

# Create the database
Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/todo{page}")
def get_todos():
    # get all todo items
    todos = session.query(Todo).all()
    count_todos = session.query(Todo).count()
    item_per_page = 5
    pages_lenght = math.ceil(count_todos / item_per_page)

    # close the session   
    session.close()
    return todos, count_todos, pages_lenght

@app.post("/todo")
def add_todo(todo: Todo_request):
    # create an instance of the ToDo database model
    tododb = Todo(text = todo.text, completed = todo.completed)
    # add it to the session and commit it
    session.add(tododb)
    session.commit()
    session.refresh(tododb)
    # close the session
    session.close()
    return tododb

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):
    # get the todo item with the given id
    todo = session.query(Todo).get(id)
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
    return None

@app.delete("/All")
def delete_all_todo():
    return "todos"

@app.patch("/completedAll")
def completed_all_todo():
    return "todos"

@app.patch("/todo/{id}")
def update_todo(id: int, text: str, completed: bool):
    # get the todo item with the given id
    todo = session.query(Todo).get(id)
    # update todo item with the given text (if an item with the given id was found)
    if todo:
        todo.text = text
        todo.completed = completed
        # todo.completed = 
        session.commit()
    # close the session
    session.close()
    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
    return todo