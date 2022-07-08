from threading import Thread, Lock
from werkzeug.routing import BaseConverter
from src.html_render import HTMLRender
import os
import uuid
import time


PATH = os.path.join(os.getcwd(), "public", "builds")
TYPES = {
    "img": {
        "ext": ("png", "jpg", "jpeg", "webp", "bmp", "tiff"),
        "func": HTMLRender.screenshot
    },
    "raw": {
        "ext": ("raw-png", "base64"),
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


def validation(data: dict, interface: dict):
    """
    A function to validate the data received from the user is valid

    Parameters:
        data (dict): The data received from the user
        interface (dict): The interface of the data

    Returns:
        bool: True if the data is valid, False otherwise
    """
    error = {
        "code": None,
        "messages": []
    }

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

    return error

class Building:
    def __init__(self, html, css) -> None:
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
    def convertURL(cls, url, format_, selector):
        obj = cls(None, None)
        Manager.builds.append(obj)

        filename = f"{obj.id}.{format_}"
        img = HTMLRender.screenshot(
            url=url,
            selector=selector,
            filename=filename
        )

        return (None, filename)[img]

    def destroy(self, format_):
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
