import logging

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


options = webdriver.ChromeOptions()
options.add_argument("--window-size=1366,768")
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(
    options=options
    )


def search_in_wb(search_words):
    try:
        driver.get('https://www.wildberries.ru/')
        sleep(3)
        button_search = driver.find_element(By.CSS_SELECTOR, '#searchInput')
        button_search.send_keys(search_words)
        button_search.send_keys(Keys.ENTER)
        sleep(4)
    except StaleElementReferenceException:
        logging.error(StaleElementReferenceException, exc_info=True)