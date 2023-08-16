import time
import traceback
import sys
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
options = FirefoxOptions()
options.add_argument("--headless")

if len(sys.argv) < 3:
    print("Usage: firefox-script.py <url> <adminpw>")
    exit(-1)

base_url = sys.argv[1]
admin_pw = sys.argv[2]

login_url = base_url + "/wp-login.php"
print(f"Base url: {base_url} PW: {admin_pw}") #TODO: Removeme

while True:
    try:
        browser = webdriver.Firefox(options=options)
        # visit other page first to establish proper context for adding cookies
        browser.get(base_url + "/wp-login.php")

        username = browser.find_element(By.ID, "user_login")
        password = browser.find_element(By.ID, "user_pass")
        form = browser.find_element(By.ID, "loginform") 
        browser.execute_script(f"arguments[0].setAttribute('action', '{login_url}')", form)
        
        username.send_keys("admin") # add your WordPress UserName
        password.send_keys(admin_pw) # add your WordPress Password

        submitButton = browser.find_element(By.ID,"wp-submit")
        submitButton.click()

        # go brrrrr
        browser.get(base_url + "/")

        resp = requests.get(base_url + "/?rest_route=/wp/v2/posts").json()

        for entry in resp:
             browser.get(entry["link"])

        time.sleep(30)
        browser.close()
    except:
        traceback.print_exc()
        # server might not be up yet
        time.sleep(30)
        pass
