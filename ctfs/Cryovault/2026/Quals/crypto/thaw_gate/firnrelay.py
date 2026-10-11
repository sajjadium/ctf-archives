#!/usr/bin/env python3
"""
firnrelay - operator-side library for the SASTRUGI thaw gateway.

Wire protocol 1, as specified for gateway firmware 2.6 in PROTOCOL.md. Where this file
and PROTOCOL.md disagree, PROTOCOL.md wins and this file has a bug.

Contents:
  - P-256 point encoding, validation and ECDH (pycryptodome does the arithmetic)
  - the length-prefixed encoding used by every transcript, MAC input and signature
  - HKDF-SHA256 and the session key schedule
  - the frame codec: AES-256-GCM plus an HMAC-SHA256 commitment
  - deterministic Schnorr signatures over P-256 (badge commits, gateway postings,
    release tokens)
  - parsers for resumption tickets and release tokens
  - a line-JSON client (it starts or rejoins a session of the shared service) with the
    OPEN, RESUME and CONFIRM handshakes and a frame session object

Requires pycryptodome (pip install pycryptodome).
"""

import hashlib
import hmac
import json
import secrets
import socket
import struct

from Crypto.Cipher import AES
from Crypto.PublicKey.ECC import EccPoint

# --------------------------------------------------------------------------- P-256
P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
GX = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
GY = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
BASE = EccPoint(GX, GY, curve="p256")

PROTO = b"SASTRUGI/1"
GATEWAY_ROLE_TAG = hashlib.sha256(b"SASTRUGI/1/gateway-role").digest()[:8]
DENIED = {"ok": False, "err": "EDENIED"}

C2G = 0     # frame direction byte: operator to gateway
G2C = 1     # frame direction byte: gateway to operator

TICKET_MAGIC = b"SASTRUGI-TKT/1\x00\x00"
TOKEN_MAGIC = b"SASTRUGI-REL/1\x00\x00"
TICKET_BLOB_LEN = 56
TICKET_LEN = TICKET_BLOB_LEN + 32
TOKEN_BLOB_LEN = 100
SIG_LEN = 97
TOKEN_LEN = TOKEN_BLOB_LEN + SIG_LEN


class ProtocolError(Exception):
    """Raised for anything malformed or unverifiable on either side of the wire."""


class Denied(Exception):
    """The gateway answered with its refusal line."""


def u8(x):
    return struct.pack(">B", x)


def u32(x):
    return struct.pack(">I", x)


def u64(x):
    return struct.pack(">Q", x)


def lp(*parts):
    """Length-prefixed concatenation: each part is a 4-byte big-endian length followed
    by its bytes. Every transcript, MAC input, KDF info and signed message uses it."""
    out = []
    for p in parts:
        if isinstance(p, str):
            p = p.encode()
        out.append(struct.pack(">I", len(p)))
        out.append(p)
    return b"".join(out)


