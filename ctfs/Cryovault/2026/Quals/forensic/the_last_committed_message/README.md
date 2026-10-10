d3va

The Last Committed Message
Recover the note and its attachment record as they stood when export export-07abca69cd99 was acknowledged.

A note replacement, its attachment-record upsert and its operation record commit together; an acknowledged export describes the state immediately after its operation committed.

Export log:

{"export_id":"export-62b1b1bf2210","operation_id":"op-ba318af959d3","status":"failed"}
{"export_id":"export-48255bece7af","operation_id":"op-c00c33ee5d7a","status":"acknowledged"}
{"export_id":"export-59a9962ed0b6","operation_id":"op-bb8aee1557f6","status":"failed"}
{"export_id":"export-38059628d63a","operation_id":"op-1248f8f02ad3","status":"acknowledged"}
{"export_id":"export-0867099876f6","operation_id":"op-9c0e3dbc9fba","status":"failed"}
{"export_id":"export-07abca69cd99","operation_id":"op-c46dc0e04bdd","status":"timeout"}
{"export_id":"export-486ffa289ec8","operation_id":"op-c01684bb21b6","status":"failed"}
{"export_id":"export-07abca69cd99","operation_id":"op-09e0d79b4b14","status":"acknowledged"}
{"export_id":"export-a2376a4b945c","operation_id":"op-7f467b8fcaec","status":"acknowledged"}
{"export_id":"export-4f38471c799b","operation_id":"op-ade44944bc42","status":"acknowledged"}
{"export_id":"export-01406ade729a","operation_id":"op-f77041bb306e","status":"acknowledged"}
{"export_id":"export-2911ac50d28a","operation_id":"op-bee4d469a78c","status":"failed"}
{"export_id":"export-792d73b761a5","operation_id":"op-a69a71ba327f","status":"acknowledged"}
{"export_id":"export-506fe98ddc47","operation_id":"op-6727657e6537","status":"acknowledged"}
Evidence, in order: note id; revision as a decimal string; destination exactly as stored; the attachment sha256 recorded for that state (lowercase hex).

Flag
evidence = [<fields in the order above>]                       # list of ASCII strings
E        = json.dumps(evidence, ensure_ascii=True, separators=(",", ":")).encode("ascii")
key      = hashlib.scrypt(b"isfcr-forensics\x00" + E, salt=bytes.fromhex("a3845b1a904c5ee73abe7329b5d735d7"),
                          n=131072, r=8, p=1, maxmem=2**28, dklen=32)
flag     = AESGCM(key).decrypt(bytes.fromhex("ca98cff993b27fd3bb352436"), bytes.fromhex("3fa8b9049b01fb8d12df130b404352f9c678c272cccb7e6c034554c902f1ca4d574fc04db8892fead1ad394735e021"), b"the-last-committed-message")
Flag format: isfcr{...}
