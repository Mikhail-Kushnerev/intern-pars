import logging
import re
import time
from typing import Match

from selenium.webdriver.remote.webelement import WebElement
from tqdm import tqdm
from selenium.webdriver.common.by import By
from constants import URL, PATTERN
from configs import driver, config_logging
from utils import check_items, check_price, check_connect, check_click_opt
from outputs import write_csv


objects_history: dict[str, list[str]] = {}


def pars_item() -> None:
    for i in tqdm(objects_history.values()):
        driver.get(i[0])
        time.sleep(1)
        check_click_opt(driver, By.CLASS_NAME, "nK")
        div_tag: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, ".c_5 .rt")
        print(i[0], len(div_tag))
        string: Match[str] | None = re.search(PATTERN, div_tag[1].text)
        if string:
            i.extend(string.group("ID", "country"))
        driver.refresh()


def pars_site(items: list[object]) -> None:
    for i in tqdm(items):
        target: WebElement = i.find_element(By.TAG_NAME, "a")
        link: str = target.get_attribute("href")
        name: WebElement = target.find_element(By.CSS_SELECTOR, ".SW")
        if name.text in objects_history:
            continue
        promo: str = "null"
        div_tag = check_price(target, By.CSS_SELECTOR, ".S_6")
        if len(div_tag) == 2:
            promo: list[str] = re.findall(r"\d+", div_tag[1])
            div_tag: str = div_tag[0]
        div_tag: list[str] | str = re.findall(r"\d+", div_tag) if div_tag != "Нет в наличии" else div_tag
        objects_history[name.text] = [link, ''.join(div_tag), ''.join(promo)]
    return pars_item()


def main():
    logger = config_logging()
    page: int = 1
    while True:
        site: str = URL + "page/{}/".format(page)
        connect = check_connect(driver, site)
        if not connect:
            logger.error("Дизконнект")
            return
        logging.info(f"Есть соединение c {site}")
        time.sleep(1)
        block: WebElement = check_items(driver, By.CLASS_NAME, "uo")
        if not block:
            break
        items: list[WebElement] = block.find_elements(By.CSS_SELECTOR, ".vk .vm")
        pars_site(items)
        page += 1
        driver.refresh()
    driver.quit()
    logging.info("Запись файла")
    write_csv(objects_history)


if __name__ == "__main__":
    main()
