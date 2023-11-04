import json
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_talisman import Talisman
import os
from PIL import Image
import random
import re
from string import ascii_lowercase
from pymongo import MongoClient
import requests
from hashlib import md5
from io import BytesIO

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')

Image.MAX_IMAGE_PIXELS = 1000000  # 1MP

db = MongoClient(MONGO_HOST, 27017).absurdres

app = Flask(__name__, static_url_path='/assets')
static_dir = app.root_path + '/static'
Talisman(app, force_https=False, content_security_policy={
         'script-src': "'self'"}, content_security_policy_nonce_in=['script-src'])


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html.jinja')


@app.route('/post', methods=['POST'])
def post_post():
    title = request.form.get('title')
    body = request.form.get('body')
    if title is None or body is None:
        return 'no title or body', 400

    post_id = ''.join(random.choice(ascii_lowercase) for _ in range(16))
    db.posts.insert_one({
        'post_id': post_id,
        'title': title,
        'body': body,
    })
    return redirect(url_for('get_post', post_id=post_id))


@app.route('/image', methods=['POST'])
def post_image():
    image = request.files.get('image')
    if image is None:
        return 'no image', 400

    filename, *_, extension = os.path.basename(image.filename).split('.')
    if any(c not in ascii_lowercase for c in filename):
        return 'invalid filename', 400

    image_data = image.read()
    image_x2 = Image.open(BytesIO(image_data))
    image_x1 = image_x2.resize((image_x2.width // 2, image_x2.height // 2))

    image_id = md5(image_data).hexdigest()

    db.images.insert_one({
        'image_id': image_id,
        'files': [
            {
                'path': f'images/{filename}.x2.{extension}',
                'title': image.filename,
                'zoom': 2,
            },
            {
                'path': f'images/{filename}.x1.{extension}',
                'title': image.filename,
                'zoom': None,
            },
        ],
    })

    image_x1.save(f'{static_dir}/images/{filename}.x1.{extension}')
    image_x2.save(f'{static_dir}/images/{filename}.x2.{extension}')

    return redirect(url_for('get_image', image_id=image_id))


@app.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = db.posts.find_one({'post_id': post_id})
    return render_template('post.html.jinja', title=post['title'], body=post['body'])


@app.route('/images/<image_id>', methods=['GET'])
def get_image(image_id):
    image = db.images.find_one({'image_id': image_id})
    return render_template('image.html.jinja', img=get_img('', image_id), image_id=image_id, files=image['files'])


@app.route('/report', methods=['POST'])
def post_report():
    url = request.form.get('url')
    assert(url.startswith('http://') or url.startswith('https://'), 'invalid url')

    req = requests.post('http://reporter:8080/report', json={'url': url})
    return make_response(req.text, req.status_code)


@app.template_filter('json')
def json_filter(dttm):
    return json.dumps(dttm, ensure_ascii=False)


def get_img_srcset(file):
    if file['zoom'] is not None:
        return f'/assets/{file["path"]} {file["zoom"]}x'
    return f'/assets/{file["path"]}'


def get_img(alt, image_id):
    if request.path.startswith('/images/'):
        image_id = request.path.split('/')[-1]

    image = db.images.find_one({'image_id': image_id})
    if image is None:
        return ''

    srcset = ', '.join(get_img_srcset(file) for file in image['files'])
    return f'<img srcset="{srcset}" alt="{alt}">'


def replace_img(match):
    return get_img(match.group(1).decode(), match.group(2).decode()).encode()


@app.after_request
def after_request(response):
    response.direct_passthrough = False

    data = response.get_data()
    response.data = re.sub(b'!\\[(.*?)\\]\\((.+?)\\)', replace_img, data)

    return response
