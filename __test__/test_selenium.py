import time

from selenium import webdriver

wd = webdriver.Chrome('/Users/noah/cafe24/libs/selenium-chrome-driver/chromedriver')

wd.get('http://www.goobne.co.kr/store/search_store.jsp')

time.sleep(2)
html = wd.page_source
print(html)

wd.quit()
