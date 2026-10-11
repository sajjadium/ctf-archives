# SASTRUGI thaw gateway - wire protocol 1

This document specifies gateway firmware 2.6.0.

## 0. Notation

| Notation | Meaning |
|---|---|
| `lp(x1, ..., xk)` | for each part in order: its length as a 4-byte big-endian integer, then its bytes. Strings are UTF-8 |
| `u8(x)`, `u32(x)`, `u64(x)` | big-endian unsigned integers of 1, 4 and 8 bytes |
| `a \|\| b` | byte concatenation |
| `H(m)` | SHA-256 |
| `HMAC(k, m)` | HMAC-SHA256 |
| `HKDF-Extract`, `HKDF-Expand` | RFC 5869 with SHA-256 |
| `n`, `B` | the group order and the base point of P-256 |
| points | SEC1 uncompressed, 65 bytes. A received point must be on P-256 and not the identity |
| `x(P)` | the x-coordinate of P as 32 big-endian bytes |
| `wide(k, p1, ..., pj)` | `(int(HMAC(k, lp("SASTRUGI/1/scalar", 0x01, p1, ..., pj)) \|\| HMAC(k, lp("SASTRUGI/1/scalar", 0x02, p1, ..., pj))) mod (n - 1)) + 1` |
| on the wire | one JSON object per line in each direction; every byte string is lowercase hex |

**Schnorr signatures** (badge commits, gateway postings, release tokens). Secret d, public
Q = d·B, message m:

- k = wide(d as 32 big-endian bytes, "nonce", m); R = k·B
- e = int(H(lp("SASTRUGI/1/schnorr", R, Q, m))) mod n
- s = (k + e·d) mod n
- signature = R (65 bytes) || s (32 bytes); valid iff R is a valid point, s < n and
  s·B = R + e·Q

**Manifest digest**: H of the manifest's canonical JSON (keys sorted, no whitespace,
UTF-8). `roster.json` carries the canonical thaw manifest and its digest.

## 1. Model

Badges sign in to the gateway and hold sessions. Every session has a badge and a role
tag. Time at the gateway is counted in beats, not seconds: the gateway publishes a beat
challenge, a live session answers it, and the next challenge depends on that answer.
Beats are grouped into watches; the duty rota assigns each watch a pair of roles on duty.
Co-authorisations (commits) are deposited on the board of the current watch.

## 2. Keys

### 2.1 Fixed values

`GATEWAY_ROLE_TAG = H("SASTRUGI/1/gateway-role")[0:8]`

### 2.2 Per-instance key schedule

Every instance has a 256-bit master M, chosen when the instance is provisioned. Live
masters are never transmitted; a decommissioned instance's master is published with its
records.

With `ks(label) = HMAC(M, lp("SASTRUGI/1/ks", label))`:

| Value | Definition |
|---|---|
| instance id | `ks("instance")[0:16]` |
| gateway static scalar g | `wide(M, "gateway static")`; G = g·B |
| `K_eph` | `ks("ephemeral")`; the gateway ephemeral scalar of the handshake with session id sid and operator ephemeral point E is `wide(K_eph, sid, E)` |
| `K_sid` | `ks("sid")`; the session id of the i-th handshake of the instance (i = 1, 2, ...) is `HMAC(K_sid, lp("SASTRUGI/1/sid", u64(i)))[0:16]` |
| `K_role` | `ks("role")`; the role tag of role name r is `HMAC(K_role, lp("SASTRUGI/1/role", r))[0:8]` |
| `K_fresh` | `ks("fresh")`; the beat chain, section 3.5 |
| `K_ticket` | `ks("ticket")`; the ticket tag, section 3.6 |

## 3. Messages

A refused request, of any kind, is answered with `{"ok":false,"err":"EDENIED"}`.

### 3.1 HELLO

`{"op":"HELLO"}` is answered with
`{"ok":true,"gateway":"SASTRUGI thaw gateway","fw":"2.6.0","proto":1,"instance":...,"G":...,"posting":...,"fresh":...}`.

A *posting* is `{"w":w,"slot":slot,"of":L,"duty":{"arm":tag,"cs":tag},"sig":signature}`,
where L is the rota length and the signature is the gateway's (key g) over
`lp("SASTRUGI/1/posting", instance id, u32(w), u8(slot), u8(L), arm tag, cs tag)`.

The *freshness echo* is `{"w":w,"n":n,"c":c}`: the current watch, the number of beats
answered in it, and the current beat challenge. Every successful answer carries it as
`"fresh"`.

### 3.2 Signed messages

