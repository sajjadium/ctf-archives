from flask import Flask, request, Response
import subprocess
import os

app = Flask(__name__)


def validate(key: str) -> bool:
    # E.g. key == "{name}" -> True
    #      key == "name"   -> False
    if len(key) == 0:
        return False
    is_valid = True
    for i, c in enumerate(key):
        if i == 0:
            is_valid &= c == "{"
        elif i == len(key) - 1:
            is_valid &= c == "}"
        else:
            is_valid &= c != "{" and c != "}"
    return is_valid


def template(text: str, params: dict[str, str]) -> str:
    # A very simple template engine
    for key, value in params.items():
        if not validate(key):
            return f"Invalid key: {key}"
        text = text.replace(key, value)
    return text


@app.after_request
def waf(response: Response):
    if b"SECCON" in b"".join(response.response):
        return Response("Try harder")
    return response


@app.route("/")
@app.route("/<path:filename>")
def index(filename: str = "index.html"):
    if ".." in filename or "%" in filename:
        return "Do not try path traversal :("

    try:
        proc = subprocess.run(
            ["curl", f"file://{os.getcwd()}/public/{filename}"],
            capture_output=True,
            timeout=1,
        )
    except subprocess.TimeoutExpired:
        return "Timeout"

    if proc.returncode != 0:
        return "Something wrong..."
    return template(proc.stdout.decode(), request.args)
