#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

import urllib.parse
import re
import sys
import traceback
import os
import time

def fatal(err_msg):
    print(err_msg, flush=True)
    exit(1)

def get(prompt, regex):
    inp = input(prompt)
    if not re.match(regex, inp):
        fatal(f"Input {inp} does not match regex {regex}")
    return inp

username = "hxp_admin"
password = "testtesttesttest"
challenge_ip = "chall"
proxy_username = "hxp"
proxy_password = "hxp"
port = 8091

if len(sys.argv) == 4:
    challenge_ip = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    print("Please supply connection details for your instance:")
    proxy_username = get("Please give instance username: ", r"^[a-zA-Z0-9_-]+$")
    proxy_password = get("Please give instance password: ", r"^[a-zA-Z0-9_-]+$")
    port = get("Please give instance port: ", r"^\d+$")

if username == None or len(username) < 5:
    fatal('Admin username somehow broken. Contact hxp admin.')

if password == None or len(password) < 12:
    fatal('Admin password somehow broken. Contact hxp admin.')


regex = r'^.{0,100}$'
print(f"Please give the path the admin should check. (should match {regex})")
path = get(f"http://{challenge_ip}:{port}/", regex)

forbidden = ["!settings", "!sqlite", "!debuginfo"]
for f in forbidden:
    if f in path:
        fatal(f"'{f}' is forbidden")

if "!profile" in path and username in path:
    fatal(f"admin doesn't want to visit their own profile")

# Visit URL
url = f"http://{proxy_username}:{proxy_password}@{challenge_ip}:{port}/"

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")

driver = None

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)
    wait = WebDriverWait(driver, 1)

    # Login
    login_url = url + "!login"
    print(f"Logging into {login_url}", flush=True)
    driver.get(login_url)

    # Hack to bypass the submit location checks
    login_form = driver.find_element(By.CLASS_NAME, "login-block")
    driver.execute_script('arguments[0].innerHTML = " <input type=\'text\' name=\'submit.y\' value=1 /> <input type=\'text\' name=\'submit.x\' value=1 /> " + arguments[0].innerHTML', login_form)

    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_button = driver.find_element(By.ID, 'submit')
    submit_button.submit()

    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    time.sleep(1)

    url += path
    print(f"Visiting {url}", flush=True)
    driver.get(url)

    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    time.sleep(1)

except Exception as e:
    fatal(e)
finally:
    if driver:
        driver.quit()

print(f'Done visiting', flush=True)
