#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import re
import sys
import os
import time
from urllib.parse import quote

def get(prompt, regex):
    inp = input(prompt)
    if not re.match(regex, inp):
        print(f"Input {inp} does not match regex {regex}", flush=True)
        exit(1)
    return inp

USERNAME = "admin"
PASSWORD = "admin123"
CHALLENGE_IP = "chall"
PROXY_USERNAME = "hxp"
PROXY_PASSWORD = "hxp"
PORT = 8081

if len(sys.argv) == 3:
    # remote setup, IP, proxy, admin_password and port will differ!
    CHALLENGE_IP = sys.argv[1]
    PASSWORD = sys.argv[2]

    print("Please supply connection details for your instance")
    PROXY_USERNAME = get("Please give instance username: ", r"^[a-zA-Z0-9_-]+$")
    PROXY_PASSWORD = get("Please give instance password: ", r"^[a-zA-Z0-9_-]+$")
    PORT = get("Please give instance port: ", r"^\d+$")

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")
driver = None

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)

    # log in
    base_url = f"http://{quote(PROXY_USERNAME)}:{quote(PROXY_PASSWORD)}@{CHALLENGE_IP}:{PORT}"
    print(f"Logging in to {base_url}", flush=True)
    driver.get(base_url)

    wait.until(lambda d: d.find_element(By.ID, "login-link-a"))
    time.sleep(2)

    driver.find_element(By.ID, "login-link-a").click()

    wait.until(lambda d: d.find_element(By.ID, "modal-login").get_attribute("aria-hidden") == "false")
    time.sleep(2)

    username_input = driver.find_element(By.ID, "user-login-form-username")
    username_input.send_keys(USERNAME)

    password_input = driver.find_element(By.ID, "user-login-form-password")
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(By.ID, "modal-login-ok")
    login_button.click()

    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    time.sleep(2)

    print(f"Hopefully logged in", flush=True)

    # visit url
    url = f"http://{CHALLENGE_IP}:{PORT}/repository/internal"
    print(f"Visiting {url}", flush=True)
    driver.get(url)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    time.sleep(2)

except Exception as e:
    print(e, file=sys.stderr, flush=True)
    print('Error while visiting')
finally:
    if driver:
        driver.quit()

print('Done visiting', flush=True)
