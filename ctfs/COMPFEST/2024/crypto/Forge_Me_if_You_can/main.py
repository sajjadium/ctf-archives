from flask import Flask, request, jsonify
from Crypto.Util.number import bytes_to_long, getPrime, inverse
from hashlib import sha256, sha512, sha3_256, sha3_512, blake2b, blake2s

app = Flask(__name__)

algo_round = [sha256, sha3_256, sha3_512, blake2b, blake2s]

magic_string = b"SkibidiSigmaRizzleDizzleMyNizzleOffTheHizzleShizzleKaiCenat"

def xor_256(a, b):
    if len(a) < len(b):
        a = a + b"\x00" * (len(b) - len(a))
    elif len(b) < len(a):
        b = b + b"\x00" * (len(a) - len(b))
    return bytes([x ^ y for x, y in zip(a, b)])

def sigma_round(bytes_to_hash):
    result = b""
    for i in range(0, len(bytes_to_hash), 4):
        current = bytes_to_hash[i:i+4]
        current = algo_round[i % len(algo_round)](current).digest()[:2]
        
        result += current
    return result

def icb_256(bytes_to_hash):
    if len(bytes_to_hash) < 64:
        bytes_to_hash = sha512(bytes_to_hash).digest()

    temp = sigma_round(bytes_to_hash)
    result = b""
    for i in range(0, len(temp), 32):
        
        result = xor_256(result, temp[i:i+32])
        
    return result

p = getPrime(696)
q = getPrime(420)
n = p * q
public_key = getPrime(666)
secret_key = inverse(public_key, (p-1)*(q-1))

def rsa_sign(message, secret_key, n):
    return pow(bytes_to_long(icb_256(message)), secret_key, n)

def rsa_verify(signature, public_key, n, original_message):
    return pow(bytes_to_long(signature), public_key, n) == bytes_to_long(icb_256(original_message))

@app.route('/sign', methods=['GET'])
def sign():
    print(request.args.get('message'))
    message = bytes.fromhex(request.args.get('message'))
    if not message:
        return jsonify({"error": "Message parameter is missing"}), 400
    if icb_256(message) == icb_256(magic_string):
        return jsonify({"error": "Signing this message is not allowed"}), 403
    signature = rsa_sign(message, secret_key, n)
    
    return jsonify({"signature": signature})
    
@app.route('/pubkey', methods=['GET'])
def pubkey():
    return jsonify({"n": n, "e": public_key})

@app.route('/get_flag', methods=['GET'])
def come_sweet_flag():
    signature = bytes.fromhex(request.args.get('signature'))
    if signature is None:
        return jsonify({"error": "Signature parameter is missing"}), 400
    if rsa_verify(signature, public_key, n, magic_string):
        return jsonify({"flag": "COMPFEST16{redacted}"})
    else:
        return jsonify({"error": "wrong"}), 403

if __name__ == '__main__':
    app.run("0.0.0.0", port=8080)
