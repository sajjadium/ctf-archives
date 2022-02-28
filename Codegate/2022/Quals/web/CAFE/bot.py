#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--disable-logging')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
#options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")

driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
driver.implicitly_wait(3)

driver.get('http://3.39.55.38:1929/login')
driver.find_element_by_id('id').send_keys('admin')
driver.find_element_by_id('pw').send_keys('$MiLEYEN4')
driver.find_element_by_id('submit').click()
time.sleep(2)

driver.get('http://3.39.55.38:1929/read?no=' + str(sys.argv[1]))
time.sleep(2)

driver.quit()
  