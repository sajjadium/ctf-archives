import os
import re

from uuid import uuid4

from flask import Flask, json, request, redirect, url_for, flash, render_template, jsonify
from flask_login import LoginManager, login_manager, login_required, login_user, current_user, logout_user
from redis import Redis
from sqlalchemy.exc import IntegrityError

from database import init_db
from models import User, Image, Share

app = Flask(__name__)
app.config.from_object('config.Config')

db = init_db(app)

redis = Redis(host=app.config.get('REDIS_HOST'), port=app.config.get('REDIS_PORT'), db=0, password=app.config.get('REDIS_PASSWORD'))
redis.set('queued_count', 0)
redis.set('proceeded_count', 0)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.before_first_request
def init_admin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password=app.config.get('ADMIN_PASSWORD'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()


@app.route('/')
@login_required
def index():
    images = Image.query.filter_by(owner=current_user).all()
    return render_template('index.html', images=images)


@app.after_request
def add_header(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' blob:"
    return response


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
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.verify_password(password):
                login_user(user)
                return redirect(url_for('index'))

        flash('Login failed')
        return redirect(url_for('login'))

    elif request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/image/upload', methods=['POST'])
@login_required
def upload_image():
    img_file = request.files['img_file']
    if img_file:
        ext = os.path.splitext(img_file.filename)[1]
        if ext in ['.jpg', '.png']:
            filename = uuid4().hex + ext

            img_path = os.path.join(app.config.get('UPLOAD_FOLDER'), filename)
            img_file.save(img_path)

            return jsonify({'img_url': f'/static/image/{filename}'}), 200

    return jsonify({}), 400


@app.route('/image', methods=['GET', 'POST'])
@login_required
def create_image():
    if request.method == 'POST':
        title = request.form.get('title')
        img_url = request.form.get('img_url')
        
        if title and img_url:
            if not img_url.startswith('/static/image/'):
                flash('Image creation failed')
                return redirect(url_for('create_image'))

            image = Image(title=title, url=img_url, owner=current_user)
            db.session.add(image)
            db.session.commit()
            res = redirect(url_for('index'))
            res.headers['X-ImageId'] = image.id
            return res
        return redirect(url_for('create_image'))

    elif request.method == 'GET':
        return render_template('create_image.html')


@app.route('/image/<image_id>')
@login_required
def image(image_id):
    try:
        image = Image.query.filter_by(owner=current_user, id=image_id).first()
        if image: # if my image
            return render_template('image.html', image=image)

        share = Share.query.filter_by(shared_user=current_user, image_id=image_id).first()
        if share: # if shared image
            image = Image.query.filter_by(id=image_id).one()
            return render_template('image.html', image=image, shared=True)
    except Exception as e:
        print(e)
        return ('', 404)
    return ('', 404)


PATTERN_IMG_ID = re.compile(r'^image/([0-9a-f-]{36})')

@app.route('/share', methods=['POST'])
@login_required
def share():
    share_target = User.query.filter_by(username='admin').first() # Now users can share image only with admin
    try:
        path = request.json['path']
        img_id = PATTERN_IMG_ID.match(path).groups()[0]
        image = Image.query.filter_by(owner=current_user, id=img_id).first()
        if image:
            share = Share(image=image, shared_user=share_target)
            db.session.add(share)
            db.session.commit()

            # send_notification_mail(share_target, app.config.get("BASE_URL")+path) # implement before official release
            print(f'[*] share {path}')
            redis.rpush('query', path)
            redis.incr('queued_count')

            return jsonify({'result': 'ok'}), 200
    except IntegrityError as e:
        print(e)
        return jsonify({'error': 'Already shared'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 400
    return jsonify({}), 404


if __name__ == '__main__':
    app.run('0.0.0.0')