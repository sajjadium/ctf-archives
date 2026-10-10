d3va

The Image That Forgot
Recover the incident token of the container instance that was serving dispatch-ac1af5608a at 2026-08-14T10:10:08.555+05:30.

Each note in vault.json is AES-256-GCM under one of its keys: 12-byte nonce; data is ciphertext followed by the 16-byte tag; the plaintext is the token. The associated data is the ASCII compact JSON list [service_id,key_version,manifest_digest,event_id], where manifest_digest is the sha256:-prefixed digest of the image manifest the instance ran and event_id identifies the event that started the instance.

Evidence fields, in order: event_id, manifest_digest, service_id, key_version, token.

Flag
evidence = [<fields in the order above>]                       # list of ASCII strings
E        = json.dumps(evidence, ensure_ascii=True, separators=(",", ":")).encode("ascii")
key      = hashlib.scrypt(b"isfcr-forensics\x00" + E, salt=bytes.fromhex("8b57a161139a064a196625972f7e602d"),
                          n=131072, r=8, p=1, maxmem=2**28, dklen=32)
flag     = AESGCM(key).decrypt(bytes.fromhex("244cb048e982870d71f68dfe"), bytes.fromhex("02e462042292a430220d3959e46c379b7f96d44726c6c390338ed11b7ee9878875de07ad212f4dbbda1994c3e2574c"), b"the-image-that-forgot")
Flag format: isfcr{...}
