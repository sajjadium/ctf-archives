from flask import Flask, request
from Crypto.Cipher import DES
from hashlib import md5
import os

PORT = int(os.environ.get('PORT', '5000'))
app = Flask(__name__)

invitation_codes = []

def new_invitation_code():
    return os.urandom(8).hex()


def check_invitation_code(username:str, code:str):
    des = DES.new(md5(username.encode()).digest()[:8], DES.MODE_CFB)
    code = des.decrypt(code.encode()).hex()[:16]
    if code in invitation_codes:
        invitation_codes.remove(code)
        return True
    return False


@app.get('/')
def index():
    return "Welcome to VIP service. To get an invite code, please contact ppk@aaa.com"


@app.post('/<username>')
def check(username):
    token = request.cookies.get('token')
    if not token:
        return "unauthorized access?"
    code = request.form.get('code')
    if not code:
        return "no invitation code specified"
    if check_invitation_code(username, code):
        return 'ok'
    return 'invalid invitation code'


@app.get('/new')
def new_code():
    code = new_invitation_code()
    invitation_codes.append(code)
    print('new invitation code:', code)
    return "done"


if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
