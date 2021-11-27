#!/usr/bin/python3
import hashlib
import os
import sys

from common import *

cleanup_old_sessions()

password = os.environ.get("QUERY_PARAM_PASSWORD")
if password is None:
  respond_and_exit({
      "error": "Missing password parameter."
  }, status_code=400, status_msg="Bad Request")

sid = os.urandom(20).hex()

hash = hashlib.sha256(SALT + decode_param_value(password)).digest()

with open(f"session_{sid}", "wb") as f:
  f.write(hash)

respond_and_exit({
    "sid": sid
})
