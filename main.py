import math
from fastapi import FastAPI, status, HTTPException
from db import engine, session
from models.todo_model import Base, Todo
from models.todo_model_update import Todo_update
from models.todo_model_add import Todo_add
# from models.todo_model_delete import Todo_delete

# Create the database
Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/todo/{page}")
def get_todos(page: int):
    # get all todo items
    item_per_page = 5
    todos = session.query(Todo).offset(page * item_per_page).limit(item_per_page).all()
    count_todos = session.query(Todo).count()
    pages_lenght = math.ceil(count_todos / item_per_page)

    # close the session   
    session.close()
    return todos, count_todos, pages_lenght

@app.post("/todo")
def add_todo(todo: Todo_add):
    # create an instance of the ToDo database model
    tododb = Todo(text = todo.text, completed = False)
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

# @app.delete("/todo", status_code=status.HTTP_204_NO_CONTENT)
# def delete_todo(id: Todo_delete):
#     # get the todo item with the given id
#     todo = session.query(Todo).get(id)
#     # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
#     if todo:
#         session.delete(todo)
#         session.commit()
#         session.close()
#     else:
#         raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
#     return None

@app.patch("/todo/{id}")
def update_todo(id: int, body:Todo_update):
    # get the todo item with the given id
    todo = session.query(Todo).get(id)
    # update todo item with the given text (if an item with the given id was found)
    if body:
        todo.text = body.text 
        todo.completed = body.completed 
        # todo.completed = 
        session.commit()
        new_todo = {
            "id":todo.id,
            "text": todo.text,
            "completed": todo.completed,
        }
    # close the session
    session.close()
    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
    return new_todo

@app.delete("/All")
def delete_all_todo():
    session.query(Todo).filter(Todo.completed == True).delete(
            synchronize_session='fetch')
    todos = session.query(Todo).all()
    # close the session  
    session.commit() 
    session.close()
    return todos

@app.patch("/completedAll/{completed_all}")
def completed_all_todo(completed_all:bool):
    # todos = session.query(Todo).update(Todo.completed: completed_all)
    todos = session.query(Todo).update({"completed": completed_all}, synchronize_session='fetch')
    session.commit() 
    completed: completed_all


    return todos