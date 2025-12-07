import os
import sqlite3
import flask

app = flask.Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.post('/login')
def login():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    
    db = sqlite3.connect("file:db.db?mode=ro", uri=True)
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM fish WHERE username = '" + username + "' AND password ='" + password +"';")

    try:
        count = cur.fetchone()[0]
        if count > 0:
            flask.session["username"] = username
            
            cur.close()
            db.close()
            return flask.redirect('/admarine')
        else:
            cur.close()
            db.close()
            return flask.render_template("index.html", error="Incorrect password")
    except TypeError:
        cur.close()
        db.close()
        return flask.render_template("index.html", error="No user found")
    
@app.route('/admarine')
def admin():
    if 'username' not in flask.session:
        return flask.redirect('/')
    return flask.render_template("admin.html")

DISALLOWED_WORDS = ["insert", "create", "alter", "drop", "delete", "backup", "transaction", "commit", "rollback", "replace", "update", "pragma", "attach", "load", "vacuum"]

@app.post('/monitor')
def monitor():
    if 'username' not in flask.session:
        return flask.redirect('/')
    
    query = flask.request.form.get('query')
    
    for word in DISALLOWED_WORDS:
        if word in query.lower():
            return flask.redirect('/admarine')
    
    db = sqlite3.connect("file:db.db?mode=ro", uri=True)
    cur = db.cursor()
    try:
        cur.execute(query)
    except:
        cur.close()
        db.close()
        return flask.render_template('/admin.html', error="Invalid query")
    
    cur.close()
    db.close()
    return flask.render_template("/admin.html", error="Successful process")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9995)