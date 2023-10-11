from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import PATTERN
from webdriver_manager.core.utils import read_version_from_cmd


def get_driver() -> WebDriver:
    chrome_options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  # noqa
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")

    version = read_version_from_cmd("google-chrome --version", PATTERN["google-chrome"])
    service = Service(ChromeDriverManager(driver_version=version).install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
