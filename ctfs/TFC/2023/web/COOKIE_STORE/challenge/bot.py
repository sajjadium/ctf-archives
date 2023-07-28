from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse

FLAG = "TFCCTF{fake_flag}"

def bot(fields):
    chrome_options = Options()

    chrome_options.add_argument('headless')
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('disable-dev-shm-usage')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('disable-background-networking')
    chrome_options.add_argument('disable-default-apps')
    chrome_options.add_argument('disable-extensions')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('disable-sync')
    chrome_options.add_argument('disable-translate')
    chrome_options.add_argument('hide-scrollbars')
    chrome_options.add_argument('metrics-recording-only')
    chrome_options.add_argument('no-first-run')
    chrome_options.add_argument('safebrowsing-disable-auto-update')
    chrome_options.add_argument('media-cache-size=1')
    chrome_options.add_argument('disk-cache-size=1')

    client = webdriver.Chrome(options=chrome_options)

    fields = urllib.parse.quote(fields)
    
    time.sleep(2)
    client.get(f"http://localhost:1337/form_builder?fields={fields}")

    time.sleep(2)
    try:
        client.find_element(By.ID, "title").send_keys(FLAG)
    except:
        pass
    client.execute_script("""document.querySelector('input[type="submit"]').click();""")
    time.sleep(2)

    client.quit()
