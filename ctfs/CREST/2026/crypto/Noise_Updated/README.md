CTF7
An incident response team recovered signed audit records, a public key, fragments of a signing service, and an encrypted evidence capsule. The service was retired before investigators could recover its configuration. Determine whether the signatures expose the signing key and recover the evidence.

Objectives:

Establish that the signatures are valid and determine what the evidence implies about nonce generation.
Reconcile the conflicting configuration clues. The candidate exponent range is deliberately wider than the previous build; do not assume the stale constant is authoritative.
Derive the relevant ECDSA relation and recover the private scalar using a justified cryptanalytic method.
Verify the recovered scalar against pubkey.pem and the complete signature set.
Recover and authenticate the flag from sealed_flag.bin.
Format notes: sealed_flag.bin begins with the five-byte magic WBSG1, followed by a 12-byte AES-GCM nonce and then ciphertext plus authentication tag. The AES-256-GCM associated data is CRY-03. The encryption key is derived as SHA-256 of the recovered private scalar encoded as 32 big-endian bytes.

The artifacts are offline; no network interaction is needed. Submit the flag in CREST{...} format.
