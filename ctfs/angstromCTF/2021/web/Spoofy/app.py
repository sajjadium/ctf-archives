from flask import Flask, Response, request
import os
from typing import List

FLAG: str = os.environ.get("FLAG") or "flag{fake_flag}"
with open(__file__, "r") as f:
    SOURCE: str = f.read()

app: Flask = Flask(__name__)


def text_response(body: str, status: int = 200, **kwargs) -> Response:
    return Response(body, mimetype="text/plain", status=status, **kwargs)


@app.route("/source")
def send_source() -> Response:
    return text_response(SOURCE)


@app.route("/")
def main_page() -> Response:
    if "X-Forwarded-For" in request.headers:
        # https://stackoverflow.com/q/18264304/
        # Some people say first ip in list, some people say last
        # I don't know who to believe
        # So just believe both
        ips: List[str] = request.headers["X-Forwarded-For"].split(", ")
        if not ips:
            return text_response("How is it even possible to have 0 IPs???", 400)
        if ips[0] != ips[-1]:
            return text_response(
                "First and last IPs disagree so I'm just going to not serve this request.",
                400,
            )
        ip: str = ips[0]
        if ip != "1.3.3.7":
            return text_response("I don't trust you >:(", 401)
        return text_response("Hello 1337 haxx0r, here's the flag! " + FLAG)
    else:
        return text_response("Please run the server through a proxy.", 400)
