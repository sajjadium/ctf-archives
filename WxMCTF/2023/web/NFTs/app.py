from flask import Flask, request, render_template, redirect, flash, make_response
from flask import send_from_directory
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file.save(os.path.join("./nfts/", file.filename))
            return redirect(request.url)

    return render_template('index.html')

@app.route('/nfts')
def browse_nfts():
    nfts = os.listdir("nfts")
    return render_template('nfts.html', nfts=nfts)

@app.route('/nft/<name>')
def send_nft(name):
    return send_from_directory("nfts", name, mimetype="application/octet-stream", as_attachment=True)