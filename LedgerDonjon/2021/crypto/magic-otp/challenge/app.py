#!/usr/bin/env python3

import base64
import hashlib
import hmac
import json
import os
import struct
import sys
import time

from flask import Flask, jsonify, request, send_from_directory, stream_with_context, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import device


app = Flask(__name__, static_url_path="/assets/", static_folder="data/assets/")
limiter = Limiter(app, key_func=get_remote_address)


def time_now():
    return time.time()


def get_otp_secret():
    otp_secret = os.environ.get("OTP_SECRET")
    if not otp_secret:
        print("OTP_SECRET environment variable is unset", file=sys.stderr)
        sys.exit(1)

    return base64.b64decode(otp_secret)


def check_otp(otp):
    otp_secret = get_otp_secret()

    # a new OTP is generated every 30 seconds
    epoch = int(time_now() / 30)

    # OTPs are valid during 1 minute
    for epoch_offset in range(0, 2):
        value = struct.pack('>q', epoch - epoch_offset)
        hmac_hash = hmac.new(otp_secret, value, hashlib.sha256).digest()
        offset = hmac_hash[-1] & 0x0F
        truncated_hash = hmac_hash[offset:offset + 4]
        truncated_hash = struct.unpack('>L', truncated_hash)[0]
        truncated_hash &= 0x7FFFFFFF

        if otp == f"{truncated_hash:010d}":
            return True

    return False


def device_response(callback, **kwargs):
    """
    Stream the response since the communication with the device is not instant.
    It prevents concurrent HTTP requests from being blocked.
    """

    def generate_device_response(callback, **kwargs):
        # force headers to be sent
        yield b""

        # generate reponse
        yield json.dumps(callback(**kwargs)).encode()

    return Response(stream_with_context(generate_device_response(callback, **kwargs)), content_type="application/json")


@limiter.limit("10/minute")
@app.route("/api/get_flag", methods=["POST"])
def get_flag():
    content = request.get_json(force=True, silent=True)
    if content is None or "otp" not in content:
        return jsonify({"error": "missing otp"})

    if not check_otp(content["otp"]):
        return jsonify({"error": "invalid otp"})

    flag = os.environ.get("FLAG", "CTF{FLAG environment variable is unset}")
    return jsonify({"message": f"Congratulation! Here's the flag: {flag}."})


@app.route("/api/get_encrypted_otp", methods=["POST"])
def get_encrypted_otp():
    content = request.get_json(force=True, silent=True)
    if content is None or "deviceid" not in content:
        return jsonify({"error": "missing device id"})

    def callback(request, deviceid):
        epoch = int(time_now() / 30)
        try:
            encrypted_otp = device.get_encrypted_otp(request, epoch, deviceid)
        except device.DeviceError as e:
            return {"error": f"failed to generate encrypted otp: {e}"}

        return {"encrypted_otp": encrypted_otp}

    return device_response(callback, request=request, deviceid=content["deviceid"])


@app.route("/api/get_server_pubkey", methods=["GET"])
def get_server_pubkey():
    def callback(request):
        pubkey = device.get_server_pubkey(request)
        return {"pubkey": pubkey.hex()}

    return device_response(callback, request=request)


@app.route("/api/list_registered_devices", methods=["GET"])
def list_registered_devices():
    def callback(request):
        pubkeys = device.list_registered_devices(request)
        return {"pubkeys": [pubkey.hex() for pubkey in pubkeys]}

    return device_response(callback, request=request)


@app.route("/", methods=['GET'])
def index():
    return send_from_directory("data/assets/", "index.html")


if __name__ == "__main__":
    tls_cert = os.path.join(os.path.dirname(__file__), "data/https.pem")
    app.run(host="0.0.0.0", port=9000, threaded=True, use_reloader=False, ssl_context=(tls_cert, tls_cert))
