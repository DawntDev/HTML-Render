from typing import Annotated, Generic, List, Literal, Type, Union, TypeVar, Optional
import uuid as identifier
import time
import os


Self =TypeVar("Self", bound="PageBuilder")

class PageBuilder(Generic[Self]):
    __builds_path = os.path.join(os.getcwd(), "public", "builds")
    __builds: List[Type[Self]] = []
    
    @property
    def uuid(self) -> identifier.UUID:
        return self.__uuid
    
    @property
    def path(self) -> str:
        return self.__path
    
    @staticmethod
    def get_build(uuid: identifier.UUID) -> Optional[Type[Self]]:
        for build in PageBuilder.__builds:
            if build.uuid == uuid:
                return build
            

    def __init__(self, html: str, css: str, js: str) -> None:
        """
        Class for build a html file from the given data of request
        and convert it format required.

        Parameters
        ----------
        html: str
            The html code to build
        css: str
            The css code to build
        js: str
            The JavaScript code of page to build
        """
        
        self.__uuid = identifier.uuid4()
        self.__path = f"{self.__builds_path}/{self.__uuid}.html"
        
        if all(isinstance(arg, str) for arg in (html, css, js)):
            with open(self.__path, "w") as f:
                with open("./src/template.html", "r") as template:
                    template = template.read()
                    f.write(template.format(id=self.__uuid, css=css, html=html, js=js))

    def convert(
        self, 
        file_format: str, 
        type_of: str, 
        selector: str, 
        size: Annotated[List[str], 2], 
        timeout: float
        ) -> Union[str, Literal[False]]:
        """
        Convert the html file to the given format.

        Parameters
        ----------
        file_format: str
            The format to convert the html file to.
        type_of: str
            The type of the file to convert.
        selector: str
            CSS selector of the element to capture.
        size: list[str, str]
            The size of the image to capture.
        timeout: int
            Timeout for a page to load.
            
        Returns
        -------
        bool | str
        bool: False if the page could not be converted.
        str: The url of the converted file.
        """
        
        PageBuilder.__builds.append(self)
        filename = f"{self._uuid}.{file_format}"
        url = f"{LOCAL}/api/v1/builds/{self._uuid}.html"
        
        match type_:
            case "img":
                img = TYPES[type_]["func"](url, filename, selector, size, timeout)
            case "raw":
                img = TYPES[type_]["func"](url, filename, selector, size, timeout)
            case _:
                img = False
                
        return (False, filename)[img]

    @classmethod
    def convert_url(cls, url: str, format_: str, type_: str, selector: str, size: list[str, str], timeout: float) -> bool | str:
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
        
        Returns
        -------
        bool | str
        bool: False if the page could not be converted.
        str: The url of the converted file.
        """
        obj = cls(None, None, None)
        Manager.builds.append(obj)
        filename = f"{obj._uuid}.{format_}"
        
        match type_:
            case "img":
                img = TYPES[type_]["func"](url, filename, selector, size, timeout)
            case "raw":
                img = TYPES[type_]["func"](url, filename, selector, size, timeout)
            case _:
                img = False
                
        return (False, filename)[img]

    def destroy(self) -> None:
        """
        Destroy the file created by the build.

        Parameters
        ----------
        format_: str
            The format of the file to destroy.
        """
        
        time.sleep(15)
        while os.path.exists(self.__path):
            try:
                os.remove(self.__path)
                PageBuilder.__builds.remove(self)
            except:
                time.sleep(2)