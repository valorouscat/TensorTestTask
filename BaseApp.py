from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import logging
import datetime


logger = logging.getLogger(__name__)

def screenshot(driver, item) -> None:
    """
    Generate a screenshot using the provided driver and item.

    Parameters:
        driver (object): The driver for capturing the screenshot.
        item (str): The item to be included in the screenshot filename.
    """
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    driver.save_screenshot(f'screenshot_{timestamp}_{item}.png')


class BasePage:

    def __init__(self, driver):
        """
        Initializes the class with the provided driver and sets the base URL to 'https://sbis.ru/'.
        """
        self.driver = driver
        self.base_url = 'https://sbis.ru/'

    def find_element(self, locator, parent=None, time=2) -> WebElement | None:
        """
        Find and return an element located by the given locator within the specified parent element or the default driver. 
        If the element is not found within the specified time, an exception is raised.
        
        Args:
            locator: The locator used to find the element.
            parent: The parent element within which to search for the element (default is None).
            time: The time to wait for the element to be located (default is 2).
        """
        try:
            if parent:
                logger.info(f"Find element by locator {locator} in parent {parent}")
                return WebDriverWait(parent, time).until(EC.presence_of_element_located(locator),
                                                        message=f"Can't find element by locator {locator} in parent {parent}")
            else:
                logger.info(f"Find element by locator {locator}")
                return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                              message=f"Can't find element by locator {locator}")
        except Exception as error:
            if parent:
                logger.exception(f"Can't find element by locator {locator} in parent {parent}: {error}")
                screenshot(self.driver, locator)
            else:
                logger.exception(f"Can't find element by locator {locator}: {error}")
                screenshot(self.driver, locator)

    def find_elements(self, locator, parent=None, time=2) -> list[WebElement] | None:
        """
        Find and return an elements located by the given locator within the specified parent element or the default driver. 
        If the elements is not found within the specified time, an exception is raised.
        
        Args:
            locator: The locator used to find the elements.
            parent: The parent element within which to search for the element (default is None).
            time: The time to wait for the element to be located (default is 2).
        """
        try:
            if parent:
                logger.info(f"Find elements by locator {locator} in parent {parent}")
                return WebDriverWait(parent, time).until(EC.presence_of_all_elements_located(locator),
                                                         message=f"Can't find elements by locator {locator} in parent {parent}")
            else:
                logger.info(f"Find elements by locator {locator}")
                return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                              message=f"Can't find elements by locator {locator}")
        except Exception as error:
            if parent:
                logger.exception(f"Can't find elements by locator {locator} in parent {parent}: {error}")
                screenshot(self.driver, locator)
            else:
                logger.exception(f"Can't find elements by locator {locator}: {error}")
                screenshot(self.driver, locator)

    def go_to_site(self) -> None:
        """
        A method to navigate to a website using the provided base URL.
        """
        try:
            logger.info(f"Open site {self.base_url}")
            self.driver.get(self.base_url)
        except Exception as error:
            logger.exception(f"Can't open site {self.base_url}: {error}")
            screenshot(self.driver, self.base_url)
    
    # NOTE: this method is not used, found better (in my opinion) sollution
    # def switch_to_window_with_title(self, title: str) -> None:
    #     """
    #     Switches to a window with the specified title.

    #     Args:
    #         title (str): The title of the window to switch to.
    #     """
    #     try: 
    #         logger.info(f"Switch to window with title {title}")
    #         for window in self.driver.window_handles:
    #             self.driver.switch_to.window(window)
    #             if self.driver.title == title:
    #                 return

    #         logger.warning(f"Can't switch to window with title {title}")
    #     except Exception as error:
    #         logger.exception(f"Can't switch to window with title {title}: {error}")
    #         screenshot(self.driver, title)
            
    def switch_to_new_tab(self) -> None:
        """
        Switches to a new tab in the browser window.
        """
        try:
            logger.info(f"Switch to new tab")
            WebDriverWait(self.driver, 2).until(EC.number_of_windows_to_be(2))
            self.driver.switch_to.window(self.driver.window_handles[1])
        except Exception as error:
            logger.exception(f"Can't switch to new tab: {error}")
            screenshot(self.driver, 'switch_to_new_tab')
    
    def get_url(self) -> str | None:
        """
        Method to get the current URL from the driver.
        """
        try:
            logger.info(f"Get url {self.driver.current_url}")
            return self.driver.current_url
        except Exception as error:
            logger.exception(f"Can't get url {error}")
            screenshot(self.driver, 'get_url')
    
    def scroll_to_element(self, element) -> None:
        """
        Scroll to the specified element using JavaScript scrollIntoView function.

        Args:
            element: The element to scroll to.
        """
        try:
            logger.info(f"Scroll to element {element}")
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except Exception as error:
            logger.exception(f"Can't scroll to element: {error}")
            screenshot(self.driver, 'scroll_to_element')

    def wait_SPA_url_change(self, original_url) -> bool | None:
        """
        Check if the Single Page Application (SPA) URL has changed.

        Args:
            original_url (str): The original URL to compare against.
        """
        try:
            logger.info(f"Check SPA url change {original_url}")
            return WebDriverWait(self.driver, 2).until(EC.url_changes(original_url), message=f"Can't wait SPA url change for {original_url}")
        except Exception as error:
            logger.exception(f"Can't wait SPA url change: {error}")
            screenshot(self.driver, 'wait_SPA_url_change')

    def get_title(self) -> str | None:
        """
        Method to get the title of current page from the driver.
        """
        try:
            logger.info(f"Get title {self.driver.title}")
            return self.driver.title
        except Exception as error:
            logger.exception(f"Can't get title {error}")
            screenshot(self.driver, 'get_title')