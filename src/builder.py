from . import Renderer
import uuid as identifier
import os

from typing import Annotated, List, Literal, Set, Union, Optional, Self


class Builder:
    __builds_path = os.path.join(os.getcwd(), "public", "builds")
    __renders_path = os.path.join(os.getcwd(), "public", "renders")
    __builds: Set[Self] = set()

    @property
    def path(self) -> str:
        """Static path of build."""
        return self.__path

    @staticmethod
    def get_build(uuid: str) -> Optional["Builder"]:
        for build in Builder.__builds:
            if build.__uuid == identifier.UUID(uuid):
                return build

    @classmethod
    def from_url(
        cls,
        domain: str,
        url: str,
    ) -> Self:
        """
        Class method to convert urls, through the constructor. This to give them an id, in addition to being stored in the Manager as an instance of the class.

        Parameters
        ----------
        url: `str`
            The url to convert.
        domain: `str`
            The domain, of server

        Returns
        -------
        @Builder
        """
        return cls(domain=domain, url=url)

    def __init__(
        self,
        domain: str,
        url: Optional[str] = None,
        html: Optional[str] = None,
        css: Optional[str] = None,
        js: Optional[str] = None,
    ) -> None:
        """
        Class for build a html file from the given data of request
        and convert it format required.

        Parameters
        ----------
        html: `Optional[str]`
            The html code to build
        css: `Optional[str]`
            The css code to build
        js: `Optional[str]`
            The JavaScript code of page to build
        domain: `Optional[str]`
            Current domain of the server
        url: `Optional[str]`
            URL of resource to render
        """

        self.__uuid = identifier.uuid4()
        self.__url = (f"{domain}/api/v2/builds/{self.__uuid}.html", url)[bool(url)]

        if all(isinstance(arg, str) for arg in (html, css, js)):
            self.__path = f"{self.__builds_path}/{self.__uuid}.html"
            with open(self.__path, "w") as f:
                with open("./src/template.html", "r") as template:
                    template = template.read()
                    f.write(template.format(id=self.__uuid, css=css, html=html, js=js))

    def convert(
        self, selector: str, format: str, size: Annotated[List[str], 2], timeout: float
    ) -> Union[str, Literal[False]]:
        """
        Convert the html file to the given format.

        Parameters
        ----------
        selector: `str`
            CSS selector of the element to capture.
        format: `str`
            The format to convert the html file to.
        size: `List[str, str]`
            The size of the image to capture.
        timeout: `float`
            Timeout for a page to load.

        Returns
        -------
        bool | str
        bool: False if the page could not be converted.
        str: The url of the converted file.
        """
        self.__builds.add(self)
        filename = f"{self.__uuid}.{format}"
        path = f"{self.__renders_path}/{filename}"
        img = False

        match format:
            case val if val in ("png", "jpg"):
                img = Renderer.screenshot(
                    self.__url, 
                    path, 
                    selector, 
                    size, 
                    timeout
                )

                self.__path = path
                Builder.__builds.add(self)

            case val if val in ("bin", "base64"):
                img = Renderer.raw(
                    self.__url, 
                    path, 
                    selector, 
                    size, 
                    timeout
                )

                self.__path = path
                Builder.__builds.add(self)

        if not img:
            Builder.__builds.remove(self)
            return img

        return filename

    def destroy(self) -> None:
        """Destroy the file created by the build."""
        while os.path.exists(self.__path):
            try:
                os.remove(self.__path)
                Builder.__builds.remove(self)
            except:
                ...
