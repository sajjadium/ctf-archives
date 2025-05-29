from hidden import KEY, MSG
from Crypto.Cipher import AES
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Indestructible Vault !"

@app.route('/vault/<pwd>')
def encrypt(pwd):
    pwd = bytes.fromhex(pwd)
    assert len(pwd) == 16 and len(KEY) == 16
    cipher = AES.new(KEY, AES.MODE_CFB, pwd, segment_size= 128)
    return cipher.encrypt(MSG.encode()).hex()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10010, debug=False)