| Message | Bytes signed |
|---|---|
| commit | `lp("SASTRUGI/1/commit", instance id, u32(w), kind, role tag, manifest digest)`, kind = "ARM" or "CS", signed by the badge |
| posting | section 3.1, signed by the gateway |
| release token | the first 100 bytes of the token, section 3.7, signed by the gateway |

### 3.3 Handshakes

**Full handshake.**
`{"op":"OPEN","badge":id,"e":E}` (E = e·B, e fresh) is answered with
`{"ok":true,"sid":sid,"e":Eg,"role":tag,"conf":conf_g,"fresh":...}`, where `tag` is the
role tag the session will hold.

    T   = lp("SASTRUGI/1/open", instance id, G, badge id, Q_badge, E, Eg, sid)
    th  = H(T)
    IKM = x(e·Eg) || x(e·G) || x(d_badge·Eg)          (operator side)
        = x(eg·E) || x(g·E) || x(eg·Q_badge)          (gateway side)

**Resumption.**
`{"op":"RESUME","ticket":ticket,"role":tag,"e":E,"binder":binder}` is answered like OPEN.

    offer  = lp("SASTRUGI/1/resume", instance id, G, ticket, E)
    binder = HMAC(rms, lp("SASTRUGI/1/binder", H(offer)))
    T      = offer || lp(Eg, sid)
    th     = H(T)
    IKM    = rms || x(e·Eg)                           (gateway side: rms || x(eg·E))

rms is the ticket's resumption secret, returned with the ticket by MINT.

**Keys and confirmations** (both handshakes). `prk = HKDF-Extract(salt = th, IKM)`; for
each label L in "conf", "c2g", "c2g cm", "g2c", "g2c cm", "beat":
`K_L = HKDF-Expand(prk, lp("SASTRUGI/1/key", L, th), 32)`.

    conf(tag) = HMAC(K_conf, lp("SASTRUGI/1/confirm", tag, th))

The gateway's `conf_g` is `conf(GATEWAY_ROLE_TAG)`. The operator completes the handshake
with `{"op":"CONFIRM","sid":sid,"conf":conf(tag)}`, tag being the session's role tag.
The answer to a successful CONFIRM is the session's first gateway frame, ESTABLISHED.

### 3.4 Frames

`{"op":"FRAME","sid":sid,"seq":s,"ct":ct,"cm":cm}`. The gateway answers with
`{"ok":true,"sid":sid,"seq":s',"ct":ct',"cm":cm',"fresh":...}`, plus `"posting"` when the
request closed a watch. Direction byte d is 0 for operator to gateway (keys `K_c2g`,
`K_c2g cm`) and 1 for gateway to operator (`K_g2c`, `K_g2c cm`).

    nonce = 00 00 00 || u8(d) || u64(s)
    aad   = lp("SASTRUGI/1/frame", sid, u64(s), u8(d))
    ct    = AES-256-GCM(key, nonce, body, aad) with the 16-byte tag appended
    cm    = HMAC(cm key, lp(aad, nonce, ct))

The receiver checks cm first and the GCM tag second. Bodies are UTF-8 JSON objects.
Operator sequence numbers start at 0 for each session; the gateway's start at 0 with
ESTABLISHED.

### 3.5 Beats

    a  = HMAC(K_beat, lp("SASTRUGI/1/beat", instance id, u32(w), u32(n), c, role tag))

After an accepted beat, `c := HMAC(K_fresh, lp("SASTRUGI/1/next", c, a))`. When watch
w + 1 opens, `c := HMAC(K_fresh, lp("SASTRUGI/1/watch", u32(w + 1), c))`. Before watch 0
the chain starts from `HMAC(K_fresh, lp("SASTRUGI/1/genesis"))` and watch 0 opens on it
the same way.

### 3.6 Tickets

88 bytes:

| Offset | Size | Field |
|---|---|---|
| 0 | 16 | `SASTRUGI-TKT/1` followed by two zero bytes |
| 16 | 16 | instance id |
| 32 | 8 | badge id, NUL-padded |
| 40 | 8 | role tag of the minting session |
| 48 | 4 | u32 mint watch |
| 52 | 4 | u32 serial |
| 56 | 32 | `HMAC(K_ticket, bytes 0..55)` |

### 3.7 Release tokens

197 bytes:

| Offset | Size | Field |
|---|---|---|
| 0 | 16 | `SASTRUGI-REL/1` followed by two zero bytes |
| 16 | 16 | instance id |
| 32 | 4 | u32 watch |
| 36 | 32 | manifest digest |
| 68 | 32 | board digest: `H(lp("SASTRUGI/1/board", lp(badge id, role tag, kind, manifest digest), ...))` over the board's commits for this manifest, in deposit order |
| 100 | 97 | gateway signature over bytes 0..99 |

