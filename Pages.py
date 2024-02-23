from BaseApp import BasePage, screenshot
from selenium.webdriver.remote.webelement import WebElement
import locators
import logging
import os
import time
import re


logger = logging.getLogger(__name__)



class SBISMainPage(BasePage):
    '''
    Main page of SBIS
    '''
    
    def click_to_header(self, name: str) -> None:
        """
    	Click to the header link based on the provided menu name.
        
        Args:
            menu (str): The menu item to click on.
    	"""
        try:
            logger.info(f"Click to header menu: {name}.")
            all_headers = self.find_elements(locators.SBISMainPageLocators.LOCATOR_HEADER)
            wanted_menu = [item for item in all_headers if name in item.text][0]
            wanted_menu.click()
        except Exception as error:
            logger.exception(f"Can't click to header menu {name}: {error}")
            screenshot(self.driver, 'click_to_header')

    def click_to_footer(self, name: str) -> WebElement | None:

        try:
            logger.info(f"Click to footer menu: {name}.")
            all_footers = self.find_elements(locators.SBISMainPageLocators.LOCATOR_FOOTER)
            wanted_menu = [item for item in all_footers if name in item.text][0]
            self.scroll_to_element(wanted_menu)
            return wanted_menu.click()
        except Exception as error:
            logger.exception(f"Can't click to footer menu {name}: {error}")
            screenshot(self.driver, 'click_to_footer')

    

class SBISContactPage(BasePage):
    '''
    Contact page of SBIS
    '''

    def click_to_the_logo(self) -> None:
        """
        Click to the logo element.
        """
        try:
            logger.info(f"Click to the logo.")
            logo_page = self.find_element(locators.SBISContactPageLocators.LOCATOR_LOGO_TENSOR)
            logo_page.click()
        except Exception as error:  
            logger.exception(f"Can't click on the logo: {error}")
            screenshot(self.driver, 'click_to_the_logo')
    
    def check_region_chooser(self) -> WebElement | None:
        """
        Check the region chooser and return the first element found, or None if not found.
        """
        try:
            logger.info(f"Check the region chooser.")
            all_region_choosers = self.find_elements(locators.SBISContactPageLocators.LOCATOR_REGION_CHOOSER)
            return all_region_choosers[0]
        except Exception as error:
            logger.exception(f"Can't choose a region: {error}")
            screenshot(self.driver, 'region_chooser')
    
    def check_partners_list(self) -> WebElement | None:
        """
        Check the partners list and return the WebElement or None if not found.
        """
        try:
            logger.info(f"Check the partners list.")
            all_partners = self.find_elements(locators.SBISContactPageLocators.LOCATORS_PARTNERS_LIST)
            return all_partners
        except Exception as error:
            logger.exception(f"Can't check the partners list: {error}")
            screenshot(self.driver, 'check_partners_list')
    
    def change_region(self, region: str) -> None:
        """
        Change the region.

        Args:
            region (str): The region to change to.
        """
        try:
            logger.info(f"Change the region to: {region}.")
            original_url = self.get_url()
            self.check_region_chooser().click()
            regions_panel = self.find_element(locators.SBISContactPageLocators.LOCATORS_REGIONS_PANEL)
            all_regions = self.find_elements(locators.SBISContactPageLocators.LOCATORS_REGIONS_PANEL_ITEMS, parent=regions_panel)
            wanted_region = [item for item in all_regions if region in item.text][0]
            wanted_region.click()
            self.wait_SPA_url_change(original_url)
        except Exception as error:
            logger.exception(f"Can't change the region: {error}")
            screenshot(self.driver, 'change_region')

