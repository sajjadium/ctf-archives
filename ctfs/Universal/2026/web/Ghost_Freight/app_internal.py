import os

from flask import Flask, abort

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8081
SECRET_PATH_FILE = "/tmp/secret_path"

app = Flask(__name__)

FLAG = os.environ.get("FLAG", "uctf{dev-ghost-freight}")


@app.get("/")
def home():
    return ("Ghost Freight internal cargo service.\n", 200, {"Content-Type": "text/plain"})


@app.get("/<path:path>")
def check_path(path: str):
    try:
        current_secret = open(SECRET_PATH_FILE).read().strip()
    except FileNotFoundError:
        abort(503, "service not ready")

    if path == current_secret:
        return (FLAG + "\n", 200, {"Content-Type": "text/plain"})

    abort(404, "unknown manifest")


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", DEFAULT_HOST), port=int(os.getenv("PORT", DEFAULT_PORT)))
