import os
from flask import Flask, flash, request, redirect, render_template, send_file
import io
import random
from Crypto.Util.number import long_to_bytes as l2b

app=Flask(__name__, template_folder='./template')

app.secret_key = "OFCOURSETHISISNOTHEREALSECRETKEYBOI"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def xor(a, b):
    return b''.join([bytes([_a ^ _b]) for _a, _b in zip(a, b)])

def encropt(buff):
    rand = random.getrandbits(len(buff)*8)
    return xor(buff, l2b(rand))


@app.route('/', methods=['GET'])
def upload_form():
    return render_template('./upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            buff = io.BytesIO()
            buff.write(encropt(file.read()))
            buff.seek(0)
            return send_file(
                buff,
                mimetype="text/plain",
                as_attachment=True,
                download_name='lalalalululu')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

@app.route('/flago', methods=['GET'])
def send_flago():
    flago = open('./flago/flago.jpg', 'rb')
    buff = io.BytesIO()
    buff.write(encropt(flago.read()))
    buff.seek(0)
    return send_file(
        buff,
        mimetype="text/plain",
        as_attachment=True,
        download_name='babababububu')

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 5000, debug = False)