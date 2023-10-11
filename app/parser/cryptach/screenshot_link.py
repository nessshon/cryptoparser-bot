import logging
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from app.parser.driver import get_driver


def get_screenshot_link(token_address: str) -> bytes | None:
    """
    This function takes a screenshot of a given token address
    from the website https://cryptach.org/ru/scan/

    Args:
        token_address (str): The address of the token

    Returns:
        bytes: The screenshot image data in bytes, if successful.
        None: If an error occurred or the screenshot couldn't be taken.
    """
    driver = get_driver()

    try:
        driver.get(f'https://cryptach.org/en/scan/{token_address}')

        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.ID, 'global-loader'))
        )

        result_error = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'result-error'))
        )
        text_errors = ['error', 'There is no information about this address.', 'Invalid address']
        if result_error.text in text_errors:
            return None

        driver.execute_script("document.body.style.zoom='50%'")

        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.row.d-flex.justify-content-center'))
        )
        screenshot = element.screenshot_as_png

        return screenshot

    except Exception as err:
        logging.error(traceback.format_exc())
        logging.error(err)

    finally:
        driver.quit()
