import math
from fastapi import HTTPException
from db import session
from models.todo_model import Todo
from schemes.todo_sheme_add import Todo_add
from schemes.todo_cheme_update import Todo_update


def is_completed(filter_item):
    if filter_item == "Active":
        return False
    if filter_item == "Completed":
        return True
    return None


def get_todos(page: int, filter: str):
    filter_value = is_completed(filter)
    # item_per_page = 5  # caps
    ITEM_PER_PAGE = 5
    query = session.query(Todo)
    if filter_value != None:
        query = query.filter(Todo.completed == filter_value)

    count_todos = query.count()

    count_active_todos = session.query(Todo).filter(Todo.completed == False).count()
    pages_length = math.ceil(count_todos / ITEM_PER_PAGE)
    pages = [i for i in range(pages_length)]
    info = {
        "count_active_todos": count_active_todos,
        "pages": pages,
        # "pages": pages_length,
    }
    if filter_value != None:
        todos = (
            session.query(Todo)
            .filter(Todo.completed == filter_value)
            .offset(page * ITEM_PER_PAGE)
            .limit(ITEM_PER_PAGE)
            .all()
        )
        return {"todos": todos, "info": info}
    todos = session.query(Todo).offset(page * ITEM_PER_PAGE).limit(ITEM_PER_PAGE).all()
    session.close()

    return {"todos": todos, "info": info}


def add_todo(todo: Todo_add):
    tododb = Todo(text=todo.text, completed=False)
    session.add(tododb)
    session.commit()
    session.refresh(tododb)
    session.close()
    return tododb


def delete_todo(id: int):
    todo = session.query(Todo).get(id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    session.delete(todo)
    session.commit()
    session.close()
    return "Deleted Successfully"


def update_todo(id: int, body: Todo_update):
    todo = session.query(Todo).get(id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    if body:
        todo.text = body.text
        todo.completed = body.completed
        session.commit()

        new_todo = {
            "id": todo.id,
            "text": todo.text,
            "completed": todo.completed,
        }
    count_active_todos = session.query(Todo).filter(Todo.completed == False).count()
    new_todo_and_count_active_todo = {
        "new_todo": new_todo,
        "count_active_todos": count_active_todos,
    }
    session.close()
    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    return new_todo_and_count_active_todo


def delete_all_todo():
    session.query(Todo).filter(Todo.completed == True).delete(
        synchronize_session="fetch"
    )
    todos = session.query(Todo).all()
    session.commit()
    session.close()
    return todos


def completed_all_todo(completed_all: bool):
    session.query(Todo).update(
        {"completed": completed_all}, synchronize_session="fetch"
    )
    session.commit()
    todos = session.query(Todo).all()
    return todos
