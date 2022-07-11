from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime
import time
import os


class HTMLRender:
    @staticmethod
    def init(PATH: str="public/builds") -> None:
        """
        A method to initialize the HTMLRender class.
        """
        print("\n\n\x1b[1;32m[HTMLRender]\x1b[0m - Initializing...")
        __options = webdriver.EdgeOptions()
        __options.headless = True

        HTMLRender.__PATH = PATH
        HTMLRender.__LOGS = os.path.join(os.getcwd(), "src", "errors.log")
        
        HTMLRender.__driver = webdriver.Edge(
            service=Service(EdgeChromiumDriverManager().install()),
            options=__options,
        )

        HTMLRender.__getSize = lambda direct, select: (
            HTMLRender.__driver.execute_script(
                f"return document.querySelector('{select}').parentNode.scroll{direct}"
            )
        )

        HTMLRender.__driver.set_window_size("1920", "1080")  # May need manual adjustment
        HTMLRender.__driver.get("about:blank")

    
    @staticmethod
    def __cover_window(size: list[str, str], selector: str) -> None:
        """
        Method for reconfiguring screen size by dynamic measurements.

        Parameters
        ----------
        size: list[str, str]
            The size of the window.
        
        selector: str
            CSS selector of the element to be covered.
        """
        fulls = size.count("full")
        if fulls == 2:  # [full, full]
            size = [
                HTMLRender.__getSize("Width", selector),
                HTMLRender.__getSize("Height", selector),
            ]

        elif fulls:  # [full, x] or [x, full]
            direct = size.index("full")
            size[direct] = HTMLRender.__getSize(("Width", "Height")[direct], selector)
        
        elif not "".join(size).isdigit(): # ["text", "text"] neither fulls nor digits
            raise ValueError("Invalid size.")
        
        HTMLRender.__driver.set_window_size(*size)

    
    @staticmethod
    def screenshot(url: str, filename: str, selector: str, size: list[str, str], timeout: float) -> bool:
        """
        A method to take a screenshot of the given url.

        Parameters
        ----------
        url: str
            The url to take a screenshot.
        filename: str
            The filename of the screenshot.
        selector: str
            The selector of element to capture.
        size: list[str, str]
            The size of the screenshot
        timeout: float
            The timeout of the screenshot.
            
        Returns
        -------
        bool
            True: if the screenshot was taken.
            False: if the screenshot was not taken.
        """
        try:
            HTMLRender.__driver.get(url)
            if size != ["1920", "1080"]: 
                HTMLRender.__cover_window(size, selector)
            time.sleep(timeout)

            HTMLRender.__driver.find_element(By.CSS_SELECTOR, selector).screenshot(f"{HTMLRender.__PATH}/{filename}")
            return os.path.exists(f"{HTMLRender.__PATH}/{filename}") # Return True if file exists
        
        except Exception as e:
            HTMLRender.generate_log(
                url= url,
                filename= filename,
                exception= e
            )
            return False

    @staticmethod
    def raw(url: str, filename: str, selector: str, size: list[str, str], timeout: float):
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
        selector: str
            The selector of element to capture.
        timeout: float (default: 2.5)
            The timeout of the screenshot.
        """
        try:
            HTMLRender.__driver.get(url)
            if size != ["1920", "1080"]: 
                HTMLRender.__cover_window(size, selector)
            time.sleep(timeout)

            element = HTMLRender.__driver.find_element(By.CSS_SELECTOR, selector)
            if filename.endswith(".bin"):
                element = element.screenshot_as_png
                with open(f"{HTMLRender.__PATH}/{filename}", "wb") as f:
                    f.write(element)
            else:
                element = element.screenshot_as_base64
                with open(f"{HTMLRender.__PATH}/{filename}", "w") as f:
                    f.write(element)
            
            return os.path.exists(f"{HTMLRender.__PATH}/{filename}") # Return True if file exists
        
        except Exception as e:
            HTMLRender.generate_log(
                url= url,
                filename= filename,
                exception= e
            )
            return False

    @staticmethod
    def recording(url, filename, format): pass

    
    @staticmethod
    def generate_log(url: str, filename: str, exception: Exception):
        """
        Function to generate logs about the errors that occur with the renderer.
        
        Parameters
        ----------
        url: str
            The url that was being rendered.
        filename: str
            The filename of the screenshot.
        exception: Exception
            The exception that was thrown.
        """
        print(f"\x1b[1;31m[HTMLRender]\x1b[0m - Error occurred during execution (generating log)")
        with open(HTMLRender.__LOGS, "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(60, "-"))
            f.write(f"\n[HTMLRender] - Error: {exception}")
            f.write(f"\nURL: '{url}'")
            f.write(f"\nFilename: '{filename}'")
            f.write("\nTraceback:")
            f.write(f"\n\tFrom: '{exception.__traceback__.tb_frame.f_code.co_filename}:{exception.__traceback__.tb_lineno}'")
            f.write(f"\n\tFunction: '{exception.__traceback__.tb_frame.f_code.co_name}'")
            f.write("\n\tArguments: {\n")
            for name, value in exception.__traceback__.tb_frame.f_locals.items(): f.write(f"\t\t{name}: {value}\n")
            f.write("\t}")
            f.write(f"\n\tException: {exception}")
            f.write("\n------------------------------------------------------------\n\n")