class SBISDownloadPage(BasePage):

    def __init__(self, driver):
        try:
            logger.info(f"Init Download page.")
            self.driver = driver
            self.base_url = 'https://sbis.ru/download'
            self.wait_SPA_url_change(self.base_url)
        except Exception as error:
            logger.exception(f"Can't init Download page: {error}")
            screenshot(self.driver, 'init_download_page')

    def switch_os(self, name: str) -> None:
        """
        A method to switch the operating system on the page.

        Args:
            name (str): The name of the operating system to switch to.
        """
        try:
            logger.info(f"Switch OS to: {name}.")
            original_url = self.get_url()
            if name == 'Windows' and 'innerTab=default' in self.get_url():
                return
            os_menu = self.find_elements(locators.SBISDownloadPageLocators.LOCATOR_DOWNLOAD_OS_MENU_BUTTONS)
            wanted_os = [item for item in os_menu if name in item.text and item.is_displayed()][0]
            wanted_os.click()
            self.wait_SPA_url_change(original_url)
        except Exception as error:
            logger.exception(f"Can't switch OS: {error}")
            screenshot(self.driver, 'switch_os')

    def click_vertical_menu(self, name: str) -> None:
        """
        Clicks on the specified vertical menu item.
        
        Args:
            name (str): The name of the vertical menu item to be clicked.
        """
        try:
            logger.info(f"Click vertical menu: {name}.")
            original_url = self.get_url()
            vertical_menu = self.find_elements(locators.SBISDownloadPageLocators.LOCATOR_VERTICAL_MENU)
            wanted_menu = [item for item in vertical_menu if name in item.text][0]
            wanted_menu.click()
            self.wait_SPA_url_change(original_url)
        except Exception as error:
            logger.exception(f"Can't click vertical menu: {error}")
            screenshot(self.driver, 'click_vertical_menu')

    def click_download_link(self, name: str) -> dict:
        """
        Clicks on a download link with the given name.

        Args:
            name (str): The name of the download link to click.

        Returns:
            dict: {
                'name': file_name,
                'size': file_size
                  }
        """
        try:
            logger.info(f"Click download link: {name}.")
            all_download_blocks = self.find_elements(locators.SBISDownloadPageLocators.LOCATOR_DOWNLOAD_BLOCK)
            wanted_block = [item for item in all_download_blocks if name in self.find_element(
                locators.SBISDownloadPageLocators.LOCATOR_DOWNLOAD_BLOCK_TITLE,
                parent=item
                ).text][0]
            link = self.find_element(locators.SBISDownloadPageLocators.LOCATOR_DOWNLOAD_LINK, parent=wanted_block)
            link.click()
            file_name = link.get_attribute('href').split('/')[-1]
            file_size = re.search(r'\d+\.\d+', link.text).group()
            return {
                'name':file_name,
                'size': file_size
                }
        except Exception as error:
            logger.exception(f"Can't click download link: {error}")
            screenshot(self.driver, 'click_download_link')

    def wait_for_download(self, download_dir, file_name, file_size: float, timeout=60) -> bool:
        """
        A function to wait for a file to be downloaded to the specified directory, with a specified file name and size within a given timeout period.
        
        Parameters:
            download_dir: The directory where the file is expected to be downloaded.
            file_name: The name of the file to be downloaded.
            file_size: The expected size of the file to be downloaded.
            timeout: The maximum time to wait for the file to be downloaded (default is 60 seconds).
            
        Returns:
            bool: True if the file is successfully downloaded within the specified parameters, False otherwise.
        """
        try:
            logger.info(f"Wait for download: {download_dir}, {file_name}, {file_size} mb.")
            start_time = time.time()
            file_path = os.path.dirname(os.path.abspath(__file__)) + download_dir + '\\' + file_name
            while not os.path.exists(file_path):
                time.sleep(1)
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"Timeout: File {file_name} not found within {timeout} seconds.")
            actual_file_size = os.path.getsize(file_path)
            lower_bound = file_size - 1024
            upper_bound = file_size + 1024
            if not lower_bound <= file_size <= upper_bound:
                raise ValueError(f"File {file_name} size ({file_size} bytes) is not within the acceptable tolerance.")
            return True
        except Exception as error:
            logger.exception(f"Can't wait for download: {error}")
            screenshot(self.driver, 'wait_for_download')
                
class TensorMainPage(BasePage):
    '''
    Tensor main page
    '''
    def __init__(self, driver):
        try:
            logger.info(f"Init Tensor main page.")
            super().__init__(driver)
            self.switch_to_new_tab()
        except Exception as error:
            logger.exception(f"Can't switch to new tab: {error}")
            screenshot(self.driver, 'switch_to_new_tab')

    def find_cards(self) -> list[WebElement] | None:
        """
        Find and return the cards elements.
        """
        try:
            logger.info(f"Find the cards.")
            all_cards = self.find_elements(locators.TensorMainPageLocators.LOCATOR_CARD)
            return all_cards
        except Exception as error:
            logger.exception(f"Can't find the cards: {error}")
            screenshot(self.driver, 'find_cards')
    
    def check_card(self, cards: list[WebElement], card_text: str) -> WebElement | None:
        """
        Check if the given card text exists in the list of cards.

        Args:
            cards (list[WebElement]): A list of WebElement objects representing the cards.
            card_text (str): The text to search for in the cards.
        """
        try:
            logger.info(f"Check the card.")
            # NOTE: isn't used
            # self.switch_to_window_with_title('Тензор — IT-компания')
            # all_cards = self.find_elements(locators.TensorMainPageLocators.LOCATOR_CARD)
            # wanted_card = [item for item in cards if card_text in item.text][0]
            for card in cards:
                if card_text in card.text:
                    return card
        except Exception as error:
            logger.exception(f"Can't check the card: {error}")
            screenshot(self.driver, 'check_card')

    def click_to_the_detail_link(self, parent) -> None:
        """
        Clicks on the detail link after finding the element and scrolling to it.
        """
        try:
            logger.info(f"Click to the detail link.")
            detail_page = self.find_element(locators.TensorMainPageLocators.LOCATOR_LINK, parent=parent)
            self.scroll_to_element(detail_page)
            detail_page.click()
        except Exception as error:
            logger.exception(f"Can't click to the detail link: {error}")
            screenshot(self.driver, 'click_to_the_detail_link')
    
class TensorAboutPage(BasePage):
    '''
    Tensor about page
    '''

    def check_photos(self, block_name: str) -> bool:
        """
        Check the photos in given block on the page and verify if they all have the same dimensions. 
        Returns True if all photos have the same dimensions, otherwise returns False.
        """
        try:
            logger.info(f"Check the photos.")
            all_sections = self.find_elements(locators.TensorAboutPageLocators.LOCATOR_SECTION)
            wanted_section = [item for item in all_sections if block_name in item.text][0]
            all_images = self.find_elements(locators.TensorAboutPageLocators.LOCATOR_IMAGES, parent=wanted_section)
            wight = all_images[0].get_attribute('width')
            height = all_images[0].get_attribute('height')
            for image in all_images[1:]:
                if image.get_attribute('width') != wight or image.get_attribute('height') != height:
                    return False
            return True
        except Exception as error:
            logger.exception(f"Can't check the photos: {error}")
            screenshot(self.driver, 'check_photos')
