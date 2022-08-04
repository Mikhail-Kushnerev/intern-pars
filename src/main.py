import logging
import re
import time
from typing import Match

from tqdm import tqdm
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from src.constants import URL, PATTERN
from src.configs import driver, config_logging, redis_client
from src.utils import check_items, check_price, check_connect, check_click_opt
from src.outputs import write_csv

objects_history: dict[str, list[str]] = {}


def pars_item(items) -> None:
    """
    Разбор товаров на ID и страну-производителя
    :param items: список кортежей
    """
    for (link, target) in tqdm(items):
        check_connect(driver, link)
        time.sleep(0.5)
        check_click_opt(driver, By.CLASS_NAME, "nK")
        time.sleep(0.5)
        div_tag: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, ".c_5 .rt")
        string: Match[str] | None = re.search(PATTERN, div_tag[1].text)
        if string:
            target.extend(string.group("ID", "country"))


def pars_site(items: list[WebElement]) -> dict[str, list[str]]:
    """
    Разбор конкретной страницы на название товара, цену (актуальную/нет), ссылки
    :param items: список товаров
    :return: промежуточный словарь для записи уникальных товаров
    """
    item_pars: list[tuple[str, list[str]]] = []
    part_result: dict[str, list[str]] = {}
    for i in items:
        target: WebElement = i.find_element(By.TAG_NAME, "a")
        link: str = target.get_attribute("href")
        name: WebElement = target.find_element(By.CSS_SELECTOR, ".SW")
        if (obj := name.text) in objects_history or obj.encode() in redis_client.keys():
            continue
        with redis_client:
            redis_client.set(obj, obj)
        promo: str = "null"
        div_tag = check_price(target, By.CSS_SELECTOR, ".S_6")
        if len(div_tag) == 2:
            promo: list[str] = re.findall(r"\d+", div_tag[1])
            div_tag: str = div_tag[0]
        div_tag: list[str] | str = re.findall(r"\d+", div_tag) if div_tag != "Нет в наличии" else div_tag
        objects_history[name.text] = [link, ''.join(div_tag), ''.join(promo)]
        item_pars.append((link, objects_history[obj]))
        part_result[obj]: dict[str, list[str]] = objects_history[obj]
    pars_item(item_pars)
    return part_result


def main():
    config_logging()
    logging.info("Запуск парсера")
    page: int = 1
    while True:
        site: str = URL + "page/{}/".format(page)
        connect = check_connect(driver, site)
        if not connect:
            logging.error("Дизконнект")
            return
        logging.info(f"Есть соединение c {site}")
        time.sleep(1)
        block: WebElement = check_items(driver, By.CSS_SELECTOR, ".dv .dV .uo")
        if not block:
            break
        items: list[WebElement] = block.find_elements(By.CSS_SELECTOR, ".vk .vm")
        part_result: dict[str, list[str]] = pars_site(items)
        logging.info(f"Запись данных страницы {page}")
        write_csv(part_result)
        page += 1
    driver.quit()
    objects_history.clear()
    with redis_client:
        redis_client.flushdb()
    logging.info("Завершение работы")


if __name__ == "__main__":
    main()
