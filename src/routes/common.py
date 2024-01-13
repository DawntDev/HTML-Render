from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

common = APIRouter()


@common.get("/", response_class=HTMLResponse)
def index(request: Request):
    return request.app.templates.TemplateResponse( # type: ignore
        request=request, name="index.html"
    )

@common.get("/new_render", response_class=HTMLResponse)
def new_render(request: Request):
    return request.app.templates.TemplateResponse( # type: ignore
        request=request, name="new-render.html"
    )