from flask import Flask, request, jsonify
import redis
import random
import os
import os

app = Flask(__name__)


@app.route('/adduser')
def adduser():
    port = random.randint(50000, 60000)
    if os.system(f"redis-server --port {port} --daemonize yes --protected-mode no") == 0:
        return str(port), 200
    else:
        return "0", 500


@app.route('/getuser/<port>', methods=["GET"])
def getuser(port):
    r = redis.Redis(port=port)
    res = []
    for key in r.scan_iter("*"):
        res.append({key.decode(): r.get(key).decode()})
    return jsonify(res)


@app.route('/putuser/<port>', methods=["POST"])
def putuser(port):
    r = redis.Redis(port=port)
    r.mset(request.json)
    return "", 200


@app.route("/bio/<port>", methods=["POST", "GET"])
def bio(port):
    if request.method == "GET":
        if os.path.exists(f"/tmp/{port}.txt"):
            with open(f"/tmp/{port}.txt") as f:
                return f.read()
        else:
            return ""
    elif request.method == "POST":
        with open(f"/tmp/{port}.txt", 'w') as f:
            f.write(request.json.get("bio"))
        return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
