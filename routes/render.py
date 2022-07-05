from flask import redirect, render_template, request 
from tools import Yarn, Building

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
    error = {
        "code": None,
        "messages": []
    }
    
    interface = {
        "keys": ("elements", "selector", "css", "format", "options"),
        "types": (str, str, str, str, dict),
        "defaults": (None, None, "", "base64", {}) # None means that the element cannot be missing in this case elements is required
    }

    # Check that all keys are present and have the correct type
    for key, type_, default in zip(*interface.values()):
        if not key in data:
            if default is None:
                error["messages"].append(f"Missing key: {key}")
            data[key] = default
        elif data[key]:
            if not isinstance(data[key], type_):
                error["messages"].append(f"Invalid type for key: {key}")
        else:
            error["messages"].append(f"The key {key} is empty")
    
    if error["messages"]:
        error["code"] = 400
        return render_template("error.html", error=error), error["code"] # Return error page
    
    build = Building(data["elements"], data["css"])
    
    Yarn(target=build.launch, args=(data["format"], data["selector"])).run()
    return "render"
    