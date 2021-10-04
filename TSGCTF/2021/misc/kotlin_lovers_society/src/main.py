from flask import Flask, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
import datetime
import uuid
from PIL import Image
import numpy as np
import io
import os

max_file_size = 3760

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * max_file_size

ref = np.array(Image.open(f'static/kls_symbol.png'))
# Reminder: submit your file on our remote server to get the flag
flag = os.environ.get('FLAG', 'CTF{Fake_flag_Dont_submit}')
prod = 'KLS_PROD' in os.environ


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    f = request.files['file']
    payload = f.read()

    try:
        f = io.BytesIO(payload)
        got = np.array(Image.open(f, formats=['SGI']))
    except:
        return render_template('index.html', error='Your file is corrupted')
    if not np.array_equal(ref, got):
        return render_template('index.html', error='Your file is wrong')
    if len(payload) > max_file_size:
        return render_template('index.html', error='Your file is too large')

    if prod:
        now = datetime.datetime.now().strftime('%m-%d-%H_%M_%S')
        uid = str(uuid.uuid4())
        with open(f'submissions/{now}-{uid}.sgi', 'wb+') as f:
            f.write(payload)
    return render_template('index.html', flag=flag)


@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def app_handle_413(_):
    return render_template('index.html', error='Your file is toooo large')


if __name__ == '__main__':
    app.run(debug=True)
