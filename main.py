import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routes import common, api
import os, shutil

app = FastAPI()
origins = ["*"]
current_dir = os.path.dirname(__file__)

with open(os.path.join(current_dir, "src", "routes", "api", "schema.json"), "r") as f:
    app.schemas = json.load(f)  # type: ignore
    app.templates = Jinja2Templates( # type: ignore
        directory=os.path.join(
            current_dir, 
            "public"
        )
    )  

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(
        current_dir, 
        "public", 
        "static"
    )),
    name="static",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Regenerate folders
for path in ("public/builds", "public/renders"):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

@app.exception_handler(404)
def not_found(request: Request, *_):
    return app.templates.TemplateResponse( #type: ignore
        "not-found.html", 
        {"request": request}, 
        status_code=404
    )  

app.include_router(common)
app.include_router(api)
