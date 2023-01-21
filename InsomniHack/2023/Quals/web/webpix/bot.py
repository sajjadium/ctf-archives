#!/usr/bin/python3
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from waitress import serve
import os

app = Flask(__name__)

def visit(url):

    options = Options()
    options.add_argument('headless')
    options.add_argument('no-sandbox')
  
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get(os.environ.get("URL"))
    driver.add_cookie({'name': 'flag','value': os.environ.get("FLAG")})

    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')
    except:
        pass
    finally:
        driver.quit()


@app.route("/visit", methods=["POST"])
def response():
    try:
        url = request.json.get("url")
        assert(url.startswith('https://') or url.startswith('http://'))
        visit(url)
        return {"Success": "1"}
    except:
        return {"Failure": "1"}

@app.errorhandler(404)
def error_handler(error): 
    return "<h1>URL not found</h1><br/>", 404

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8888)