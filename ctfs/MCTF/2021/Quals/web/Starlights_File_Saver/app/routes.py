import os

from flask import redirect, url_for, send_from_directory, escape, jsonify, request
from app import app, cache, db
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, File
from werkzeug.utils import secure_filename


@app.route('/api/')
def index():
    if current_user.is_authenticated:
        return jsonify({"Username": current_user.username})
    else:
        return jsonify({"Message": "Not auth"}), 403


@app.route('/api/login', methods=["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({"Message": "You authenticated already."})
    if request.method == "POST":
        post_data = request.get_json(force=True)
        user = User.query.filter_by(username=post_data.get("login")).first()
        if user is None or not user.check_password(post_data.get("password")):
            return jsonify({"Message": "Wrong credentials"}), 400
        login_user(user, remember=post_data.get("remember"))
        return jsonify({"Message": "Login success."})


@app.route('/api/logout')
def logout():
    logout_user()
    return jsonify({"Message": "Logout committed."})


@app.route('/api/register', methods=["POST"])
def register():
    if current_user.is_authenticated:
        return jsonify({"Message": "You authenticated already."})
    if request.method == "POST":
        post_data = request.get_json(force=True)
        user = User(username=post_data.get("login"))
        user.set_password(post_data.get("password"))
        if User.query.filter_by(username=post_data.get("login")).first() is not None \
                or escape(post_data.get("login")) != post_data.get("login") \
                or secure_filename(post_data.get("login")) != post_data.get("login"):
            return jsonify({"Message": "Bad username."}), 400
        db.session.add(user)
        db.session.commit()
        login_user(user)
        os.mkdir(os.path.join(app.config["UPLOAD_FOLDER"], current_user.username))
        return jsonify({"Message": "Register success."})


@app.route("/api/<username>/files", methods=["GET"])
@cache.cached(timeout=10)
def ufiles(username):
    if not current_user.is_authenticated:
        return jsonify({"Message": "Not auth"}), 403
    if username != current_user.username:
        return jsonify({"Message": "You have no access to files!"}), 403
    files = File.query.filter_by(user_id=current_user.id).all()
    return jsonify(files)


@app.route('/api/<username>/files/upload', methods=["POST"])
def upload(username):
    if not current_user.is_authenticated:
        return jsonify({"Message": "Not auth"}), 403
    if username != current_user.username:
        return jsonify({"Message": "You have no access to files!"}), 403
    f = request.files['file']
    filename = f.filename
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], current_user.username, filename))
    file = File(filename=f.filename, user_id=current_user.id)
    db.session.add(file)
    db.session.commit()
    return jsonify({"Message": "File uploaded successfully."})


@app.route("/api/files/<id>")
def files(id):
    if not current_user.is_authenticated:
        return jsonify({"Message": "Not auth"}), 403
    file = File.query.filter_by(id=id).first()
    if file is None or file.user_id != current_user.id:
        return jsonify({"Message": "You have no access to files!"})
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], current_user.username), file.filename,
                               as_attachment=True)


@app.route("/api/healthcheck")
def healthcheck():
    if os.environ.get("Secret_Flag"):
        return "Ok!"
    else:
        return "Something wrong!", 500
