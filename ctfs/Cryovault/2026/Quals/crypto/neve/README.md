AJ

A NEVE sounding head watches the outer jacket loop: hand it a symbol and it answers with one bit. Its calibration table was sealed into the vault's recovery bundle and never written down anywhere else. Recover the table and open the bundle. The handout is the vendor's bench model of an earlier revision, a recorded factory session and the firmware changelog.


# NEVE

The outer jacket loop on SHARD-24 is watched by a NEVE sounding head. You hand it a
symbol, 0 to 15, and it answers with one bit.

The head's calibration table, 32 rows of 16 grades, went into the vault's recovery bundle
when the head was potted, and nowhere else. Your instance is a field head running NV-4.2.1.
Recover the table and open the bundle.

## Files

| File | What it is |
|---|---|
| `README.md` | this file |
| `neve_bench.py` | bench model of the NV-3.4.2 head: a local head and a client (`Link`) |
| `factory_session.jsonl` | a factory session recorded on bench head `8628b99c4a630c03633e576b312f2e0d` |
| `CHANGELOG` | firmware revisions |

## Connecting

Start your instance on the instancer page. It gives you a `wss://` address that carries
the head's byte stream, and the commands to use it:

    python3 cvconnect.py wss://HOST/ws/TOKEN             like netcat: type requests, read answers
    python3 cvconnect.py -l 9000 wss://HOST/ws/TOKEN     a local port for your own code:
                                                         nc 127.0.0.1 9000, Link("127.0.0.1", 9000)

`cvconnect.py` is on the instancer page; `websocat -b wss://HOST/ws/TOKEN` works as well.

## Protocol

The head speaks one JSON protocol in two framings, on the same port:

- **lines**: one JSON object per line in each direction. This is what the instancer
  address carries, and what `nc` and `Link(host, port)` speak.
- **WebSocket**: an HTTP/1.1 upgrade on the head's port, then one JSON request per text
  message and one answer per message (a message may also carry several requests, one per
  line). `Link("ws://HOST:PORT/")` or any WebSocket client.

Either way there is one response per request, in order. A request longer than 16384 bytes
is answered with `EARG` and the connection is closed.

**OPEN** `{"cmd":"OPEN"}`

    {"ok":true,"session":"<32 hex>","head":"NV-4.2.1","instance":"<32 hex>","t":0,"row":1,"budget":1250000,"bit":0}

A session is a head of its own, with its own table, round counter, output and budget. Every
other request names its session. Anyone who has the session token can use the session.
The head keeps up to 4096 sessions for as long as the instance lives. When it is full,
opening a session drops the one that has confirmed the fewest rows and been idle longest.

**HELLO** `{"cmd":"HELLO","session":"<token>"}` answers with the session's state, in the
same shape as OPEN. Without `session` it answers `{"ok":true,"head":...,"instance":...}`.

**SOUND** `{"cmd":"SOUND","session":"<token>","t":<round>,"row":<row>,"syms":"<hex digits>"}`

- `syms`: 1 to 4096 symbols, one hex digit each, sounded in the order given.
- `t`: the session's round counter. It advances by one per symbol; a request must carry the
  current value.
- `row`: the table row the head sounds against. Any row from 1 to the first unconfirmed row.

      {"ok":true,"t":<new round>,"row":<row>,"budget":<left>,"bits":"<one 0 or 1 per symbol>"}

**CHECKPOINT** `{"cmd":"CHECKPOINT","session":"<token>","row":<row>,"grades":"<16 digits 0-7, cell 0 first>"}`

- `row` may be any row up to the first unconfirmed one. If the grades are right the row is
  confirmed, and confirming the first unconfirmed row opens the next.
- If they are wrong the answer is `EMISS` and 4096 is taken from the budget. A checkpoint
  is refused with `EBUDGET` while less than 4096 is left.

      {"ok":true,"row":<first unconfirmed row>,"budget":<left>}

**BUNDLE** `{"cmd":"BUNDLE","session":"<token>"}`

    {"ok":true,"bundle":"<hex>"}

Errors are `{"ok":false,"err":"<code>",...}`:

| code | meaning | state changed |
|---|---|---|
| `EARG` | malformed request or unknown command | no |
| `ESESSION` | no such session | no |
| `ESEQ` | `t` is not the round counter; the answer carries the current `t` | no |
| `EROW` | that row is not open; the answer carries the first unconfirmed `row` | no |
| `EBUDGET` | not enough budget left for the request; carries `budget` | no |
| `EMISS` | wrong grades; carries `row` and `budget` | 4096 charged |

Requests are paced at about 40 per second per instance, and OPEN at about one per second.
An idle connection is closed after 5 minutes, and an HTTP upgrade request must be complete
within 10 seconds. With 64 connections open, a new connection closes the one that has been
idle longest. Sessions outlive connections.

## The table

32 rows of 16 cells. Every cell has a grade from 0 to 7, and every grade stands for a
probability:

| grade | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| p | 0.1800 | 0.2714 | 0.3629 | 0.4543 | 0.5457 | 0.6371 | 0.7286 | 0.8200 |

p = 0.18 + 0.64 g / 7. Row 1 is open from the start. Every later row opens when the row
before it is confirmed.

## Budget

1,250,000 per session: one per symbol sounded, plus 4096 per wrong checkpoint. It is never
refilled. Confirmed rows stay open for sounding, at the usual cost.

## The bundle

    bundle = nonce (12 bytes) || ciphertext || tag (16 bytes)          AES-256-GCM
    key    = HKDF-SHA256(IKM  = the 512 grades, one byte each, row 1 cell 0 first,
                         salt = the 16-byte session token,
                         info = "NV4 recovery bundle", length = 32)
    associated data = the 16-byte instance id followed by the 16-byte session token

## The bench

`neve_bench.py` models NV-3.4.2, the last revision that has a bench model, and speaks the
current protocol in both framings.

    python neve_bench.py serve --port 19640          a bench head on 127.0.0.1 (random tables)
    python neve_bench.py serve --port 19640 --seed 7 the same bench head every time
    python neve_bench.py factory                     replay factory_session.jsonl bit for bit

`Link("127.0.0.1", 9000, log="session.jsonl")` (or `Link("ws://HOST:PORT/", ...)`) talks to
a bench head or to your field head and appends every SOUND exchange to the log.

The factory session file starts with the bench session's own record (instance, session,
keystream key, table, sealed bundle), followed by every SOUND and CHECKPOINT of the session.
