from flask import Flask, request, jsonify, render_template
import flask
import json
import hashlib
import os
import secrets
import string

app = Flask(__name__)

def sha248(x):
    return hashlib.sha256(x).hexdigest()[2:]

def verify(secret, id, hash):
    '''new_id = ""
    for i in range(max(len(secret), len(id))):
        new_id += chr(ord(secret[i % len(secret)]) ^ ord(id[i % len(id)]))'''
    id_arr = [i for i in id]
    for i in range(16):
        id_arr[i] = ord(secret[i]) ^ id[i]
    id = bytes(id_arr)
    print(id)
    new_hash = sha248(id)
    print(new_hash)
    print(hash)
    if new_hash in hash:
        return True
    return False

def rand_secret():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(16))

def auth(table, secret):
    print("{} authenticating".format(table))

    if table == "" or secret == "" or table == None or secret == None:
        return jsonify(status="ERR", message="invalid arguments")

    s_data = None
    with open("data/secrets.json") as f:
        s_data = json.load(f)

    if table not in s_data:
        return jsonify(status="ERR", message="table not found")

    if secret != s_data[table]:
        return jsonify(status="ERR", message="invalid authentication")

    return jsonify(status="OK")

@app.route("/authapi", methods = ["GET"])
def authapi():
    table = request.args.get("table")
    secret = request.args.get("secret")
    return auth(table, secret)

def get(table, t_hash, t_id):
    print("{} get".format(table))

    if table == "" or t_hash == "" or t_id == "" or table == None or t_hash == None or t_id == None:
        return jsonify(status="ERR", message="invalid arguments")

    s_data = None
    with open("data/secrets.json") as f:
        s_data = json.load(f)

    if table not in s_data:
        return jsonify(status="ERR", message="table not found")

    t_id_bytes = bytes.fromhex(t_id)
    if len(t_id_bytes) < 16:
        t_id_bytes = ("\x00" * (16 - len(t_id_bytes))).encode() + t_id_bytes
    print(t_id_bytes)
    if not verify(s_data[table], t_id_bytes, t_hash):
        return jsonify(status="ERR", message="invalid authentication")

    cur_data = None
    try:
        with open("data/data.json") as f:
            cur_data = json.load(f)[table]
    except ValueError as e:
        return jsonify(status="ERR", message="data corrupted, contact admin")

    sort_data = sorted(cur_data.items(), key=lambda item: item[1], reverse=True)[:int(t_id, 16)] # ("name", score)
    res_data = []
    c_rank = 0
    c_cnt = 0
    prev = None
    for name, score in sort_data:
        c_cnt += 1
        if score != prev:
            c_rank += c_cnt
            prev = score
            c_cnt = 0
        res_data.append([name, score, c_rank])

    return jsonify(status="OK", message=res_data)


@app.route("/getapi", methods = ["GET"])
def getapi():
    table = request.args.get("table")
    t_hash = request.args.get("hash")
    t_id = request.args.get("id")
    return get(table, t_hash, t_id)

@app.route("/getf", methods = ["GET"])
def getf():
    table = request.args.get("table")
    t_hash = request.args.get("hash")
    t_id = request.args.get("id")
    print(t_id)
    res = get(table, t_hash, t_id).json
    if res["status"] != "OK":
        return res["status"]
    return render_template("get.html", data=res["message"], tname=table, tn=str(int(t_id, 16)))

@app.route("/getgenf", methods = ["GET"])
def getgenf():
    return render_template("getgenf.html")

def update(table, secret, r_data):
    print("{} update".format(table))

    if table == "" or secret == "" or table == None or secret == None:
        return jsonify(status="ERR", message="invalid arguments")

    s_data = None
    with open("data/secrets.json") as f:
        s_data = json.load(f)

    if table not in s_data:
        return jsonify(status="ERR", message="table not found")

    if secret != s_data[table]:
        return jsonify(status="ERR", message="invalid authentication")

    upd_data = None
    try:
        upd_data = json.loads(r_data)
    except ValueError as e:
        return jsonify(status="ERR", message="json parsing failed")

    cur_data = None
    try:
        with open("data/data.json") as f:
            cur_data = json.load(f)
    except ValueError as e:
        return jsonify(status="ERR", message="data corrupted, contact admin")

    for name in upd_data:
        if name not in cur_data[table]:
            cur_data[table][name] = 0
        cur_data[table][name] += upd_data[name]

    with open("data/data.json", "w") as f:
        json.dump(cur_data, f)

    return jsonify(status="OK")

@app.route("/updateapi", methods = ["GET"])
def updateapi():
    table = request.args.get("table")
    secret = request.args.get("secret")
    upd_data = request.args.get("data")
    return update(table, secret, upd_data)

@app.route("/updatef", methods = ["GET"])
def updatef():
    return render_template("updatef.html")

def newtbl(table):
    if table == "" or table == None:
        return jsonify(status="ERR", message="invalid arguments")
    data = None
    with open("data/secrets.json") as f:
        data = json.load(f)
    if table in data:
        return jsonify(status="ERR", message="table already exists")
    t_secret = rand_secret()
    data[table] = t_secret
    with open("data/secrets.json", "w") as f:
        json.dump(data, f)
    with open("data/data.json") as f:
        data = json.load(f)
    data[table] = {}
    with open("data/data.json", "w") as f:
        json.dump(data, f)
    return jsonify(status="OK", message=t_secret)

@app.route("/newtblapi", methods = ["GET"])
def newtblapi():
    table = request.args.get("table")
    return newtbl(table)

@app.route("/newtblf", methods = ["GET"])
def newtblf():
    return render_template("newtbl.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.isdir("data"):
        os.mkdir("data")
    if not os.path.isfile("data/secrets.json"):
        with open("data/secrets.json", "w") as f:
            f.write("{ }")
    if not os.path.isfile("data/used.txt"):
        with open("data/used.txt", "w") as f:
            pass
    if not os.path.isfile("data/data.json"):
        with open("data/data.json", "w") as f:
            f.write("{ }")
    app.run()
