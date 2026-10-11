#!/usr/bin/env python3
"""Run one job on your unit, or read its line set.

    python3 client.py <unit-url>                    GET /  (this unit's lines and limits)
    python3 client.py <unit-url> trace trace        POST /run, one argument per line
"""
import json
import sys
import urllib.error
import urllib.request

url = sys.argv[1].rstrip("/")
lines = sys.argv[2:]
if lines:
    req = urllib.request.Request(url + "/run", data=json.dumps({"job": "\n".join(lines)}).encode(),
                                 headers={"content-type": "application/json"}, method="POST")
else:
    req = urllib.request.Request(url + "/")
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(resp.status, resp.read().decode())
except urllib.error.HTTPError as e:
    print(e.code, e.read().decode())
