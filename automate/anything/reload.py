from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as cs
import time

URL = 'https://okachanblog622.com/%e3%80%905g%e3%81%a3%e3%81%a6%e6%9c%ac%e5%bd%93%e3%81%ab%e6%97%a9%e3%81%84%e3%81%ae%ef%bc%9f%e3%80%91iphone13%e3%82%92%e4%bd%bf%e3%81%a3%e3%81%a64g%e3%81%a85g%e3%81%ae%e5%9b%9e%e7%b7%9a%e9%80%9f'


chrome_service = cs.Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=chrome_service)
driver.get(URL)



while True:
    # リロードする
    driver.refresh()
    time.sleep(5)
