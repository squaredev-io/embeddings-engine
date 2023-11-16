from fastapi import APIRouter, Depends, status
from embeddings_engine.schemas import Test

documents_router = APIRouter()


@documents_router.get(
    "/items/{item_id}",
    response_model=Test,
    summary="Get an item by id",
    status_code=status.HTTP_200_OK,
    # responses=add_error_responses([401, 404]),
    description="This endpoint allows you to get an item by giving its id.",
)
def get_item(item_id: int):
    return Test(name="Charis")
