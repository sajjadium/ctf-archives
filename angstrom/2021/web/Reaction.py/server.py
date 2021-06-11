from flask import escape, session, request, Flask, redirect
from collections import Counter
import uuid
import string
from functools import wraps
from threading import Lock
import subprocess
import json
import requests

# exceptions bad results good
OK = 1
ERR = 2

SAFECHARS = set(string.ascii_letters + string.digits + "_")

# templating engines are for chumps
STYLESHEET = """
body {
    background-color: black;
}

* {
    font-family: monospace;
    color: white;
    font-size: 18px;
}

form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
}

input {
    width: 50%;
    background: none;
    border-width: 0 0 1px 0;
    border-color: white;
    border-style: solid;
    margin-bottom: 10px;
}

input::placeholder {
    color: #9e9e9e;
}

input[type=submit] {
    width: 20%;
    border-width: 1px;
    cursor: pointer;
}

p {
    text-align: center;
}

.error {
    color: #f44336;
}

a {
    color: #4dd0e1;
}
""".strip()

PAGE_TEMPLATE = f"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Reaction.py demo</title>
        <style>{STYLESHEET}</style>
    </head>
    <body>$$BODY$$<script src="https://www.google.com/recaptcha/api.js" async defer></script></body>
</html>
""".strip()

LOGIN_PAGE = PAGE_TEMPLATE.replace(
    "$$BODY$$",
    """
<form action="/login" method="POST">
    $$ERROR$$
    <a href="/register">Register instead</a>
    <input type="text" name="username" placeholder="username">
    <input type="password" name="pw" placeholder="password">
    <input type="submit" value="login">
</form>
""".strip(),
)

REGISTER_PAGE = PAGE_TEMPLATE.replace(
    "$$BODY$$",
    """
<form action="/register" method="POST">
    $$ERROR$$
    <a href="/login">Login instead</a>
    <input type="text" name="username" placeholder="username">
    <input type="password" name="pw" placeholder="password">
    <input type="submit" value="login">
