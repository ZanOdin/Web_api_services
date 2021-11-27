import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['mail']
mail_mongo = db.mail
mail_list = []

driver = webdriver.Firefox()
driver.get('https://mail.ru/')

elem = driver.find_element(By.CLASS_NAME, 'email-input')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element(By.CLASS_NAME, 'button')
elem.click()
time.sleep(3)

elem = driver.find_element(By.CLASS_NAME, 'password-input')
elem.send_keys('NextPassword172#')

elem = driver.find_element(By.CLASS_NAME, 'second-button')
elem.click()
time.sleep(2)

elements = driver.find_elements(By.CLASS_NAME, 'llc')
i = 0

while i < len(elements):
    mail_info = {}
    link = elements[i].get_attribute('href')
    driver.get(link)
    time.sleep(1)

    who = driver.find_element(By.CLASS_NAME, 'letter-contact').text
    date = driver.find_element(By.CLASS_NAME, 'letter__date').text
    theme = driver.find_element(By.CLASS_NAME, 'thread__subject').text
    text = driver.find_element(By.CLASS_NAME, 'letter__body').text

    back_button = driver.find_element(By.CLASS_NAME, 'portal-menu-element')
    back_button.click()
    # ошибка при выходе и взятии элементов страницы
    mail_info['who'] = who
    mail_info['date'] = date
    mail_info['theme'] = theme
    mail_info['text'] = text

    mail_list.append(mail_info)
    mail_mongo.insert_one(mail_info)
    time.sleep(1)
    elements = driver.find_elements(By.CLASS_NAME, 'llc')
    i += 1

pprint(mail_list)
print(f"Количество новостей в БД: {mail_mongo.estimated_document_count()}")
