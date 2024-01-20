from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

v1 = APIRouter(prefix="/v1", deprecated=True)


@v1.get("/urlToImage")
@v1.post("/urlToImage")
@v1.post("/render")
def deprecated():
    return PlainTextResponse(
        "This version is deprecated, please check the documentation."
    )
