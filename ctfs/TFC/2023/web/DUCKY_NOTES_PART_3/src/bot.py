from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os

def bot(username):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('headless')
    options.add_argument('ignore-certificate-errors')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('disable-infobars')
    options.add_argument('disable-background-networking')
    options.add_argument('disable-default-apps')
    options.add_argument('disable-extensions')
    options.add_argument('disable-gpu')
    options.add_argument('disable-sync')
    options.add_argument('disable-translate')
    options.add_argument('hide-scrollbars')
    options.add_argument('metrics-recording-only')
    options.add_argument('no-first-run')
    options.add_argument('safebrowsing-disable-auto-update')
    options.add_argument('media-cache-size=1')
    options.add_argument('disk-cache-size=1')
    

    client = webdriver.Chrome(options=options)

    client.get(f"http://localhost:1337/login")
    time.sleep(3)

    client.find_element(By.ID, "username").send_keys('admin')
    client.find_element(By.ID, "password").send_keys(os.environ.get("ADMIN_PASSWD"))
    client.execute_script("document.getElementById('login-btn').click()")
    time.sleep(3)

    client.get(f"http://localhost:1337/posts/view/{username}")
    time.sleep(30)

    client.quit()
