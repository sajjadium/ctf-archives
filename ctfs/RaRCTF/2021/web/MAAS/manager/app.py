from flask import Flask, request, jsonify
import requests
import redis

import os
from binascii import hexlify

app = Flask(__name__)


@app.before_first_request
def setup():
    red = redis.Redis(host="manager_users")
    red.set("current", 0)
    add_user("admin", hexlify(os.urandom(16)).decode())


def get_user(name=None, uid=None):
    if name == "current":
        return None
    red = redis.Redis(host="manager_users")
    if uid is not None:
        user = red.get(str(uid))
        if user is not None:
            user, password = user.decode().split(",")
            return uid, user, password
        return None
    elif name is not None:
        for key in red.scan_iter("*"):
            if key.decode() == "current":
                continue
            user = red.get(key)
            if user is not None:
                user, password = user.decode().split(",")
                if user == name:
                    return int(key.decode()), user, password
    else:
        return None


def add_user(name, password):
    if name == "current":
        return None
    red = redis.Redis(host="manager_users")
    uid = str(red.get("current").decode())
    red.incr("current", 1)
    red.set(uid, f"{name},{password}")
    return uid


@app.route("/login", methods=["POST"])
def login():
    user = request.json['username']
    password = request.json['password']
    entry = get_user(name=user)
    if entry:
        if entry[2] == password:
            data = {"uid": entry[0], "name": user}
            if user == "admin" and entry[0] == 0:
                data['flag'] = open("/flag.txt").read()
            return jsonify(data)
        else:
            return jsonify({"error": "Incorrect password"})
    else:
        return jsonify({"uid": add_user(user, password), "name": user})


@app.route("/update", methods=["POST"])
def update():
    return jsonify(requests.post("http://manager_updater:8080/",
                                 data=request.get_data()).json())


app.run(host="0.0.0.0", port=5000)
