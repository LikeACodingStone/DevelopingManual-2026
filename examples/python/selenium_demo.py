"""Selenium 4; local HTML only, no account and no external target website."""
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    with webdriver.Chrome(options=options) as driver:
        html = '<input id="name"><button onclick="document.getElementById(\'out\').textContent=document.getElementById(\'name\').value">Go</button><p id="out"></p>'
        driver.get('data:text/html;charset=utf-8,' + quote(html))
        driver.find_element(By.ID, 'name').send_keys('PCM')
        driver.find_element(By.TAG_NAME, 'button').click()
        WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, 'out'), 'PCM'))
        print('browser interaction OK')

if __name__ == '__main__':
    main()
