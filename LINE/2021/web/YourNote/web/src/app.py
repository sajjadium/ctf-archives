from flask import Flask, flash, redirect, url_for, render_template, request, jsonify, send_file, Response, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy import or_

import json
import os
import secrets
import requests

from database import init_db, db
from models import User, Note, NoteSchema

app = Flask(__name__)
if os.getenv('APP_ENV') == 'PROD':
    app.config.from_object('config.ProdConfig')
else:
    app.config.from_object('config.DevConfig')

init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect(app)

Session(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login', redirect=request.full_path))


@app.before_first_request
def insert_initial_data():
    try:
        admin = User(
            username='admin',
            password=app.config.get('ADMIN_PASSWORD')
        )
        db.session.add(admin)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return

    admin_note = Note(
        title='Hello world',
        content=('Lorem ipsum dolor sit amet, consectetur '
        'adipiscing elit, sed do eiusmod tempor incididunt...'),
        owner=admin
    )
    db.session.add(admin_note)

    admin_note = Note(
        title='flag',
        content=app.config.get('FLAG'),
        owner=admin
    )
    db.session.add(admin_note)
    db.session.commit()


@app.route('/')
@login_required
def index():
    notes = Note.query.filter_by(owner=current_user).all()
    return render_template('index.html', notes=notes)


@app.route('/search')
@login_required
def search():
    q = request.args.get('q')
    download = request.args.get('download') is not None
    if q:
        notes = Note.query.filter_by(owner=current_user).filter(or_(Note.title.like(f'%{q}%'), Note.content.like(f'%{q}%'))).all()
        if notes and download:
            return Response(json.dumps(NoteSchema(many=True).dump(notes)), headers={'Content-disposition': 'attachment;filename=result.json'})
    else:
        return redirect(url_for('index'))
    return render_template('index.html', notes=notes, is_search=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists.')
                return redirect(url_for('register'))
            user = User(
                username=username,
                password=password
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        
        flash('Registeration failed')
        return redirect(url_for('register'))

    elif request.method == 'GET':
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    url = request.args.get('redirect')
    if url:
        url = app.config.get('BASE_URL') + url
        if current_user.is_authenticated:
            return redirect(url)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.verify_password(password):
                login_user(user)
                if url:
                    return redirect(url)
                return redirect(url_for('index'))

        flash('Login failed')
        return redirect(url_for('login'))

    elif request.method == 'GET':    
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/note', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        try:
            if title and content:
                note = Note(
                    title=title,
                    content=content,
                    owner=current_user
                )
                db.session.add(note)
                db.session.commit()
                return redirect(url_for('note', note_id=note.id))
        except DataError:
            flash('Note creation failed')
        return redirect(url_for('create_note'))
        
    elif request.method == 'GET':
        return render_template('create_note.html')


@app.route('/note/<note_id>')
@login_required
def note(note_id):
    try:
        note = Note.query.filter_by(owner=current_user, id=note_id).one()
    except NoResultFound:
        flash('Note not found')
        return render_template('note.html')
    
    return render_template('note.html', note=note)


@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        url = request.form.get('url')
        proof = request.form.get('proof')
        if url and proof:
            res = requests.get(
                app.config.get('CRAWLER_URL'),
                params={
                    'url': url,
                    'proof': proof,
                    'prefix': session.pop('pow_prefix')
                }
            )
            prefix = secrets.token_hex(16)
            session['pow_prefix'] = prefix
            return render_template('report.html', pow_prefix=prefix, pow_complexity=app.config.get('POW_COMPLEXITY'), msg=res.json()['msg'])
        else:
            return redirect('report')
    elif request.method == 'GET':
        prefix = secrets.token_hex(16)
        session['pow_prefix'] = prefix
        return render_template('report.html', pow_prefix=prefix, pow_complexity=app.config.get('POW_COMPLEXITY'))


if __name__ == '__main__':
    app.run('0.0.0.0')