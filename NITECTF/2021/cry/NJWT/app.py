from flask import Flask, render_template, request, make_response
import NJWT
import os, base64
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
FLAG = os.environ.get('FLAG')

Obj = NJWT.NJWT()

@app.route('/')
def index():
    cookie = "None"
    resp = make_response(render_template("index.html", display=cookie))
    try:
        resp.set_cookie('NJWT', cookie)
    except TypeError:
        print("TypeError")
    return resp

@app.route('/generateToken', methods=["GET", "POST"])
def generateToken():
    if request.method == "GET":
        return render_template("index.html", display="THAT IS NOT HOW YOU ARE SUPPOSED TO GENERATE TOKEN.")
    else:
        username = request.form['username']
        cookie = Obj.generate_token(username)
        resp = make_response(render_template("index.html", display=cookie))
        if cookie == "not_auth":
            return render_template("index.html", display='Username Admin is not allowed.')
        try:
            resp.set_cookie('NJWT', cookie)
        except TypeError:
            print("TypeError")
        return resp


@app.route('/verify', methods=["POST", "GET"])
def verify():
    if request.method == 'GET':
        return render_template('response.html', msg="Error")
    else:
        token = request.cookies.to_dict()['NJWT']

        flag = Obj.verify_token(token)
        
        if flag == 'access_denied':
            return render_template('response.html', msg="Access Denied")
        elif flag == "invalid_signature":
            return render_template('response.html', msg="Invalid Signature")
        elif flag == "invalid_header":
            return render_template('response.html', msg="Invalid Header")
        elif flag == "Success":
            return render_template('flag.html', msg=FLAG)
        else:
            return render_template('response.html', msg="Error")
        

if __name__ == '__main__':
    app.run(debug=True)