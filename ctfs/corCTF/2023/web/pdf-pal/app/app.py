from flask import Flask, abort, url_for, request, redirect, send_from_directory, send_file, jsonify
from urllib.parse import unquote, urlparse
import hashlib
import requests
import os
import io

app = Flask(__name__)
files = []

def blacklist(text, extra=()):
    banned = ["flag", "txt", "root", "output", "pdf-gen"] + list(extra)
    return any(item in text or item in unquote(text) for item in banned)

@app.route("/")
def index():
    return send_from_directory('./pages/', 'index.html')

@app.route("/view/<requested_file>")
def view(requested_file):
    for file in files:
        if file["pdf"] == requested_file:
            path = os.path.abspath("/pdf-gen/output/" + file["pdf"])
            if not path.startswith("/pdf-gen/output/"):
                return abort(400, ":lemonthink:")

            with open(path, "rb") as pdf:
                data = pdf.read()
            sha256 = hashlib.sha256(data).hexdigest()

            if sha256 != file["hash"]:
                return abort(400, ":lemonthink:")

            return send_file(io.BytesIO(data), attachment_filename=file["pdf"], mimetype='application/pdf')

    return abort(404)

@app.route("/files")
def list_files():
    return jsonify(files)

@app.route("/generate", methods=['GET'])
def generate_get():
    return send_from_directory('./pages/', 'generate.html')

@app.route("/generate", methods=['POST'])
def generate_post():
    global files

    url = request.form.get("url")
    if url:
        if blacklist(url, [".pdf"]):
            return abort(400, "Invalid url")

        if urlparse(url).scheme == "file":
            return abort(400, "Local files not allowed")

        r = requests.post("http://127.0.0.1:7778/generate", json={"url": url})
        resp = r.json()

        if not resp["success"]:
            return abort(400, resp["message"])

        files.append({
            "pdf": resp["pdf"],
            "hash": resp["hash"]
        })

        # max 5 files
        if len(files) > 5:
            files = files[len(files) - 5:]

        return redirect(url_for("view", requested_file=resp["pdf"]))

    return abort(400, "Missing url")

@app.route("/rename", methods=['POST'])
def rename_file():
    original_name = request.form.get("original_name")
    new_name = request.form.get("new_name")

    if not original_name or not new_name:
        return abort(400, "Missing file names")

    if blacklist(original_name) or blacklist(new_name):
        return abort(400, "Invalid file to rename")

    if not new_name.endswith(".pdf"):
        return abort(400, "Invalid file to rename")

    original_path = os.path.abspath("/pdf-gen/output/" + original_name)
    new_path = os.path.abspath("/pdf-gen/output/" + new_name)
    
    if not os.path.exists(original_path) or os.path.exists(new_path):
        return abort(400, "Invalid file name")

    with open(original_path, "rb") as f:
        if f.read(5) != b"%PDF-":
            return abort(400, "File to rename is not a PDF")
        data = f.read()

    with open(new_path, "wb") as f:
        f.write(data)

    os.remove(original_path)

    for file in files:
        if file["pdf"] == original_name:
            file["pdf"] = new_name

    return redirect(url_for("index"))
