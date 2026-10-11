AJ

Frostline's cold archive keeps one copy of every chunk it is given, the keeper's bay policy included. Open a bucket at the address below; the keeper opens bay 07 only for operators the policy names.


# MORAINE - Frostline cold archive

Every team works in its own **bucket**: a private archive with its own keeper and its own
bay policy. Open one with

    POST /session          (Accept: application/json)  ->  {"token": "...", "base": "https://.../s/<token>"}

and use every route below under `base`. A bucket closes after about three hours unused; a new
session is a new bucket with a new keeper and a new policy. `client.py` wraps the API.

## Objects

| Route | |
|---|---|
| `GET /` | your operator id and the objects in the bucket |
| `GET /whoami` | your operator id |
| `GET /objects` | every object in the bucket, yours and the keeper's |
| `PUT /objects/<name>` | store the request body (1-8192 bytes) as a new object |
| `GET /objects/<name>` | the object's record: size and chunk list |
| `GET /objects/<name>/data` | the object's bytes |
| `DELETE /objects/<name>` | delete one of your objects |
| `GET /usage` | object and slot counts for the bucket |
| `POST /release` | ask the keeper to open bay 07 for you |

Names are 1-64 characters of `a-z 0-9 . _ -`, starting with a letter or digit. A name in use
cannot be stored again; delete the object first.

The archive stores objects as variable-size chunks. A chunk the bucket already holds is not
stored twice: `stored_bytes` in the answer to a `PUT` counts only the bytes that were new.
An object's record lists its chunks in order:

    {"name": "notes.txt", "owner": "you", "size": 913,
     "chunks": [{"slot": 9, "len": 311, "tag": "5b0f0c2a"}, ...]}

`tag` is the bucket's 32-bit integrity tag of the chunk's bytes. Every chunk is checked against
its tag whenever the archive reads an object.

## The keeper

`bay-07.policy` belongs to the keeper. You may read it but not change or delete it. Its record
also carries the policy's `revision`, its `sum` (a 32-bit checksum of the whole policy) and the
keeper's `seal`, an HMAC over the policy's record (revision, sum and chunk list) under a key
only the keeper holds.

`POST /release` asks the keeper to open bay 07. The keeper checks the seal against the
policy's record, reads the policy from the archive, checks it against its sum, and opens the
bay for an operator whose id appears under `release.to`. It answers `403 not_listed` for
anyone else.

## Errors

Errors are JSON: `{"error": "...", "detail": "..."}`. `429` means slow down (each bucket
allows about 25 requests a second).