### 3.8 Frame bodies

| Operator body | Gateway answer |
|---|---|
| `{"t":"BEAT","w":w,"n":n,"a":a}` | `{"t":"BEAT","presence":p,"closed":bool}`; when closed is true the envelope carries the new watch's posting |
| `{"t":"MINT"}` | `{"t":"TICKET","ticket":...,"rms":...}` |
| `{"t":"COMMIT","kind":"ARM" or "CS","manifest":digest,"role":tag,"sig":signature}` | `{"t":"COMMITTED","kind":...,"manifest":...,"board":count}` |
| `{"t":"RELEASE","manifest":digest}` | `{"t":"RELEASED","token":...}` |
| `{"t":"THAW","token":token}` | `{"t":"THAWED","manifest":...,"seal":...,"notice":...}`; seal is null and notice present for any manifest but the canonical one |
| `{"t":"STATUS"}` | `{"t":"STATUS","badge":...,"role":...,"presence":p,"quorum":q,"w":w,"board":[...]}` |
| `{"t":"CLOSE"}` | `{"t":"CLOSED"}` |

The gateway's first frame on a session: `{"t":"ESTABLISHED","badge":id,"role":tag,"quorum":q,"w":w}`.

## 4. Clauses

### C-01 Roster and role tags

`roster.json` lists every badge with its rostered role and its static P-256 key. Every instance assigns each role name an 8-byte role tag (section 2.2). The gateway confirms and signs as itself under the fixed tag `GATEWAY_ROLE_TAG` (section 2.1).

### C-02 HELLO

Messages: HELLO

HELLO returns the instance id, the gateway static key G, the posting of the current watch and the freshness echo. It changes no state.

### C-03 Watches and the rota

The gateway keeps a watch index w (from 0), the number n of beats answered in watch w, and the beat challenge c. The rota is a fixed cycle of slots; watch w runs on slot w mod L, L being the rota length. A slot has a duty pair - an arming role tag and a countersign role tag, never equal - and a span, a number of beats. Every watch has a posting signed by the gateway (section 3.1).

### C-04 Full handshake

Messages: OPEN, CONFIRM

OPEN(badge, e) begins a full handshake for `badge`. The gateway answers with a session id, its ephemeral key, the role tag the session will hold and its own confirmation under `GATEWAY_ROLE_TAG`. CONFIRM(sid, conf) completes the handshake. Transcript and keys: section 3.3.

Requires:

- **G04a** OPEN: `badge` is listed in the roster
- **G04b** OPEN: `e` is a valid P-256 point
- **G04c** CONFIRM (of an OPEN or a RESUME): `sid` names a pending handshake begun in the current watch
- **G04d** CONFIRM of an OPEN: `conf` is the operator confirmation under the badge's rostered role tag

Effects:

- **E04a** a session is established for `badge`, holding its rostered role tag, with presence 0

### C-05 Sessions

Messages: CLOSE

A session lives from its CONFIRM until it is closed, replaced, or its watch closes (C-07). Each badge has at most one live session: a CONFIRM for a badge that already has a live session ends that session. A pending handshake lapses when its watch closes. The commits a session deposited leave the board when the session ends before its watch closes.

Effects:

- **E05a** on CONFIRM: the badge's previous live session, if any, ends
- **E05b** CLOSE: the session ends
- **E05c** when a session ends before its watch closes, its commits leave the board

### C-06 Frames

Messages: FRAME, STATUS

Every request on an established session is a FRAME carrying an AES-256-GCM ciphertext and a commitment (section 3.4). The gateway answers with a frame under its own next sequence number. A refused frame does not consume its sequence number. STATUS returns the session's badge, role tag, presence, q and the board of watch w, and changes no state.

Requires:

- **G06a** `sid` names a live session
- **G06b** `seq` is the session's next operator sequence number
- **G06c** the commitment verifies; it is checked before the GCM tag
- **G06d** the GCM tag verifies
- **G06e** the body is a JSON object naming a known request

Effects:

- **E06a** the operator sequence number advances by one

### C-07 Beats

Messages: BEAT

BEAT(w, n, a) answers the current beat challenge.

Requires:

- **G07a** `w` and `n` are the current watch index and beat count
- **G07b** `a` is the session's beat answer for (w, n, c, the session's role tag), section 3.5

Effects:

