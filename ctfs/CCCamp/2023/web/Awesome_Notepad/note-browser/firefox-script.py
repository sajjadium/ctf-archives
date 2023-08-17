import time
import traceback
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
options = FirefoxOptions()
options.add_argument("--headless")

if os.environ["TICKET_APP_ROOT"]:
    ticket_url = os.environ["TICKET_APP_ROOT"]
else:
    ticket_url = "http://localhost:8000"

while True:
    try:
        browser = webdriver.Firefox(options=options)
        # visit other page first to establish proper context for adding cookies
        browser.get(ticket_url)
        time.sleep(30)
        browser.close()
    except:
        traceback.print_exc()
        # server might not be up yet
        time.sleep(30)
        pass
