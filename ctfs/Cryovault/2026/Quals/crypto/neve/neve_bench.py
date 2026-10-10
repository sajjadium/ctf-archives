#!/usr/bin/env python3
"""
neve_bench.py - bench model of the NEVE sounding head, firmware NV-3.4.2.

    python neve_bench.py serve [--port 19640] [--seed N]     run a bench head locally
    python neve_bench.py factory [factory_session.jsonl]      replay the factory session

A bench head speaks the same protocol as a field head (see README.md): JSON lines on a
plain connection, or JSON messages on a WebSocket to the same port. Each session gets its
own table and keystream key, drawn at random (or from --seed), so no two bench sessions
agree, and none of them agrees with a field head.

Link is a small client for either kind of head, over either framing; give it a path and it
appends every SOUND exchange to that file as JSON lines.

Standard library only, plus pycryptodome or cryptography for the bundle.
"""

import argparse
import asyncio
import base64
import hashlib
import hmac
import json
import os
import socket
import ssl
import sys
import urllib.parse

ROWS = 32
CELLS = 16
GRADE_P = [0.18 + i * 0.64 / 7 for i in range(8)]
GRADE_T = [int(round(p * (1 << 32))) for p in GRADE_P]
BUDGET = 1_250_000
MISS_CHARGE = 4096
MAX_SYMS = 4096
HEAD_NAME = "NV-3.4.2"
BUNDLE_INFO = b"NV4 recovery bundle"
HEX = set("0123456789abcdefABCDEF")
TOKEN_CHARS = set("0123456789abcdef")


# ---------------------------------------------------------------------------- table
def chained_rows(seed):
    """Each row's cells come from that row's seed; the next row's seed is
    SHA256(seed || row)."""
    rows = []
    for _ in range(ROWS):
        cells = hashlib.sha256(seed + b"NV/cells").digest()
        row = [c & 7 for c in cells[:CELLS]]
        rows.append(row)
        seed = hashlib.sha256(seed + bytes(row)).digest()
    return rows


def hkdf_sha256(ikm, salt, info, length=32):
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    out, block, i = b"", b"", 1
    while len(out) < length:
        block = hmac.new(prk, block + info + bytes([i]), hashlib.sha256).digest()
        out += block
        i += 1
    return out[:length]


def bundle_key(rows, session):
    """HKDF-SHA256 over the 512 grades, row 1 cell 0 first, one byte each."""
    return hkdf_sha256(bytes(g for row in rows for g in row), session, BUNDLE_INFO, 32)


def _gcm(key, nonce, aad, data, tag=None):
    try:
        from Crypto.Cipher import AES
        c = AES.new(key, AES.MODE_GCM, nonce=nonce)
        c.update(aad)
        if tag is None:
            ct, t = c.encrypt_and_digest(data)
            return ct + t
        return c.decrypt_and_verify(data, tag)
    except ImportError:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        if tag is None:
            return AESGCM(key).encrypt(nonce, data, aad)
        return AESGCM(key).decrypt(nonce, data + tag, aad)


def seal_bundle(rows, instance, session, nonce, text):
    return nonce + _gcm(bundle_key(rows, session), nonce, instance + session, text)


def open_bundle(rows, instance, session, blob):
    """blob = nonce(12) | ciphertext | tag(16); raises on a wrong table."""
    return _gcm(bundle_key(rows, session), blob[:12], instance + session, blob[12:-16],
                blob[-16:])


# ---------------------------------------------------------------------------- head
class BenchSession:
    """Head state for one bench session."""

    def __init__(self, rows, instance, session, coin_key, nonce, budget=BUDGET):
        self.rows = [list(r) for r in rows]
        self.instance, self.session = instance, session
        self.coin_key, self.nonce = coin_key, nonce
        self.budget = budget
        self.t = 0
        self.bit = 0
        self.prev = 0
        self.frontier = 1
        self.used = 0

    def draw(self, t):
        return int.from_bytes(hashlib.sha256(self.coin_key + t.to_bytes(8, "big")).digest()[:4], "big")

    def sound(self, row, syms):
        thr = [GRADE_T[g] for g in self.rows[row - 1]]
        out = []
        for b in syms:
            if self.draw(self.t) < thr[(b - self.prev) & 15]:
                self.bit ^= 1
            self.prev = b
            out.append("1" if self.bit else "0")
            self.t += 1
        self.used += len(syms)
        return "".join(out)

    def checkpoint(self, row, grades):
        if list(grades) == self.rows[row - 1]:
            if row == self.frontier:
                self.frontier += 1
            return True
        self.used = min(self.budget, self.used + MISS_CHARGE)
        return False

    def bundle(self):
        text = ("NEVE bench bundle\ninstance %s\nsession %s\nbench heads seal no recovery data\n"
                % (self.instance.hex(), self.session.hex())).encode()
        return seal_bundle(self.rows, self.instance, self.session, self.nonce, text)


