import hashlib
import os
import secrets

import fastcrc
import werkzeug.security
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from flask import Flask, Response, request, send_from_directory

app = Flask(__name__)

SERVER_KEY = bytes.fromhex(os.environ.get("SERVER_KEY", ""))
IV_LEN = 16
# USER_LEN = can potentially vary
NONCE_LEN = 42
MAC_LEN = 8
KEY_LEN = 32

USER_DB = {
    # Someone keeps hacking us and reading out the admin's /flag.txt.
    # Disabling this account to see if that helps.
    # "admin": "7a2f445babffa758471e3341a1fadce9abeff194aded071e4fd48b25add856a7",

    # Other accounts. File a ticket similar to QDB-244321 to add or modify passwords.
    "azure": "9631758175d2f048db1964727ad2efef4233099b97f383e4f1e121c900f3e722",
    "cthon": "980809b1482352ae59be5d3ede484c0835b46985309a04ac1bad70b22a167670",
}


def response(text, status=200):
    return Response(text, status=status, mimetype="text/plain")


@app.route("/", methods=["GET", ])
def root():
    return response("""Endpoints:
  - /auth?user=<user>: Auth a user with an optional password. Returns an auth token.
  - /read/<path>?token=<token>: Read out a file from a user's directory. Token required.
""")


@app.route("/auth", methods=["GET", ])
def auth():
    """Return a token once the user is successfully authenticated.
    """
    user = request.args.get("user")
    password = request.args.get("password", "")
    if not user or user not in USER_DB:
        return response("Bad or missing 'user'", 400)

    password_hash = USER_DB[user]
    given = hashlib.pbkdf2_hmac("SHA256", password.encode(), user.encode(), 1000).hex()
    if password_hash != given:
        return response("Bad 'password'", 400)

    # User is authenticated! Return a super strong token.
    return response(encrypt_token(user, SERVER_KEY).hex())


@app.route("/read", defaults={"path": None})
@app.route("/read/<path>", methods=["GET", ])
def read(path: str):
    """Read a static file under the user's directory.

    Lists contents if no path is provided.

    Decrypts the token to auth the request and get the user's name.
    """
    try:
        user = decrypt_token(bytes.fromhex(request.args.get("token", "")), SERVER_KEY)
    except ValueError:
        user = None

    if not user:
        return response("Bad or missing token", 400)

    user_dir = werkzeug.security.safe_join("users", user)

    if path is None:
        listing = "\n".join(sorted(os.listdir(os.path.join(app.root_path, user_dir))))
        return response(listing)

    return send_from_directory(user_dir, path)


def encrypt_token(user: str, key: bytes) -> bytes:
    """Encrypt the user string using "authenticated encryption".

    JWTs and JWEs scare me. Too many CVEs! I think I can do better...

    Here's the token format we use to encrypt and authenticate a user's name.
    This is sent to/from the server in ascii-hex:
      len :  16    variable      42      8
      data:  IV ||   USER   || NONCE || MAC
                  '------------------------' Encrypted
    """
    assert len(key) == KEY_LEN

    user_bytes = user.encode("utf-8")

    iv = secrets.token_bytes(IV_LEN)
    nonce = secrets.token_bytes(NONCE_LEN)

    cipher = Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor()

    mac = gen_mac(iv + user_bytes + nonce)

    ciphertext = cipher.update(user_bytes + nonce + mac) + cipher.finalize()

    return iv + ciphertext


def decrypt_token(token: bytes, key: bytes) -> [None, str]:
    assert len(key) == KEY_LEN

    iv, ciphertext = splitup(token, IV_LEN)
    if not iv or not ciphertext:
        return None

    cipher = Cipher(algorithms.AES(key), modes.CTR(iv)).decryptor()
    plaintext = cipher.update(ciphertext) + cipher.finalize()

    user_bytes, nonce, mac = splitup(plaintext, -(NONCE_LEN + MAC_LEN), -MAC_LEN)
    if not user_bytes or len(nonce) != NONCE_LEN or len(mac) != MAC_LEN:
        return None

    computed = gen_mac(iv + user_bytes + nonce)
    if computed != mac:
        return None

    return user_bytes.decode("utf-8")


def gen_mac(data: bytes) -> bytes:
    # A 64-bit CRC should be pretty good. Faster than a hash, and can't be brute forced.
    crc = fastcrc.crc64.go_iso(data)
    return int.to_bytes(crc, length=MAC_LEN, byteorder="big")


def splitup(data: bytes, *indices):
    last_index = 0
    for index in indices:
        yield data[last_index:index]
        last_index = index
    yield data[last_index:]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT"), debug=False)
