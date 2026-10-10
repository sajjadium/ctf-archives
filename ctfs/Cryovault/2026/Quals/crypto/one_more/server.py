#!/usr/bin/env python3
"""
one-more  --  a blind Schnorr signing service (secp256k1).

Talk to it one command per message:

    open                  -> "id <k> R <hex64>"      opens a signing session
    sign <k> <c>          -> "s <int>"               one challenge per session
    submit                -> then send ONE more message, a JSON line:
                             [[msg_hex, Rx, Ry, s], ...]
    quit

On connect the service sends "X <hex64>" -- its public key for THIS connection.
Every connection is an independent instance with its own fresh key.

A signature (R, s) on m is valid iff   s*G == R + H(R,m)*X,
with H(R,m) = SHA256(x||y||m) mod n.

The service is blind: it never sees the message, only the scalar challenge you
hand it, and it answers each session exactly once. So it signs once per
session, and you walk away with one signature per session. That is the deal.

Hand back MORE valid signatures, on distinct messages, than the number of
challenges I answered, and you get the flag.

    python3 server.py                  # WebSocket on ws://127.0.0.1:1337
    python3 server.py --stdio          # one command per line on stdin
"""
import asyncio
import json
import os
import secrets
import hashlib
import sys
from pathlib import Path

from websockets.exceptions import ConnectionClosed

from ecdsa.curves import SECP256k1
from ecdsa.ellipticcurve import Point

G = SECP256k1.generator
N = int(SECP256k1.order)

MAX_SESSIONS = 512          # "open" calls per connection
MAX_SUBMIT   = 600          # signatures accepted in one submit (CPU bound)
MAX_COMMANDS = 2 * MAX_SESSIONS + 64
MAX_MESSAGE  = 4 << 20      # bytes
CONN_TIMEOUT = 1800         # seconds per connection (ref attack ~220s over WAN)
MAX_CONCURRENT = 512        # simultaneous connections (longer timeout = more overlap)


def ser(P):
    return int(P.x()).to_bytes(32, "big") + int(P.y()).to_bytes(32, "big")


def H(R, m):
    return int.from_bytes(hashlib.sha256(ser(R) + m).digest(), "big") % N


def flag(strict):
    env = os.environ.get("ONE_MORE_FLAG")
    if env:
        return env.strip()
    p = Path(__file__).with_name("flag.txt")
    if p.exists():
        return p.read_text().strip()
    if strict:
        sys.exit("refusing to serve: no flag.txt beside server.py and no "
                 "ONE_MORE_FLAG in the environment")
    return "isfcr{placeholder__real_flag_is_on_the_live_service}"


class Session:
    """The whole challenge. One instance per connection; nothing is shared."""

    def __init__(self, flag_value):
        self.x = secrets.randbelow(N)
        self.X = G * self.x
        self.pending = {}       # session id -> nonce r  (removed once signed)
        self.opened = 0
        self.answered = 0       # how many challenges we actually signed
        self.commands = 0
        self.expect_json = False
        self.done = False
        self.flag = flag_value

    def greeting(self):
        return "X " + ser(self.X).hex()

    def feed(self, line):
        """Map one input message to a list of reply messages."""
        self.commands += 1
        if self.commands > MAX_COMMANDS:
            self.done = True
            return ["err too many commands"]

        if self.expect_json:
            self.expect_json = False
            self.done = True
            return self._judge(line)

        parts = line.split()
        if not parts:
            return []
        cmd = parts[0]

        if cmd == "open":
            if self.opened >= MAX_SESSIONS:
                return ["err too many sessions"]
            r = secrets.randbelow(N)
            self.pending[self.opened] = r
            out = f"id {self.opened} R {ser(G * r).hex()}"
            self.opened += 1
            return [out]

        if cmd == "sign":
            try:
                k, c = int(parts[1]), int(parts[2]) % N
            except (IndexError, ValueError):
                return ["err usage: sign <id> <c>"]
            if k not in self.pending:
                return ["err no such open session"]
            r = self.pending.pop(k)          # one answer per session
            self.answered += 1
            return [f"s {(r + c * self.x) % N}"]

        if cmd == "submit":
            self.expect_json = True
            return []

        if cmd == "quit":
            self.done = True
            return []

        return ["err unknown command"]

    def _judge(self, raw):
        try:
            sigs = json.loads(raw)
            if not isinstance(sigs, list):
                raise ValueError
        except Exception:
            return ["err bad json"]
        if len(sigs) > MAX_SUBMIT:
            return [f"err at most {MAX_SUBMIT} signatures"]

        seen, good = set(), 0
        for item in sigs:
            try:
                m_hex, rx, ry, s = item
                m = bytes.fromhex(m_hex)
            except Exception:
                continue
            if m in seen:
                continue
            try:
                R = Point(SECP256k1.curve, int(rx), int(ry))
            except Exception:
                continue                     # not on the curve
            if G * (int(s) % N) == R + self.X * H(R, m):
                seen.add(m)
                good += 1

        out = [f"valid {good} answered {self.answered}"]
        if good > self.answered:
            out.append(f"one more! {self.flag}")
        else:
            out.append("that is not more than I gave you.")
        return out


# ---------------------------------------------------------------- websocket

async def ws_main(host, port):
    from websockets.asyncio.server import serve

    flag_value = flag(strict=True)
    gate = asyncio.Semaphore(MAX_CONCURRENT)

    async def handler(ws):
        if gate.locked():
            await ws.send("err server busy, try again shortly")
            return
        async with gate:
            sess = Session(flag_value)
            await ws.send(sess.greeting())
            try:
                async with asyncio.timeout(CONN_TIMEOUT):
                    async for msg in ws:
                        if isinstance(msg, bytes):
                            msg = msg.decode("utf-8", "replace")
                        # EC work is CPU-bound: keep the event loop free
                        for reply in await asyncio.to_thread(sess.feed, msg):
                            await ws.send(reply)
                        if sess.done:
                            break
            except (TimeoutError, asyncio.TimeoutError):
                try:
                    await ws.send("err connection timed out")
                except Exception:
                    pass
            except ConnectionClosed:
                pass
            except Exception as e:
                print(f"handler error: {type(e).__name__}: {e}",
                      file=sys.stderr, flush=True)

    async with serve(handler, host, port,
                     max_size=MAX_MESSAGE,
                     ping_interval=20, ping_timeout=20):
        print(f"one-more listening on ws://{host}:{port}", file=sys.stderr)
        await asyncio.get_running_loop().create_future()


# -------------------------------------------------------------------- stdio

def stdio_main():
    sess = Session(flag(strict=False))
    out = sys.stdout
    out.write(sess.greeting() + "\n")
    out.flush()
    for line in sys.stdin:
        for reply in sess.feed(line):
            out.write(reply + "\n")
        out.flush()
        if sess.done:
            return


if __name__ == "__main__":
    if "--stdio" in sys.argv:
        stdio_main()
    else:
        h = os.environ.get("ONE_MORE_HOST", "127.0.0.1")
        p = int(os.environ.get("ONE_MORE_PORT", "1337"))
        asyncio.run(ws_main(h, p))
