from flask import Flask, request, jsonify, render_template_string
import redis
import requests
import re
import json
import sys
app = Flask(__name__)


@app.route('/getid/<username>')
def getid(username):
    red = redis.Redis(host="redis_users")
    return red.get(username).decode()


@app.route('/useraction', methods=["POST"])
def useraction():
    mode = request.form.get("mode")
    username = request.form.get("username")
    if mode == "register":
        r = requests.get('http://redis_userdata:5000/adduser')
        port = int(r.text)
        red = redis.Redis(host="redis_users")
        red.set(username, port)
        return ""
    elif mode == "adddata":
        red = redis.Redis(host="redis_users")
        port = red.get(username).decode()
        requests.post(f"http://redis_userdata:5000/putuser/{port}", json={
            request.form.get("key"): request.form.get("value")
        })
        return ""
    elif mode == "getdata":
        red = redis.Redis(host="redis_users")
        port = red.get(username).decode()
        r = requests.get(f"http://redis_userdata:5000/getuser/{port}")
        return jsonify(r.json())
    elif mode == "bioadd":
        bio = request.form.get("bio")
        bio.replace(".", "").replace("_", "").\
            replace("{", "").replace("}", "").\
            replace("(", "").replace(")", "").\
            replace("|", "")

        bio = re.sub(r'\[\[([^\[\]]+)\]\]', r'{{data["\g<1>"]}}', bio)
        red = redis.Redis(host="redis_users")
        port = red.get(username).decode()
        requests.post(f"http://redis_userdata:5000/bio/{port}", json={
            "bio": bio
        })
        return ""
    elif mode == "bioget":
        red = redis.Redis(host="redis_users")
        port = red.get(username).decode()
        r = requests.get(f"http://redis_userdata:5000/bio/{port}")
        return r.text
    elif mode == "keytransfer":
        red = redis.Redis(host="redis_users")
        port = red.get(username).decode()
        red2 = redis.Redis(host="redis_userdata",
                           port=int(port))
        red2.migrate(request.form.get("host"),
                     request.form.get("port"),
                     [request.form.get("key")],
                     0, 1000,
                     copy=True, replace=True)
        return ""

@app.route("/render", methods=["POST"])
def render_bio():
    data = request.json.get('data')
    if data is None:
        data = {}
    return render_template_string(request.json.get('bio'), data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
