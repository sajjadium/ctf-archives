#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import hmac
from hashlib import sha256
from base64 import b64decode, b64encode
import binascii


FAILURE = {"success": False, "signature": ""}


def verify(key, msg, sig):
    return hmac.compare_digest(sig, auth(key, msg))


def auth(key, msg):
    return hmac.new(msg, key, sha256).digest()


def main():
    print("HMAC authenticator started", flush=True)

    key = os.urandom(32)
    for line in sys.stdin:
        try:
            rpc = json.loads(line)
            if not isinstance(rpc, dict) or "message" not in rpc or len(rpc["message"]) == 0:
                print(FAILURE, flush=True)
                continue

            msg = b64decode(rpc["message"])
            retval = None

            if rpc.get("method", "") == "auth":    
                signature = auth(key, msg)
                retval = {"success": True, "signature": b64encode(signature).decode()}

            else:
                sig = rpc.get("signatures", {}).get("hmac")
                if sig is None or len(sig) == 0:
                    print(FAILURE, flush=True)
                    continue
                retval = {"success": verify(key, msg, b64decode(sig)), "signature": ""}

            print(json.dumps(retval), flush=True)

        except Exception as e:
            print(FAILURE, flush=True)


if __name__ == "__main__":
    main()
