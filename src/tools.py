from werkzeug.routing import BaseConverter
from src.html_render import HTMLRender
import os
import uuid
import time

LOCAL = "http://localhost:5000"
PATH = os.path.join(os.getcwd(), "public", "builds")
TYPES = {
    "img": {
        "ext": ("png", "jpg"),
        "func": HTMLRender.screenshot
    },
    "raw": {
        "ext": ("bin", "base64"),
        "func": HTMLRender.raw
    }
}

# Intermediate metaclass in the movement of elements between files, in order to avoid errors due to circular imports.
Manager = type("Manager", (object,), {})

# Regular expression converter for flask
RegexConverter = type(
    "RegexConverter",
    (BaseConverter,),
    {
        "__init__": lambda self, url_map, *items: (
            super(RegexConverter, self).__init__(url_map),
            setattr(self, "regex", items[0]),
        )[0]
    }
)


def validation(data: dict, interface: dict) -> dict:
    """
    A function to validate the data received from the user is valid

    Parameters
    ----------
    data: dict
        The data received from the user.
    interface dict: 
        The interface of the data

    Returns:
        bool: True if the data is valid, False otherwise
    """
    error = {
        "code": None,
        "messages": []
    }

    # Check if the data contains the keys of the interface
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

    # Check if the format is valid
    for type_ in TYPES:
        if data["format"] in TYPES[type_]["ext"]:
            data["type"] = type_
            break
    else:
        error["messages"].append(f"Invalid format: {data['format']}")
        
    return error

