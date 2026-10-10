d3va

Signed, But Which Original?
Find the derivative that satisfies case.json, and its ancestry. Evidence, six ASCII strings in this order: the derivative's asset SHA-256, its manifest_id, its ancestry's manifest_ids from capture to derivative joined with >, the capture's asset SHA-256, the target incident ID, and the tree_size of the checkpoint you relied on. Digests are lowercase hex.

Flag
evidence = [<fields in the order above>]                       # list of ASCII strings
E        = json.dumps(evidence, ensure_ascii=True, separators=(",", ":")).encode("ascii")
key      = hashlib.scrypt(b"isfcr-forensics\x00" + E, salt=bytes.fromhex("df2fd39adb32a812294cfe264c4a0ddc"),
                          n=131072, r=8, p=1, maxmem=2**28, dklen=32)
flag     = AESGCM(key).decrypt(bytes.fromhex("d2705557b11d25f6a1607cfd"), bytes.fromhex("7bad7e996d62c88b017ef105997ca1235e513b8b24a724eb88a5204d1771614af735db56d5d02cc8177133b8d79101"), b"signed-but-which-original")
Flag format: isfcr{...}
