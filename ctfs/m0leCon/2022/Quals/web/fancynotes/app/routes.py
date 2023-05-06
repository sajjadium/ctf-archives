import hashlib
import os
import uuid
from flask import render_template, request, redirect, make_response, send_file
from .validators import validate_registration, validate_login, validate_note
from .models import *
from .utils import generate_cookie, get_user, save_picture
from .db import db


def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/registration', methods=['POST', 'GET'])
    def registration():
        if request.method == 'GET':
            return render_template('registration.html')
        if request.method == 'POST':
            form_data = request.form

            error = validate_registration(form_data)
            if error:
                return render_template('registration.html', error=error)

            if User.query.filter_by(username=form_data['username']).count() > 0:
                return render_template('registration.html', error='Username already taken')

            user = User(
                username=form_data['username'],
                password=form_data['password'],
                locale='en'
            )
            db.session.add(user)
            db.session.commit()

            return redirect("/login")

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        if request.method == 'POST':
            form_data = request.form

            error = validate_login(form_data)
            if error:
                return render_template('login.html', error=error)

            user = User.query.filter_by(username=form_data['username'], password=form_data['password']).first()
            if user is None:
                return render_template('login.html', error='Wrong credentials')

            response = make_response(redirect("/notes"))
            response.set_cookie('user', generate_cookie(user))
            return response

    @app.route('/logout')
    def logout():
        response = make_response(redirect("/"))
        response.delete_cookie('user')
        return response

    @app.route('/notes', methods=['POST', 'GET'])
    def notes():
        if request.method == 'GET':
            user = get_user()
            if not user:
                return redirect("/login")
            notes = Note.query.filter(
                Note.user.has(username=user['username'])
            ).all()
            return render_template('notes.html', user=user, notes=notes)
        if request.method == 'POST':
            user = get_user()
            if not user:
                return redirect("/login")

            if user['username'] == 'admin':
                return send_file('static/chao.gif', mimetype='image/gif')

            form_data = request.form

            error = validate_note(form_data)
            if error:
                notes = Note.query.filter(Note.user.has(
                    username=user['username']
                )).all()
                return render_template('notes.html', user=user, notes=notes, error=error)

            picture_id = None
            if 'picture' in request.files:
                picture_id = save_picture(request.files['picture'])

            note = Note(
                title=form_data['title'], body=form_data['body'], picture_id=picture_id)
            userobj = User.query.filter_by(username=user['username']).first()
            userobj.notes.append(note)
            db.session.commit()

            return render_template('notes.html', user=user, notes=userobj.notes)

    @app.route('/pictures/<id>')
    def pictures(id):
        user = get_user()
        if not user:
            return redirect("/login")

        note = Note.query.filter(Note.user.has(
            username=user['username'])).filter_by(id=id).first()
        if not note:
            return make_response("nope", 404)

        return send_file(os.path.join('/tmp/uploads', note.picture_id))
