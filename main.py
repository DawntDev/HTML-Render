import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from os.path import dirname, join
from src.routes import common, api

app = FastAPI()
origins = ["*"]
current_dir = dirname(__file__)

with open(join(current_dir, "routes", "api", "schema.json"), "r") as f:
    app.schemas = json.load(f) # type: ignore
    app.templates = Jinja2Templates(directory=join(current_dir, "public")) # type: ignore

app.mount(
    "/static", 
    StaticFiles(directory=join(current_dir, "public", "static")), 
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(404)
def not_found(request: Request, *_):
    return app.templates.TemplateResponse("not-found.html", {"request": request}) # type: ignore
                                          
app.include_router(common)
app.include_router(api)
