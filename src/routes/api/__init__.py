from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .builds import builds
from .rules import rules
from .v2 import v2

api = APIRouter(prefix="/api")

api.add_api_route("/builds/{filename}", builds, methods=["GET", "POST"], name="builds")
api.add_api_route("/rules/{version}", rules, methods=["GET"], response_class=HTMLResponse,  name="rules")
api.include_router(v2)
