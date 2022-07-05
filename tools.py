from threading import Thread, Lock
from werkzeug.routing import BaseConverter
import os, uuid, json

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
        self.id = uuid.uuid4()
        with open(f"./public/builds/{self.id}.html", "w") as f:
            with open("./src/template.html", "r") as template:
                template = template.read()
                f.write(template.format(id=self.id, css=css, html=html))
    
    def launch(self, format, selector):
        print(f"Building {self.id}")
        pass
                
class RegexConverter(BaseConverter):
    """
    Convert a regular expression into a converter.
    
    Parameters
    ----------
    url_map : werkzeug.routing.Map
        The url map to add the converter to.
        
    items : tuple
        The regular expression to convert.
    """
    
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]



class Manager:
    """
    A class to manage the data of the bot.
    
    Parameters:
    -----------
    key: str
    value: any
    """
    
    __data = {}  # Elements to management
    def __init__(self, **kwargs):
        self.__data.update(**kwargs)

    @staticmethod
    def getItem(key):
        return Manager.__data[key]
