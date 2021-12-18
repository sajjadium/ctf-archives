#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
from flask_hcaptcha import hCaptcha
import uuid
import os

ADMIN_COOKIE = os.environ.get('FLAG', 'X-MAS{test}')

app = Flask (__name__)

images = [{'url': img_url, 'desc': 'meme'} for img_url in open("images.txt", "r").read().strip().split("\n")]

pending_images = {} # id: image obj

@app.route ('/', methods = ['GET'])
def index():
    return render_template ("index.html", images=images)


@app.route ('/submit', methods = ['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template ("submit.html")

    image_url = request.form.get('url')
    image_desc = request.form.get('desc')
    if not isinstance(image_url, str) or not isinstance(image_desc, str) or len(image_url) > 256 or len(image_url) < 8:
        return 'NOPE'

    if len(image_desc) > 164 or len(image_desc) < 4:
        return 'NOPE'

    blacklist = ['src', '"', "'", '+', '\\', '[', ']', '-']
    for blacklist_thing in blacklist:
        if blacklist_thing in image_desc.lower():
            return 'NOPE'

    if 'script' in image_desc or 'nonce' in image_desc:
        return 'NOPE (according to our latest security audit)'

    image_id = str(uuid.uuid4())
    image_obj = { 'url': image_url, 'desc': image_desc }
    pending_images[image_id] = image_obj
    return render_template ("submit.html", message=f"Image {image_id} submitted successfully.")


@app.route ('/list', methods = ['GET'])
def list():
    if request.cookies.get('admin_cookie', False) != ADMIN_COOKIE:
        return 'NOPE'
    return render_template ("list.html", image_ids=[_ for _ in pending_images.keys()])


@app.route ('/api/unapproved/<image_id>', methods = ['GET'])
def unapprovedImage(image_id):
    return pending_images.pop(image_id)


@app.route ('/image/<image_id>', methods = ['GET', 'POST', 'DELETE'])
def image(image_id):
    if request.method == 'GET':
        if request.cookies.get('admin_cookie', False) != ADMIN_COOKIE or pending_images.get(image_id, False) == False:
            return 'NOPE'
        return render_template ("image_review.html", image_id=image_id, title=pending_images[image_id]['desc'])

    action = request.form.get('action')
    if not isinstance(action, str) or action not in ['APPROVE', 'REJECT']:
        return 'NOPE'

    if action == "REJECT":
        pending_images.pop(image_id)
    
    return redirect("/list", code=302)


if __name__ == '__main__':
    app.run (host = '127.0.0.1', port = 2000)
