from fastapi import APIRouter
from .url_to_image import method_get, method_post
from .render import render

v2 = APIRouter(prefix="/v2")

v2.add_api_route("/url_to_image", method_get, methods=["GET"], name="url_to_image")
v2.add_api_route("/url_to_image", method_post, methods=["POST"], name="url_to_image")
v2.add_api_route("/render", render, methods=["POST"], name="render")