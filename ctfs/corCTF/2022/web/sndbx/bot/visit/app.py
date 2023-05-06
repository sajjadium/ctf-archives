import config
import requests
import os
import json
import base64

from urllib.parse import quote
from playwright.sync_api import sync_playwright
from flask import Flask, request

app = Flask(__name__)

def start(script):
	print(f'{config.CASTLE_BASE}?eval={quote(script)}&flag={config.FLAG}')

	os.makedirs('/etc/firefox/policies', exist_ok=True)
	os.makedirs('/usr/lib/mozilla/certificates/', exist_ok=True)

	with open('/etc/firefox/policies/policies.json', 'w') as f:
		f.write(json.dumps({
			'policies': {
				'Certificates': {
					'Install': ['sndbx.pem']
				}
			}
		}))

	with open('/usr/lib/mozilla/certificates/sndbx.pem', 'w') as f:
		f.write(requests.get(config.CA_URL, verify=False).text)

	with sync_playwright() as p:
		browser = p.firefox.launch(firefox_user_prefs={
			'security.enterprise_roots.enabled': True,
			'network.dns.disablePrefetch': True,
			'media.peerconnection.enabled': False
		}, executable_path='/app/firefox/firefox')

		context = browser.new_context()
		page = context.new_page()

		page.goto(f'{config.CASTLE_BASE}?eval={quote(script)}&flag={config.FLAG}')
		page.wait_for_timeout(30000)

		browser.close()

@app.route('/', methods=['POST'])
def run():
	data = request.json['message']['data']
	payload = json.loads(base64.b64decode(data))
	start(payload['js'])
	return '', 204
