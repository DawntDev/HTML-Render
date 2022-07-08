from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import os


class HTMLRender:
    @staticmethod
    def init(PATH="public/builds"):
        """
        A method to initialize the HTMLRender class.
        """
        __options = webdriver.EdgeOptions()
        __options.headless = True

        HTMLRender.__PATH = PATH
        HTMLRender.__driver = webdriver.Edge(
            service=Service(EdgeChromiumDriverManager().install()),
            options=__options,
        )

        HTMLRender.__driver.set_window_size("1920", "1080")  # May need manual adjustment
        HTMLRender.__driver.get("about:blank")

    @staticmethod
    def screenshot(url, selector, filename, size=("1920", "1080"), timeout=2.5):
        """
        A method to take a screenshot of the given url.

        Parameters
        ----------
        url: str
            The url to take a screenshot.
        selector: str
            The selector of element to capture.
        filename: str
            The filename of the screenshot.
        size: tuple (default: ("1920", "1080"))
            The size of the screenshot
        timeout: float (default: 2.5)
            The timeout of the screenshot.
        """
        try:
            HTMLRender.__driver.set_window_size(*size) if size != ("1920", "1080") else None
            HTMLRender.__driver.get(url)
            time.sleep(timeout)

            name, ext = filename.split(".")
            HTMLRender.__driver.find_element(By.CSS_SELECTOR, selector).screenshot(f"{HTMLRender.__PATH}/{name}.{ext}")
            return os.path.exists(f"{HTMLRender.__PATH}/{name}.{ext}") # Return True if file exists
        except:
            return False

    @staticmethod
    def raw(url, selector, timeout=2.5):
        """
        A method to get the raw of a image

        Parameters
        ----------
        url: str
            The url to get the raw html.
        selector: str
            The selector of element to capture.
        timeout: float (default: 2.5)
            The timeout of the screenshot.
        """
        try:
            HTMLRender.__driver.get(url)
            time.sleep(timeout)
            return HTMLRender.__driver.find_element(By.CSS_SELECTOR, selector).get_attribute("innerHTML")
        except:
            return None

    @staticmethod
    def recording(url, filename, format): pass
