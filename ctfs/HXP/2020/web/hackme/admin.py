#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of

import urllib.parse
import re
import sys
import traceback

# HTTP request from stdin (ynetd), ignoring any headers or really anything else
query = sys.stdin.readline(1024).strip()
match = re.match(r'\AGET\s+/report\?url=([a-zA-Z0-9/_.-]+)\s+HTTP/\d\.\d\Z', query)
if not match:
    print('Invalid query:', urllib.parse.quote(query, safe='/?= '), file=sys.stderr, flush=True)
    print('HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n')
    exit(0)

# Visit URL
endpoint = 'http://127.0.0.1/'
admin = '__ADMIN_EMAIL__'
password = '__ADMIN_PASSWORD__'

url = endpoint + match.group(1).lstrip('/')
print('Visiting', url, file=sys.stderr, flush=True)

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

try:
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
    wait = WebDriverWait(driver, 1)

    # Log in
    driver.get(endpoint)
    driver.find_element_by_css_selector('button.ui-signin').click()
    email_input = driver.find_element_by_name('email')
    password_input = driver.find_element_by_name('password')
    wait.until(visibility_of(email_input))

    email_input.send_keys(admin)
    password_input.send_keys(password)
    driver.find_element_by_css_selector('button[formaction="/login"]').click()

    # Fetch URL and wait for complete page load
    driver.get(url)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

    print('HTTP/1.1 204 No Content\r\nContent-Length: 0\r\n\r\n')
except:
    traceback.print_stack(file=sys.stderr)
    print('HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n')
finally:
    driver.quit()

print('Done visiting', url, file=sys.stderr, flush=True)
