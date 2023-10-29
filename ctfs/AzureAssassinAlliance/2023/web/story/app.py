from flask import Flask, render_template_string, jsonify, request, session, render_template, redirect
import random
from utils.captcha import Captcha, generate_code
from utils.minic import *
app = Flask(__name__)
app.config['SECRET_KEY'] = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    username = session.get('username', '')

    if username != "" and username is not None:
        return render_template("home.html")
    return render_template('index.html')

@app.route('/captcha')
def captcha():
    gen = Captcha(200, 80)
    buf , captcha_text = gen.generate()

    session['captcha'] = captcha_text
    return buf.getvalue(), 200, {
        'Content-Type': 'image/png',
        'Content-Length': str(len(buf.getvalue()))
    }

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', '')
    captcha = request.json.get('captcha', '').upper()

    if captcha == session.get('captcha', '').upper():
        session['username'] = username
        return jsonify({'status': 'success', 'message': 'login success'})
    return jsonify({'status': 'error', 'message': 'captcha error'}), 400

@app.route('/vip', methods=['POST'])
def vip():
    captcha = generate_code()
    captcha_user = request.json.get('captcha', '')
    if captcha == captcha_user:
        session['vip'] = True
    return render_template("home.html")

@app.route('/write', methods=['POST','GET'])
def rename():
    if request.method == "GET":
        return redirect('/')
    
    story = request.json.get('story', '') 
    if session.get('vip', ''):

        if not minic_waf(story):
            session['username'] = ""
            session['vip'] = False
            return jsonify({'status': 'error', 'message': 'no way~~~'})
        
        session['story'] = story
        return jsonify({'status': 'success', 'message': 'success'})
    
    return jsonify({'status': 'error', 'message': 'Please become a VIP first.'}), 400

@app.route('/story', methods=['GET'])
def story():
    story = session.get('story','')
    if story is not None and story != "":
        tpl = open('templates/story.html', 'r').read()
        return render_template_string(tpl % story) 
    return redirect("/")       


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)