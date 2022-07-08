from flask import redirect, render_template, request, url_for
from src.tools import Building, validation, TYPES


def urlToImage():
    if request.method == "POST":
        data = request.get_json()
        interface = {
            "keys": ("url", "selector", "format", "options"),
            "types": (str, str, str, dict),
            "defaults": (None, "body", "base64", {}) # None means that the element cannot be missing in this case elements is required
        }

        error = validation(data, interface)

    url = request.args.get("url")
    if url:
        response = Building.convertURL(url, "png", "body")
        if response:
            return redirect(f"/api/v1/builds/{response}")
        else:
            return render_template("error.html", error={"code": 502, "messages": ["Error while rendering the page"]})

    return render_template("error.html", error={"code": 404, "messages": ["URL not found"]}), 404
