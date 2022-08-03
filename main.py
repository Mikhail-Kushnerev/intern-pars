import re
import time
from pprint import pprint as pp

from tqdm import tqdm
from selenium.webdriver.common.by import By

from constants import URL, PATTERN
from configs import driver
from utils import check_items, check_price


def main():
    d = {}
    # site: int = 1
    # while True:
    #     site += 1
    driver.get(URL)
    time.sleep(3)
    block = check_items(driver, By.CLASS_NAME, "uo")
    if not block:
        return
    items = block.find_elements(By.CSS_SELECTOR, ".vm")
    for i in tqdm(items):
        tag_a = i.find_element(By.TAG_NAME, "a")

        link = tag_a.get_attribute("href")
        name = tag_a.find_element(By.CSS_SELECTOR, ".SW")
        promo = ""
        div_tag = check_price(tag_a, By.CSS_SELECTOR, ".S_6")
        if len(div_tag) == 2:
            promo = re.findall(r"\d+", div_tag[1])
            div_tag = div_tag[0]
        div_tag = re.findall(r"\d+", div_tag)
        d[name.text] = [link, ''.join(div_tag), ''.join(promo)]
    for i in tqdm(d.values()):
        driver.get(i[0])
        time.sleep(3)
        try:
            driver.find_element(By.CLASS_NAME, "nK").click()
        except:
            pass
        div_tag = driver.find_elements(By.CSS_SELECTOR, ".c_5 .rt")[1]
        string = re.search(PATTERN, div_tag.text)
        if string:
            i.extend(string.group("ID", "country"))
        print(i)

    pp(len(d))
    # time.sleep(3)
    driver.quit()


if __name__ == "__main__":
    main()
