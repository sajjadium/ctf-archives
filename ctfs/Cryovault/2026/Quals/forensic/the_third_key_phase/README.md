d3va

The Third Key Phase
Recover the exact bytes of the file the intake service accepted for request 6e26102a48d71fe1d7f68231.

Evidence fields, in order: the request id, the client_random of the connection that delivered the file, and the SHA-256 of the file (lowercase hex).

Flag
evidence = [<fields in the order above>]                       # list of ASCII strings
E        = json.dumps(evidence, ensure_ascii=True, separators=(",", ":")).encode("ascii")
key      = hashlib.scrypt(b"isfcr-forensics\x00" + E, salt=bytes.fromhex("55cfbdc7a31326404d59e133d991dc88"),
                          n=131072, r=8, p=1, maxmem=2**28, dklen=32)
flag     = AESGCM(key).decrypt(bytes.fromhex("f684f2db484cdd8e6f38b16e"), bytes.fromhex("c4805539a3db8bc0bba5f5fb6ad76c1125d889aab86af18041007f8f49e30d2b5822be5cf8d26d21ddb576b25d06bc"), b"the-third-key-phase")
Flag format: isfcr{...}