def sha256(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(p)
    return h.digest()


def hm(key, *parts):
    """HMAC-SHA256 over the plain concatenation of parts."""
    return hmac.new(key, b"".join(parts), hashlib.sha256).digest()


def ct_eq(a, b):
    return hmac.compare_digest(a, b)


def hkdf_extract(salt, ikm):
    return hm(salt, ikm)


def hkdf_expand(prk, info, length=32):
    out, block, i = b"", b"", 1
    while len(out) < length:
        block = hm(prk, block, info, bytes([i]))
        out += block
        i += 1
    return out[:length]


def wide_scalar(key, *parts):
    """wide(key, parts...) of PROTOCOL.md section 0: a scalar in [1, N-1]."""
    a = hm(key, lp(b"SASTRUGI/1/scalar", b"\x01", *parts))
    b = hm(key, lp(b"SASTRUGI/1/scalar", b"\x02", *parts))
    return int.from_bytes(a + b, "big") % (N - 1) + 1


# --------------------------------------------------------------------------- points
def pt_encode(pt):
    if pt.is_point_at_infinity():
        raise ProtocolError("point at infinity has no encoding")
    return b"\x04" + int(pt.x).to_bytes(32, "big") + int(pt.y).to_bytes(32, "big")


def pt_decode(data):
    """SEC1 uncompressed only. Rejects bad length, bad prefix, coordinates >= p,
    off-curve points and the identity."""
    if not isinstance(data, (bytes, bytearray)) or len(data) != 65 or data[0] != 4:
        raise ProtocolError("bad point encoding")
    x = int.from_bytes(data[1:33], "big")
    y = int.from_bytes(data[33:], "big")
    if x >= P or y >= P:
        raise ProtocolError("bad point encoding")
    try:
        pt = EccPoint(x, y, curve="p256")
    except ValueError:
        raise ProtocolError("point not on P-256")
    if pt.is_point_at_infinity():
        raise ProtocolError("identity point")
    return pt


def base_mult(k):
    return BASE * k


def ecdh(k, pt):
    """x-coordinate of k*pt, 32 bytes."""
    r = pt * k
    if r.is_point_at_infinity():
        raise ProtocolError("degenerate shared point")
    return int(r.x).to_bytes(32, "big")


def scalar_bytes(k):
    return int(k).to_bytes(32, "big")


def random_scalar():
    return secrets.randbelow(N - 1) + 1


# --------------------------------------------------------------------------- Schnorr
def schnorr_nonce(d, msg):
    """k = wide(d, "nonce", m), PROTOCOL.md section 0."""
    return wide_scalar(scalar_bytes(d), b"nonce", msg)


def schnorr_challenge(r_enc, q_enc, msg):
    return int.from_bytes(sha256(lp(b"SASTRUGI/1/schnorr", r_enc, q_enc, msg)), "big") % N


def schnorr_sign(d, msg):
    q_enc = pt_encode(base_mult(d))
    k = schnorr_nonce(d, msg)
    r_enc = pt_encode(base_mult(k))
    e = schnorr_challenge(r_enc, q_enc, msg)
    s = (k + e * d) % N
    return r_enc + s.to_bytes(32, "big")


def schnorr_verify(q_pt, msg, sig):
    if not isinstance(sig, (bytes, bytearray)) or len(sig) != SIG_LEN:
        return False
    try:
        r_pt = pt_decode(bytes(sig[:65]))
    except ProtocolError:
        return False
    s = int.from_bytes(sig[65:], "big")
    if s >= N:
        return False
    e = schnorr_challenge(bytes(sig[:65]), pt_encode(q_pt), msg)
    lhs = base_mult(s)
    rhs = r_pt + q_pt * e
    if lhs.is_point_at_infinity() or rhs.is_point_at_infinity():
        return False
    return int(lhs.x) == int(rhs.x) and int(lhs.y) == int(rhs.y)


# --------------------------------------------------------------------------- messages
def commit_message(instance_id, watch, kind, role_tag, manifest):
    return lp(b"SASTRUGI/1/commit", instance_id, u32(watch), kind, role_tag, manifest)


def posting_message(instance_id, watch, slot, slots, arm_tag, cs_tag):
    return lp(b"SASTRUGI/1/posting", instance_id, u32(watch), u8(slot), u8(slots),
              arm_tag, cs_tag)


def beat_answer(beat_key, instance_id, watch, beat, challenge, role_tag):
    return hm(beat_key, lp(b"SASTRUGI/1/beat", instance_id, u32(watch), u32(beat),
                           challenge, role_tag))


def board_digest(entries):
    """entries: list of (badge, role_tag, kind, manifest) in deposit order."""
    return sha256(lp(b"SASTRUGI/1/board", *[lp(b, r, k, m) for (b, r, k, m) in entries]))


def badge_field(badge_id):
    raw = badge_id.encode()
    if not 1 <= len(raw) <= 8:
        raise ProtocolError("badge id must be 1..8 bytes")
    return raw + b"\x00" * (8 - len(raw))


def parse_ticket(ticket):
    """Split a resumption ticket into its fields (PROTOCOL.md section 3.6)."""
    if not isinstance(ticket, (bytes, bytearray)) or len(ticket) != TICKET_LEN:
        raise ProtocolError("bad ticket length")
    blob = bytes(ticket[:TICKET_BLOB_LEN])
    if blob[:16] != TICKET_MAGIC:
        raise ProtocolError("bad ticket magic")
    mint_watch, serial = struct.unpack(">II", blob[48:56])
    return {
        "instance": blob[16:32].hex(),
        "badge": blob[32:40].rstrip(b"\x00").decode("ascii", "replace"),
        "role": blob[40:48].hex(),
        "mint_watch": mint_watch,
        "serial": serial,
        "tag": bytes(ticket[TICKET_BLOB_LEN:]).hex(),
    }


def parse_token(token):
    if not isinstance(token, (bytes, bytearray)) or len(token) != TOKEN_LEN:
        raise ProtocolError("bad token length")
    blob = bytes(token[:TOKEN_BLOB_LEN])
    if blob[:16] != TOKEN_MAGIC:
        raise ProtocolError("bad token magic")
    (watch,) = struct.unpack(">I", blob[32:36])
    return {"instance": blob[16:32].hex(), "watch": watch, "manifest": blob[36:68].hex(),
            "board": blob[68:100].hex(), "sig": bytes(token[TOKEN_BLOB_LEN:]).hex()}


def verify_token(gateway_pt, token):
    return (isinstance(token, (bytes, bytearray)) and len(token) == TOKEN_LEN
            and token[:16] == TOKEN_MAGIC
            and schnorr_verify(gateway_pt, bytes(token[:TOKEN_BLOB_LEN]),
                               bytes(token[TOKEN_BLOB_LEN:])))


def verify_posting(gateway_pt, instance_id, posting):
    try:
        msg = posting_message(instance_id, posting["w"], posting["slot"], posting["of"],
                              bytes.fromhex(posting["duty"]["arm"]),
                              bytes.fromhex(posting["duty"]["cs"]))
        return schnorr_verify(gateway_pt, msg, bytes.fromhex(posting["sig"]))
    except (KeyError, TypeError, ValueError, struct.error):
        return False


def manifest_digest(manifest_obj):
    """SHA-256 of the canonical JSON form: sorted keys, no whitespace, UTF-8."""
    blob = json.dumps(manifest_obj, sort_keys=True, separators=(",", ":")).encode()
    return sha256(blob)


# --------------------------------------------------------------------------- key schedule
KEY_LABELS = ("conf", "c2g", "c2g cm", "g2c", "g2c cm", "beat")


def session_keys(transcript_hash, ikm):
    prk = hkdf_extract(transcript_hash, ikm)
    return {lab: hkdf_expand(prk, lp(b"SASTRUGI/1/key", lab, transcript_hash))
            for lab in KEY_LABELS}


def confirm_mac(conf_key, role_tag, transcript_hash):
    return hm(conf_key, lp(b"SASTRUGI/1/confirm", role_tag, transcript_hash))


def open_transcript(instance_id, gateway_enc, badge_id, badge_enc, eph_c_enc,
                    eph_g_enc, sid):
    return lp(b"SASTRUGI/1/open", instance_id, gateway_enc, badge_id, badge_enc,
              eph_c_enc, eph_g_enc, sid)


def resume_offer(instance_id, gateway_enc, ticket, eph_c_enc):
    return lp(b"SASTRUGI/1/resume", instance_id, gateway_enc, ticket, eph_c_enc)


def resume_binder(rms, offer):
    return hm(rms, lp(b"SASTRUGI/1/binder", sha256(offer)))


def resume_transcript(offer, eph_g_enc, sid):
    return offer + lp(eph_g_enc, sid)


# --------------------------------------------------------------------------- frames
def frame_nonce(direction, seq):
    return b"\x00\x00\x00" + bytes([direction]) + u64(seq)


def frame_aad(sid, seq, direction):
    return lp(b"SASTRUGI/1/frame", sid, u64(seq), bytes([direction]))


def seal_frame(enc_key, cm_key, sid, seq, direction, body):
    """-> (ct, cm). ct is the GCM ciphertext with its 16-byte tag appended; cm is the
    commitment HMAC over aad, nonce and ct."""
    nonce = frame_nonce(direction, seq)
    aad = frame_aad(sid, seq, direction)
    c = AES.new(enc_key, AES.MODE_GCM, nonce=nonce)
    c.update(aad)
    ct, tag = c.encrypt_and_digest(body)
    ct = ct + tag
    return ct, hm(cm_key, lp(aad, nonce, ct))


def open_frame(enc_key, cm_key, sid, seq, direction, ct, cm):
    """-> the frame body (PROTOCOL.md section 3.4). Raises ProtocolError on any failure."""
    if not isinstance(ct, (bytes, bytearray)) or len(ct) < 16:
        raise ProtocolError("short frame")
    nonce = frame_nonce(direction, seq)
    aad = frame_aad(sid, seq, direction)
    if not ct_eq(hm(cm_key, lp(aad, nonce, bytes(ct))), bytes(cm)):
        raise ProtocolError("commitment mismatch")
    c = AES.new(enc_key, AES.MODE_GCM, nonce=nonce)
    c.update(aad)
    try:
        return c.decrypt_and_verify(bytes(ct[:-16]), bytes(ct[-16:]))
    except ValueError:
        raise ProtocolError("gcm tag mismatch")


# --------------------------------------------------------------------------- files
class Badge:
    def __init__(self, badge_id, d, role_name):
        self.id = badge_id
        self.d = d
        self.Q = base_mult(d)
        self.role_name = role_name

    @property
    def public(self):
        return pt_encode(self.Q)


def load_badge(path):
    with open(path, encoding="utf-8") as f:
        b = json.load(f)
    badge = Badge(b["badge"], int(b["d"], 16), b["role"])
    if badge.public.hex() != b["Q"]:
        raise ProtocolError("badge file is inconsistent")
    return badge


def load_roster(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------- client
class Wire:
    """One TCP connection, one JSON object per line in each direction.

    The service is shared. The first line of a connection picks a session, which is a
    gateway instance of its own: Wire(host, port) starts a new one, and its token is
    Wire.session; Wire(host, port, session=token) joins that session again, from this or
    any other connection. Connections in different sessions reach different instances."""

    def __init__(self, host, port, timeout=30.0, session=None):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.rfile = self.sock.makefile("rb")
        self.sent = 0
        if session is None:
            r = self.request({"op": "SESSION"})
        else:
            r = self.request({"op": "RESUME", "token": session})
        if not r.get("ok"):
            self.close()
            raise Denied(r)
        self.session = r["session"]

    def request(self, obj):
        self.sock.sendall(json.dumps(obj, separators=(",", ":")).encode() + b"\n")
        self.sent += 1
        line = self.rfile.readline()
        if not line:
            raise ConnectionError("gateway closed the connection")
        return json.loads(line.decode())

    def close(self):
        try:
            self.rfile.close()
        finally:
            self.sock.close()


class Gateway:
    """What HELLO says about the instance you are connected to."""

    def __init__(self, hello):
        if not hello.get("ok"):
            raise Denied(hello)
        self.hello = hello
        self.instance_id = bytes.fromhex(hello["instance"])
        self.G_enc = bytes.fromhex(hello["G"])
        self.G = pt_decode(self.G_enc)


class Session:
    """An established session: frame keys, sequence numbers, identity and role.

    Construct with Session.open(...) or Session.resume(...)."""

    def __init__(self, wire, gw, sid, keys, badge_id, role_tag):
        self.wire = wire
        self.gw = gw
        self.sid = sid
        self.keys = keys
        self.badge_id = badge_id
        self.role = role_tag
        self.c2g_seq = 0
        self.g2c_seq = 0
        self.established = None
        self.last = None          # last full cleartext response (fresh echo, posting)

    # -- handshakes ----------------------------------------------------------
    @classmethod
    def open(cls, wire, gw, badge, eph=None):
        ec = eph or random_scalar()
        ec_enc = pt_encode(base_mult(ec))
        r = wire.request({"op": "OPEN", "badge": badge.id, "e": ec_enc.hex()})
        if not r.get("ok"):
            raise Denied(r)
        sid = bytes.fromhex(r["sid"])
        eg_enc = bytes.fromhex(r["e"])
        eg = pt_decode(eg_enc)
        role = bytes.fromhex(r["role"])
        th = sha256(open_transcript(gw.instance_id, gw.G_enc, badge.id.encode(),
                                    badge.public, ec_enc, eg_enc, sid))
        ikm = ecdh(ec, eg) + ecdh(ec, gw.G) + ecdh(badge.d, eg)
        keys = session_keys(th, ikm)
        if not ct_eq(confirm_mac(keys["conf"], GATEWAY_ROLE_TAG, th), bytes.fromhex(r["conf"])):
            raise ProtocolError("gateway confirmation does not verify")
        s = cls(wire, gw, sid, keys, badge.id, role)
        s._confirm(confirm_mac(keys["conf"], role, th))
        return s

    @classmethod
    def resume(cls, wire, gw, ticket, rms, eph=None):
        """Resume with a ticket and its resumption secret (PROTOCOL.md section 3.3)."""
        role_tag = bytes.fromhex(parse_ticket(ticket)["role"])
        ec = eph or random_scalar()
        ec_enc = pt_encode(base_mult(ec))
        offer = resume_offer(gw.instance_id, gw.G_enc, ticket, ec_enc)
        r = wire.request({"op": "RESUME", "ticket": ticket.hex(), "role": role_tag.hex(),
                          "e": ec_enc.hex(), "binder": resume_binder(rms, offer).hex()})
        if not r.get("ok"):
            raise Denied(r)
        sid = bytes.fromhex(r["sid"])
        eg_enc = bytes.fromhex(r["e"])
        eg = pt_decode(eg_enc)
        th = sha256(resume_transcript(offer, eg_enc, sid))
        keys = session_keys(th, rms + ecdh(ec, eg))
        if not ct_eq(confirm_mac(keys["conf"], GATEWAY_ROLE_TAG, th), bytes.fromhex(r["conf"])):
            raise ProtocolError("gateway confirmation does not verify")
        s = cls(wire, gw, sid, keys, parse_ticket(ticket)["badge"], role_tag)
        s._confirm(confirm_mac(keys["conf"], role_tag, th))
        return s

    def _confirm(self, conf):
        r = self.wire.request({"op": "CONFIRM", "sid": self.sid.hex(), "conf": conf.hex()})
        if not r.get("ok"):
            raise Denied(r)
        self.established = self._open_reply(r)
        self.last = r

    # -- frames --------------------------------------------------------------
    def _open_reply(self, r):
        if r.get("sid") != self.sid.hex() or r.get("seq") != self.g2c_seq:
            raise ProtocolError("unexpected frame header from gateway")
        body = open_frame(self.keys["g2c"], self.keys["g2c cm"], self.sid, self.g2c_seq,
                          G2C, bytes.fromhex(r["ct"]), bytes.fromhex(r["cm"]))
        self.g2c_seq += 1
        return json.loads(body.decode())

    def call(self, body):
        """Send one frame body (a dict), return the gateway's decrypted answer (a dict).
        A refusal raises Denied and leaves both sequence numbers where they were."""
        raw = json.dumps(body, separators=(",", ":")).encode()
        ct, cm = seal_frame(self.keys["c2g"], self.keys["c2g cm"], self.sid, self.c2g_seq,
                            C2G, raw)
        r = self.wire.request({"op": "FRAME", "sid": self.sid.hex(), "seq": self.c2g_seq,
                               "ct": ct.hex(), "cm": cm.hex()})
        if not r.get("ok"):
            raise Denied(r)
        self.c2g_seq += 1
        self.last = r
        return self._open_reply(r)

    # -- conveniences ----------------------------------------------------------
    def beat(self, watch, beat, challenge):
        a = beat_answer(self.keys["beat"], self.gw.instance_id, watch, beat, challenge,
                        self.role)
        return self.call({"t": "BEAT", "w": watch, "n": beat, "a": a.hex()})

    def commit(self, badge, kind, manifest, watch):
        sig = schnorr_sign(badge.d, commit_message(self.gw.instance_id, watch, kind.encode(),
                                                   self.role, manifest))
        return self.call({"t": "COMMIT", "kind": kind, "manifest": manifest.hex(),
                          "role": self.role.hex(), "sig": sig.hex()})
