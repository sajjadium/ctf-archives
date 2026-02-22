import os
import jwt
import datetime
from flask import Flask, request, make_response, jsonify
from Crypto.Util import number
from Crypto.PublicKey import RSA

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

def generate_parameter_p(bits, D=7331):
    while True:
        s = number.getRandomNBitInteger(bits // 2)
        p_val = (D * (s**2) + 1)
        if p_val % 4 == 0:
            p = p_val // 4
            if number.isPrime(p):
                return p

def initialize_system_parameters():
    p = generate_parameter_p(1024)
    q = number.getPrime(1024)
    n = p * q
    e = 65537
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    key = RSA.construct((n, e, d, p, q))
    return key.export_key(), key.publickey().export_key()

PRIVATE_KEY, PUBLIC_KEY = initialize_system_parameters()

@app.route('/')
def index():
    token = request.cookies.get('auth_token')
    
    if not token:
        payload = {
            'user': 'g00s3',
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
        resp = make_response("Hello g00s3")
        resp.set_cookie('auth_token', token, httponly=True)
        return resp

    try:
        data = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'])
        user = data.get('user')
        
        if user == 'whale':
            return jsonify({
                "status": "authorized",
                "message": "congr8s! whale",
                "flag": "THJCC{TEST_ME}"
            })
        else:
            return f"Hello {user}"
            
    except:
        payload = {
            'user': 'g00s3',
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
        resp = make_response("Hello g00s3")
        resp.set_cookie('auth_token', token, httponly=True)
        return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
