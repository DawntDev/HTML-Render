from werkzeug.routing import BaseConverter
from src.html_render import HTMLRender
import os
import uuid
import time


PATH = os.path.join(os.getcwd(), "public", "builds")
TYPES = {
    "img": {
        "ext": ("png", "jpg"),
        "func": HTMLRender.screenshot
    },
    "raw": {
        "ext": ("bin", "base64"),
        "func": HTMLRender.raw
    },
    "video": {
        "ext": ("mp4", "gif"),
        "func": HTMLRender.recording
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

class Building:
    def __init__(self, html: str, css: str) -> None:
        """
        Class for build a html file from the given data of request
        and convert it format required.

        Parameters
        ----------
        html: str
            The html code to build
        css: str
            The css code to build
        """
        self.id = uuid.uuid4()
        if html and css:
            with open(f"./public/builds/{self.id}.html", "w") as f:
                with open("./src/template.html", "r") as template:
                    template = template.read()
                    f.write(template.format(id=self.id, css=css, html=html))

    def convert(self, format_, selector):
        """
        Convert the html file to the given format.

        Parameters
        ----------
        format_: str
            The format to convert the html file to.

        selector: str
            The selector of element to capture.
        """

        Manager.builds.append(self)
        return True

    @classmethod
    def convertURL(cls, url: str, format_: str, type_: str, selector: str, size: list[str, str], timeout: float, fps: int) -> bool | str:
        """
        Class method to convert urls, through the constructor. This to give them an id, in addition to being stored in the Manager as an instance of the class.
        
        Parameters
        ----------
        url: str
            The url to convert.
        format_: str
            The format to convert the url to.
        type_: str
            The type of the file to convert.
        selector: str
            CSS selector of the element to capture.
        size: list[str, str]
            The size of the image to capture.
        timeout: int
            Timeout for a page to load.
        fps: int
            The frames per second of the video.
        
        Returns
        -------
         bool: False if the page could not be converted
         or
         str: The url of the converted file.
        """
        obj = cls(None, None)
        Manager.builds.append(obj)
        filename = f"{obj.id}.{format_}"
        
        match type_:
            case "img":
                img = TYPES[type_]["func"](url, filename, selector, size, timeout)
            case "raw":
                img = TYPES[type_]["func"](url, filename, selector, size, timeout)
            case "video":
                img = TYPES[type_]["func"](url, filename, selector, size, timeout, fps)
            case _:
                img = False
                
        return (False, filename)[img]

    def destroy(self, format_: str) -> None:
        """
        Destroy the file created by the build.

        Parameters
        ----------
        format_: str
            The format of the file to destroy.
        """
        file = f"{PATH}/{self.id}.{format_}"

        time.sleep(15)
        while os.path.exists(file):
            try:
                os.remove(file)
                Manager.builds.remove(self)
            except:
                time.sleep(2)
