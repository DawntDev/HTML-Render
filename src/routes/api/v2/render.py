from fastapi import Request
from fastapi.responses import RedirectResponse
from src.schemas.renders import RenderSource
from src import Builder


def render(request: Request, render: RenderSource):
    source = render.model_dump()
    page = Builder(
        str(request.base_url),
        source.pop("url"),
        source.pop("elements"),
        source.pop("css"),
        source.pop("js"),
    )

    response = page.convert(**source)
    if not response:
        return request.app.templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"code": 502, "messages": ["Error while rendering the page"]},
        )

    return RedirectResponse(request.url_for("builds", filename=response))
