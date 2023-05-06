

import os, queue, secrets
from random import seed, randrange
import logging.config

from flask import Flask, request, redirect, url_for, session, render_template, jsonify, Response
from flask_executor import Executor
from flask_jwt_extended import JWTManager
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException


from common.config import load_config, Config
from common.logger import set_logger
from common.error import APIError, FileNotAllowed, NullParam

from me7_ba11.meatball import MeatBall


conf = load_config()
work_queue = queue.Queue()

os.makedirs(os.path.dirname(os.path.join(os.path.dirname(__file__), "../", conf["common"]["log"]["app_log_file"])), exist_ok=True)
logging.config.dictConfig(conf["logging"])

app = Flask(__name__)
executor = Executor(app)

app.config.from_object(Config)
app.jinja_env.add_extension("jinja2.ext.loopcontrols")
app.config['EXECUTOR_TYPE'] = 'thread'
app.config['EXECUTOR_MAX_WORKERS'] = 5

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

secret = secrets.token_bytes(2048)

backup_count = conf["common"]["log"]["backupCount"]


local_config = {
    "keyForEncryption" : secret,
    }

mb = MeatBall("./meat.ball",local_config, )


@app.before_request
def before_request():
    userAgent = request.headers

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


@app.route('/')
def index():
    return render_template(
        'index.html.j2')

@app.route('/append', methods=["GET","POST"])
def append():

    try:
        if request.method == 'GET':
            return render_template(
            'append.html.j2')
        elif request.method == 'POST':
            param = request.form.to_dict()
            if param.items().__len__() != 0:
                result = mb.append(param=param)
                return jsonify(
                    result
                ), 200
            else:
                raise NullParam
    except Exception as e:
        return jsonify({
                "error": APIError("Error Occur", str(e)).__dict__
        }), 400

@app.route('/update', methods=["GET","POST"])
def update():
    try:
        if request.method == 'GET':
            return render_template(
            'update.html.j2')
        elif request.method == 'POST':
            param = request.form.to_dict()
            if param.items().__len__() != 0:
                return jsonify(
                    mb.update(param=param)
                ), 200
            else:
                raise NullParam
    except Exception as e:
        return jsonify({
                "error": APIError("Error Occur", str(e)).__dict__
        }), 400


@app.route('/get', methods=["GET"])
def get():
    param = request.args.to_dict()
    try:
        if param.get('key') == None:
            return render_template(
            'get.html.j2')
        return jsonify(
            mb.get(param)
        ), 200
    except Exception as e:
        return jsonify({
                "error": APIError("Error Occur", str(e)).__dict__
        }), 400

@app.route('/env', methods=["GET"])
def env():
    try:
        return jsonify(
            mb.get_env()
        ), 200
    except Exception as e:
        return jsonify({
                "error": APIError("Error Occur", str(e)).__dict__
        }), 400

@app.route('/upload', methods=["GET","POST"])
def upload():
    try:
        key = request.form.get('key')
        if request.method == 'GET':
            return render_template(
            'upload.html.j2')
        elif request.method == 'POST':

            if 'file' not in request.files:
                return 'there is no file in form!'
            
            file = request.files['file']

            if file and allowed_file(file.filename):
                _file = file.read()
            else:
                raise FileNotAllowed(file.filename.rsplit('.',1)[1])
            param = request.form.to_dict()

            if param.items().__len__() != 0:
                if key:
                    result = mb.update(param=param, _file=_file)
                else:
                    result = mb.append(param=param, _file=_file)
                return result
            else:
                raise NullParam
        return jsonify(
            result
        ), 200
    except Exception as e:
        return jsonify({
                "error": APIError("Error Occur", str(e)).__dict__
        }), 400

@app.route('/delete', methods=["POST"])
def delete():
    try:
        param = request.form.to_dict()
        if param.items().__len__() != 0:
            return jsonify({
                "result": mb.delete(param)
            }), 200
        else:
            raise NullParam
    except Exception as e:
        return jsonify({
                "error": APIError("Error Occur", str(e)).__dict__
        }), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')

