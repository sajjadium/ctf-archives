from flask import Flask, request, render_template, redirect, abort, url_for
from hashlib import md5
from utils import *

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            fnew = request.files['file']
            fbase = open("dog.jpg", "rb")

            # Check if file has been uploaded before
            if isWhitelisted(fnew):
                fid = saveFile(fnew)
                return redirect(url_for('view', fid = fid))

            # New files are checked pixel by pixel
            if compareJPG(fnew, fbase):
                whitelistAdd(fnew)
                fid = saveFile(fnew)
                return redirect(url_for('view', fid = fid))
            else:
                return abort(401)
        except:
            return abort(401)
        
@app.route('/view/<uuid:fid>', methods=['GET'])
def view(fid):
    try:
        f1 = open("cat.jpg", "rb")
        f2 = open("static/uploads/" + str(fid) + ".jpg", "rb")

        if compareJPG(f1,f2):
            flag = "FLAG{test_flag}"
            return render_template('fileview.html', fid = fid, flag = flag)
        else:
            return render_template('fileview.html', fid = fid)
    except:
        return abort(404)

@app.errorhandler(401)
def page_not_found(error):
    return render_template('dogsonly.html'), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('dogonotfound.html'), 404
