from flask import Flask, send_from_directory, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import logging, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['FILES_FOLDER'] = '/tmp/app'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

logging.basicConfig(filename='/tmp/app/app.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["120/minute"]
)


@app.route('/')
def index():
    app.logger.info('Home page accessed')
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['FILES_FOLDER'], filename))
            return redirect('/')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/get_file/<path:name>')
def get_file(name):
    return send_from_directory(app.config['FILES_FOLDER'], name, as_attachment=True)


@app.errorhandler(429)
def ratelimit_handler(e):
    return 'If you keep that request rate, you will are only contributing the climate change. Respect <a href=\"https://www.youtube.com/watch?v=0YPC6sfgj2I\">our environment</a> and find smarter solutions'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

