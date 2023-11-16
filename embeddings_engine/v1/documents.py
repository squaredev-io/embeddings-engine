from fastapi import APIRouter, Depends, status
from embeddings_engine.schemas import Test
from fastapi import FastAPI, File, UploadFile


documents_router = APIRouter()


@documents_router.post(
    "/items/{item_id}",
    summary="Get an item by id",
    status_code=status.HTTP_200_OK,
    # responses=add_error_responses([401, 404]),
    description="This endpoint allows you to get an item by giving its id.",
)
def get_item(file: UploadFile):
    return {"file": file.filename, "content": "test"}