class BenchHead:
    def __init__(self, seed=None):
        self.seed = seed
        self.material = os.urandom(32) if seed is None else hashlib.sha256(b"NV3 bench %d" % seed).digest()
        self.instance = hashlib.sha256(self.material + b"id").digest()[:16]
        self.sessions = {}
        self.opened = 0

    def open(self):
        self.opened += 1
        if self.seed is None:
            session = os.urandom(16)
        else:
            session = hashlib.sha256(self.material + b"session %d" % self.opened).digest()[:16]
        m = hashlib.sha512(self.material + session).digest()
        s = BenchSession(chained_rows(m[:32]), self.instance, session,
                         hashlib.sha256(m + b"coin").digest(), hashlib.sha256(m + b"nonce").digest()[:12])
        self.sessions[session] = s
        return s


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _status(head, s):
    return {"ok": True, "session": s.session.hex(), "head": HEAD_NAME, "instance": head.instance.hex(),
            "t": s.t, "row": s.frontier, "budget": s.budget - s.used, "bit": s.bit}


def dispatch(head, req):
    """One request -> one response, same shapes as a field head."""
    if not isinstance(req, dict):
        return {"ok": False, "err": "EARG"}
    cmd = req.get("cmd")
    if cmd == "OPEN":
        return _status(head, head.open())
    if cmd == "HELLO" and "session" not in req:
        return {"ok": True, "head": HEAD_NAME, "instance": head.instance.hex()}
    if cmd not in ("HELLO", "SOUND", "CHECKPOINT", "BUNDLE"):
        return {"ok": False, "err": "EARG"}
    tok = req.get("session")
    if not isinstance(tok, str) or len(tok) != 32 or not set(tok) <= TOKEN_CHARS:
        return {"ok": False, "err": "EARG"}
    s = head.sessions.get(bytes.fromhex(tok))
    if s is None:
        return {"ok": False, "err": "ESESSION"}
    if cmd == "HELLO":
        return _status(head, s)
    if cmd == "BUNDLE":
        return {"ok": True, "bundle": s.bundle().hex()}
    if cmd == "SOUND":
        t, row, syms = req.get("t"), req.get("row"), req.get("syms")
        if not (_is_int(t) and _is_int(row) and isinstance(syms, str)
                and 1 <= len(syms) <= MAX_SYMS and set(syms) <= HEX and 0 <= t < (1 << 62)
                and 1 <= row <= ROWS):
            return {"ok": False, "err": "EARG"}
        if t != s.t:
            return {"ok": False, "err": "ESEQ", "t": s.t}
        if row > s.frontier:
            return {"ok": False, "err": "EROW", "row": s.frontier}
        if len(syms) > s.budget - s.used:
            return {"ok": False, "err": "EBUDGET", "budget": s.budget - s.used}
        bits = s.sound(row, [int(c, 16) for c in syms])
        return {"ok": True, "t": s.t, "row": row, "budget": s.budget - s.used, "bits": bits}
    row, grades = req.get("row"), req.get("grades")
    if not (_is_int(row) and 1 <= row <= ROWS and isinstance(grades, str)
            and len(grades) == CELLS and set(grades) <= set("01234567")):
        return {"ok": False, "err": "EARG"}
    if row > s.frontier:
        return {"ok": False, "err": "EROW", "row": s.frontier}
    if s.budget - s.used < MISS_CHARGE:
        return {"ok": False, "err": "EBUDGET", "budget": s.budget - s.used}
    if s.checkpoint(row, [int(c) for c in grades]):
        return {"ok": True, "row": s.frontier, "budget": s.budget - s.used}
    return {"ok": False, "err": "EMISS", "row": row, "budget": s.budget - s.used}


