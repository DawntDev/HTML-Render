from selenium.webdriver import Remote
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os

from typing import Annotated, Callable, List, Literal


class Renderer:
    __driver: Remote
    __cmd_executor = "http://localhost:4444/wd/hub"
    __base_options = Options()

    @staticmethod
    def __await_element(selector: str, timeout: float):
        """
        Wait for the desired element to appear in the DOM

        Parameters
        ----------
            selector `str`:
                CSS selector of the element to await
            timeout `float`:
                Timeout for element
        """
        WebDriverWait(Renderer.__driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    @staticmethod
    def __configure_driver(func: Callable) -> Callable:
        """
        Establish the predefined configurations for the proper functioning of the driver.
        """

        def wrapped(*args, **kwargs):
            Renderer.__driver = Remote(
                Renderer.__cmd_executor, 
                options=Renderer.__base_options
            )

            Renderer.__driver.set_window_size("1920", "1080")
            output = func(*args, **kwargs)
            Renderer.__driver.close()
            return output
        return wrapped

    @staticmethod
    def __cover_window(size: Annotated[List[str], 2], selector: str):
        """
        Method for reconfiguring screen size by dynamic measurements.

        Parameters
        ----------
        size: `List[str, str]`
            The size of the window.

        selector: `str`
            CSS selector of the element to be covered.
        """
        fulls = size.count("full")

        if fulls == 2:  # [full, full]
            size = [
                Renderer.__get_size("Width", selector),
                Renderer.__get_size("Height", selector),
            ]

        elif fulls:  # [full, x] or [x, full]
            direct = size.index("full")
            size[direct] = Renderer.__get_size(("Width", "Height")[direct], selector)

        Renderer.__driver.set_window_size(*size)

    @staticmethod
    def __get_size(direct: Literal["Width", "Height"], select: str) -> str:
        """
        Execute a JavaScript code through which we will obtain the measurement of the whole page, either in width or height.

        Parameters
        ----------
            direct: `Literal[Width, Height]`
                Direction from which we want to obtain the measurement
            select `str`:
                CSS selector of the element to be taken as maximum

        Returns
        -------
            str: Measurement in text form
        """
        return Renderer.__driver.execute_script(
            f"return document.querySelector('{select}').parentNode.scroll{direct}"
        )

    @staticmethod
    @__configure_driver
    def screenshot(
        url: str,
        path: str,
        selector: str,
        size: Annotated[List[str], 2],
        timeout: float,
    ) -> bool:
        """
        A method to take a screenshot of the given url.

        Parameters
        ----------
        url: `str`
            The url to take a screenshot.
        path: `str`
            The path of the screenshot.
        selector: `str`
            The selector of element to capture.
        size: `List[str, str]`
            The size of the screenshot
        timeout: `float`
            The timeout of the screenshot.

        Returns
        -------
        bool
            `True`: if the screenshot was taken.
            `False`: if the screenshot was not taken.
        """
        try:
            Renderer.__driver.get(url)
            Renderer.__await_element(selector, timeout)

            if size != ["1920", "1080"]: 
                Renderer.__cover_window(size, selector)
            
            Renderer.__driver.find_element(
                By.CSS_SELECTOR, 
                selector
            ).screenshot(path)
            
            return os.path.exists(path)
        except TimeoutException:
            return False
        
        except Exception:
            return False

    @staticmethod
    @__configure_driver
    def raw(
        url: str,
        path: str,
        selector: str,
        size: Annotated[List[str], 2],
        timeout: float,
    ):
        """
        A method to get the raw of a image

        Types of raw:
            bin:
                The raw of the image in binary format.
            base64:
                The raw of the image in base64 format.

        Parameters
        ----------
        url: str
            The url to get the raw html.
        path: str
            The path of file.
        selector: str
            The selector of element to capture.
        timeout: float (default: 2.5)
            The timeout of the screenshot.

        Returns
        -------
        bool
            `True`: if the screenshot was taken.
            `False`: if the screenshot was not taken.
        """
        try:
            Renderer.__driver.get(url)
            Renderer.__await_element(selector, timeout)

            if size != ["1920", "1080"]: 
                Renderer.__cover_window(size, selector)
            
            element = Renderer.__driver.find_element(By.CSS_SELECTOR, selector)
            is_bin = path.endswith(".bin")

            with open(path, ("w", "wb")[is_bin]) as file:
                source = (
                    element.screenshot_as_png
                    if is_bin
                    else element.screenshot_as_base64
                )

                file.write(source)

            return os.path.exists(path)

        except TimeoutException:
            return False

        except Exception:
            return False   
        
