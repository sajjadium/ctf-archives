from flask import Flask, request, render_template, jsonify
from tempfile import NamedTemporaryFile
from types import SimpleNamespace
from os import remove
from Crypto.Util.number import getPrime, long_to_bytes
from hashlib import sha512
from logger import Logger
from montgomery import rsa_crt, modExp
import json

rsa_keysize = 1024
flag = open('flag.txt', "rb").read()

app = Flask(__name__, static_url_path='', static_folder='static')

## RSA parameter setup
try:
	with open("/secret/rsaparams", "r") as f:
		rsa = json.load(f, object_hook = lambda x: SimpleNamespace(**x))
		if (rsa.n.bit_length() != rsa_keysize):
			raise Exception()
except Exception:		
	rsa = SimpleNamespace()
	rsa.p = getPrime(rsa_keysize // 2)
	rsa.q = getPrime(rsa_keysize // 2)
	rsa.e = getPrime(rsa_keysize // 2)
	rsa.n = rsa.p * rsa.q
	rsa.d = pow(rsa.e, -1, (rsa.p - 1) * (rsa.q - 1))

## treasure and hint!
xor = lambda a, b: bytes([x^y for x, y in zip(a, b)])
rsa.treasure = int(xor(sha512(long_to_bytes(rsa.d)).digest(), flag).hex(), 16)
hint = bin(rsa.p)[2:5]

## index page
@app.route('/')
def index():
	return render_template('index.html', rsa=rsa, hint=hint)

## modular exponentiation request handler
@app.route('/modexp', methods=['POST'])
def modexp():
	try:
		data = request.json

		base = int(data["base"])
		exp = rsa.d if data["use_d"] else int(data["exp"])
		mod = rsa.n if data["use_n"] else int(data["mod"])
		loglevel = int(data["loglevel"])

		logfile = NamedTemporaryFile(prefix="modexp", mode="w", delete=False)
		logger = Logger(loglevel, logfile)

		if mod == rsa.n:
			result = rsa_crt(base, exp, rsa.p, rsa.q, logger)
		else:
			#chcek modulus size to prevent DoS attack
			if mod.bit_length() > rsa_keysize:
				raise Exception()
			result = modExp(base, exp, mod, logger)

		logfile.close()
		log = open(logfile.name).read()

		remove(logfile.name)

		return jsonify({"status": "success", "res": str(result), "log": log})
	except Exception:
		return jsonify({"status": "fail", "res": "Something wrong", "log": ""})

if __name__ == "__main__":
	app.run(debug=False)
