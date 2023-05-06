from functools import wraps
from flask import Flask, render_template, g, jsonify, request, session, redirect, url_for, abort
from hyper import HTTPConnection
import sqlite3

from internal import internal_bp
from utils import get_uuid


DATABASE = 'database/sql.db'

app = Flask(__name__)
app.register_blueprint(internal_bp)

app.secret_key = get_uuid()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "uid" not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_notelist():
    query = "SELECT * FROM note WHERE uid = ? LIMIT 10"
    cur = get_db().execute(query, [session["uid"]])
    rv = cur.fetchall()
    return rv

def get_note(uuid):
    query = "SELECT * FROM note WHERE id = ?"
    cur = get_db().execute(query, [uuid])
    rv = cur.fetchone()
    return rv

def save_note(title, content):
    query = "INSERT INTO note VALUES (?,?,?,?)"
    _id = get_uuid()
    db = get_db()
    db.cursor().execute(query, (session["uid"], _id, title, content))
    db.commit()
    return _id

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/", methods=["GET"])
def main():
    if "uid" not in session:
        session["uid"] = get_uuid()
    return render_template("index.html")

@app.route("/note", methods=["GET", "POST"])
@session_required
def note():
    if request.method == "GET":
        rv = get_notelist()
        return render_template("note.html", notes=rv)
    else:
        title = request.form.get("title")
        content = request.form.get("content")
        if type(title) == str and type(content) == str: 
            _id = save_note(title, content)
            return redirect(f"/note/{_id}")
        else:
            return redirect("/note")

@app.route("/note/<uuid>", methods=["GET"])
@session_required
def get_note_with_uuid(uuid):
    rv = get_note(uuid)
    if rv == None:
        abort(404)
    return render_template("view_note.html", note=rv)


if __name__ == "__main__":
    init_db()
    app.run("0.0.0.0", port=12000, debug=False)