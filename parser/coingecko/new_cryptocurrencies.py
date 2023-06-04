"""
This module is used to retrieve a list of new cryptocurrencies from the CoinGecko
website using Selenium webdriver.

Classes:
- Chain: represents a blockchain network and contains its name and contract address.
- Token: represents a cryptocurrency and contains its name, symbol, price, 1-hour
         change, 24-hour change, 24-hour volume, FDV, and last added timestamp.

Functions:
- get_new_cryptocurrencies: retrieves a list of new cryptocurrencies from the CoinGecko website
                            using Selenium webdriver. It returns a list of Token objects.
"""
import logging
from dataclasses import dataclass

from selenium.common import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser import BASE_DIR
from parser.driver import get_driver


@dataclass
class Chain:
    name: str
    contract_address: str


@dataclass
class Token:
    class ChainType:
        BSC = "BNB Smart Chain"
        Ethereum = "Ethereum"

    chains: list[Chain]
    name: str
    symbol: str
    price: str
    one_hour_change: str
    twenty_four_hour_change: str
    twenty_four_hour_volume: str
    FDV: str
    last_added: str


class LastToken:
    def __init__(self, filename: str = f"{BASE_DIR}/data/last_token"):
        self.filename = filename

    def save(self, text: str) -> None:
        with open(self.filename, "w") as f:
            f.write(text)

    def update(self, new_text: str) -> None:
        with open(self.filename, "w") as f:
            f.write(new_text)

    def load(self) -> None | str:
        try:
            with open(self.filename, "r") as f:
                text = f.read()
        except FileNotFoundError:
            self.save(str())
            return None

        return text


def get_new_tokens() -> list[Token]:
    """
    Retrieves a list of new tokens (cryptocurrencies) since the last retrieved token.

    Returns:
        list: A list of new tokens.
    """
    last_token = LastToken().load()
    new_tokens: list[Token] = []

    try:
        tokens = get_new_cryptocurrencies()

        if last_token is None:
            new_tokens = tokens
        else:
            for token in tokens:
                if token.chains[0].contract_address == last_token:
                    break
                new_tokens.append(token)
        LastToken().update(tokens[0].chains[0].contract_address)

    except Exception as err:
        logging.error(err)

    return new_tokens


def get_new_cryptocurrencies() -> list[Token]:
    """
    This function is used to get a list of new cryptocurrencies from the CoinGecko website. It uses Selenium to open
    a webdriver headless and retrieve a list of Token objects. It iterates over the table body specified in the website
    and extracts the details of the cryptocurrency such as name, symbol, price, 24 hour change, 24 hour volume, FDV,
    and last added. The function returns a list of Token objects.
    """
    driver = get_driver()

    try:
        tokens: list[Token] = []
        chains: list[Chain] = []

        driver.get('https://www.coingecko.com/ru/new-cryptocurrencies')
        for element in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "tbody[data-target='currencies.contentBox'] tr"))):

            try:
                dropdown_button = element.find_element(By.ID, 'dropdownMenuButton')
                dropdown_button.click()
                names = dropdown_button.find_elements(By.CLASS_NAME, 'font-bold')
                contract_addresses = dropdown_button.find_elements(By.CSS_SELECTOR, 'i[data-address]')
                chains = [Chain(name=name.text, contract_address=contract_address.get_attribute("data-address")) for
                          name, contract_address in zip(names, contract_addresses)]
                dropdown_button.click()
            except NoSuchElementException:
                pass

            token = Token(
                chains=chains,
                name=element.find_element(
                    By.CSS_SELECTOR,
                    "span[class='lg:tw-flex font-bold tw-items-center tw-justify-between']").text,
                symbol=element.find_element(
                    By.CSS_SELECTOR,
                    "span[class='d-lg-inline font-normal text-3xs tw-ml-0 md:tw-ml-2 md:"
                    "tw-self-center tw-text-gray-500 dark:tw-text-white dark:tw-text-opacity-60']").text,
                price=element.find_element(
                    By.CSS_SELECTOR,
                    "span[class='no-wrap']").get_attribute("data-price-previous"),
                one_hour_change=element.find_element(
                    By.CSS_SELECTOR,
                    "td[class='td-change1h change1h stat-percent text-right col-market']").text.strip('%'),
                twenty_four_hour_change=element.find_element(
                    By.CSS_SELECTOR,
                    "td[class='td-change24h change24h stat-percent text-right col-market']").text.strip('%'),
                twenty_four_hour_volume=element.find_element(
                    By.CSS_SELECTOR,
                    "td[class='td-liquidity_score lit text-right col-market']").text,
                FDV=element.find_element(
                    By.CSS_SELECTOR,
                    "td[class='td-fdv tw-text-right']").text,
                last_added=element.find_element(
                    By.CLASS_NAME, "trade").text
            )
            tokens.append(token)
        return tokens

    except Exception as err:
        logging.error(err)

    finally:
        driver.quit()
