from selenium import webdriver
from threading import Thread, Lock
from werkzeug.routing import BaseConverter
import os, uuid, json


class HTMLRender:
    __options = webdriver.EdgeOptions()
    __options.headless = True
    __options.add_argument("--ignore-certificate-errors")
    __driver = webdriver.Edge("./src/msedgedriver.exe", options=__options)
    
    @staticmethod
    def screenshot(url, filename, format):
        HTMLRender.__driver.get(url)
        HTMLRender.__driver.save_screenshot(filename)
        HTMLRender.__driver.quit()
    
    @staticmethod
    def captureElement(url, filename, format):
        HTMLRender.__driver.get(url)
        HTMLRender.__driver.save_screenshot(filename)
        HTMLRender.__driver.quit()

    @staticmethod
    def recording(url, filename, format):
        HTMLRender.__driver.get(url)
        HTMLRender.__driver.save_screenshot(filename)
        HTMLRender.__driver.quit()
    
    @staticmethod
    def recordingElement(url, filename, format):
        HTMLRender.__driver.get(url)
        HTMLRender.__driver.save_screenshot(filename)
        HTMLRender.__driver.quit()
    
    
class Yarn(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, lock=False):
        if lock:
            self._lock = Lock()
            args = (*args, self._lock)
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def __join(self, *args):
        Thread.join(self, *args)
        return self._return

    def launch(self):
        self.start()
        return self.__join()
    
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
        with open(f"./public/builds/{self.id}.html", "w") as f:
            with open("./src/template.html", "r") as template:
                template = template.read()
                f.write(template.format(id=self.id, css=css, html=html))

    def convert(self, format, selector):
        print(f"Building {self.id}")
        pass
    
# Intermediate metaclass in the movement of elements between files, in order to avoid errors due to circular imports.
Manager = type("Manager",(object,) ,{})

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