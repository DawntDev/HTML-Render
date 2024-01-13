from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, RedirectResponse

v1 = APIRouter(prefix="/v1", deprecated=True)

@v1.get("/urlToImage")
@v1.get("/builds")
@v1.post("/urlToImage")
@v1.post("/render")
def deprecated(request: Request):
    if request.method == "GET":
        return RedirectResponse(request.app.url_for(""))
    else:
        return PlainTextResponse("This version is deprecated, please check the documentation.")