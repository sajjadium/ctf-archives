import sqlite3
import requests
from flask import Flask, render_template, g, request, redirect
from lxml import etree
import base64
import time

app = Flask(__name__)

DATABASE = "db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def search(param):
    achievements = query_db("select * from achievements where achievement like '%' || ? || '%'", (param,))
    return achievements

@app.route("/", methods=["GET"])
def index():
    req_time = int(time.time())
    base64_time = base64.urlsafe_b64encode(req_time.to_bytes((req_time.bit_length() + 7) // 8, byteorder="big")).decode()
    return render_template("index.html", epochtime=req_time, basesftime=base64_time, apiurl=request.url_root+"api")

@app.route("/api", methods=["GET"])
def rick():
    requests.get("https://api.countapi.xyz/hit/alex-fan-club-api.litctf.live/ricks")
    return redirect("https://youtu.be/dQw4w9WgXcQ")

def processXML(root):
    stime = root.xpath("/req/stime")[0].text
    ntime = root.xpath("/req/ntime")[0].text
    stext = root.xpath("/req/search")[0].text
    while True:
        try:
            stime_int = int.from_bytes(base64.urlsafe_b64decode(stime), byteorder="big")
            break;
        except:
            stime += 'A'
    while True:
        try:
            ntime_int = int.from_bytes(base64.urlsafe_b64decode(ntime), byteorder="big")
            break;
        except:
            ntime += 'A'
    if ntime_int < stime_int:
        return "lol wtf r u time traveller"
    if ntime_int > stime_int + 65:
        return "request expired after one minute"
    ach_list = search(stext)
    ach_list = [i[0] for i in ach_list]
    return "\n".join(ach_list)

@app.route("/api", methods=["POST"])
def api():
    req_time = int(time.time()) + 5
    b64_time = request.form.get("time").encode()
    prefix_xml = b'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY sendtime "' + b64_time + b'"> <!ENTITY nowtime "' + base64.urlsafe_b64encode(req_time.to_bytes((req_time.bit_length() + 7) // 8, byteorder="big")) + b'"> ]><req><stime>&sendtime;</stime><ntime>&nowtime;</ntime>'
    suffix_xml = b'</req>'
    parser = etree.XMLParser()
    root = etree.fromstring(prefix_xml + request.form.get("search").encode() + suffix_xml, parser=parser)
    return processXML(root)

