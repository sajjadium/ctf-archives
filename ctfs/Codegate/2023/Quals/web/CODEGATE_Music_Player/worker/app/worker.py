#!/usr/bin/python3 -u
#-*- coding: utf-8 -*-
# Developer: stypr (https://harold.kim/)
# Target is at http://nginx/

import os
import asyncio
import time
import redis
import requests
from pyppeteer import launch

redis = redis.Redis('redis')
redis.select(1)
browser = None
browser_option = {
    'executablePath': '/usr/bin/google-chrome-stable',
    'options': {'args': [
        '--no-sandbox',
        '--disable-default-apps',
        '--disable-extensions',
        '--disable-gpu',
        '--disable-sync',
        '--disable-translate',
        '--hide-scrollbars',
        '--metrics-recording-only',
        "--js-flags='--jitless'",
        '--mute-audio',
        '--no-first-run',
        '--safebrowsing-disable-auto-update',
        '--disable-dev-shm-usage',
        '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    ]},
    'handleSIGINT': False,
    'handleSIGTERM': False,
    'handleSIGHUP': False,
    'headless': True
}

async def init_browser():
    global browser
    _browser = await launch(**browser_option)
    page = await _browser.newPage()
    try:
        await page.goto("http://nginx/")
        cookie = {
            "name": "SECRET",
            "value": os.environ['SECRET'],
            "domain": "nginx",
            "path": "/",
            "httpOnly": True,
            "secure": False
        }
        await page.setCookie(cookie)
    except Exception as e:
        print("[!] Error during browser initialization: " + str(e))
    finally:
        await page.close()
    print("[.] Browser is now loaded.")
    return _browser

async def render(url):
    timeout = 3
    try:
        print("[.] Begin crawling...")
        page = await browser.newPage()
        await page.goto(url, {
            'timeout': timeout * 1000,
            'waitUntil' : 'networkidle0'
        })
        await page.close()
        print("[.] Rendering complete..")

    except Exception as e:
        print(f"[!!] {e}")

    finally:
        await page.close()

async def main(loop):
    global browser
    while True:
        try:
            print("[+] Handler has begun..")
            data = redis.blpop("query")[1].decode()
            if data:
                print(f"[*] Got a new request: {data}")
                if not browser:
                    browser = await init_browser()
                _task = await asyncio.wait_for(render(data), timeout=5)

        except Exception as e:
            print(f"[!] {e}")

        finally:
            await asyncio.sleep(0.01)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
