from flask import redirect, render_template, request 
from src.tools import Building, Manager, validation

def render():
    """
    Render a template

    Params
    ------
    element: str
        The HTML element to render (e.g. <h1>)
    selector: str
        The CSS selector to render (e.g. .title)
    css: str
        The CSS to apply to the element (e.g. h1 h1{ color: red; })
    format: str (default: base64)
        The format of the output (e.g. png, jpg, base64) 
    options: dict (optional)
        The options to pass to the template (e.g. {'width': '100', 'height': '100'})
    """
    
    data = request.get_json()
    interface = {
        "keys": ("elements", "css", "js", "selector", "format", "size", "timeout"),
        "types": (str, str, str, str, str, list, float),
        # None means that the element cannot be missing in this case elements is required
        "defaults": (None, "", "", "body", "png", ["1920", "1080"], 2.5)
    }

    # Check that all keys are present and have the correct type
    error = validation(data, interface)
    
    if error["messages"]:
        error["code"] = 400
        return render_template("error.html", error=error), error["code"] # Return error page
    
    # Build the html file
    build = Building(data["elements"], data["css"], data["js"])
    Manager.builds.append(build)
    
    response = build.convert(
        format_=data["format"],
        type_=data["type"],
        selector=data["selector"],
        size=data["size"],
        timeout=data["timeout"]
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
    