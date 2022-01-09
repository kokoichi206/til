import time
from selenium import webdriver

driver = webdriver.Chrome('./chromedriver')
driver.get('http://www.google.com/xhtml')
time.sleep(5)
print(driver.title)

search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)
print(driver.title)

driver.save_screenshot('search_results.png')

driver.quit()
