from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, send_from_directory
import sqlite3
import os
import uuid
import re
from waitress import serve


app = Flask(__name__)
app.secret_key = os.environ['secret_key']
app.config['TEMPLATES_AUTO_RELOAD'] = True
con = sqlite3.connect("user.db", check_same_thread=False)
con.set_trace_callback(print)
cur = con.cursor()
UPLOAD_FOLDER = './templates/static'
ALLOWED_EXTENSIONS = {'gif', 'jpg', 'jpeg', 'png', 'svg'}


def get_fileext(filename):
    fileext = filename.rsplit('.', 1)[1].lower()
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return fileext
    return None

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'usersess' in session:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return render_template('profile.html', error='No file selected')
            file = request.files['file']
            # If the user does not select a file, the browser submits an empty file without a filename.
            if file.filename == '':
                return render_template('profile.html', error='No file selected')
            fileext = get_fileext(file.filename)
            file.seek(0, 2) # seeks the end of the file
            filesize = file.tell() # tell at which byte we are
            file.seek(0, 0) # go back to the beginning of the file
            if fileext and filesize < 1*1024*1024:
                filename = session["usersess"]+"."+fileext
                if session['filename']:
                    os.remove(UPLOAD_FOLDER+"/"+session['filename'])
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                session['filename'] = filename
                return redirect(url_for('profile'))
        return redirect(url_for('profile'))
    else:
        return(redirect(url_for('login')))
        
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pattern = r'[^a-zA-Z0-9{_}]'
        if re.search(pattern, username) or re.search(pattern, password):
            return render_template('login.html', error='Sus input detected!')
        
        query = f'SELECT * FROM users WHERE dXNlcm5hbWVpbmJhc2U2NA = "{username}" AND cGFzc3dvcmRpbmJhc2U2NA = "{password}";'
        try:
            if cur.execute(query).fetchone():
                session['usersess'] = str(uuid.uuid4())
                session['filename'] = None
                return redirect(url_for('profile'))
            else:
                raise Exception('Invalid Credentials. Please try again.')
        except:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/profile')
def profile():
    if 'usersess' in session:
        filename = session['filename']
        if not filename:
            return render_template('profile.html')
        else:
            return render_template('profile.html', file_link="./uploads/"+filename)
    else:
        return redirect(url_for('login'))

@app.route('/uploads/<path:path>')
def viewfile(path):
    if session['filename'] == path:
        try:
            return render_template('static'+'/'+path)
        except:
            return send_from_directory(UPLOAD_FOLDER, path)

    else:
        return redirect(url_for('profile'))

if __name__ == '__main__':
	serve(app, host='0.0.0.0', port=5000)
