from selenium.webdriver.common.by import By

from exceptions import EmptyList, NoPrice


def check_items(driver, element, value):
    try:
        block = driver.find_element(element, value)
    except Exception:
        print(Exception("Ничего нет"))
        return False
    else:
        return block


def check_price(tag, element, value):
    try:
        price = tag.find_element(element, value)
        try:
            promo = tag.find_element(By.CSS_SELECTOR, ".S_8")
        except:
            return price.text
        else:
            return (price.text, promo.text)
    except Exception:
        empty = tag.find_element(By.CLASS_NAME, "r_2")
        return empty.text
    # return price.text
