AJ

The vault's cold-chain attestation unit keeps a 64-bit chain register and speaks a terse line language. You may submit jobs of up to thirteen lines; each job runs on a unit of its own and returns whatever notes its lines produce. The unit lists its line letters and their operand ranges, not what they do.

A trace line shows you part of the register. A seal line reports the current seal when the register is clear; a manifest line releases the manifest to a register that matches the seal. The unit is re-cut every two minutes, and every cut has its own seal.

Start with GET / on the unit. The handout is the interface notes and a small client.


# BLIND RATCHET - field interface

The vault's cold-chain attestation unit keeps a 64-bit chain register and speaks a terse
line language over HTTP. Every team has its own unit: start your instance and use the
`http://<host>:<port>/` address it gives you.

## Endpoints

    GET  /      this unit's line set, operand ranges, limits and note formats (JSON)
    POST /run   one job:  {"job": "<lines>"}

## Jobs

- A job is at most 13 lines and at most 96 bytes. Lines are separated by a
  single LF (`\n`); one trailing LF is ignored.
- Each job runs on a unit of its own. Its notes come back when the whole job has finished.
- A letter line is a letter, a slash and an operand, as in `x/7`. Which letters your unit
  has, and which operands each takes, is in its `GET /`. Operands are decimal, 1 to 3
  digits; leading zeros are accepted. One letter takes no operand.
- `trace` adds the note `chain <8 hex digits>`: part of the register.
- `seal` adds `seal <16 hex digits>` (the current cut's seal) when the register is clear,
  and `locked` otherwise.
- `manifest` adds `manifest <text>` when the register matches the current cut's seal, and
  `locked` otherwise.
- The unit is re-cut every 120 seconds. A job runs entirely in the cut in which it
  starts, and every cut has its own seal. `GET /` says when the next cut starts.
- If any line of a job is not valid, nothing runs: the answer is HTTP 400
  `{"error": "rejected", "line": k}`, k being the first refused line (0 when the request
  is not a job at all).
- More than 20 jobs per second on one unit: HTTP 429 `{"error": "busy"}`.

## Example exchanges

Recorded from a demonstration unit. Its letters are not yours, and no register value
below means anything on your unit.

```
GET /
200 {"unit": "cold-chain attestation unit", "register_bits": 64, "lines": ["j/", "k/<0-63>", "n/<0-9>", "v/<1-31>", "trace", "seal", "manifest"], "operands": "decimal, 1 to 3 digits, leading zeros accepted", "job": {"max_lines": 13, "max_bytes": 96, "line_separator": "LF"}, "notes": {"trace": "chain <8 hex digits>", "seal": "seal <16 hex digits> | locked", "manifest": "manifest <text> | locked"}, "cut_s": 120, "next_cut_in_s": 78, "jobs_per_second": 20}

POST /run  {"job": "trace"}
200 {"notes": ["chain 253b5241"]}

POST /run  {"job": "v/05\ntrace"}
200 {"notes": ["chain 5d30f7f9"]}

POST /run  {"job": "trace\nk/64"}
400 {"error": "rejected", "line": 2}
```

## client.py

    python3 client.py http://<host>:<port>
    python3 client.py http://<host>:<port> trace trace

Flag format: `isfcr{…}`
