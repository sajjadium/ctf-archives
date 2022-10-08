import os
from urllib.parse import parse_qs, urlencode

from flask import Flask, render_template, send_from_directory, make_response, request, flash, redirect, url_for
from werkzeug.security import safe_join
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
app.secret_key = os.environ["SEC_KEY"]

INFO_DIR_NAME = "infos"
PREMIUM_INFO_DIR_NAME = "premium-infos"
INSTANCE_KEY = os.environ["SEC_KEY"].encode()


def serialize_user(user):
    data = urlencode(user).encode()
    aes = AES.new(INSTANCE_KEY, AES.MODE_CBC)
    ct = aes.encrypt(pad(data, 16))
    # guarantee ciphertext integrity
    mac = HMAC.new(INSTANCE_KEY, ct).digest()
    return (aes.iv + ct + mac).hex()


def deserialize_user(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)
    iv, ct, mac = ciphertext[:16], ciphertext[16:-16], ciphertext[-16:]

    # Check ciphertext integrity
    if not HMAC.new(INSTANCE_KEY, ct).digest() == mac:
        raise ValueError("Ciphertext was manipulated.")

    aes = AES.new(INSTANCE_KEY, AES.MODE_CBC, iv=iv)
    plaintext = unpad(aes.decrypt(ct), 16)
    user_obj_raw = parse_qs(plaintext.decode())
    user_obj = {k: v[0] for k, v in user_obj_raw.items()}

    return user_obj


@app.route('/')
def index():
    countries = os.listdir(INFO_DIR_NAME)
    countries.sort()
    premium_flags = os.listdir(PREMIUM_INFO_DIR_NAME)
    premium_flags.sort()
    resp = make_response(
        render_template("home.html", countries=countries, premium_flags=premium_flags)
    )

    # TODO: implement login for premium members once somebody finally buys premium
    resp.set_cookie("user", serialize_user({"user": "stduser", "role": "pleb"}))

    return resp

@app.route('/premium')
def premium():
    return render_template("premium.html")


@app.route('/info/<country>')
def flag_info(country):
    info_file = safe_join(INFO_DIR_NAME, country)
    if not info_file:
        return "Bad request", 400

    if not os.path.exists(info_file):
        flash("Country does not exist")
        return redirect(url_for("index"))

    info = open(info_file).read()
    return render_template("info.html", country=country, info=info)


@app.route('/premium-info/<country>')
def premium_info(country):
    user_cookie = request.cookies.get('user')

    if not user_cookie:
        flash("Cookie not found!")
        return redirect(url_for("index"))

    try:
        user = deserialize_user(user_cookie)
    except ValueError as ex:
        flash("Inavlid Cookie: " + str(ex))
        return redirect(url_for("index"))

    if user["role"] != "premium":
        flash("You haven't payed for premium!")
        return redirect(url_for("index"))

    info_file = safe_join(PREMIUM_INFO_DIR_NAME, country)
    info = open(info_file).read()

    return render_template("info.html", country=country, info=info)


if __name__ == '__main__':
    app.run()
