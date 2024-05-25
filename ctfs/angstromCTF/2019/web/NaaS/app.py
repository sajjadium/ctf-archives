from flask import Flask, request, redirect, make_response
app = Flask(__name__)

import requests
import json
import subprocess
import random

pastes = {}

html = """<!doctype html>
<html>
	<head>
		<title>Yet Another Pastebin</title>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css">
	<head>
	<body style="text-align: center;">
		<h1 style="color: #96cdd1; margin-top: 1.5em;">Yet Another Pastebin</h1>
		<h3>Create Paste</h3>
		<form method="POST">
			<textarea required name="paste" style="width: 50em; height: 20em;"></textarea><br>
			<button type="submit">Create</button>
		</form>
	</body>
</html>"""

@app.route("/", methods=["GET", "POST"])
def get_pastes():
	if request.method == "POST":
		p = request.form.get("paste", "")
		pid = "%8x" % random.getrandbits(4*8)
		pastes[pid] = p
		return redirect("/" + pid)
	return html

@app.route("/<string:id>")
def get_paste(id):
	if id in pastes:
		html = """<!doctype html>
<html>
	<head>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css">
		<title>View Paste</title>
	</head>
	<body>
		<pre id="paste">{}</pre>
		<small id="report">If you think this paste shouldn't be here, <a href="#">report it</a>.</small>
		<script>
		function send () {{
			fetch("/report", {{
				method: "POST",
				headers: {{
					"Content-Type": "application/json"
				}},
				body: JSON.stringify({{ url: location.href }})
			}})
			paste.innerHTML = "An admin will review this paste shortly."
			report.innerHTML = ""
		}}
		report.onclick = send
		</script>
	</body>
</html>"""
		nonceify = requests.post("https://naas.2019.chall.actf.co/nonceify", data=html).json()
		r = make_response(nonceify["html"].format(pastes[id]))
		r.headers["Content-Security-Policy"] = nonceify["csp"]
		return r
	else: return redirect("/")

@app.route("/report", methods=["POST"])
def report():
	print(request.get_json())
	subprocess.Popen(["node", "visit.js", request.get_json()["url"]])
	return "OK"