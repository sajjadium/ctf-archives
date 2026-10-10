AJ

Frostline's runbook is shared with every operator except one line: the keeper's seal, re-cut every minute and redacted on your copy. Open a console at the address below; each console is a runbook service of its own.


# Frostline runbook service

Every Frostline operator works from the same operations runbook. The keeper holds the
master; your copy is the export for shift operators, with the keeper's seal redacted. The
vault door opens for the seal in force.

The service speaks HTTP. Request and response bodies are JSON unless noted.

## Sessions

Open the service's address from the challenge page in a browser and press the button, or
open a session from a script:

    $ curl -s -X POST $URL/session -H 'accept: application/json'
    {"token":"<token>","base":"$URL/s/<token>"}

Each session is a runbook service of its own, with its own copy of the runbook, its own
seal and its own limits. Every path below lives under your session's base,
`$BASE` = `$URL/s/<token>`. A session closes after about three hours unused; a closed or
unknown one answers 404.

## GET /runbook

Your copy of the runbook as `text/plain; charset=utf-8`, with the seal shown as `######`.

## POST /hunks/check

Your editor asks this before it commits a batch of hunks: would they still apply to the
keeper's master?

    {"hunks": [{"near": 1234, "find": "...", "put": "..."}, ...]}

- `near` - where in the keeper's master the hunk sits, as an offset.
- `find` - the text the hunk expects to replace there: 16 to 32 bytes of UTF-8.
- `put` - the replacement text: at most 64 bytes of UTF-8.

Up to 32 hunks per request. The answer has one entry per hunk, in request order:

    {"applies": [true, false, ...]}

Hunks are checked against the master, seal included, not against your copy. Nothing is
ever committed: the master is read-only.

## POST /unseal

    {"seal": "<six symbols>"}

A seal is six symbols from `0123456789abcdefghjkmnpqrstvwxyz`. It is re-cut every 60
seconds, at unix times that are multiples of 60, and the seal line on your copy shows when
the one in force was cut. The seal just replaced is still accepted for 10 seconds.
Three attempts per cut.

    200 {"flag":"<the flag>"}
    403 {"error":"seal rejected"}
    429 {"error":"no attempts left for this seal"}

## Limits

Per session, checks: one per second on average, in bursts of up to 8. Beyond that, or
while the service is busy, the answer is 429 with `Retry-After`. Request bodies up to
64 KiB.

## Example

From a demo session, not yours:

    $ curl -s $BASE/runbook | head -n 6
    FROSTLINE CORP - CRYOVAULT BAY 07
    Operations runbook for the SHARD-24 brine loop, LN₂ and LOX service
    Revision 26.9 · shared copy for shift operators

    1. Operating limits
    jacket setpoint −42.0 °C · alarm at −39.2 °C · trip at −35.5 °C

    $ cat hunks.json
    {"hunks": [{"near": 0, "find": "FROSTLINE CORP - CRYOVAU", "put": "FROSTLINE CORP - CRYOVAU"}, {"near": 0, "find": "End of runbook. Uncontrolled", "put": ""}]}
    $ curl -s $BASE/hunks/check -H 'content-type: application/json' -d @hunks.json
    {"applies":[true,false]}

`client.py` opens a session and wraps the three calls (Python 3, standard library only).
