import sqlite3
from flask import Flask, render_template, g, request

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

@app.route("/", methods=["GET"])
def index():
    param = request.args.get("param")
    achievements = query_db("select * from achievements")
    if param != None:
        sqli = 1 in [c in param for c in "*-/ |%"]
        if sqli:
            return render_template("sqli.html")
        achievements = query_db("select * from achievements where achievement like '%" + param + "%'")
    achievements = [achievement[0] for achievement in achievements]
    return render_template("index.html", achievements=achievements)
