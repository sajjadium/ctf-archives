from utils import *
from flask import Flask, render_template, request,Response, session, redirect, url_for,jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
import logging
import bleach, time

app = Flask(__name__)
app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")

app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket.db'
admin_password = os.environ.get('PASSWD', uuid.uuid4().hex)
captcha_secret_key = os.environ.get('RECAPTCHA_SECRET_KEY', "")
site_key = os.environ.get('SITE_KEY', "")
csp_header_value = (
        "default-src 'self'; "
        "script-src 'self' ; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "frame-src 'none'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "manifest-src 'self'; "
        "upgrade-insecure-requests; "
        "block-all-mixed-content; "
        "require-sri-for script style; "
    )

db = SQLAlchemy(app)
ADMIN_COOKIE = ""


class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))

# Define the Ticket model


class Ticket(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    title = db.Column(db.String(100))
    new = db.Column(db.Integer)
    content = db.Column(db.Text)
    username = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


def is_valid_ticket(id, username):
    # mess = ""
    if not is_valid_uuid(id):
        return "Invalid ticket id"

    ticket = db.session.get(Ticket, id)
    if not ticket or (ticket.username != username and username != "admin"):
        return "No ticket found"

    return "OK"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = User.query.filter_by(username=username).first()
            print(user)
            if user and password == user.password:
                session['username'] = username.strip()
                # Redirect to the home page or perform other actions upon successful login
                return redirect(url_for('home'))
        return render_template('login.html', error_message='Invalid username or password.')
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        error_message= "success"
        if username and password:
            print(User.query.filter_by(username=username).first())
            if User.query.filter_by(username=username).first():
                error_message = 'Username already exists. Please choose a different username.'
                return render_template('signup.html', error_message=error_message)
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
        else:
            error_message = 'Invalid username or password.'
        return render_template('signup.html', error_message=error_message)
    else:
        return render_template('signup.html')


@app.route('/ticket', methods=['POST'])
def post_ticket():
    data = request.form
    username = session.get('username')
    if not username:
        res = "No user found"
        return render_template("home.html", error_message=res)
    title = data.get('title')[:100]
    content = (data.get('content'))
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    unique_filename = str(uuid.uuid4()) 
    file_path = os.path.join("/tmp/", unique_filename+os.path.splitext(file.filename)[1])
    file.save(file_path)
    if not data['content'] or not data['title']:
        res = "Content and Title is empty"
        return render_template("home.html", error_message=res)
    if username=="admin":
        content = "[IMPORTANT ALERT]"+ content
    else:
        content = "[NOMAL ALERT]"+ content
    content+=f"<br>Attachment: http://localhost/tmp/{unique_filename}"
    ticket = Ticket(id=unique_filename, title=title,
                    content=content, username=username,new=1)
    db.session.add(ticket)
    db.session.commit()

    return redirect(url_for(f'get_ticket', id=ticket.id))


@app.route('/ticket/<id>')
def get_ticket(id):
    username = session.get('username')
    if not username:
        res = "No user found"
        return render_template("ticket.html", error_message=res)

    if not is_valid_uuid(id):
        res = "Invalid ticket id"
        return render_template("ticket.html", error_message=res)

    ticket = db.session.get(Ticket, id)
    if not ticket or (ticket.username != username and username != "admin"):
        res = "No ticket found"
        return render_template("ticket.html", error_message=res)
    else:
        ticket.new=0;
        db.session.add(ticket)
        return render_template("ticket.html", ticket=ticket,files=f"/tmp/{id}")

@app.route('/tmp/<id>')
def get_files(id):
    if not is_valid_uuid(id):
        res = "Invalid ticket id"
        return jsonify({'error': res}), 400

    ticket = db.session.get(Ticket, id)
    if not ticket :
        res = "No ticket found"
        return jsonify({'error': res}), 400
    else:
        files = os.popen(f"cat /tmp/{id}*").read()
        return jsonify(data=files),200,{'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/report', methods=['POST', 'GET'])
def report():
    if request.method == "POST":
        username = session.get('username')
        data = request.form
        if not username:
            res = "No user found"
            return render_template("ticket.html", error_message=res)

        id = data.get("id")

        res = is_valid_ticket(id, username)
        if res != "OK":
            return render_template("ticket.html", error_message=res)

        # send request to bot worker
        
        ticket = db.session.get(Ticket, id)
        r = requests.post("http://127.0.0.1:5001/",
                          data={"id": id, "title": bleach.clean(ticket.title),"content": bleach.clean(ticket.content) })
        app.logger.info(r.text)
        time.sleep(3)
        return render_template("ticket.html", error_message=res)
    else:
        return render_template("ticket.html")

@app.route('/IsNew')
def isnew():
    client_ip = request.remote_addr
    print(client_ip)
    if client_ip:
        if client_ip == "127.0.0.1":
            id = request.args.get("id")
            res = is_valid_uuid(id)
            if res:
                ticket = db.session.get(Ticket, id)
                return render_template("admin.html",ticket=ticket),200,{"Content-Security-Policy":csp_header_value}
        return render_template("home.html")
    else:
        return redirect(url_for('login'))
@app.route('/')
def home():
    username = session.get('username')
    print(username)
    if username:
        return render_template("home.html")
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def create_admin_user():
    global admin_password
    admin_username = 'admin'
    admin_user = db.session.get(User, admin_username)
    if not admin_user:
        admin_user = User(username=admin_username, password=admin_password)
        db.session.add(admin_user)
        db.session.commit()
    else:
        admin_password = admin_user.password
        
with app.app_context():
    db.create_all()
    create_admin_user()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(debug=False, port=80, host='0.0.0.0')
