import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from flask import Flask, request
import time


app = Flask(__name__)

import sys
import logging

TASK = os.environ.get('BASE_URL') or "http://127.0.0.1:5000"
flag = os.environ.get('FLAG') or 'justCTF{fake}'
pwd = os.environ.get('PASSWD') or 'admin'

def visit_url(url, timeout):
    if type(url) != str or not url.startswith("http"):
        return
    print("Visiting:",url, file=sys.stdout, flush=True)
    options = Options()
    options.add_argument('no-sandbox')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('disable-infobars')
    options.add_argument('disable-background-networking')
    options.add_argument('disable-default-apps')
    options.add_argument('disable-gpu')
    options.add_argument('disable-sync')
    options.add_argument('disable-translate')
    options.add_argument('disable-lazy-image-loading')
    options.add_argument('hide-scrollbars')
    options.add_argument('metrics-recording-only')
    options.add_argument('mute-audio')
    options.add_argument('no-first-run')
    options.add_argument('dns-prefetch-disable')
    options.add_argument('safebrowsing-disable-auto-update')
    options.add_argument('media-cache-size=1')
    options.add_argument('disk-cache-size=1')
    options.add_argument('disable-features=LazyImageLoading,AutomaticLazyImageLoading,LazyFrameLoading,AutomaticLazyFrameLoading,AutoLazyLoadOnReloads')
    options.add_argument('--js-flags=--noexpose_wasm,--jitless')
    options.add_argument('hide-scrollbars')
    options.add_argument('load-extension=ninja-cookie')

    try:
        browser = webdriver.Chrome('/usr/local/bin/chromedriver', options=options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])

        browser.get(TASK+"/login")
        WebDriverWait(browser, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')
        inputElement = browser.find_element_by_id("username")
        inputElement.send_keys(flag)
        inputElement = browser.find_element_by_id("password")
        inputElement.send_keys(pwd)
        browser.find_element_by_id("submit").click()
        WebDriverWait(browser, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')
        time.sleep(timeout)

        browser.get(url)
        WebDriverWait(browser, 30).until(lambda r: r.execute_script('return document.readyState') == 'complete')
        time.sleep(30)
    except:
        print('Error visiting', url, traceback.format_exc(), file=sys.stderr, flush=True)
    finally:
        print('Done visiting', url, file=sys.stderr, flush=True)

@app.route("/", methods=['GET'])
def visit():
    visit_url(request.args.get("url"), 1)
    return "ok"

