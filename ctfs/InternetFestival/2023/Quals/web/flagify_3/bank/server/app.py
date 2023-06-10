from flask import Flask, request, redirect, session, jsonify
from flask_login import LoginManager, login_user, current_user, login_required
from db import DB, DBException
import utils
import os
import jwt
import pyotp
import requests

app = Flask(__name__)
login_manager = LoginManager(app)

app.config['SECRET_KEY'] = utils.random_string(20)
app.config['SHARED_SECRET'] = os.environ.get('SHARED_SECRET', 'segreto_segretissimo_much_segreto')
app.config['CAPTCHA_KEY'] = os.environ.get('CAPTCHA_KEY', 'ASD')

@login_manager.user_loader
def load_user(user_id):
    db = DB()
    current_user = db.get_user_from_id(user_id)
    return current_user


@app.route('/api/register', methods=['POST'])
def register_view():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({
            'error' : 'Invalid username or password'
        }), 400

    db = DB()

    if db.register(username, password):
        return jsonify({}), 201

    return jsonify({
        'error' : "Can't register, try again"
    }), 400


@app.route('/api/login', methods=['POST'])
def login_view():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({
            'error' : 'Invalid username or password'
        }), 400
    
    db = DB()

    user = db.login(username, password)

    if user:
        login_user(user)
        return jsonify({
            'status': 'Correctly logged in!'
        }), 200

    return jsonify({
        'error' : 'Invalid credentials'
    }), 400


@app.route('/api/user', methods=['GET'])
@login_required
def user_view():
    return jsonify({
        'id' : current_user.id,
        'username' : current_user.username,
        'credit' : current_user.credit,
        'totp_enabled' : current_user.totp_secret is not None
    }), 200


@app.route('/api/disable_totp', methods=['POST'])
@login_required
def disable_totp_view():
    db = DB()
    db.disable_totp(current_user.get_id())
    return jsonify({}), 200


@app.route('/api/enable_totp', methods=['POST'])
@login_required
def enable_totp_view():
    if current_user.totp_secret:
        return jsonify({
            'error' : 'TOTP already enabled'
        }), 400
    
    db = DB()

    new_totp = pyotp.random_base32()
    db.enable_totp(current_user.get_id(), new_totp)

    totp_url = pyotp.totp.TOTP(new_totp).provisioning_uri(name=current_user.username, issuer_name='web challenge from random CTF')

    return jsonify({
        'totp_url' : totp_url
    }), 201


@app.route('/api/checkout', methods=['POST'])
@login_required
def checkout_transaction():
    if not current_user.totp_secret:
        return jsonify({
            'error':'You must enable 2FA before spending'
        }), 400

    given_totp = request.form.get('totp')

    if not given_totp or given_totp != pyotp.TOTP(current_user.totp_secret).now():
        return jsonify({
            'error' : 'Invalid OTP'
        }), 400

    token = request.form.get('token')
    if not token:
        return jsonify({
            'error' : 'No transaction provided!'
        }), 400

    try:
        url, amount, transaction_id = utils.parse_token(token, app.config['SHARED_SECRET'])
    except jwt.exceptions.DecodeError:
        return jsonify({
            'error' : 'Invalid transaction'
        }), 400

    if amount > current_user.credit:
        return jsonify({
            'error' : 'Not enough money'
        }), 400

    response_data = {
        "transaction_id":transaction_id,        
    }

    db = DB()
    try:
        db.decrement_user_credit(current_user.id, amount)
        response_data['status'] = True
    except DBException:
        response_data['status'] = False

    response_token = jwt.encode(response_data, app.config['SHARED_SECRET'])

    return jsonify({
        'url' : f'{url}?token={response_token}'
    }), 200


@app.route("/api/report", methods=["POST"])
@login_required
def report_url():
    url = request.form.get("url")
    captcha = request.form.get("captcha")

    if url and captcha:
        try:
            r = requests.post(f'https://www.google.com/recaptcha/api/siteverify?secret={app.config["CAPTCHA_KEY"]}&response={captcha}')

            if not r.json().get('success'):
                return jsonify({
                    'error': 'Invalida captcha'
                }), 400

            r = requests.post("http://flagify3_bot:8080/visit", data={
                "url":url
            })

            return jsonify({
                'response' : r.text
            }), 200
        except:
            pass

    return jsonify({
        'error':'Error during requests'
    }), 400


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')