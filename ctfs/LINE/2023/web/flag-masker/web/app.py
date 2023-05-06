from flask import Flask, Response, session, render_template, abort, request, redirect
from captcha.image import ImageCaptcha
from core.database import Database
from core.report import Report
from core.config import Config
from string import digits
from base64 import b64encode
from random import choice
from uuid import uuid4

app = Flask(__name__)
db = Database()
report = Report()
image = ImageCaptcha(width=300, height=70)


def check_owner(uid):
    return session.get("uid", False) == uid


def check_params(data):
    if not data.get("memo") or not data.get("secret"):
        return None

    if len(data.get("memo")) > 100:
        return None

    if not isinstance(data.get("secret"), bool):
        return None

    return {"memo": data.get("memo"), "secret": data.get("secret")}


def check_url(data):
    if not data.get("url") and not data.get("captcha"):
        return None

    return {"url": data.get("url"), "captcha": data.get("captcha")}


def log(text):
    print(text, flush=True)


@app.after_request
def after_request(response):
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.route("/", methods=["GET"])
def main():
    if not session.get("uid", False):
        session["uid"] = uuid4().__str__()
        return redirect(f"{session['uid']}")

    else:
        return redirect(f"{session['uid']}")


@app.route("/<string:uid>", methods=["GET"])
def memo_view(uid):
    try:
        owner = check_owner(uid)
        memo = db.loads(
            {
                "uid": uid,
            }
        )
        if not memo and not owner:
            return abort(403)

        return render_template("index.html", memo=memo, owner=owner)

    except:
        abort(404)


@app.route("/<string:uid>", methods=["POST"])
def memo_handle(uid):
    try:
        params = check_params(request.get_json())
        params = request.get_json()
        if not params:
            abort(400)

        if not check_owner(uid):
            abort(403)

        db.write({"uid": uid, "memo": params["memo"], "secret": params["secret"]})
        return ""

    except:
        abort(404)


@app.route("/<string:uid>/alert", methods=["GET"])
def memo_alert(uid):
    log(f"Memo {uid} contains flag!")
    return ""


@app.route("/config", methods=["GET"])
def config():
    return Response('{"regex": "LINECTF\\\{(.+)\\\}"}', mimetype="application/json")


@app.route("/report", methods=["GET"])
def report_view():
    session["captcha"] = "".join(choice(digits) for _ in range(8))
    captcha = b64encode(image.generate(session["captcha"]).getvalue()).decode()
    return render_template("report.html", captcha=captcha)


@app.route("/report", methods=["POST"])
def report_handle():
    try:
        params = check_url(request.get_json())
        if not params:
            abort(400)

        if session["captcha"] != params["captcha"]:
            session.pop("captcha")
            abort(400)

        report.submit({"url": params["url"]})
        session.pop("captcha")
        return ""

    except:
        abort(400)


app.secret_key = Config.secret
app.run(host="0.0.0.0", port=8000, debug=False)
