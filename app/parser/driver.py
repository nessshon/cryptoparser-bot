from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import PATTERN
from webdriver_manager.core.utils import read_version_from_cmd


def get_driver() -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")

    version = read_version_from_cmd("google-chrome --version", PATTERN["google-chrome"])
    service = Service(ChromeDriverManager(driver_version=version).install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
