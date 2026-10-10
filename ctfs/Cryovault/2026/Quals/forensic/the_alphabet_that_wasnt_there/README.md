d3va

The Alphabet That Wasn't There
Decode the 16 × 16 symbol grid on the page of the document in damaged.pdf whose catalog carries the /CaseID bytes 9697624543591457a15dc6d9a4797c45 (hex). In reference.pdf the n-th symbol from the left is the n-th hex digit of 8bd4e257f916c30a.

Reading order, in the page's default user space: rows from top to bottom (descending baseline y), and within a row from left to right (ascending baseline x). A symbol drawn rotated is still the same symbol.

Evidence fields, in order: the CaseID above (32 lowercase hex digits); the grid (256 lowercase hex digits in reading order).

Flag
evidence = [<fields in the order above>]                       # list of ASCII strings
E        = json.dumps(evidence, ensure_ascii=True, separators=(",", ":")).encode("ascii")
key      = hashlib.scrypt(b"isfcr-forensics\x00" + E, salt=bytes.fromhex("8a251a8101ffa67ed383a445a05e77f2"),
                          n=131072, r=8, p=1, maxmem=2**28, dklen=32)
flag     = AESGCM(key).decrypt(bytes.fromhex("cf5d90d20b821db4c5bf1b73"), bytes.fromhex("27b4469da3cc30f3ec487d60be3053aa2d5aa00c9f4da69fe54e7d51da8463883b4aa1b0a10a69c45c4e974171133f"), b"the-alphabet-that-wasnt-there")
Flag format: isfcr{...}
