import datetime
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from pymongo import MongoClient


def parse_letter(letter_we, driver):
    """
    Парсинг письма
    :param letter_we: Вэбэелемент ссылки на письмо
    :param driver: Вэб драйвер
    :return:
    """
    url = letter_we.get_attribute('href')
    # Открываем новый таб для письма
    main_window = driver.current_window_handle
    driver.execute_script("window.open(''),'_blank'")
    driver.switch_to.window(driver.window_handles[1])

    driver.get(url)
    time.sleep(3)

    moment_text = driver.find_element(By.CSS_SELECTOR, '.letter__date').text.lower()
    moment_text = moment_text.replace('сегодня', str(datetime.date.today()))
    moment_text = moment_text.replace('вчера', str(datetime.date.today() - datetime.timedelta(days=1)))
    data = {
        'url': url,
        'from_name': driver.find_element(By.CSS_SELECTOR, '.letter-contact').text,
        'from_email': driver.find_element(By.CSS_SELECTOR, '.letter-contact').get_attribute('title'),
        'moment': moment_text,
        'title': driver.find_element(By.CSS_SELECTOR, "h2.thread-subject").text,
        'body': driver.find_element(By.CSS_SELECTOR, ".letter__body").text
    }
    # Закрываем таб
    driver.close()
    driver.switch_to.window(main_window)
    return data


def main():
    # Загружаем настройки из файла .env
    load_dotenv()

    # Подклюаем MongoDb
    client = MongoClient('localhost', 27017)
    db = client[os.getenv('DB_NAME')]
    storage = db[os.getenv('TABLE_NAME')]

    # Инициализация браузера
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get('https://e.mail.ru/login')

    # Поиск формы входа
    auth_form = driver.find_element(By.ID, 'auth-form')
    iframe = auth_form.find_element(By.TAG_NAME, 'iframe')

    driver.switch_to.frame(iframe)
    # Ввод логина
    inp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    inp.send_keys(os.getenv('USER_MAIL'), Keys.ENTER)
    time.sleep(5)
    # Ввод пароля
    inp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    inp.send_keys(os.getenv('PASSWORD_MAIL'), Keys.ENTER)

    driver.switch_to.default_content()
    driver.implicitly_wait(5)

    msg_len = 0
    container = driver.find_element(By.CSS_SELECTOR, 'div.ReactVirtualized__Grid__innerScrollContainer')
    while True:
        if msg_len >= 50:
            break
        letters = container.find_elements(By.CSS_SELECTOR, 'a.js-letter-list-item')
        current_len = len(letters)
        if msg_len < current_len:
            new_cnt = current_len - msg_len
            for i in range(new_cnt):
                letter_data = parse_letter(letters[i], driver)
                # сохраняем письмо
                if len(list(storage.find({'url': letter_data['url']}))) == 0:
                    storage.insert_one(letter_data)
            msg_len = current_len
        else:
            break
        time.sleep(2)

    driver.close()


if __name__ == '__main__':
    main()