- **E07a** the session's presence increases by one, n increases by one and c becomes the next challenge
- **E07b** if n now equals the span of the watch's slot, the watch closes: every session ends, pending handshakes lapse, the board is cleared, w increases by one, n = 0, and the next posting is issued

### C-08 Tickets

Messages: MINT

MINT issues a resumption ticket for the session's badge (section 3.6).

Requires:

- **G08a** no ticket has been minted for this badge in watch w

Effects:

- **E08a** the gateway returns a ticket naming the instance, the session's badge, the session's role tag, w and a serial, together with the ticket's resumption secret

### C-09 Resumption

Messages: RESUME, CONFIRM

RESUME(ticket, role, e, binder) resumes the ticket's session in the watch after the one that minted the ticket, without a full handshake. CONFIRM(sid, conf) completes it. Transcript and keys: section 3.3.

Requires:

- **G09a** the ticket tag verifies under the gateway's ticket key
- **G09b** the ticket names this instance
- **G09c** the ticket's mint watch is w - 1
- **G09d** the ticket's serial has not been spent
- **G09e** `binder` verifies under the ticket's resumption secret
- **G09f** `role` is the role tag recorded in the ticket
- **G09g** CONFIRM of a RESUME: `conf` is the operator confirmation under that role tag

Effects:

- **E09a** the ticket's serial is spent
- **E09b** a session is established for the ticket's badge, holding the ticket's role tag, with presence 0

### C-10 Presence

A session's presence is the number of beats it has answered (C-07). The presence quorum q is reported in ESTABLISHED.

### C-11 Commits

Messages: COMMIT

COMMIT(kind, manifest, role, sig) deposits a commit on the board of watch w.

Requires:

- **G11a** `kind` is ARM or CS and `manifest` is 32 bytes
- **G11b** the session's presence is at least q
- **G11c** `role` equals the session's role tag
- **G11d** the session's role tag is the duty pair's arming tag (ARM) or countersign tag (CS)
- **G11e** `sig` is a Schnorr signature over the commit message (section 3.2) under the roster key of the session's badge
- **G11f** the board holds no commit of this kind for this manifest
- **G11g** CS only: the board holds an ARM for this manifest

Effects:

- **E11a** the commit (badge, role tag, kind, manifest) joins the board

### C-12 Release

Messages: RELEASE

RELEASE(manifest) asks the gateway for a release token.

Requires:

- **G12a** the board holds an ARM and a CS for the manifest
- **G12b** the ARM carries the duty pair's arming tag and the CS its countersign tag
- **G12c** the ARM and the CS were deposited by two different badges
- **G12d** no token has been minted for this manifest in watch w

Effects:

- **E12a** the gateway returns a release token (section 3.7) binding the instance, w, the manifest and the board digest, signed with the gateway key

### C-13 Thaw

Messages: THAW

THAW(token) presents a release token to the vault interlock.

Requires:

- **G13a** the token is well formed, names this instance and its signature verifies under G

Effects:

- **E13a** for the canonical thaw manifest (`roster.json`) the vault answers with its seal; for any other manifest it answers with a rehearsal notice

### C-14 Refusals and persistence

A request that fails any guard of any clause, or that cannot be parsed, is answered with the single line `{"ok":false,"err":"EDENIED"}` and changes no state. Requests are processed one at a time, in arrival order, across all connections. All state persists across reconnects for the life of the instance.


## 5. State and message table

| Clause | Message | Requires | Effects |
|---|---|---|---|
| C-04 | OPEN, CONFIRM | G04a G04b G04c G04d | E04a |
| C-05 | CLOSE | - | E05a E05b E05c |
| C-06 | FRAME, STATUS | G06a G06b G06c G06d G06e | E06a |
| C-07 | BEAT | G07a G07b | E07a E07b |
| C-08 | MINT | G08a | E08a |
| C-09 | RESUME, CONFIRM | G09a G09b G09c G09d G09e G09f G09g | E09a E09b |
| C-11 | COMMIT | G11a G11b G11c G11d G11e G11f G11g | E11a |
| C-12 | RELEASE | G12a G12b G12c G12d | E12a |
| C-13 | THAW | G13a | E13a |

A FRAME request (C-06) must pass G06a to G06e before the guards of the body's own clause are checked. CONFIRM completes the handshake begun by the OPEN (C-04) or RESUME (C-09) that issued its sid.


## 6. Limits

| Item | Value |
|---|---|
| request pacing | 60 requests per second per instance, bursts of 60, shared by all connections |
| line length | 8192 bytes; a longer line is refused and the connection closed |
| idle connection | closed after 300 seconds without a request |
| connections | 32 per instance |
