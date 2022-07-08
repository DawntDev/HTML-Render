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
        "keys": ("elements", "selector", "css", "format", "options"),
        "types": (str, str, str, str, dict),
        "defaults": (None, "body", "", "base64", {}) # None means that the element cannot be missing in this case elements is required
    }

    # Check that all keys are present and have the correct type
    error = validation(data, interface)
    
    if error["messages"]:
        error["code"] = 400
        return render_template("error.html", error=error), error["code"] # Return error page
    
    # Build the html file
    build = Building(data["elements"], data["css"])
    Manager.builds.append(build)
    
    # response = Yarn(target=build.convert, args=(data["format"], data["selector"])).launch()
    
    return "render"
    