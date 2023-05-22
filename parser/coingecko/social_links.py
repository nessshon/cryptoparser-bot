""" 
This module provides a function for scraping social links of a cryptocurrency token from coingecko.com. 

Function: 
- get_social_links(address: str) -> dict:  
  Given a token address, this function returns a dictionary containing the social links of the token if available. 

Example usage: 
    data = get_social_links('bitcoin') #returns social links of Bitcoin 

Dependencies: 
    - selenium 
    - ChromeDriver 

Note:  
    - The ChromeDriver path should be added to the system environment variables. 
    - The function uses Chrome in a headless mode for scraping data.  
"""
from contextlib import suppress
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser.driver import get_driver


def get_social_links(address: str) -> dict:
    """ 
    Given a token address, this function returns a dictionary containing
    the social links of the token if available.

    Parameters: 
        address (str): The address of the token for which
        social links are to be extracted.

    Returns: 
        data (dict): A dictionary containing the social links of the token,
        with the key as the social media platform and value as the URL.

    Raises: 
        Raises TimeoutException if the webpage takes too long to load. 
    """
    driver = get_driver()

    try:
        data: dict = {}

        driver.get(f'https://www.coingecko.com/ru/Криптовалюты/{address}')

        with suppress(TimeoutException):
            disclaimer_menu = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "cookie-notice"))
            )
            agree_button = disclaimer_menu.find_element(By.XPATH, '//button[contains(text(), "Соглашаюсь")]')
            driver.execute_script("arguments[0].click();", agree_button)

        website_element = driver.find_element(
            By.XPATH,
            '//span[contains(text(), "Веб-сайт")]/following-sibling::div/a'
        )
        data['Web-site'] = website_element.get_attribute('href')

        social_elements = driver.find_elements(
            By.XPATH,
            '//span[contains(text(), "Сообщество")]/following-sibling::div/a'
        )
        for element in social_elements:
            try:
                link_type = element.find_element(By.TAG_NAME, 'i').get_attribute('class').split('fa-')[1]
                key, value = link_type.capitalize(), element.get_attribute('href')
            except NoSuchElementException:
                key, value = element.text, element.get_attribute('href')
            if "instagram.com" in value:
                key = 'Instagram'
            if "youtube.com" in value:
                key = 'Youtube'

            data[key] = value

        return data

    finally:
        driver.quit()
