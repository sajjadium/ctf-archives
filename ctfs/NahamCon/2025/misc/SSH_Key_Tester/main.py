#!/usr/bin/env python3
import os
import base64
import binascii as bi
import tempfile
import traceback
import subprocess
import sys

from flask import Flask, request
import random

sys.path.append("../")

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB


@app.route("/", methods=["GET", "POST"])
def run():
    print(request.files)
    if len(request.files) != 2:
        return "Please submit both private and public key to test.", 400

    if not request.files.get("id_rsa"):
        return "`id_rsa` file not found.", 400
    if not request.files.get("id_rsa.pub"):
        return "`id_rsa.pub` file not found.", 400
        

    privkey = request.files.get("id_rsa").read()
    pubkey = request.files.get("id_rsa.pub").read()
    if pubkey.startswith(b"command="):
        return "No command= allowed!", 400
    os.system("service ssh start")
    userid = "user%d" % random.randint(0, 1000)
    os.system("useradd %s && mkdir -p /home/%s/.ssh" % (userid, userid))
    with open("/tmp/id_rsa", "wb") as fd:
        fd.write(privkey)
    os.system("chmod 0600 /tmp/id_rsa")
    with open("/home/%s/.ssh/authorized_keys" % userid, "wb") as fd:
        fd.write(pubkey)
    os.system("timeout 2 ssh -o StrictHostKeyChecking=no -i /tmp/id_rsa %s@localhost &" % userid)
    return "Keys pass the checks.", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
