import base64
import secrets
import urllib.parse
from flask import Flask, render_template, request, session, redirect, url_for, abort

SECRET_KEY = secrets.token_bytes(32)

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/", methods=["GET"])
def index():
    if not "memo" in session:
        session["memo"] = [b"Tsukushi"]
    return render_template("index.html")


@app.route("/write", methods=["GET"])
def write_get():
    if not "memo" in session:
        return redirect(url_for("index"))
    return render_template("write_get.html")


@app.route("/read", methods=["GET"])
def read_get():
    if not "memo" in session:
        return redirect(url_for("index"))
    return render_template("read_get.html")


@app.route("/write", methods=["POST"])
def write_post():
    if not "memo" in session:
        return redirect(url_for("index"))
    memo = urllib.parse.unquote_to_bytes(request.get_data()[8:256])
    if len(memo) < 8:
        return abort(403, "これくらいの長さは記憶してください。👻")
    try:
        session["memo"].append(memo)
        if len(session["memo"]) > 5:
            session["memo"].pop(0)
        session.modified = True
        filename = base64.b64encode(memo).decode()
        with open(f"./memo/{filename}", "wb+") as f:
            f.write(memo)
    except:
        return abort(403, "エラーが発生しました。👻")
    return render_template("write_post.html", id=filename)


@app.route("/read", methods=["POST"])
def read_post():
    if not "memo" in session:
        return redirect(url_for("index"))
    filename = urllib.parse.unquote_to_bytes(request.get_data()[7:]).replace(b"=", b"")
    filename = filename + b"=" * (-len(filename) % 4)
    if (
        (b"." in filename.lower())
        or (b"flag" in filename.lower())
        or (len(filename) < 8 * 1.33)
    ):
        return abort(403, "不正なメモIDです。👻")
    try:
        filename = base64.b64decode(filename)
        if filename not in session["memo"]:
            return abort(403, "メモが見つかりません。👻")
        filename = base64.b64encode(filename).decode()
        with open(f"./memo/{filename}", "rb") as f:
            memo = f.read()
    except:
        return abort(403, "エラーが発生しました。👻")
    return render_template("read_post.html", id=filename, memo=memo.decode())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=31415)
