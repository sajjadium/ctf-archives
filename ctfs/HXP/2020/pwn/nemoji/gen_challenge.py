#!/usr/bin/env python3

import urllib.request
import sys
import hashlib

KNOWN_GOOD_HASH = "9eb64f52f8970d0ce86b9ae366ea55cab35032ca6a2fd15f14f1354f493644d6"
DRGNS_GOOD_URL = "https://storage.googleapis.com/dragonctf-prod/noemoji_9eb64f52f8970d0ce86b9ae366ea55cab35032ca6a2fd15f14f1354f493644d6/main"

def nop(dat, start, end):
    dat[start:end] = b"\x90" * (end - start)
    return dat

def main(do_download = False):
    dat = urllib.request.urlopen(DRGNS_GOOD_URL).read() if do_download else open("main", "rb").read()

    h = hashlib.sha256()
    h.update(dat)
    if h.hexdigest() != KNOWN_GOOD_HASH:
        print("hash check failed.")
        return -2

    dat = bytearray(dat) ## writable, pls

    ## Spice it up
    dat = nop(dat, 0x13a4, 0x13b3)
    dat = nop(dat, 0x1504, 0x1528)
    dat = nop(dat, 0x152e, 0x1537)
    dat = nop(dat, 0x1679, 0x1697)
    dat[0x207f:0x2091] = b"emoji (\xe5\xaf\x9d\xe6\x96\x87\xe5\xad\x97)!"
    dat[0x2107:0x210c] = b"DrgnS"

    open("vuln", "wb").write(dat)

if __name__ == "__main__":
    do_download = len(sys.argv) == 2 and sys.argv[1] == "steal_from_dragons"
    main(do_download)
