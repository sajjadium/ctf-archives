# from ducnt && khanghh import <3. GLHF everyone
import uuid
import json
import time
import logging
import hashlib
import string
import pycurl
import random
import string

from web3 import Web3
from flask import Flask, render_template, json, request, redirect, session, jsonify, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse
from io import BytesIO
from contextlib import closing
from flask_session import Session

mysql = MySQL()
app = Flask(__name__)

app.secret_key = '#####CENSORED#####'
app.config['MYSQL_DATABASE_USER'] = 'TetCTFToken'
app.config['MYSQL_DATABASE_PASSWORD'] = '#####CENSORED#####'
app.config['MYSQL_DATABASE_DB'] = 'TetCTFToken'
app.config['MYSQL_DATABASE_HOST'] = "TetCTFTokenDatabase"
app.config["WAFWTF"] = ["..","../","./","union","select","from","where","ftp","ssh","redis","mysql","smtp","file","mail","curl","flag"]
app.config["STRING_ONLY"] = string.ascii_letters
app.config["SECRET_KEY"] = "#####CENSORED#####"
app.config["LIST_USERNAME_BY_DEAULT"] = ["admin","ducnt","khanghh"]

app.config["RPC_URL"] = "https://bsc-testnet.public.blastapi.io"
app.config["FLAGSTORE_ADDRESS"] = "#####CENSORED#####"
app.config["FLAGSTORE_ABI"] = """[{ "inputs": [ { "internalType": "string", "name": "", "type": "string" } ], "name": "flagClaimed", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" }]"""

mysql.init_app(app)

@app.route('/')
def main():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        return render_template('index.html')

@app.route('/showBuyFlag', methods=['GET', 'POST'])
def showBuyFlag():
    if session.get('user'):

        global _pow2
        _pow2 = proof_that_tony_stark_has_a_heart()

        return render_template('buyflag.html',pow=_pow2)
    else:
        return render_template('index.html')


@app.route('/showDashboard')
def showDashboard():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        return render_template('signin.html')

@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        return render_template('signin.html')


@app.route('/showSignUp')
def showSignUp():

    global _pow3
    _pow3 = proof_that_tony_stark_has_a_heart()

    return render_template('signup.html',pow=_pow3)


@app.route('/showforgotpassword')
def showForgotPassword():
    global _pow
    _pow = proof_that_tony_stark_has_a_heart()
    return render_template('forgotpassword.html', pow=_pow)


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')



@app.route('/secret-token/<Type>',methods=['GET'])
def gen_token(Type):
    return Type

@app.route('/trigger-reset-passwd-with-username/<string:_username>',methods=['GET'])
def userType(_username):

    try:

        _pow_from_player = request.args['inputPoW']

        if verify_pow(_pow,str(_pow_from_player)):
            for _check in app.config["LIST_USERNAME_BY_DEAULT"]:
                if _check in _username:
                    return render_template('error.html',error = "Permission Denied !!!")
            _secret_token = str(uuid.uuid4())

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_secret_token)
            cursor.callproc('sp_ResetPasswdUser',(_username, _hashed_password))
            data = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()

            _secret_reset_passwd_URL = url_for('gen_token',Type = _secret_token, _external=True)

            for _WAF_WTF in app.config["WAFWTF"]:
                if _WAF_WTF in _secret_reset_passwd_URL:
                    return render_template('error.html',error = 'Oops, Not Today !!!')

            _trigger_send_url = parse(_secret_reset_passwd_URL)

            return render_template('notification.html', noti = "Reset Passwd Successfully. If Your User Exist, Check it out !!!")


        else:
            return render_template('error.html',error = "Something go wrong homie !")

    except Exception as e:
        return render_template('error.html',error = "Something go wrong homie !")

        
#PoW BTW
def proof_that_tony_stark_has_a_heart():
    return str(uuid.uuid4())[:5]

