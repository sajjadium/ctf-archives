
import os, queue, secrets, uuid
from random import seed, randrange


from flask import Flask, request, redirect, url_for, session, render_template, jsonify, Response
from flask_executor import Executor
from flask_jwt_extended import JWTManager
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import exifread, exiftool
from exiftool.exceptions import *
import base64, re, ast


from common.config import load_config, Config
from common.error import APIError, FileNotAllowed



conf = load_config()
work_queue = queue.Queue()

app = Flask(__name__)
executor = Executor(app)

app.config.from_object(Config)
app.jinja_env.add_extension("jinja2.ext.loopcontrols")
app.config['EXECUTOR_TYPE'] = 'thread'
app.config['EXECUTOR_MAX_WORKERS'] = 5

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


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

@app.route('/upload', methods=["GET","POST"])
def upload():
    try:
        if request.method == 'GET':
            return render_template(
            'upload.html.j2')
        elif request.method == 'POST':
            if 'file' not in request.files:
                return 'there is no file in form!'
            file = request.files['file']
            if file and allowed_file(file.filename):
                _file = file.read()
                tmpFileName = str(uuid.uuid4())
                with open("tmp/"+tmpFileName,'wb') as f:
                    f.write(_file)
                    f.close()
                    tags = exifread.process_file(file)
                    _encfile = base64.b64encode(_file)
                    try:
                        thumbnail = base64.b64encode(tags.get('JPEGThumbnail'))
                    except:
                        thumbnail = b'None'

                with exiftool.ExifToolHelper() as et:
                    metadata = et.get_metadata(["tmp/"+tmpFileName])[0]
            else:
                raise FileNotAllowed(file.filename.rsplit('.',1)[1])

        os.remove("tmp/"+tmpFileName)
        return render_template(
            'uploaded.html.j2', tags=metadata, image=_encfile.decode() , thumbnail=thumbnail.decode()), 200
    except FileNotAllowed as e:
        return jsonify({
                "error": APIError("FileNotAllowed Error Occur", str(e)).__dict__,
        }), 400
    except ExifToolJSONInvalidError as e:
        os.remove("tmp/"+tmpFileName)
        data = e.stdout
        reg = re.findall('\[(.*?)\]',data, re.S )[0]
        metadata = ast.literal_eval(reg)
        if 0 != len(metadata):
            return render_template(
            'uploaded.html.j2', tags=metadata, image=_encfile.decode() , thumbnail=thumbnail.decode()), 200
        else:
            return jsonify({
                "error": APIError("ExifToolJSONInvalidError Error Occur", str(e)).__dict__,
        }), 400
    except ExifToolException as e:
        os.remove("tmp/"+tmpFileName)
        return jsonify({
                "error": APIError("ExifToolException Error Occur", str(e)).__dict__,
        }), 400
    except IndexError as e:
        return jsonify({
                "error": APIError("File extension could not found.", str(e)).__dict__,
        }), 400
    except Exception as e:
        os.remove("tmp/"+tmpFileName)
        return jsonify({
                "error": APIError("Unknown Error Occur", str(e)).__dict__,
        }), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')
