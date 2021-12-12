from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import os
import time
import requests

ADMIN_COOKIE = os.environ.get('ADMIN_COOKIE')

# print("Declare display", flush=True)
display = Display (visible=False, size= (320, 240))
# print("Start display", flush=True)
display.start()
	
# print("Options", flush=True)
options = Options ()
options.add_argument ("--headless")
options.add_argument ("--no-sandbox")
options.add_argument('--disable-dev-shm-usage')
# print("webdriver.Chrome", flush=True)
driver = webdriver.Chrome(options=options)

# print("set_window_size", flush=True)
driver.set_window_size(320, 240)
# print("set_page_load_timeout", flush=True)
driver.set_page_load_timeout(5)
# print("get /", flush=True)
driver.get('http://127.0.0.1:2000/')
# print("add cookie", flush=True)
driver.add_cookie({'name': 'admin_cookie', 'value': ADMIN_COOKIE})

while True:
	try:
		# print("get /quote/latest", flush=True)
		driver.get('http://127.0.0.1:2000/quote/latest')
		
		# print("reject button - press", flush=True)
		rejectBtn = WebDriverWait(driver, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "red"))
		)
		rejectBtn.click()

		# print("sleep 3", flush=True)
		time.sleep(3)
	except:
		pass

# print("quit", flush=True)
driver.quit()

# print("Stop display", flush=True)
display.stop()