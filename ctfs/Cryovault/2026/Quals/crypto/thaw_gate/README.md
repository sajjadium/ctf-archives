AJ

The vault's thaw interlock demands two operators' co-authorisation, and you carry only one badge. Get the gateway to release its seal. Send {"op":"SESSION"} first for a gateway of your own.


# THAW GATE

CryoVault cold store C-2. Thaw interlock, dual-control gateway, firmware 2.6.

The vault thaws a store only for a release token signed by the gateway. The gateway signs
one only when two different operators, each on duty, have co-authorised the thaw manifest
inside one watch: one arms it, the other countersigns it.

You carry one badge: `op-07`, duty engineer. The rest of the roster is listed with their
public keys. None of them are coming in tonight.

## Since the 2.4 audit

| 2.4 finding | 2.6 |
|---|---|
| A-1 frame partitioning | every frame carries a commitment HMAC over its header, nonce and ciphertext; the receiver checks it before the GCM tag |
| A-2 confirmation reflection | handshake confirmations carry a role tag inside the MAC: `GATEWAY_ROLE_TAG` from the gateway, the session's role tag from the operator |
| A-3 biased signature nonces | Schnorr nonces (gateway postings and release tokens, badge commits) are `wide(d, "nonce", m)` |
| A-4 ticket forgery | resumption tickets carry an HMAC-SHA256 tag under a per-instance key, and a resumption presents a binder under the ticket's resumption secret |

## Files

| File | What it is |
|---|---|
| `PROTOCOL.md` | wire protocol 1: notation, key schedule, messages, clauses |
| `firnrelay.py` | operator library: crypto, frame codec, handshakes. Needs `pycryptodome` |
| `roster.json` | the badges, their roles and public keys, and the canonical thaw manifest |
| `badge_op-07.json` | your badge, private key included |
| `recorded_session.jsonl` | a field rehearsal on retired instance `06837a5ec820a4f4eabd9c1db24988a6`, whose master was released when it was decommissioned |

## Your gateway

The gateway service is shared. Each session on it is a gateway instance of its own, with
its own keys, role tags and rota. Connect with `nc <host> <port>` and send one JSON object
per line. The first line of a connection is `{"op":"SESSION"}`, which starts a new session
and answers with its token, or `{"op":"RESUME","token":"<token>"}`, which joins a session
you started before. Then start with `{"op":"HELLO"}`. With the library,
`firnrelay.Wire(host, port)` starts a session (its token is `Wire.session`) and
`firnrelay.Wire(host, port, session=token)` joins it. Connections in different sessions
reach different instances. A session keeps its state across reconnects; one left unused
for about three hours is dropped. Share your token only with your team.