# ---------------------------------------------------------------------------- WebSocket
WS_GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
MAX_MSG = 16384


def _xor4(data, mask):
    """RFC 6455 masking: XOR with the 4-byte key repeated."""
    n = len(data)
    if not n:
        return data
    m = (mask * (n // 4 + 1))[:n]
    return (int.from_bytes(data, "big") ^ int.from_bytes(m, "big")).to_bytes(n, "big")


def _frame(opcode, payload, mask=None):
    n = len(payload)
    m = 0x80 if mask else 0
    if n < 126:
        head = bytes((0x80 | opcode, m | n))
    elif n < 65536:
        head = bytes((0x80 | opcode, m | 126)) + n.to_bytes(2, "big")
    else:
        head = bytes((0x80 | opcode, m | 127)) + n.to_bytes(8, "big")
    return head + (mask + _xor4(payload, mask) if mask else payload)


def _requests(payload):
    """One JSON request per message, or several, one per line. None = malformed."""
    text = payload.decode("utf-8", "replace")
    try:
        return [json.loads(text)]
    except Exception:
        pass
    lines = [ln for ln in text.split("\n") if ln and not ln.isspace()]
    if len(lines) < 2:
        return [None]
    out = []
    for ln in lines:
        try:
            out.append(json.loads(ln))
        except Exception:
            out.append(None)
    return out


async def _serve(host, port, seed):
    head = BenchHead(seed)

    async def handshake(reader, writer, first):
        hdr = {}
        while True:
            ln = await reader.readline()
            if ln in (b"\r\n", b"\n", b""):
                break
            k, _, v = ln.decode("latin-1").partition(":")
            hdr["".join(k.split()).lower()] = " ".join(v.split())
        key = hdr.get("sec-websocket-key", "")
        if not first.startswith(b"GET ") or "websocket" not in hdr.get("upgrade", "").lower() \
                or hdr.get("sec-websocket-version") != "13" or not key:
            body = b"send JSON lines, or upgrade to a WebSocket\r\n"
            writer.write(b"HTTP/1.1 426 Upgrade Required\r\nSec-WebSocket-Version: 13\r\n"
                         b"Content-Length: %d\r\nConnection: close\r\n\r\n%s" % (len(body), body))
            return False
        accept = base64.b64encode(hashlib.sha1(key.encode() + WS_GUID).digest())
        writer.write(b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n"
                     b"Connection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n" % accept)
        return True

    async def messages(reader, writer):
        parts = None
        while True:
            b0, b1 = await reader.readexactly(2)
            opcode, n = b0 & 0x0F, b1 & 0x7F
            if n == 126:
                n = int.from_bytes(await reader.readexactly(2), "big")
            elif n == 127:
                n = int.from_bytes(await reader.readexactly(8), "big")
            if n + sum(len(p) for p in parts or ()) > MAX_MSG:
                writer.write(_frame(0x1, b'{"ok":false,"err":"EARG"}') + _frame(0x8, b"\x03\xf1"))
                return
            mask = await reader.readexactly(4) if b1 & 0x80 else None
            data = await reader.readexactly(n)
            if mask:
                data = _xor4(data, mask)
            if opcode == 0x8:
                writer.write(_frame(0x8, data[:2]))
                return
            if opcode == 0x9:
                writer.write(_frame(0xA, data))
                continue
            if opcode in (0x1, 0x2, 0x0):
                parts = (parts or []) + [data]
                if b0 & 0x80:
                    yield b"".join(parts)
                    parts = None

    async def lines(reader, writer, line):
        while line:
            try:
                req = json.loads(line)
            except Exception:
                req = None
            writer.write((json.dumps(dispatch(head, req), separators=(",", ":")) + "\n").encode())
            await writer.drain()
            try:
                line = await reader.readline()
            except ValueError:
                writer.write(b'{"ok":false,"err":"EARG"}\n')
                return

    async def handle(reader, writer):
        try:
            try:
                first = await reader.readline()
            except ValueError:
                first = None
                writer.write(b'{"ok":false,"err":"EARG"}\n')
            if first and first.split(b" ")[0] in (b"GET", b"HEAD", b"POST", b"PUT", b"OPTIONS") \
                    and first.rstrip().endswith((b"HTTP/1.1", b"HTTP/1.0")):
                if await handshake(reader, writer, first):
                    async for payload in messages(reader, writer):
                        for req in _requests(payload):
                            resp = dispatch(head, req)
                            writer.write(_frame(0x1, json.dumps(resp, separators=(",", ":")).encode()))
                        await writer.drain()
            elif first:
                await lines(reader, writer, first)
            await writer.drain()
        except (ConnectionError, asyncio.IncompleteReadError, asyncio.LimitOverrunError):
            pass
        finally:
            writer.close()

    srv = await asyncio.start_server(handle, host, port, limit=16384)
    print("bench head %s on %s:%d (JSON lines, or ws://%s:%d/)  instance %s"
          % (HEAD_NAME, host, port, host, port, head.instance.hex()), flush=True)
    async with srv:
        await srv.serve_forever()


# ---------------------------------------------------------------------------- client
class Link:
    """Client for a bench or field head.

        Link("HOST", PORT)        a plain connection, one JSON object per line - a bench
                                  head, or the local port of `cvconnect.py -l PORT wss://...`
        Link("ws://HOST:PORT/")   a WebSocket, one JSON request per message
        Link("wss://HOST/path/")  the same over TLS
        Link(..., log="session.jsonl") appends every SOUND exchange to that file
    """

    def __init__(self, target, port=None, session=None, log=None, timeout=60):
        if port is not None:
            self.ws = False
            self.sock = socket.create_connection((target, port), timeout=timeout)
            self.f = self.sock.makefile("rb")
        else:
            self.ws = True
            self._upgrade(target, timeout)
        self.log = open(log, "a", encoding="utf-8") if log else None
        self.session = session
        self.t = None

    def _upgrade(self, url, timeout):
        u = urllib.parse.urlsplit(url)
        if u.scheme not in ("ws", "wss") or not u.hostname:
            raise ValueError("expected HOST, PORT or a ws:// / wss:// URL, got %r" % url)
        tls = u.scheme == "wss"
        port = u.port or (443 if tls else 80)
        self.sock = socket.create_connection((u.hostname, port), timeout=timeout)
        if tls:
            self.sock = ssl.create_default_context().wrap_socket(self.sock, server_hostname=u.hostname)
        self.f = self.sock.makefile("rb")
        host = "[%s]" % u.hostname if ":" in u.hostname else u.hostname
        key = base64.b64encode(os.urandom(16))
        path = (u.path or "/") + ("?" + u.query if u.query else "")
        self.sock.sendall(b"GET %s HTTP/1.1\r\nHost: %s:%d\r\nUpgrade: websocket\r\n"
                          b"Connection: Upgrade\r\nSec-WebSocket-Key: %s\r\n"
                          b"Sec-WebSocket-Version: 13\r\n\r\n"
                          % (path.encode(), host.encode(), port, key))
        status = self.f.readline()
        while self.f.readline() not in (b"\r\n", b"\n", b""):
            pass
        if b" 101 " not in status:
            raise ConnectionError("no WebSocket upgrade: %r" % status.rstrip())

    def _read(self, n):
        data = self.f.read(n)
        if len(data) < n:
            raise ConnectionError("head closed the connection")
        return data

    def send(self, text):
        """One request: a line, or one text message."""
        data = text.encode() if isinstance(text, str) else text
        if self.ws:
            self.sock.sendall(_frame(0x1, data, os.urandom(4)))
        else:
            self.sock.sendall(data.rstrip(b"\n") + b"\n")

    def recv(self):
        """One response: a line, or one message."""
        if not self.ws:
            line = self.f.readline()
            if not line:
                raise ConnectionError("head closed the connection")
            return line.decode()
        parts = []
        while True:
            b0, b1 = self._read(2)
            opcode, n = b0 & 0x0F, b1 & 0x7F
            if n == 126:
                n = int.from_bytes(self._read(2), "big")
            elif n == 127:
                n = int.from_bytes(self._read(8), "big")
            mask = self._read(4) if b1 & 0x80 else None
            data = self._read(n) if n else b""
            if mask:
                data = _xor4(data, mask)
            if opcode == 0x8:
                raise ConnectionError("head closed the connection (%s)"
                                      % (int.from_bytes(data[:2], "big") if len(data) >= 2 else "-"))
            if opcode == 0x9:
                self.sock.sendall(_frame(0xA, data, os.urandom(4)))
                continue
            if opcode == 0xA:
                continue
            parts.append(data)
            if b0 & 0x80:
                return b"".join(parts).decode()

    def call(self, obj):
        self.send(json.dumps(obj, separators=(",", ":")))
        return json.loads(self.recv())

    def open(self):
        r = self.call({"cmd": "OPEN"})
        if r.get("ok"):
            self.session, self.t = r["session"], r["t"]
        return r

    def hello(self):
        r = self.call({"cmd": "HELLO", "session": self.session})
        self.t = r.get("t")
        return r

    def sound(self, row, syms):
        """syms: str of hex digits or list of ints 0..15."""
        if not isinstance(syms, str):
            syms = "".join("%x" % s for s in syms)
        if self.t is None:
            self.hello()
        t0 = self.t
        r = self.call({"cmd": "SOUND", "session": self.session, "t": t0, "row": row, "syms": syms})
        if "t" in r:
            self.t = r["t"]
        if r.get("ok") and self.log:
            self.log.write(json.dumps({"kind": "sound", "t": t0, "row": row, "syms": syms,
                                       "bits": r["bits"]}) + "\n")
            self.log.flush()
        return r

    def checkpoint(self, row, grades):
        if not isinstance(grades, str):
            grades = "".join(str(g) for g in grades)
        return self.call({"cmd": "CHECKPOINT", "session": self.session, "row": row, "grades": grades})

    def bundle(self):
        return bytes.fromhex(self.call({"cmd": "BUNDLE", "session": self.session})["bundle"])

    def close(self):
        if self.ws:
            try:
                self.sock.sendall(_frame(0x8, (1000).to_bytes(2, "big"), os.urandom(4)))
            except OSError:
                pass
        for x in (self.f, self.sock, self.log):
            try:
                if x:
                    x.close()
            except OSError:
                pass


# ---------------------------------------------------------------------------- factory
def factory(path):
    with open(path, encoding="utf-8") as fh:
        recs = [json.loads(line) for line in fh if line and not line.isspace()]
    hdr = recs[0]
    assert hdr["kind"] == "factory", "first record must be the factory header"
    rows = [[int(c) for c in r] for r in hdr["table"]]
    instance, session = bytes.fromhex(hdr["instance"]), bytes.fromhex(hdr["session"])
    s = BenchSession(rows, instance, session, bytes.fromhex(hdr["coin_key"]),
                     bytes.fromhex(hdr["bundle"])[:12])
    n_sound = n_ok = 0
    for r in recs[1:]:
        if r["kind"] == "sound":
            assert r["t"] == s.t, "t out of order at %d" % r["t"]
            bits = s.sound(r["row"], [int(c, 16) for c in r["syms"]])
            assert bits == r["bits"], "bits differ in the block at t=%d" % r["t"]
            n_sound += len(r["syms"])
        elif r["kind"] == "checkpoint":
            ok = s.checkpoint(r["row"], [int(c) for c in r["grades"]])
            assert ok == r["ok"], "checkpoint outcome differs for row %d" % r["row"]
            n_ok += ok
    text = open_bundle(rows, instance, session, bytes.fromhex(hdr["bundle"])).decode()
    print("factory session reproduces: %d soundings, %d rows confirmed, bundle opens:"
          % (n_sound, n_ok))
    for line in text.splitlines():
        print("  | " + line)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="NEVE NV-3.4 bench model")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("serve", help="run a bench head")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=19640)
    p.add_argument("--seed", type=int)
    p = sp.add_parser("factory", help="replay the factory session")
    p.add_argument("path", nargs="?", default=os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "factory_session.jsonl"))
    a = ap.parse_args(argv)
    if a.cmd == "serve":
        try:
            asyncio.run(_serve(a.host, a.port, a.seed))
        except KeyboardInterrupt:
            pass
        return 0
    return factory(a.path)


if __name__ == "__main__":
    sys.exit(main())