def verify_pow(_pow, _result):
    if hashlib.md5(_result.encode('utf-8')).hexdigest()[:5] == str(_pow):
        return True
    else:
        return False

def parse(_url):
    try:
        _obj = BytesIO()
        crl = pycurl.Curl()
        crl.setopt(crl.URL, _url)
        crl.setopt(crl.WRITEDATA, _obj)
        crl.setopt(pycurl.TIMEOUT, 10)
        try:
            crl.perform()
        except Exception as e:
            crl.close()
            return render_template('error.html',error = "Something go wrong homie !")
        crl.close()
        return True
    except Exception as e:
        return render_template('error.html',error = "Something go wrong homie !")


def isFlagClaimed(_addr):
    try:
        w3 = Web3(Web3.HTTPProvider(app.config["RPC_URL"]))
        flagStore = w3.eth.contract(address=app.config["FLAGSTORE_ADDRESS"], abi=app.config["FLAGSTORE_ABI"])

        return flagStore.functions.flagClaimed(_addr).call()

    except Exception as e:
        return render_template('error.html',error = "Something go wrong homie !")


def check_FlagClaimable_on_smartcontract(_username):
    try:
        
        isClaimed = isFlagClaimed(str(_username))
        return isClaimed

    except Exception as e:
        return render_template('error.html',error = "Something go wrong homie !")


@app.route('/signUp',methods=['POST'])
def signUp():
    try:

        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _pow_from_player = request.form['inputPoW']

         #we are in the private token sale phase so you cannot login ATM
        _password = str(uuid.uuid4())

        if verify_pow(_pow3, _pow_from_player):
            if _name and _email and _password:

                conn = mysql.connect()
                cursor = conn.cursor()       
                _hashed_password = generate_password_hash(_password)
                cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
                data = cursor.fetchall()
                conn.commit()
                cursor.close()
                conn.close()

                return render_template('notification.html', noti = "Register Successfully. For the privacy of our customers, We cannot tell you that the user exists or not. Also, We are in the private token sale phase so you cannot login ATM.")
            else:
                return render_template('error.html', error='Enter the required fields homie')

        return render_template('error.html',error = "Something go wrong homie !")

    except Exception as e:

        return render_template('error.html',error = "Something go wrong homie !")

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        cursor.close()
        con.close()
        
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]

                return redirect('/showDashboard')
            else:
                return render_template('error.html',error = 'Wrong Email Address or Password !!!')


        else:
            return render_template('error.html',error = 'Wrong Email Address or Password !!!')
    except Exception as e:
        return render_template('error.html',error = "Something go wrong homie !")

#save the best for last homie
@app.route('/buyflag',methods=['POST','GET'])
def buyflag():
    try:
        if session.get('user'):

            _user_id = int(session.get('user'))

            for _WAF_WTF in app.config["WAFWTF"]:
                if _WAF_WTF in str(_user_id):
                    return render_template('error.html',error = 'Oops, Not Today !!!')
            _pow_from_player = request.form['inputPoW']

            connn = mysql.connect()
            cursor2 = connn.cursor()
            cursor2.callproc('sp_getUsername',(_user_id,))
            data = cursor2.fetchall()
            cursor2.close()
            connn.close()

            _current_username = data[0][0]

            if verify_pow(_pow2, _pow_from_player):
                if check_FlagClaimable_on_smartcontract(_current_username):
                    flag = open('/flag.txt', 'r+')
                    _flag = flag.read()
                    flag.close()
                    return render_template('flagclaimed.html', flag = _flag)
                
                else:
                    return render_template('error.html',error = "Not Enough TetCTF Token For Claiming The Flag or Wrong Username In This Session !!!")

            else:
                return render_template('error.html',error = "Something go wrong homie !")

        else:
            return render_template('error.html',error = 'Unauthorized Access')

    except Exception as e:
        return render_template('error.html',error = "Something go wrong homie !")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='31337')