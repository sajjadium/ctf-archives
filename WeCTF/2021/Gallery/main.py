import os
import time
import uuid
from flask import Flask, request, make_response, render_template, redirect
from google.cloud import storage

from peewee import *

db = SqliteDatabase("core.db")


class User(Model):  # mapping from user token to their background pic url
    id = AutoField()
    token = CharField()
    url = TextField()

    class Meta:
        database = db


@db.connection_context()
def initialize():
    db.create_tables([User])
    User.create(token=os.environ["ADMIN_TOKEN"], url=os.environ["FLAG_URL"])


initialize()


app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth.json"  # set up Google Cloud credentials
CLOUD_STORAGE_BUCKET = "gallery-wectf21"  # Google Cloud Storage bucket name
DEFAULT_PIC = "/static/default.gif"
CSP = "script-src 'nonce-%s'; connect-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; "


def uuid4() -> str:
    return str(uuid.uuid4())


@app.route('/')
@db.connection_context()
def index():
    token = request.cookies.get("token")  # get token from cookies
    if not token:  token = uuid4()  # user has no token, generate one for them
    nonce = uuid4()  # generate a random nonce
    user_obj = User.select().where(User.token == token)
    resp = make_response(render_template("index.html", background=user_obj[-1].url if len(user_obj) > 0 else DEFAULT_PIC,
                                         nonce=nonce))  # render the template with background & CSP nonce
    resp.set_cookie("token", token)  # set cookie to the token
    resp.headers['Content-Security-Policy'] = CSP % nonce  # wanna be safe
    resp.headers['X-Frame-Options'] = 'DENY'  # ensure no one is putting our site in iframe
    return resp


def is_bad_content_type(content_type):
    return content_type and "html" in content_type  # uploading a html picture? seriously?


@app.route('/upload', methods=['POST'])
@db.connection_context()
def upload():
    token = request.cookies.get("token")
    if not token: return redirect("/")  # no token, go to home page
    uploaded_file = request.files.get('file')  # the file uploaded by user
    if not uploaded_file:
        return 'No file uploaded.', 400  # dumbass user uploads nothing
    if is_bad_content_type(uploaded_file.content_type):
        return "Don't hack me :(", 400  # hacker uploading html
    gcs = storage.Client()  # do some Google Cloud Storage bs copied from their docs
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(uuid4() + uuid4())  # use uuid + uuid as file name
    blob.upload_from_string(uploaded_file.read(), content_type=uploaded_file.content_type)  # upload it
    # get the signed url expiring in 1000min
    url = blob.generate_signed_url(expiration=int(time.time()) + 600000)\
        .replace("https://storage.googleapis.com/gallery-wectf21/", "https://gallery-img-cdn.ctf.so/")
    User.create(token=token, url=url)
    return redirect("/")  # go back home


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8083, debug=True)
