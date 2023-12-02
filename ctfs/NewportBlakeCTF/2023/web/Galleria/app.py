from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file and allowed_file(file.filename):
        file.seek(0, os.SEEK_END)
        if file.tell() > 1024 * 1024 * 2:
            return "File is too large", 413

        file.seek(0)
        filename = secure_filename(os.path.basename(file.filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('gallery'))


def check_file_path(path):
    _path = Path(path)

    parts = [*Path.cwd().parts][1:]
    for part in _path.parts:
        if part == '.':
            continue
        if part == '..':
            parts.pop()
        else:
            parts.append(part)

        if len(parts) == 0:
            return False

    _path = os.path.join(os.getcwd(), path)
    _path = Path(_path)
    return _path.exists() and _path.is_file()


@app.route('/gallery')
def gallery():
    if request.args.get('file'):
        filename = os.path.join('uploads', request.args.get('file'))
        if not check_file_path(filename):
            return redirect(url_for('gallery'))

        return send_file(filename)

    image_files = [f for f in os.listdir(
        app.config['UPLOAD_FOLDER'])]
    return render_template('gallery.html', images=image_files)


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
