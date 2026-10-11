#!/usr/bin/env python3
"""client.py - small MORAINE archive client (Python 3 standard library only).

    python3 client.py open URL                  open a bucket; prints its base URL
    python3 client.py BASE whoami
    python3 client.py BASE ls
    python3 client.py BASE put NAME FILE        ("-" reads standard input)
    python3 client.py BASE stat NAME
    python3 client.py BASE get NAME [OUT]
    python3 client.py BASE rm NAME
    python3 client.py BASE usage
    python3 client.py BASE release

URL is the archive's address (for example https://isfcrpesu-moraine.chals.io); BASE is the
bucket URL that `open` prints.
"""
import json
import sys
import urllib.error
import urllib.request


def call(method, url, data=None):
    req = urllib.request.Request(url, data=data, method=method, headers={"Accept": "application/json"})
    if data is not None:
        req.add_header("Content-Type", "application/octet-stream")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def show(status, body):
    try:
        print(json.dumps(json.loads(body), indent=2))
    except ValueError:
        sys.stdout.buffer.write(body)
    if status >= 400:
        sys.exit(1)


def main(argv):
    if len(argv) == 3 and argv[1] == "open":
        status, body = call("POST", argv[2].rstrip("/") + "/session", b"")
        if status != 201:
            show(status, body)
        print(json.loads(body)["base"])
        return
    if len(argv) < 3:
        sys.exit(__doc__)
    base, cmd, args = argv[1].rstrip("/"), argv[2], argv[3:]
    if cmd in ("whoami", "usage") and not args:
        show(*call("GET", "%s/%s" % (base, cmd)))
    elif cmd == "ls" and not args:
        show(*call("GET", base + "/objects"))
    elif cmd == "put" and len(args) == 2:
        data = sys.stdin.buffer.read() if args[1] == "-" else open(args[1], "rb").read()
        show(*call("PUT", "%s/objects/%s" % (base, args[0]), data))
    elif cmd == "stat" and len(args) == 1:
        show(*call("GET", "%s/objects/%s" % (base, args[0])))
    elif cmd == "get" and len(args) in (1, 2):
        status, body = call("GET", "%s/objects/%s/data" % (base, args[0]))
        if status != 200:
            show(status, body)
        if len(args) == 2:
            open(args[1], "wb").write(body)
        else:
            sys.stdout.buffer.write(body)
    elif cmd == "rm" and len(args) == 1:
        show(*call("DELETE", "%s/objects/%s" % (base, args[0])))
    elif cmd == "release" and not args:
        show(*call("POST", base + "/release", b""))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
