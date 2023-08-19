from flask import Flask, request
from urllib.parse import urlencode
from urllib.request import urlopen
import subprocess
import os

G_SITEKEY = os.getenv("G_SITEKEY", '"><script>document.write("reCAPTCHA is broken")</script>')
G_SECRET = os.getenv("G_SECRET", "Victoria's Secret")
app = Flask(__name__)

def escapeshellarg(arg):
	return "'"+arg.replace("'","'\\''")+"'"

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		if "g-recaptcha-response" not in request.form or request.form["g-recaptcha-response"] == "":
			return "Bad reCAPTCHA"
		data = urlencode({"secret": G_SECRET, "response": request.form["g-recaptcha-response"]}).encode('ascii')
		try:
			fetch = urlopen("https://www.google.com/recaptcha/api/siteverify", data).read().decode("utf-8")
		except Exception as e:
			return str(e)
		if '"success": true' not in fetch:
			return "reCAPTCHA is broken"
		url = escapeshellarg(request.form["url"])
		if url[:8] != "'http://" and url[:9] != "'https://":
			return "Invalid URL"
		command = "qutebrowser -T -s content.pdfjs true -s content.javascript.can_open_tabs_automatically true -s url.start_pages \"data:text/plain,\" -- %s" % url
		print(request.remote_addr + ": " + command, flush=True)
		try:
			subprocess.run(command, shell=True, timeout=30, cwd="/tmp")
		except Exception as e:
			pass
		return "<title>Kill T Browser</title><code>%s</code><hr />Kyubey should have viewed your webpage." % command
	else:
		return """<html>
<head>
<title>Kill T Browser</title>
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
</head>
<body>
<h2>Kill T Browser</h2>
<form method="post">
<p style="font-family:Courier New;background:#CCCCCC;font-size:16pt;padding:0.25em">
qutebrowser -T -s content.pdfjs true -s content.javascript.can_open_tabs_automatically true -s url.start_pages "data:text/plain," -- 
<input style="font-family:Courier New;background:#CCCCCC;font-size:16pt;border:0;width:70%%" name="url" placeholder="http://example.com">
</p>
<div class="g-recaptcha" data-sitekey="%s"></div>
<p><input type="submit"></p>
</form>
<p>Remarks: 
<ul>
<li>Timeout in 30 seconds</li>
<li>Reborn every 30 minutes</li>
</ul>
</p>
</body>
</html>""" % G_SITEKEY


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80)