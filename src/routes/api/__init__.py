from typing import Literal
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

api = APIRouter(prefix="/api")


@api.get("/rules/{version}", response_class=HTMLResponse)
def rules(request: Request, version: Literal["v1", "v2"] = "v2"):
    return request.app.templates.TemplateResponse(
        request=request, 
        name="rules.html", 
        context={
            "rules": request.app.schemas[version],
            "deprecated": version != "v2"
        }
    )
    
