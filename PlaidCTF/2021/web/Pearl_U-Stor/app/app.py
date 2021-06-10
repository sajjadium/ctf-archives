from flask import Flask, render_template, url_for, request, send_from_directory, send_file, make_response, abort, redirect
from forms import AppFileForm
import os
from io import BytesIO
from werkzeug.utils import secure_filename
from subprocess import Popen
import uuid
import sys
from paste.translogger import TransLogger
import waitress
import time
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TMP_FOLDER'] = '/tmp'
app.config['RECAPTCHA_DATA_ATTRS'] = {'bind': 'recaptcha-submit', 'callback': 'onSubmitCallback', 'size': 'invisible'}
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get("APP_RECAPTCHA_PUBLIC_KEY")
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get("APP_RECAPTCHA_PRIVATE_KEY")
csrf = CSRFProtect(app)

def get_cookie(cookies):
    if 'id' in cookies:
        cookie_id = cookies.get('id')

        if cookie_id.strip() != '' and os.path.exists(os.path.join(app.config['TMP_FOLDER'], cookie_id)):
            return (False, cookie_id)

    cookie_id = uuid.uuid4().hex
    os.mkdir(os.path.join(app.config['TMP_FOLDER'], cookie_id))
    return (True,cookie_id)


@app.route('/', methods=["GET", "POST"])
def index():
    (set_cookie, cookie_id) = get_cookie(request.cookies)

    form = AppFileForm()
    if request.method == "GET":
        try:
            file_list = os.listdir(os.path.join(app.config['TMP_FOLDER'], cookie_id))
        except PermissionError:
            abort(404, description="Nothing here.")
        resp = make_response(render_template("index.html", form=form, files=file_list))
    elif request.method == "POST":
        errors = []
        if form.validate_on_submit():            
            myfile = request.files["myfile"]

            file_path = os.path.join(app.config['TMP_FOLDER'], secure_filename(cookie_id), secure_filename(myfile.filename))
            if os.path.exists(file_path):
                errors.append("File already exists.")
            elif secure_filename(cookie_id) == '':
                errors.append("Cannot store file.")
            else:
                try:
                    myfile.save(file_path)
                    cmd = ["chattr", "+r", file_path]
                    proc = Popen(cmd, stdin=None, stderr=None, close_fds=True)
                except:
                    errors.append("Cannot store file.")

        try:
            file_list = os.listdir(os.path.join(app.config['TMP_FOLDER'], cookie_id))
        except PermissionError:
            abort(404, description="Nothing here.")
        resp = make_response(render_template("index.html", form=form, files=file_list, errors=errors))

    if set_cookie:
        resp.set_cookie('id', cookie_id)
    return resp


@app.route('/file/<path:filename>')
def get_file(filename):
    (set_cookie, cookie_id) = get_cookie(request.cookies)
    filename = secure_filename(filename)

    if set_cookie:
        abort(404, description="Nothing here.")

    if not os.path.exists(os.path.join(app.config['TMP_FOLDER'], secure_filename(cookie_id), filename)):
        abort(404, description="Nothing here.")

    with open(os.path.join(app.config['TMP_FOLDER'], secure_filename(cookie_id), filename), "rb") as f:
        memory_file = f.read()
    return send_file(BytesIO(memory_file), attachment_filename=filename, as_attachment=True)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", message=error)

class AppLogger(TransLogger):
    def write_log(self, environ, method, req_uri, start, status, bytes):
        if method == 'POST' and 'myfile' in environ['werkzeug.request'].files:
            filename = environ['werkzeug.request'].files["myfile"].filename
        else:
            filename = ''

        if bytes is None:
            bytes = '-'
        remote_addr = '-'
        if environ.get('HTTP_X_FORWARDED_FOR'):
            remote_addr = environ['HTTP_X_FORWARDED_FOR']
        elif environ.get('REMOTE_ADDR'):
            remote_addr = environ['REMOTE_ADDR']
        d = {
            'REMOTE_ADDR': remote_addr,
            'REMOTE_USER': environ.get('REMOTE_USER') or '-',
            'REQUEST_METHOD': method,
            'REQUEST_URI': req_uri,
            'HTTP_VERSION': environ.get('SERVER_PROTOCOL'),
            'time': time.strftime('%d/%b/%Y:%H:%M:%S', start),
            'status': status.split(None, 1)[0],
            'bytes': bytes,
            'HTTP_REFERER': environ.get('HTTP_REFERER', '-'),
            'HTTP_USER_AGENT': environ.get('HTTP_USER_AGENT', '-'),
            'ID': environ['werkzeug.request'].cookies['id'] if 'id' in environ['werkzeug.request'].cookies else '',
            'FILENAME': filename
            }
        message = self.format % d
        self.logger.log(self.logging_level, message)

if __name__ == "__main__":
    format_logger = ('%(REMOTE_ADDR)s - %(REMOTE_USER)s [%(time)s] '
            '"%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" '
            '%(status)s %(bytes)s "%(ID)s" "%(FILENAME)s"')
    waitress.serve(AppLogger(app, format=format_logger), listen="*:8000")