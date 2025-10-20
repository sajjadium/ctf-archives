#!/usr/bin/env python3
import os, base64, math, hashlib
from flask import Flask, request, jsonify, abort
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import secret
app = Flask(__name__)

RSA_BITS = int(os.environ.get("RSA_BITS", "2048"))

MAX_ORACLE_QUERIES = int(os.environ.get("MAX_ORACLE_QUERIES", "20000"))

key = RSA.generate(RSA_BITS)
n = key.n
e = key.e
k = (n.bit_length() + 7) // 8
B = 1 << (8 * (k - 1))

def derive_r(n):
    h = hashlib.sha256(str(n).encode()).digest()
    candidate = int.from_bytes(h, "big") % (n - 3) + 2
    while math.gcd(candidate, n) != 1:
        candidate = (candidate + 1) % (n - 2) + 2
    return candidate

R_CONST = derive_r(n)

if math.gcd(R_CONST, n) != 1:
    raise SystemExit("R_CONST not invertible with n")
cipher_pub = PKCS1_OAEP.new(key.publickey())
ciphertext = cipher_pub.encrypt(secret.FLAG)
cipher_b64 = base64.b64encode(ciphertext).decode()

oracle_queries = 0

def bytes_to_int(b): return int.from_bytes(b, "big")

def int_to_bytes(i, length): return i.to_bytes(length, "big")

@app.route("/pub", methods=["GET"])
def pub():
    return jsonify({"n": hex(n), "e": e, "ciphertext_b64": cipher_b64})

@app.route("/oracle", methods=["POST"])
def oracle():
    global oracle_queries
    if oracle_queries >= MAX_ORACLE_QUERIES:
        abort(429)
    data = request.get_json(force=True, silent=True)
    if not data or "ct_b64" not in data:
        abort(400)
    try:
        ct_bytes = base64.b64decode(data["ct_b64"])
    except Exception:
        abort(400)
    c_int = bytes_to_int(ct_bytes)
    if c_int >= n or c_int < 0:
        return jsonify({"res": False})
    m_int = pow(c_int, key.d, n)
    oracle_queries += 1
    val = (R_CONST * m_int) % n
    res = (val >= B)
    return jsonify({"res": bool(res)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "6137")))
