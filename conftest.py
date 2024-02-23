import pytest
from selenium import webdriver
import logging
import os
import glob


def pytest_configure():
    logging.basicConfig(filename='logs.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s - %(name)-8s - %(lineno)-3s - %(levelname)s - %(message)s',
                        encoding='utf-8')

@pytest.fixture(scope="function", autouse=True)
def browser():
    # Get the absolute path of the root directory of your project
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Set the download directory to the root folder of the project
    download_dir = os.path.join(project_root, 'downloads')

    # Create the 'downloads' directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    files = glob.glob(f'{download_dir}\\*')
    for f in files:
        os.remove(f)

    options = webdriver.ChromeOptions()

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit() 
