from flask import render_template, send_from_directory
from threading import Thread
from src.tools import Manager, PATH

def builds(file):
    builds = *map(lambda x: str(x.id), Manager.builds),
    id_, format_ = file.split(".")
    index = builds.index(id_) if id_ in builds else None

    if index is None:
        error = {
            "code": 404,
            "messages": [f"Build {file} not found"]
        }
        return render_template("error.html", error=error), error["code"]

    build = Manager.builds[index]
    Thread(target=build.destroy, args=(format_,)).start()
    return send_from_directory(PATH, file)
