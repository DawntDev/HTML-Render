from flask import redirect, render_template, request
from src.tools import Building, validation


def url_to_image():
    interface = {
        "keys": ("url", "selector", "format", "size", "timeout", "fps"),
        "types": (str, str, str, list, float, int),
        # None means that the element cannot be missing in this case elements is required
        "defaults": (None, "body", "png", ["1920", "1080"], 2.5, 30)
    }
    
    data = request.get_json() if request.method == "POST" else request.args.to_dict()
    error = validation(data, interface)
    
    if error["messages"]:
        error["code"] = 400
        return render_template("error.html", error=error), error["code"]
    
    response = Building.convertURL(
        url = data["url"],
        format_= data["format"],
        type_= data["type"],
        selector = data["selector"],
        size = data["size"],
        timeout = data["timeout"],
        fps= data["fps"]
    )

    return (
        (
            render_template(
                "error.html", 
                error={"code": 502, "messages": ["Error while rendering the page"]}
            ), 
            502 # Status code to return
        ),
        redirect(f"/api/v1/builds/{response}")
    )[bool(response)] # If the response not is False, return the url converted.