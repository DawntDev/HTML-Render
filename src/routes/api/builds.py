from fastapi import BackgroundTasks, Depends
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from src import Builder
from pathlib import Path
import re

pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}\.(html|png|jpg|bin|base64)$"


def is_render(filename: Path):
    if not re.match(pattern, filename.name):
        raise HTTPException(409, "The file is not a render")
    return filename

def builds(task: BackgroundTasks, filename: Path = Depends(is_render)):
    uuid, *_ = filename.name.split(".")
    build = Builder.get_build(uuid)
    if not build:
        raise HTTPException(404, "Render not found")

    task.add_task(build.destroy)
    return FileResponse(build.path)