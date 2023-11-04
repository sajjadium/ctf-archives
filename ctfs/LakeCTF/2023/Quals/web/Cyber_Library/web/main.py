from flask import Blueprint, abort, current_app
from flask import flash, render_template, redirect, url_for, request
from flask_cors import cross_origin
from flask_login import login_user, current_user
import os
import time
import validators
from . import admin_token, sock, limiter, q, User
from .bot import visit

ORIGINS = ["http://chall.polygl0ts.ch:9010", "http://web:8080"]

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/collection')
def collection():
    return render_template('collection.html')


@main.route('/viewer')
def viewer():
    return render_template('viewer.html', is_admin=current_user.is_authenticated)


@main.route('/submit', methods=['POST'])
@limiter.limit("2/2 minute")
def submit():
    url = request.form['url']
    if validators.url(url):
        try:
            q.enqueue(visit, url, admin_token)
            flash("Thank you, a librarian will index your document shortly.", "success")
        except Exception as e:
            print(e)
            flash("Error submitting document", "danger")
    else:
        flash("Invalid URL", "danger")
    return redirect(url_for('main.index'))


@main.route('/admin/login', methods=['GET'])
def login():
    if request.args.get('token') == admin_token:
        login_user(User('admin'))
        flash("You are now logged in.", "success")
        return redirect(url_for('main.index'))
    else:
        abort(403)


@sock.route('/ws', bp=main)
@limiter.limit("2/2 minute")
@cross_origin(origins=ORIGINS)
def ws_handler(ws):
    while True:
        try:
            ws.send(current_app.counter)
            time.sleep(5)
        except:
            break
    try:
        ws.close()
    except:
        pass


@sock.route('/admin/ws', bp=main)
@cross_origin(origins=ORIGINS)
def admin_ws_handler(ws):
    # Authenticate socket with Flask-Login
    # https://flask-socketio.readthedocs.io/en/latest/implementation_notes.html#using-flask-login-with-flask-socketio
    if current_user.is_authenticated:
        print('authenticated')
        while True:
            command = ws.receive()
            if command == 'increment':
                current_app.counter += 1
                ws.send('updated')
            elif command == 'flag':
                ws.send(os.getenv('FLAG') or 'flag{flag_not_set}')
            else:
                break
    else:
        ws.send('Not Authenticated')
    ws.close()