</form>
""".strip(),
)


with open("secret.txt", "r") as f:
    admin_password = f.read().strip()

with open("flag.txt", "r") as f:
    flag = f.read().strip()

with open("captcha.json", "r") as f:
    captcha = json.load(f)

accounts = {
    "admin": {
        "username": "admin",
        "pw": admin_password,
        "bucket": [f"<p>{escape(flag)}</p>"],
        "mutex": Lock(),
    }
}


def add_component(name, cfg, bucket):
    if not name or not cfg:
        return (ERR, "Missing parameters")
    if len(bucket) >= 2:
        return (ERR, "Bucket too large (our servers aren't very good :((((()")
    if len(cfg) > 250:
        return (ERR, "Config too large (our servers aren't very good :((((()")
    if name == "welcome":
        if len(bucket) > 0:
            return (ERR, "Welcomes can only go at the start")
        bucket.append(
            """
            <form action="/newcomp" method="POST">
                <input type="text" name="name" placeholder="component name">
                <input type="text" name="cfg" placeholder="component config">
                <input type="submit" value="create component">
            </form>
            <form action="/reset" method="POST">
                <p>warning: resetting components gets rid of this form for some reason</p>
                <input type="submit" value="reset components">
            </form>
            <form action="/contest" method="POST">
                <div class="g-recaptcha" data-sitekey="{}"></div>
                <input type="submit" value="submit site to contest">
            </form>
            <p>Welcome <strong>{}</strong>!</p>
            """.format(
                captcha.get("sitekey"), escape(cfg)
            ).strip()
        )
    elif name == "char_count":
        bucket.append(
            "<p>{}</p>".format(
                escape(
                    f"<strong>{len(cfg)}</strong> characters and <strong>{len(cfg.split())}</strong> words"
                )
            )
        )
    elif name == "text":
        bucket.append("<p>{}</p>".format(escape(cfg)))
    elif name == "freq":
        counts = Counter(cfg)
        (char, freq) = max(counts.items(), key=lambda x: x[1])
        bucket.append(
            "<p>All letters: {}<br>Most frequent: '{}'x{}</p>".format(
                "".join(counts), char, freq
            )
        )
    else:
        return (ERR, "Invalid component name")
    return (OK, bucket)


def register(username, pw):
    if not username or not pw:
        return (ERR, "Missing parameters")
    if len(username) > 15 or any(x not in SAFECHARS for x in username):
        return (ERR, "Bad username")
    if username in accounts:
        return (ERR, "User already exists")
    (t, v) = add_component("welcome", username, [])
    if t == ERR:
        return (ERR, v)
    accounts[username] = {
        "username": username,
        "pw": pw,  # please don't use your actual password
        "bucket": v,
        "mutex": Lock(),
    }
    return (OK, username)


def login(username, pw):
    if not username or not pw:
        return (ERR, "Missing parameters")
    if username not in accounts:
        return (ERR, "Username and password don't match")
    if pw != accounts[username]["pw"]:
        return (ERR, "Username and password don't match")
    return (OK, username)


def reset(user):
    del user["bucket"][:]
    return (OK, ())


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex


def mustlogin(route):
    @wraps(route)
    def ret():
        if request.cookies.get("secret") == admin_password:
            fakeuser = request.args.get("fakeuser")
            if fakeuser:
                return route(user=accounts[fakeuser])
        if "username" not in session or session["username"] not in accounts:
            return redirect("/login", code=302)
        return route(user=accounts[session["username"]])

    return ret


@app.route("/", methods=["GET"])
@mustlogin
def home(user):
    return PAGE_TEMPLATE.replace("$$BODY$$", "".join(user["bucket"]))


@app.route("/login", methods=["GET"])
def login_page():
    return LOGIN_PAGE.replace("$$ERROR$$", "")


@app.route("/login", methods=["POST"])
def login_post():
    (t, v) = login(request.form.get("username"), request.form.get("pw"))
    if t == ERR:
        return (LOGIN_PAGE.replace("$$ERROR$$", f"""<p class="error">{v}</p>"""), 400)
    session["username"] = v
    return redirect("/", code=302)


@app.route("/register", methods=["GET"])
def register_page():
    return REGISTER_PAGE.replace("$$ERROR$$", "")


@app.route("/register", methods=["POST"])
def register_post():
    (t, v) = register(request.form.get("username"), request.form.get("pw"))
    if t == ERR:
        return (
            REGISTER_PAGE.replace("$$ERROR$$", f"""<p class="error">{v}</p>"""),
            400,
        )
    session["username"] = v
    return redirect("/", code=302)


@app.route("/reset", methods=["POST"])
@mustlogin
def reset_post(user):
    if user["username"] == "admin":
        return ("Cannot reset admin", 400)
    (t, v) = reset(user)
    if t == ERR:
        return (
            PAGE_TEMPLATE.replace("$$BODY$$", f"""<p class="error">{v}</p>"""),
            400,
        )
    return redirect("/", code=302)


@app.route("/newcomp", methods=["POST"])
@mustlogin
def new_component_post(user):
    with user["mutex"]:
        (t, v) = add_component(
            request.form.get("name"), request.form.get("cfg"), user["bucket"]
        )
    if t == ERR:
        return (
            PAGE_TEMPLATE.replace("$$BODY$$", f"""<p class="error">{v}</p>"""),
            400,
        )
    return redirect("/", code=302)


@app.route("/contest", methods=["POST"])
@mustlogin
def contest_submission(user):
    captcha_response = request.form.get("g-recaptcha-response")
    if not captcha_response:
        return ("Please complete the CAPTCHA", 400)
    secretkey = captcha.get("secretkey")
    if secretkey:
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secretkey, "response": captcha_response},
        ).json()
        if not r["success"]:
            return ("Invalid CAPTCHA", 400)
        subprocess.run(
            ["node", "visit.js", user["username"]],
            # stdout=subprocess.DEVNULL,
            # stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
        return PAGE_TEMPLATE.replace(
            "$$BODY$$",
            """<p>The admin should have reviewed your submission. <a href="/">Back to homepage</a></p>""",
        )


if __name__ == "__main__":
    app.run(port=8080, debug=False, host="0.0.0.0", threaded=True)
