from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import os
import time
import requests

ADMIN_COOKIE = os.environ.get('FLAG')

display = Display (visible=0, size= (320, 240))
display.start()
	
options = Options ()
options.add_argument ("--headless")
options.add_argument ("--no-sandbox")
driver = webdriver.Chrome(options=options)

driver.set_window_size(320, 240)
driver.set_page_load_timeout(7)
driver.get('http://localhost:2000/')
driver.add_cookie({'name': 'admin_cookie', 'value': ADMIN_COOKIE})

while True:
	try:
		driver.get('http://localhost:2000/list')
		button = driver.find_elements(By.CLASS_NAME, "image-link")[0]
		image_url = button.get_attribute('href')
		button.click()

		time.sleep(5)
	except:
		pass

driver.quit()
display.stop()