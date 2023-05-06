import subprocess
from flask import Flask, request, Response


app = Flask(__name__)


# Multibyte Characters Sanitizer
def mbc_sanitizer(url :str) -> str:
    bad_chars = "!\"#$%&'()*+,-;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c"
    for c in url:
        try:
            if c.encode("idna").decode() in bad_chars:
                url = url.replace(c, "")
        except:
            continue
    return url


# Scheme Detector
def scheme_detector(url :str) -> bool:
    bad_schemes = ["dict", "file", "ftp", "gopher", "imap", "ldap", "mqtt",
                   "pop3", "rtmp", "rtsp", "scp", "smbs", "smtp", "telnet", "ws"]
    url = url.lower()
    for s in bad_schemes:
        if s in url:
            return True
    return False


# WAF
@app.after_request
def waf(response: Response):
    if b"RicSec" in b"".join(response.response):
        return Response("Hi, Hacker !!!!")
    return response


@app.route("/")
def funnylfi():
    url = request.args.get("url")
    if not url:
        return "Welcome to Super Secure Website Viewer.<br>Internationalized domain names are supported.<br>ex. <code>?url=ⓔxample.com</code>"
    if scheme_detector(url):
        return "Hi, Scheme man !!!!"
    try:
        proc = subprocess.run(
            f"curl {mbc_sanitizer(url[:0x3f]).encode('idna').decode()}",
            capture_output=True,
            shell=True,
            text=True,
            timeout=1,
        )
    except subprocess.TimeoutExpired:
        return "[error]: timeout"
    if proc.returncode != 0:
        return "[error]: curl"
    return proc.stdout


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=31415)