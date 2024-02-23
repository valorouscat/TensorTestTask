from selenium.webdriver.common.by import By


class SBISMainPageLocators(object):

    LOCATOR_HEADER = (By.CSS_SELECTOR, '.sbisru-Header__menu-link')
    LOCATOR_FOOTER = (By.CSS_SELECTOR, '.sbisru-Footer__link')


class SBISContactPageLocators(object):

    LOCATOR_LOGO_TENSOR = (By.CSS_SELECTOR, '.sbisru-Contacts__logo-tensor')
    LOCATOR_REGION_CHOOSER = (By.CLASS_NAME, 'sbis_ru-Region-Chooser__text')
    LOCATORS_PARTNERS_LIST = (By.CLASS_NAME, 'sbisru-Contacts-List__col-1')
    LOCATORS_REGIONS_PANEL = (By.CLASS_NAME, 'sbis_ru-Region-Panel__list-l')
    LOCATORS_REGIONS_PANEL_ITEMS = (By.TAG_NAME, 'li')

class SBISDownloadPageLocators(object):

    LOCATOR_DOWNLOAD_OS_MENU_BUTTONS = (By.CSS_SELECTOR, '.sbis_ru-DownloadNew-innerTabs .controls-TabButton')
    LOCATOR_VERTICAL_MENU = (By.CSS_SELECTOR, '.sbis_ru-VerticalTabs__tabs .controls-TabButton')
    LOCATOR_DOWNLOAD_BLOCK = (By.CSS_SELECTOR, '.sbis_ru-DownloadNew-block')
    LOCATOR_DOWNLOAD_BLOCK_TITLE = (By.CSS_SELECTOR, '.sbis_ru-DownloadNew-h3')
    LOCATOR_DOWNLOAD_LINK = (By.CSS_SELECTOR, '.sbis_ru-DownloadNew-loadLink__link')

class TensorMainPageLocators(object):

    LOCATOR_CARD = (By.CSS_SELECTOR, '.tensor_ru-Index__card')
    LOCATOR_LINK = (By.CSS_SELECTOR, '.tensor_ru-Index__link')


class TensorAboutPageLocators(object):

    LOCATOR_SECTION = (By.CSS_SELECTOR, '.tensor_ru-container')
    LOCATOR_IMAGES = (By.TAG_NAME, 'img')