from fastapi import Request
from typing import Literal

def rules(request: Request, version: Literal["v1", "v2"] = "v2"):
    return request.app.templates.TemplateResponse(
        request=request,
        name="rules.html",
        context={"rules": request.app.schemas[version], "deprecated": version != "v2"},
    )
