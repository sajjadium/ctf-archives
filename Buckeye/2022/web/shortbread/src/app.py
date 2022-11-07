# file: app.py
from flask import Flask, render_template, request, Response, redirect
import validators
from Crypto.Hash import SHAKE256
from binascii import hexlify
from pymongo import MongoClient
import datetime
import json
import os
import random

app = Flask(__name__)

shake = SHAKE256.new(os.urandom(random.randrange(10,64)))

client = MongoClient("mongodb://shortbread-mongo", 27017)

db = client.shortbread
links = db.links

loggingDir = "/app/admin/logs"

def writeLog(path : str, text : str):
    logFileName = os.path.basename(path)

    with open(os.path.join(loggingDir, logFileName), "a+") as f:
        f.write(f"{datetime.datetime.now()} {text}")

def readLog(path : str):
    # open resource only allows accces to files within 
    # scope of current execution
    with app.open_resource(path, "r") as f:
        return f.readlines()

@app.route("/admin/api/delete/<longpath>", methods=['DELETE'])
def deleteURL(longpath):
    links.delete_one({'longpath': longpath})

    writeLog(longpath, f"[{request.remote_addr}] Deleted link {longpath}")

    return Response(json.dumps({'status':'success'}), status=200, mimetype="application/json")

@app.route("/admin/api/update/<longpath>", methods=['POST', 'UPDATE'])
def updateURL(longpath):
    short_url = request.args.get("url")
        
    if short_url is None:
        return Response(json.dumps({'status':'failure'}), status=400, mimetype="application/json")
    
    links.update_one({"longpath": longpath}, {'$set': {'shorturl': short_url}})

    writeLog(longpath, f"[{request.remote_addr}] Updated link {longpath} to {short_url}")

    return Response(json.dumps({'status': 'success'}), status=200, mimetype="application/json")
    
@app.route("/admin/api/logs", methods=['GET'])
def getLog():
    longpath = request.args.get("path")

    if longpath is None:
        return Response(json.dumps({'status':'failure'}), status=400, mimetype="application/json")

    try: 
        text = readLog(os.path.join(loggingDir, longpath))
    except FileNotFoundError:
        return Response(json.dumps({'status':'failure'}), status=404, mimetype="application/json")

    return render_template("admin.html", messages = text, url = longpath)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/forbidden", methods=['GET'])
def forbidden():
    return "FORBIDDEN\n"

@app.route('/url/<path>', methods=['GET'])
def urlRedirect(path : str):
    if isinstance(path, int):
        path = str(path)
    elif not isinstance(path, str):
        return Response(json.dumps({'error':'wtf? what you do?'}), status=404, mimetype='application/json')

    doc = links.find_one(filter={"longpath": path}) 
    
    if doc is None:
        return Response(json.dumps({'error':'invalid url'}), status=404, mimetype='application/json')
    
    return redirect(doc['shorturl'])

@app.route("/upload", methods=['POST'])
def upload():
    if 'url' not in request.args \
        or not validators.url(request.args['url']):
        return Response(json.dumps({'error':'invalid url'}), status=400, mimetype='application/json')

    url = request.args['url']
    
    # max url length is 2048. We pad to 2*len(), so we only allow
    # 1000 characters to generate the url (and then baseURL) length
    # is appended
    if len(url) > 1000:
        return Response(json.dumps({'error':'url too long'}), status=400, mimetype='application/json')

    long_url_path = hexlify(shake.read(2 * len(url))).decode('ascii')
    
    if request.url_root[-1] != "/":
        request.url_root = request.url_root + "/"
    
    long_url = f"{request.url_root}url/{long_url_path}"
    
    try:
        links.insert_one({"longurl": long_url, "longpath": long_url_path, "shorturl": url})
    except Exception:
        return Response(json.dumps({'error':'failed to upload link'}), status=500, mimetype='application/json')

    writeLog(long_url_path, f"[{request.remote_addr}] Created link {long_url} to {url}")

    return Response(json.dumps({"url": long_url}), status=200, mimetype='application/json')
    
if __name__ == "__main__":
    app.run()