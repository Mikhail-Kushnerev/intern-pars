import sys
import logging

from redis import Redis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_stealth import stealth

from constants import BASE_DIR, DT_FORMAT, LOG_FORMAT


options: Options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver: WebDriver = webdriver.Chrome(
    options=options,
    executable_path=fr"{BASE_DIR}\driver\chromedriver.exe"
)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

redis_client: Redis = Redis()


def config_logging():
    logging.basicConfig(
            level=logging.INFO,
            format=LOG_FORMAT,
            datefmt=DT_FORMAT,
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    logging.getLogger(__file__)
