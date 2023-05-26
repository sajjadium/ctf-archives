from flask import Flask
import time
from Crypto.Hash import SHA256

app = Flask(__name__)

hash_key = open("hash_key", "rb").read()[:32]
flag = open("flag.txt", "r").read().strip()


@app.route('/buy/<user>')
def buy(user):
    return "No"


@app.route('/song/<user>')
def song(user):
    return open("user/"+user+".drmsong", "rb").read().hex()


@app.route('/unlock/<meta>/<hmac>')
def unlock(meta, hmac):
    meta = bytes.fromhex(meta)

    user = None
    t = None
    for word in meta.split(b","):
        if b"user" in word:
            user = str(word[word.index(b":")+1:])[2:-1]
        if b"made" in word:
            t = float(str(word[word.index(b":")+1:])[2:-1])

    h = SHA256.new()
    h.update(hash_key)
    h.update(meta)
    if h.hexdigest() == hmac:
        if time.time() - t < 1000:
            drm_key = open("user/"+user+".drmkey", "rb").read().hex()
            drm_n = open("user/"+user+".drmnonce", "rb").read().hex()
            return drm_key + " " + drm_n + " " + flag
        else:
            return "Expired :(... pay us again"
    else:
        return "Bad Hash"


if __name__ == '__main__':
    app.run()
