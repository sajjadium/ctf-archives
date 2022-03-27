import http
import re
import secrets
import string
from base64 import b64encode
from urllib.parse import urljoin

from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required, logout_user, login_user, current_user, LoginManager
from redis.client import Redis

from database import db
from models import User, Note

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
with app.app_context():
    db.create_all()

redis = Redis(host=app.config.get('REDIS_HOST'),
              port=app.config.get('REDIS_PORT'),
              db=0,
              password=app.config.get('REDIS_PASSWORD'))

login_manager = LoginManager()
login_manager.init_app(app)

limiter = Limiter(app,
                  key_func=get_remote_address,
                  storage_uri=f'redis://{app.config.get("REDIS_HOST")}:{app.config.get("REDIS_PORT")}')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
        jsonify(
            error=str(e),
            method=request.method,
            path=request.path,
            remote_addr=get_remote_address()
        ), 429)


@app.before_first_request
def init_admin():
    if not User.query.filter_by(user_id=app.config.get('ADMIN_USERNAME')).first():
        admin = User(
            user_id=app.config.get('ADMIN_USER_ID'),
            display_name=app.config.get('ADMIN_USERNAME'),
            password=app.config.get('ADMIN_PASSWORD'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()


@app.route('/', methods=['GET'])
@login_required
def index():
    notes = Note.query.filter_by(author=current_user).all()
    ctx = {
        'csp_nonce': b64encode(secrets.token_bytes(20)).decode(),
        'notes': [
            {
                'id': str(n.id),
                'title': n.title,
                'content': n.content,
                'createdAt': n.created_at.isoformat()
            } for n in notes
        ]
    }
    return render_template('index.j2', **ctx)


@app.route('/register', methods=['GET', 'POST'])
def register():
    match request.method:
        case 'GET':
            if current_user.is_authenticated:
                return redirect(url_for('login'))
            return render_template('register.j2')

        case 'POST':
            req_user_id = request.form.get('user_id')
            req_display_name = request.form.get('display_name')
            req_password = request.form.get('password')

            if not req_user_id or not req_display_name or not req_password:
                flash('there is blank field', category='danger')
                return redirect(url_for('register'))

            if not re.match(app.config.get('USER_ID_PATTERN'), req_user_id):
                flash('invalid user id', category='danger')
                return redirect(url_for('register'))

            if len(req_display_name) > app.config.get('USER_DISPLAY_NAME_MAX_LENGTH'):
                flash('invalid display name', category='danger')
                return redirect(url_for('register'))

            try:
                if User.query.filter_by(user_id=req_user_id).first():
                    flash('specified user id already exists', category='danger')
                    return redirect(url_for('register'))

                new_user = User(
                    user_id=req_user_id,
                    display_name=req_display_name,
                    password=req_password
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            except Exception:
                flash('registration failed', category='danger')
                return redirect(url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    match request.method:
        case 'GET':
            if current_user.is_authenticated:
                return redirect(url_for('index'))
            return render_template('login.j2')

        case 'POST':
            req_user_id = request.form.get('user_id')
            req_password = request.form.get('password')

            if req_user_id and req_password:
                user = User.query.filter_by(user_id=req_user_id).first()
                if user and user.verify_password(req_password):
                    login_user(user)
                    return redirect(url_for('index'))

            flash('Login failed', category='danger')
            return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    match request.method:
        case 'GET':
            return render_template('profile.j2')
        case 'POST':
            req_display_name = request.form.get('display_name')

            if not req_display_name:
                flash('there is blank field', category='danger')
                return redirect(url_for('profile'))

            if len(req_display_name) > app.config.get('USER_DISPLAY_NAME_MAX_LENGTH'):
                flash('invalid display name', category='danger')
                return redirect(url_for('profile'))

            try:
                updating_user = User.query.get(current_user.id)
                updating_user.display_name = req_display_name
                db.session.commit()
                flash("update your profile successfully", category='success')
                return redirect(url_for('profile'))
            except Exception as e:
                flash('update failed' + str(e), category='danger')
                return redirect(url_for('profile'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/note', methods=['POST'])
def note():
    req_title = request.form.get('title')
    req_content = request.form.get('content')

    if not req_title or not req_content:
        flash('title or content is blank', category='danger')
        return redirect(url_for('index'))

    if len(req_title) > app.config.get('NOTE_TITLE_MAX_LENGTH'):
        flash(f'too long title (max length: {app.config.get("NOTE_TITLE_MAX_LENGTH")})', category='danger')
        return redirect(url_for('index'))

    if len(req_content) > app.config.get('NOTE_CONTENT_MAX_LENGTH'):
        flash(f'too long content (max length: {app.config.get("NOTE_CONTENT_MAX_LENGTH")})', category='danger')
        return redirect(url_for('index'))

    new_note = Note(
        title=req_title,
        content=req_content,
        author=current_user
    )
    db.session.add(new_note)
    db.session.commit()

    flash('added new note successfully', category='success')
    return redirect(url_for('index'))


@app.route('/plzcheckit', methods=['GET'])
@limiter.limit("1 per 15 seconds")
@login_required
def share():
    try:
        share_key = ''.join([secrets.choice(string.ascii_letters + string.digits) for _ in range(app.config.get('SHARE_ID_LENGTH'))])
        redis.rpush('query', urljoin(app.config.get('BASE_URL'), f'/shared/{share_key}'))
        redis.setnx(share_key, current_user.id)
        flash(f'admin will check your notes shortly, please wait! (waiting={redis.llen("query")}, shareKey={share_key[:16]}...)', category='success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e), category='danger')
        return redirect(url_for('index'))


@app.route('/shared/<share_key>')
@login_required
def published_note(share_key):
    if not current_user.is_admin:
        return 'you are not admin', http.HTTPStatus.UNAUTHORIZED

    author_id = redis.get(share_key)
    if not author_id:
        return 'specified key is not found', http.HTTPStatus.NOT_FOUND

    author = User.query.get(int(author_id))
    notes = Note.query.filter_by(author_id=int(author_id)).all()
    ctx = {
        'shared_user_id': author.user_id,
        'shared_user_name': author.display_name,
        'csp_nonce': b64encode(secrets.token_bytes(20)).decode(),
        'notes': [
            {
                'id': str(n.id),
                'title': n.title,
                'content': n.content,
                'createdAt': n.created_at.isoformat()
            } for n in notes
        ]
    }
    return render_template('index.j2', **ctx)


if __name__ == '__main__':
    app.run(debug=True)
