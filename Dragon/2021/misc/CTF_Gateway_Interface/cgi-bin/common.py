#!/bin/false
import glob
import hashlib
import json
import os
import sys
import time

SALT = b"SaltyMcSaltFace"

def cleanup_old_sessions():
  # Remove old sessions after 5 minutes have past.
  now = time.time()
  for session_file in glob.glob("session_*"):
    last_mod = os.path.getmtime(session_file)
    if now - last_mod > 60 * 5:
      try:
        os.unlink(session_file)
      except Exception as e:
        sys.stderr.write(str(e))
        sys.stderr.write('\n')

def respond_and_exit(content, status_code=200, status_msg="OK"):
  if type(content) is not str:
    content = json.dumps(content)

  response = [
    f"HTTP/1.1 {status_code} {status_msg}",
    "Content-Type: application/json",
    f"Content-Length: {len(content)}",
  ]

  response.extend([
    "",
    content
  ])
  print('\r\n'.join(response))

  sys.exit()

def decode_param_value(value):
  decoded = []

  i = 0
  while i < len(value):
    if value[i] == '%':
      if i + 2 >= len(value):
        return None
      try:
        decoded.append(int(value[i+1:i+3], 16))
      except ValueError:
        return None
      i += 3
    else:
      decoded.append(ord(value[i]))
      i += 1

  return bytes(decoded)

def validate_hex(s):
  ALLOWED_CHARS = set(b"0123456789abcdefABCDEF")
  return all(p in ALLOWED_CHARS for p in s)
