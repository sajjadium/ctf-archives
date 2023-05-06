import config
import requests
import os
import json
import base64

from urllib.parse import quote
from playwright.sync_api import sync_playwright
from flask import Flask, request

app = Flask(__name__)

def start(url, iid):
	print(url, iid)

	with sync_playwright() as p:
		browser = p.firefox.launch(executable_path='/app/firefox/firefox')

		context = browser.new_context()
		context.add_cookies([{
			'name': 'flag',
			'value': config.FLAG,
			'domain': f'{iid}.fly.dev',
			'path': '/',
		}])

		page = context.new_page()
		page.goto(url)
		page.wait_for_timeout(30000)

		browser.close()

@app.route('/', methods=['POST'])
def run():
	data = request.json['message']['data']
	payload = json.loads(base64.b64decode(data))
	start(payload['url'], payload['instanceId'])
	return '', 204
