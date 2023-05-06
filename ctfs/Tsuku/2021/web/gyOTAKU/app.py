import io
import os
import random
import string
import requests
import subprocess
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

def sanitize(text):
    #RCE is a non-assumed solution. <- This is not a hint.
    url = ""
    for i in text:
        if i in string.digits + string.ascii_lowercase + string.ascii_uppercase + "./_:":
            url += i
    if (url[0:7]!="http://") and (url[0:8]!="https://"):
        url = "https://www.google.com"
    return url

@app.route("/")
def gyotaku():
    filename = "".join([random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase) for i in range(15)])
    url = request.args.get("url")
    if not url:
        return "<font size=6>🐟gyOTAKU🐟</font><br><br>You can get gyotaku: <strong>?url={URL}</strong><br>Sorry, we do not yet support other files in the acquired site."
    url = sanitize(url)
    html = open(f"{filename}.html", "w")
    try:
        html.write(requests.get(url, timeout=1).text + "<br><font size=7>gyotakued by gyOTAKU</font>")
    except:
        html.write("Requests error<br><font size=7>gyotakued by gyOTAKU</font>")
    html.close()
    cmd = f"chromium-browser --no-sandbox --headless --disable-gpu --screenshot='./gyotaku-{filename}.png' --window-size=1280,1080 '{filename}.html'"
    subprocess.run(cmd, shell=True, timeout=1)
    os.remove(f"{filename}.html")
    png = open(f"gyotaku-{filename}.png", "rb")
    screenshot = io.BytesIO(png.read())
    png.close()
    os.remove(f"gyotaku-{filename}.png")
    return send_file(screenshot, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9000)