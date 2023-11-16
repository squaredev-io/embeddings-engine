from fastapi import APIRouter
from .documents import documents_router
from .texts import texts_router

v1_router = APIRouter()
v1 = "/v1"


v1_router.include_router(documents_router, prefix=f"{v1}/documents", tags=["Documents"])
v1_router.include_router(texts_router, prefix=f"{v1}/texts", tags=["Text"])
