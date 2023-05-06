from flask import Flask, render_template, request, session, redirect, jsonify
import requests
import random
import time
from binascii import hexlify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button')
def button():
    title = request.args.get('title')
    link = request.args.get('link')
    return render_template('button.html', title=title, link=link)

@app.route('/admin')
def admin():
    if (not session.get("verified")) or (not session.get("end")):
        return redirect("/pow")
    if session.get("end") < time.time():
        del session['pref']
        del session['suff']
        del session['end']
        del session['verified']
        return redirect("/pow")

    title = request.args.get('title')
    link = request.args.get('link')
    host = random.choice(["admin", "admin2", "admin3"])
    r = requests.post(f"http://{host}/xss/add", json={"title": title, "link": link}, headers={"Authorization": os.getenv("XSSBOT_SECRET")})
    return f'Nice button! The admin will take a look. Current queue position: {r.json()["position"]}'

@app.route("/pow", methods=["GET", "POST"])
def do_pow():
    if request.method == 'GET':
        import pow
        pref, suff = pow.generate()
        session['pref'], session['suff'] = pref, suff
        time.sleep(1)
        return jsonify({"pref": pref, "suff": suff})
    else:
        import pow
        difficulty = int(os.getenv("DIFFICULTY", "5"))
        pref, suff = session['pref'], session['suff']
        answer = request.json.get('answer')
        if pow.verify(pref, suff, answer, difficulty):
            session['verified'] = True
            session['end'] = time.time() + 30
            return "Thank you!"
        else:
            return "POW incorrect"

app.secret_key = hexlify(os.urandom(24))
app.run(host='0.0.0.0', port=5000)
