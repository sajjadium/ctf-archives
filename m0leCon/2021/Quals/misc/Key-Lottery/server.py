import os
import random
import string

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

safe = {}
allowed = set(string.ascii_letters + string.digits + ",")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/guess", methods=["GET", "POST"])
def guess():
    if request and request.form and "keys" in request.form:
        if len(request.form["keys"]) > 33 * 5:
            return f"Keys string is too long, it must be less than {33 * 5} characters."
        response = access_safe(action="guess", keys=request.form["keys"])
        return response
    else:
        return "Keys should be sent as comma separated string of key guesses. Letters and digits only. No spaces. Example: /guess?keys=key0,key1,key2", 400


def access_safe(action, keys="", key_set=set()):
    global safe, allowed
    if action == "lock_up_flag":
        key_set.add("".join(random.choice(list(allowed - {",", })) for i in range(32)))
        for key in key_set:
            safe[key] = os.environ["FLAG"]
        return
    bad_chars = set(keys) - allowed
    if len(bad_chars) > 0:
        return f"no symbols allowed for keys, got: {''.join(bad_chars)}", 400
    if keys.startswith(","):
        keys = keys[1:]
    if keys.endswith(","):
        keys = keys[:-1]
    if len(keys) == 0:
        return f"got empty key list: {repr(keys)}", 400
    keys = set(keys.split(",")) - {"", }
    if len(keys) > 0:
        key_set = keys
    else:
        return f"got empty key set: {repr(key_set)}", 400
    if action == "guess":
        if "FLAG" in keys:
            return "the flag's key is a 32 characters string of letters and numbers, it is ungessable.", 400
        if all(key in safe for key in key_set):
            return jsonify({key: safe[key] for key in key_set}), 200
        else:
            return f"no luck with this keys: {', '.join(key_set)}", 200
    return 500


access_safe(action="lock_up_flag")
