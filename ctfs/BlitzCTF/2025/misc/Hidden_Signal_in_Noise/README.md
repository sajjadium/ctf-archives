The file magic.mrf starts with a 4-byte magic header. After the header, the flag is hidden by splitting each character into two parts, each stored in the high nibble of bytes spaced roughly every X bytes. The low nibble contains random noise. The flag begins with Blitz{. Recover the flag by extracting and decoding these bytes.

Author: Zwique
