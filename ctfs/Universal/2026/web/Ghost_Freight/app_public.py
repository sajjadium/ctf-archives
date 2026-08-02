import html
import os
import random
import tempfile

import requests as http_client
from flask import Flask, abort, jsonify, request
from urllib.parse import urlparse

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080
MAX_RESPONSE_BYTES = 64 * 1024
SECRET_PATH_FILE = "/tmp/secret_path"

ALLOWED_SCHEMES = {"http", "https"}
FETCH_TIMEOUT = 5

app = Flask(__name__)

rng = random.Random()

_current_value = 0


def _rotate_secret_path() -> None:
    """Rotates the internal service, this ensures that nobody can reach it."""
    global _current_value
    _current_value = rng.getrandbits(32)
    path_hex = f"{_current_value:08x}"
    tmp_fd, tmp_path = tempfile.mkstemp(dir="/tmp", prefix=".secret_path_")
    try:
        os.write(tmp_fd, path_hex.encode())
        os.close(tmp_fd)
        os.replace(tmp_path, SECRET_PATH_FILE)
    except Exception:
        os.close(tmp_fd)
        os.unlink(tmp_path)
        raise


@app.before_request
def before_request():
    _rotate_secret_path()


@app.get("/")
def home() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ghost Freight</title>
  <style>
    :root {
      color-scheme: dark;
      font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
      background: #0d0f12;
      color: #c8ccd0;
    }
    body {
      margin: 0;
      min-height: 100vh;
      background: radial-gradient(ellipse at top, #141820, #0a0c10 70%);
    }
    main {
      width: min(740px, calc(100vw - 2rem));
      margin: 3rem auto;
      padding: 2rem;
      background: rgba(20, 24, 32, 0.85);
      border: 1px solid #2a3040;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.4);
      border-radius: 6px;
    }
    h1 { margin-top: 0; font-size: 2rem; color: #e0e4e8; }
    code {
      font-family: "IBM Plex Mono", monospace;
      background: #1a1e28;
      padding: 2px 6px;
      border-radius: 3px;
    }
    .endpoint { margin: 1.2rem 0; }
    .endpoint h3 { color: #7eb8da; margin-bottom: 0.3rem; }
    .hint { color: #8a8e94; font-size: 0.9rem; }
  </style>
</head>
<body>
  <main>
    <h1>Ghost Freight &mdash; Cargo Manifest Relay</h1>
    <p>Internal logistics relay for tracking freight manifests across Arachne's port network.</p>

    <div class="endpoint">
      <h3><code>GET /api/manifest</code></h3>
      <p>Returns the current shipment's tracking reference.</p>
    </div>

    <div class="endpoint">
      <h3><code>GET /api/fetch?url=&lt;url&gt;</code></h3>
      <p>Proxy endpoint for retrieving remote manifest documents. Fetches the given URL and returns its contents.</p>
    </div>
  </main>
</body>
</html>"""


@app.get("/api/manifest")
def manifest():
    """Returns a Tracking ID"""
    truncated = (_current_value >> 16) & 0xFFFF
    return jsonify({"tracking_id": f"{truncated:04x}"})


@app.get("/api/fetch")
def fetch():
    url = request.args.get("url", "").strip()
    if not url:
        abort(400, "missing url parameter")

    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        abort(400, f"scheme '{parsed.scheme}' is not allowed — use http or https")

    if not parsed.hostname:
        abort(400, "missing hostname")

    try:
        resp = http_client.get(url, timeout=FETCH_TIMEOUT, stream=True)
        body = resp.content[:MAX_RESPONSE_BYTES]
    except http_client.RequestException as exc:
        abort(502, f"upstream request failed: {exc}")

    content_type = resp.headers.get("Content-Type", "application/octet-stream")
    return body, resp.status_code, {"Content-Type": content_type}


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", DEFAULT_HOST), port=int(os.getenv("PORT", DEFAULT_PORT)))
