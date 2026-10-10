#!/usr/bin/env python3
"""Small client for the Frostline runbook service. Python 3, standard library only.

    python client.py URL session                           open a session, print its BASE
    python client.py BASE runbook                          print your copy of the runbook
    python client.py BASE check NEAR FIND [NEAR FIND ...]  ask whether hunks apply
    python client.py BASE unseal SEAL                      try a seal

URL is the service as shown on the challenge page. BASE is your session, URL/s/<token>:
`session` prints it, and so does the page you get from the button at URL.
FIND is taken as given on the command line and sent as UTF-8; put is sent as FIND.
"""
import json
import sys
import urllib.error
import urllib.request


def call(base, path, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(base.rstrip("/") + path, data=data, method="GET" if body is None else "POST")
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    base, cmd, rest = argv[1], argv[2], argv[3:]
    if cmd == "session" and not rest:
        status, body = call(base, "/session", {})
        if status == 200:
            print(base.rstrip("/") + "/s/" + json.loads(body)["token"])
        else:
            print(status, body.decode("utf-8", "replace"))
    elif cmd == "runbook":
        status, body = call(base, "/runbook")
        sys.stdout.buffer.write(body)
    elif cmd == "check":
        if not rest or len(rest) % 2:
            print("check needs NEAR FIND pairs", file=sys.stderr)
            return 2
        hunks = [{"near": int(rest[i]), "find": rest[i + 1], "put": rest[i + 1]}
                 for i in range(0, len(rest), 2)]
        status, body = call(base, "/hunks/check", {"hunks": hunks})
        print(status, body.decode("utf-8", "replace"))
    elif cmd == "unseal" and len(rest) == 1:
        status, body = call(base, "/unseal", {"seal": rest[0]})
        print(status, body.decode("utf-8", "replace"))
    else:
        print(__doc__.strip())
        return 2
    return 0 if status == 200 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
