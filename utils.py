import time

from requests import RequestException

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver


def check_click_opt(driver: WebDriver, tag, value):
    try:
        driver.find_element(tag, value).click()
    except Exception:
        pass


def check_connect(driver: WebDriver, target: str):
    try:
        driver.get(target)
    except RequestException:
        for _ in range(2):
            time.sleep(3)
            driver.refresh()
        return driver.get(target)
    else:
        return True


def check_items(driver: WebDriver, element: str, value: str):
    try:
        block: WebElement = driver.find_element(element, value)
    except Exception:
        print(Exception("Ничего нет"))
        return False
    else:
        return block


def check_price(tag: WebElement, element: str, value: str):
    try:
        price: WebElement = tag.find_element(element, value)
        try:
            promo: WebElement = tag.find_element(By.CSS_SELECTOR, ".S_8")
        except Exception:
            return price.text
        else:
            return price.text, promo.text
    except Exception:
        empty: WebElement = tag.find_element(By.CLASS_NAME, "r_2")
        return empty.text
