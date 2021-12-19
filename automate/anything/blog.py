if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as cs
import time
import config

from line.line_notify_bot import LINENotifyBot


BASE_URL = 'https://okachanblog622.com/'

chrome_service = cs.Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=chrome_service)
driver.get(BASE_URL)

found_new_article = False
LATEST_TITLE = '【5Gって本当に早いの？】iPhone13を使って4Gと5Gの回線速度の速さを比べてみた！！'
new_blog = {
    'title': '',
    'url': '',
}

def exists_new_article():
    global new_blog
    list_ = driver.find_element(by=By.ID, value='list')
    latest_element = list_.find_element_by_tag_name('a')

    exists = latest_element.get_attribute('title') != LATEST_TITLE
    if exists:
        new_blog['title'] = latest_element.get_attribute('title')
        new_blog['url'] = latest_element.get_attribute('href')

    return exists

while not found_new_article:
    # リロードする
    driver.refresh()
    time.sleep(5)

    found_new_article = exists_new_article()

bot = LINENotifyBot(access_token=config.TOKEN)

bot.send(
    message = f"「{new_blog['title']}」というブログが更新されました。（{new_blog['url']}）",
    )
