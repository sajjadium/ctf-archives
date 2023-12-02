import re
import secrets
import bcrypt
from flask import Flask, request, render_template, session, redirect, url_for
from pymongo.errors import DuplicateKeyError
from database import User
import shutil
import os
import subprocess
import numpy as np
from tensorflow.keras.models import load_model
import time
import glob
import threading

lock = threading.Lock()
app = Flask(__name__)
app.secret_key = secrets.token_bytes(28)

MODEL = "counting_stars.h5"


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session:
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("register.html")

    username, password = request.get_json().get("username"), request.get_json().get(
        "password"
    )

    if not username or not password:
        return {"msg": "Please provide username and password"}, 400

    if not isinstance(username, str) or not isinstance(password, str):
        return {"msg": "Please provide username and password"}, 400

    try:
        dir = f"models/{secrets.token_hex(28)}"
        User.insert_one(
            {
                "username": username,
                "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                "premium": 0,
                "premium_key": secrets.token_hex(28),
                "dir": dir,
            }
        )

        os.mkdir(dir)
        shutil.copyfile(MODEL, f"{dir}/{MODEL}")

        return {"msg": "Registered"}
    except DuplicateKeyError:
        return {"msg": "Username is already taken"}, 400
    except:
        return {"msg": "Something not good"}, 500


@app.route("/login", methods=["GET", "POST"])
def login():
    if session:
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("login.html")
    username, password = request.get_json().get("username"), request.get_json().get(
        "password"
    )

    if not username or not password:
        return {"msg": "Please provide username and password"}, 400

    if not isinstance(username, str) or not isinstance(password, str):
        return {"msg": "Please provide username and password"}, 400

    if user := User.find_one({"username": username}):
        if bcrypt.checkpw(password.encode(), user["password"]):
            session["username"] = user["username"]
            session["premium"] = user["premium"]
            session["premium_key"] = user["premium_key"]
            session["dir"] = user["dir"]
            session["last_time"] = -1
            session["last_time_2"] = -1
            return {"msg": "Logged in"}

    return {"msg": "Wrong username or password"}, 401


@app.route("/upgrade", methods=["GET", "POST"])
def upgrade():
    if not session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("upgrade.html")

    key = request.get_json().get("key")
    if key != session["premium_key"]:
        return {"msg": "Invalid key, please pay 500$ for a permanent key"}, 403
    else:
        User.update_one({"username": session["username"]}, {"$set": {"premium": 1}})
        session["premium"] = 1
        return {"msg": "Valid key, enjoy premium features"}

@app.route("/counting_stars", methods=["GET", "POST"])
def counting_stars():
    if not session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("counting_stars.html")

    try:
        if not (
            session["premium"] == 1
            or session["last_time"] == -1
            or time.time() - session["last_time"] >= 30
        ):
            return {
                "msg": f"Free users can only use this service every 30 seconds. Upgrade to premium for more."
            }, 403

        session["last_time"] = time.time()

        x, y = float(request.get_json().get("longtitude")), float(
            request.get_json().get("latitude")
        )

        if not x or not y:
            return {"msg": "Please provide longtitude and latitude"}, 400

        if not isinstance(x, float) or not isinstance(y, float):
            return {"msg": "So weird! Are you from another planet?"}, 400

        model = load_model(f'{session["dir"]}/{MODEL}')
        input = np.array(np.hstack(([[x]], [[y]])))
        predict = model.predict(input)[0][0]
        return {
            "msg": f"There are approximate {predict:.1f} billion stars within a radius of 2808m around your location"
        }
    except:
        return {"msg": f"Wow! The stars are aligning"}, 200


@app.route("/propose_model", methods=["GET", "POST"])
def propose_model():
    with lock:
        if not session:
            return redirect(url_for("login"))

        if request.method == "GET":
            return render_template("propose_model.html")

        try:
            if not (
                session["premium"] == 1
                or session["last_time_2"] == -1
                or time.time() - session["last_time_2"] >= 30
            ):
                return {
                    "msg": f"Free users can only use this service every 30 seconds. Upgrade to premium for more."
                }, 403

            session["last_time_2"] = time.time()

            url = request.get_json().get("url")

            if not isinstance(url, str):
                return {"msg": "Please provide url"}, 400

            if not url.startswith("http") and not url.startswith("https"):
                return {"msg": "So weird! Are you from another planet?"}, 400

            # My closed beta server can't hold big files, so I need to check length 😳
            # If you know any smarter way to check length before saving files, please contact the user with name "AP" in Discord server. I'm serious
            resp = subprocess.check_output(["wget", "--spider", "-o", "-", url]).decode()
            matches = re.findall("^Length: (\\d+)", resp, flags=re.M)
            if len(matches) != 1:
                return {"msg": "Please don't mess up our system"}, 400
            if int(matches[0]) > 10000:
                return {"msg": "My closed beta server can't hold big files"}, 400

            subprocess.check_output(["wget", "-N", "-P", session["dir"], url])

            list_of_files = glob.glob(f'{session["dir"]}/*')
            latest_file = max(list_of_files, key=os.path.getctime)

            if latest_file == f'{session["dir"]}/{MODEL}':
                os.remove(f"{session['dir']}/{MODEL}")
                shutil.copyfile(MODEL, f"{session['dir']}/{MODEL}")
                return {"msg": "Please don't mess up our system"}, 400
            else:
                return {"msg": "Please contact admin and told him to check your file"}
        except:
            return {"msg": "Something not good"}, 500


if __name__ == "__main__":
    app.run("0.0.0.0", 2808)
