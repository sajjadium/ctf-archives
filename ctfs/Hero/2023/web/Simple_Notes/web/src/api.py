from __main__ import app, secret, connect_db
from flask import request, session, jsonify
from datetime import datetime
from uuid import uuid4
import jwt


def auth_required(func):
    def verify(*args, **kwargs):
        if "logged" in session and "Authorization" in request.headers and request.headers["Authorization"]:
            token = request.headers["Authorization"].replace("Bearer ", "")

            error = 0
            try:
                user = jwt.decode(token, secret, algorithms=["HS256"])
            except:
                error = 1

            if error:
                return jsonify({"error": "Invalid token!"})
            else:
                return func(user["username"], *args, **kwargs)
        else:
            return jsonify({"error": "You must be authenticated!"})
    verify.__name__ = func.__name__
    return verify


"""
    __                _
   / /   ____  ____ _(_)___ 
  / /   / __ \/ __ `/ / __ \
 / /___/ /_/ / /_/ / / / / /
/_____/\____/\__, /_/_/ /_/
            /____/
"""
@app.route("/api/login", methods=["POST"])
def api_login():
    db = connect_db()
    cur = db.cursor()
    values = request.json

    if "username" in values and "password" in values and values["username"] and values["password"]:
        user = cur.execute("SELECT id FROM users WHERE username=? AND password=?", (values["username"], values["password"]))
        db.commit()
        user = user.fetchall()

        if len(user) == 1:
            session["username"] = values["username"]
            session["logged"] = 1
            token = jwt.encode({"username": values["username"]}, secret, algorithm="HS256")
            return jsonify({"bearer": token})

        else:
            res = jsonify({"error": "Invalid credentials!"})
            res.status_code = 400
            return res

    else:
        res = jsonify({"error": "Username and password can't be empty!"})
        res.status_code = 400
        return res


"""
    ____             _      __
   / __ \___  ____ _(_)____/ /____  _____
  / /_/ / _ \/ __ `/ / ___/ __/ _ \/ ___/
 / _, _/  __/ /_/ / (__  ) /_/  __/ /
/_/ |_|\___/\__, /_/____/\__/\___/_/
           /____/
"""
@app.route("/api/register", methods=["POST"])
def api_register():
    db = connect_db()
    cur = db.cursor()
    values = request.json

    if "username" in values and "password" in values and values["username"] and values["password"]:
        user = cur.execute("SELECT id FROM users WHERE username=?", (values["username"],))
        db.commit()
        user = user.fetchall()

        if len(user) == 1:
            res = jsonify({"error": "Username already exist!"})
            res.status_code = 400
            return res

        else:
            cur.execute(f"INSERT INTO users (username, password) VALUES (?, ?)", (values["username"], values["password"]))
            db.commit()
            return jsonify({"success": "User created!"})

    else:
        res = jsonify({"error": "Username and password can't be empty!"})
        res.status_code = 400
        return res


"""
    ____             _____ __
   / __ \_________  / __(_) /__
  / /_/ / ___/ __ \/ /_/ / / _ \
 / ____/ /  / /_/ / __/ / /  __/
/_/   /_/   \____/_/ /_/_/\___/

"""
@app.route("/api/user/<string:user>", methods=["GET"])
@auth_required
def api_note_list(username, user):
    if username != user:
        res = jsonify({"error": "Not authorized!"})
        res.status_code = 403
        return res

    db = connect_db()
    cur = db.cursor()

    notes = cur.execute("SELECT uuid, title, last_update FROM notes WHERE username=?", (username,))
    db.commit()
    notes = notes.fetchall()

    return jsonify({"notes": notes})



"""
   ______                __
  / ____/_______  ____ _/ /____ 
 / /   / ___/ _ \/ __ `/ __/ _ \
/ /___/ /  /  __/ /_/ / /_/  __/
\____/_/   \___/\__,_/\__/\___/

"""
@app.route("/api/user/<string:user>/create", methods=["POST"])
@auth_required
def api_note_create(username, user):
    if username != user:
        res = jsonify({"error": "Not authorized!"})
        res.status_code = 403
        return res

    db = connect_db()
    cur = db.cursor()
    values = request.json

    if "name" in values and values["name"]:
        cur.execute(f"INSERT INTO notes (uuid, username, title, content, last_update) VALUES (?, ?, ?, ?, ?)", (str(uuid4()), username, values["name"], "", datetime.now().strftime("%c")))
        db.commit()

        return jsonify({"success": "Note created!"})

    else:
        res = jsonify({"error": "Name can't be empty!"})
        res.status_code = 400
        return res


"""
 _    ___
| |  / (_)__ _      __
| | / / / _ \ | /| / /
| |/ / /  __/ |/ |/ /
|___/_/\___/|__/|__/

"""
@app.route("/api/user/<string:user>/<string:uuid>", methods=["GET"])
@auth_required
def api_note_get(username, user, uuid):
    if username != user:
        res = jsonify({"error": "Not authorized!"})
        res.status_code = 403
        return res

    db = connect_db()
    cur = db.cursor()

    notes = cur.execute("SELECT title, content FROM notes WHERE username=? AND uuid=?", (username, uuid))
    db.commit()
    notes = notes.fetchall()

    if len(notes) == 1:
        return jsonify({
            "title": notes[0][0],
            "content": notes[0][1]
        })
    else:
        res = jsonify({"error": "Not authorized!"})
        res.status_code = 403
        return res


"""
    ______    ___ __
   / ____/___/ (_) /_
  / __/ / __  / / __/
 / /___/ /_/ / / /_
/_____/\__,_/_/\__/

"""
@app.route("/api/user/<string:user>/<string:uuid>/edit", methods=["POST"])
@auth_required
def api_note_edit(username, user, uuid):
    if username != user:
        res = jsonify({"error": "Not authorized!"})
        res.status_code = 403
        return res

    values = request.json

    if "title" in values and "content" in values:
        db = connect_db()
        cur = db.cursor()

        notes = cur.execute("SELECT title, content FROM notes WHERE username=? AND uuid=?", (username, uuid))
        db.commit()
        notes = notes.fetchall()

        if len(notes) == 1:
            cur.execute(f"UPDATE notes SET title=?, content=?, last_update=? WHERE uuid=? AND username=?", (values["title"], values["content"], datetime.now().strftime("%c"), uuid, username))
            db.commit()
            return jsonify({"success": "Note updated!"})
        else:
            res = jsonify({"error": "Not authorized!"})
            res.status_code = 403
            return res

    else:
        res = jsonify({"error": "Title and content must be sent!"})
        res.status_code = 400
        return res
