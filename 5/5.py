from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.firefox.options import Options
import time
import hashlib
from pprint import pprint
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
new_goods = db.new_good


chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.mvideo.ru'
title_site = 'М.Видео'

driver.get(url)

assert title_site in driver.title

time.sleep(5)

section = driver.find_element_by_xpath(
    "//h2[contains(text(), 'Новинки')]/ancestor::div[3]")
actions = ActionChains(driver)
actions.move_to_element(section).perform()

btn = driver.find_element_by_xpath(
    "//h2[contains(text(), 'Новинки')]/ancestor::div[3]//a[contains(@class, 'i-icon-fl-arrow-right')]")

while True:
    time.sleep(2)
    items = driver.find_elements_by_xpath(
        "//h2[contains(text(), 'Новинки')]/ancestor::div[3]//li[contains(@class, 'gallery-list-item')]")

    for item in items:
        data = {}
        data['item'] = item.text

        hash_obj = hashlib.sha1()
        hash_obj.update(repr(data).encode('utf-8'))  # хэшируем id
        id = hash_obj.hexdigest()
        data['_id'] = id
        try:
            new_goods.insert_one(data)  # пишем в базу только уникальный id
        except:
            next

    try:
        test = driver.find_element_by_xpath(
            "//h2[contains(text(), 'Новинки')]/ancestor::div[3]//a[contains(@class, 'i-icon-fl-arrow-right disabled')]")
        break
    except NoSuchElementException:
        btn.click()


driver.close()
driver.quit()

