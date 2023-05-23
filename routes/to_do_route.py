from fastapi import APIRouter
from controllers.to_do_controller import (
    get_todos,
    add_todo,
    delete_todo,
    update_todo,
    completed_all_todo,
    delete_all_todo,
)

router = APIRouter()

router.add_api_route(path="/todo/{page}/{filter}", endpoint=get_todos, methods=["GET"])
router.add_api_route(path="/todo", endpoint=add_todo, methods=["POST"])
router.add_api_route(path="/todo/{id}", endpoint=delete_todo, methods=["DELETE"])
router.add_api_route(path="/todo/{id}", endpoint=update_todo, methods=["PATCH"])
router.add_api_route(path="/All", endpoint=delete_all_todo, methods={"DELETE"})
router.add_api_route(
    path="/completedAll/{completed_all}", endpoint=completed_all_todo, methods=["PATCH"]
)
