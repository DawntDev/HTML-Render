from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from src import Builder
from src.schemas.renders import RenderImage


def method_get(req: Request, args: RenderImage = Depends()):
    return url_to_image(req, args)


def method_post(req: Request, args: RenderImage):
    return url_to_image(req, args)


def url_to_image(request: Request, render: RenderImage):
    source = render.model_dump()
    page = Builder.from_url(str(request.base_url), source.pop("url"))

    response = page.convert(**source)
    if not response:
        return request.app.templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"code": 502, "messages": ["Error while rendering the page"]},
        )

    return RedirectResponse(request.url_for("builds", filename=response))
