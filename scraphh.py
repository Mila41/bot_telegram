from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

def parser_hh(job: str):
    browser = webdriver.Chrome(executable_path="C:\\Users\\Мила\\PycharmProjects\\SeleniumScraper\\chromedriver\\chromedriver.exe")
    browser.maximize_window()
    browser.get("http://hh.ru")
# Можно добавить опцию --headless => тогда не будет видно окна
#chromeOptions.addArguments("--headless")
    search_input = browser.find_element(By.ID, "a11y-search-input")
    search_input.send_keys("Junior python")  # Отправить нажатия клавиш

    search_button = browser.find_element(By.CSS_SELECTOR, '[data-qa="search-button"]')
    search_button.click()

    text = browser.find_element(By.CSS_SELECTOR, '[data-qa="vacancies-search-header"] h1').text

# "1 14 вакансий «Junior Python»" => 114
# Заменям \D на ""
# \D - "все что не является числом"
# \w - "все из чего состоит слово"
# * - "сколько угодно"
#

    jobs_count = re.sub(r"\D", "", text)  # Замена
#print(f"Jobs Found: {jobs_count}")
#time.sleep(5)
    browser.close()
    return jobs_count