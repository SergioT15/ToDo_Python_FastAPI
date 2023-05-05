import math
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, HTTPException
from db import engine, session
from models.todo_model import Base, Todo
from models.todo_model_update import Todo_update
from models.todo_model_add import Todo_add

# Create the database
Base.metadata.create_all(engine)

app = FastAPI()

def is_completed(filter_item):
    if filter_item == "Active":
        return False
    if filter_item == "Completed":
        return True
    return None

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/todo/{page}/{filter}")
def get_todos(page: int, filter:str):
    filter_value = is_completed(filter)
    item_per_page = 5
    count_todos = session.query(Todo).count()
    count_active_todos = session.query(Todo).filter(Todo.completed == False).count()
    pages_lenght = math.ceil(count_todos / item_per_page)
    pages = [i for i in range(pages_lenght)] 
    if filter_value != None: 
        todos = session.query(Todo).filter(Todo.completed == filter_value).offset(page * item_per_page).limit(item_per_page).all()
        return todos, count_todos, count_active_todos, pages
    todos = session.query(Todo).offset(page * item_per_page).limit(item_per_page).all()
    session.close()
    return  todos, count_todos, count_active_todos, pages

@app.post("/todo")
def add_todo(todo: Todo_add):
    tododb = Todo(text = todo.text, completed = False)
    session.add(tododb)
    session.commit()
    session.refresh(tododb)
    session.close()
    return tododb

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):
    todo = session.query(Todo).get(id)
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
    return None

@app.patch("/todo/{id}")
def update_todo(id: int, body:Todo_update):
    todo = session.query(Todo).get(id)
    if body:
        todo.text = body.text 
        todo.completed = body.completed 
        session.commit()
        new_todo = {
            "id":todo.id,
            "text": todo.text,
            "completed": todo.completed,
        }
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
    session.commit() 
    session.close()
    return todos

@app.patch("/completedAll/{completed_all}")
def completed_all_todo(completed_all:bool):
    session.query(Todo).update({"completed": completed_all}, synchronize_session='fetch')
    session.commit() 
    todos = session.query(Todo).all()
    return todos