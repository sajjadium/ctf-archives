#!/usr/bin/python3
import hashlib
import os
import sys

from common import *

cleanup_old_sessions()

sid = os.environ.get("QUERY_PARAM_SID")
if sid is None:
  respond_and_exit({
      "error": "Missing sid parameter."
  }, status_code=400, status_msg="Bad Request")

sid = decode_param_value(sid)

if not validate_hex(sid) or len(sid) != 40:
  respond_and_exit({
      "error": "Wrong sid format."
  }, status_code=400, status_msg="Bad Request")

sid = str(sid, "utf-8")
sid_file = f'session_{sid}'
if not os.path.isfile(sid_file):
  respond_and_exit({
      "error": "Auth session not found."
  }, status_code=400, status_msg="Bad Request")

with open(sid_file, "rb") as f:
  provided_hash = f.read()
os.unlink(sid_file)

GOOD_PASSWORD = bytes(os.environ.get('CTF_UNKNOWN_PASSWORD'), "utf-8")
GOOD_PASSWORD_HASH = hashlib.sha256(SALT + GOOD_PASSWORD).digest()
if provided_hash == GOOD_PASSWORD_HASH:
  respond_and_exit({
      "authSuccessful": True,
      "authMessage": "Congratz! That's the right password!"
  })
else:
  respond_and_exit({
      "error": "Wrong password."
  }, status_code=400, status_msg="Bad Request")

