import logging
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from app.parser.driver import get_driver


def get_screenshot_link(token_address: str) -> None | str:
    """
    This function parses the screenshot link for a given token
    address from the website https://cryptach.org/ru/scan/

    Args:
        token_address (str): The address of the token

    Returns:
        str: The link to the screenshot of the token, if it exists.
        False, if the link doesn't exist.
    """
    driver = get_driver()

    try:
        driver.get(f'https://cryptach.org/ru/scan/{token_address}')

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, 'global-loader'))
        )

        result_error = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'result-error'))
        )
        text_errors = ['Нет информации об этом адресе.', 'Неправильный адрес']
        if result_error.text in text_errors:
            return None

        screenshot_link_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'show-screenshot-link'))
        )
        driver.execute_script("arguments[0].click();", screenshot_link_button)

        screenshot_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="screenshot-link"]/a'))
        )
        return screenshot_link.get_attribute('href')

    except Exception as err:
        logging.error(traceback.format_exc())
        logging.error(err)

    finally:
        driver.quit()
