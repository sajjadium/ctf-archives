from flask import Flask, request, render_template, redirect, make_response, send_file
import uuid
import jwt
from functools import wraps
from datetime import datetime
import os
import json

MAX_SIZE_MB = 0.5
KID = "8c2088dfb37658e01b35aec916b3b085c3cafd5fbf03bbb2735d3f8e63defd6b"

app = Flask(__name__)
app.static_folder = "static"
app.config["MAX_CONTENT_LENGTH"] = int(MAX_SIZE_MB * 1024 * 1024)

flag = open("flag.txt", "r").read()
private_key = open("private.ec.key", "rb").read()
public_key = open("static/public_key.pem", "rb").read()

id_to_username = {}
user_files = {}


class File:
    def __init__(self, file_id, name, mime):
        self.file_id = file_id
        self.name = name
        self.mime = mime
        self.time = datetime.strftime(datetime.now(), "%a %b %d %H:%M:%S")


def login_required():
    def _login_required(f):
        @wraps(f)
        def __login_required(*args, **kwargs):
            token = request.cookies.get("token")
            if not token:
                return redirect("/register")
            user = verify_token(token)
            if user is None:
                return redirect("/register")
            return f(*args, **kwargs, user=user)

        return __login_required

    return _login_required


def generate_token(user_id):
    return jwt.encode(
        {"id": user_id},
        private_key,
        algorithm="ES256",
        headers={"kid": KID, "jku": "jwks.json"},
    )


def verify_token(token):
    try:
        header = jwt.get_unverified_header(token)
        jku = header["jku"]
        with open(f"static/{jku}", "r") as f:
            keys = json.load(f)["keys"]
        kid = header["kid"]
        for key in keys:
            if key["kid"] == kid:
                public_key = jwt.algorithms.ECAlgorithm.from_jwk(key)
                payload = jwt.decode(token.encode(), public_key, algorithms=["ES256"])
                return payload
    except Exception:
        pass
    return None


@app.route("/static/<path:path>")
def static_file(filename):
    return app.send_static_file(filename)


@app.route("/")
@login_required()
def index(user):
    return render_template(
        "index.html",
        user_id=user["id"],
        files=user_files.get(user["id"], {}).values(),
    )


@app.route("/register", methods=["GET"])
def get_register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def post_register():
    if "username" not in request.form:
        return redirect("/register?err=No+username+provided")
    username = request.form["username"]
    user_id = str(uuid.uuid4())
    user_files[user_id] = {}
    id_to_username[user_id] = username
    res = make_response(redirect("/"))
    res.set_cookie("token", generate_token(user_id))

    return res


@app.route("/upload", methods=["POST"])
@login_required()
def post_upload(user):
    if "file" not in request.files:
        return redirect(request.url + "?err=No+file+provided")
    file = request.files["file"]
    if file.filename == "":
        return redirect("/?err=Attached+file+has+no+name")
    if file:
        uid = user["id"]
        fid = str(uuid.uuid4())
        folder = os.path.join(os.getcwd(), f"uploads/{uid}")
        os.makedirs(folder, exist_ok=True)
        file.save(os.path.join(folder, fid))
        f = File(fid, file.filename, file.mimetype)
        if uid not in user_files:
            user_files[uid] = {}
        user_files[uid][fid] = f
    return redirect(f"/?success=Successfully+uploaded+file&path={uid}/{fid}")


@app.route("/view/<uuid:user_id>/<uuid:file_id>")
def view_file(user_id, file_id):
    user_id, file_id = str(user_id), str(file_id)
    try:
        f = user_files[user_id][file_id]
        return render_template(
            "view_file.html",
            username=id_to_username[user_id],
            filename=f.name,
            user_id=user_id,
            file_id=file_id,
            time=f.time,
        )
    except (FileNotFoundError, KeyError):
        return "File not found", 404
    return "Internal server error", 500


@app.route("/download/<uuid:user_id>/<uuid:file_id>")
def download_file(user_id, file_id):
    user_id, file_id = str(user_id), str(file_id)
    try:
        f = user_files[user_id][file_id]
        return send_file(
            open(os.path.join(os.getcwd(), f"uploads/{user_id}/{file_id}"), "rb"),
            mimetype=f.mime,
        )
    except (FileNotFoundError, KeyError):
        return "File not found", 404
    return "Internal server error", 500


@app.route("/flag")
@login_required()
def get_flag(user):
    if user["id"] == "admin":
        return flag
    else:
        return "admins only! shoo!"


if __name__ == "__main__":
    app.run(port=5000)
