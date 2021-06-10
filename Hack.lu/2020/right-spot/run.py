#!/usr/bin/env python3
import zlib
import sys
import os
import subprocess
import io
import bz2
import sys

from flag import flag

COMPRESSED_LIMIT   =    2**20   #  1 MB compressed
DECOMPRESSED_LIMIT = 30*2**20   # 30 MB uncompressed
EXPECTED_STRING = b"pwned!\n"
NUM_TESTS = 4

def compress(data):
    if len(data) > DECOMPRESSED_LIMIT:
        print('ERROR: File size limit exceeded!')
        exit(0)
    return bz2.compress(data, compresslevel=9)
def decompress(data):
    bz2d = bz2.BZ2Decompressor()
    output = bz2d.decompress(data, max_length=DECOMPRESSED_LIMIT)

    if bz2d.needs_input == True:
        print('ERROR: File size limit exceeded!')
        exit(0)
    return output

print(f"Welcome! Please send bz2 compressed binary data. How many bytes will you send (MAX: {COMPRESSED_LIMIT})?", flush=True)
try:
    num_bytes = int(sys.stdin.readline())
except ValueError:
    print("A valid number, please")
    exit(0)

if not (0 < num_bytes <= COMPRESSED_LIMIT):
    print("Bad number of bytes. Bye!")
    exit(0)

print("What is your calculated CRC of the compressed data (hex)?", flush=True)
try:
    crc = int(sys.stdin.readline(), 16)
except ValueError:
    print("A valid hex crc, please")
    exit(0)

print(f"Okay got CRC: {crc:x}, please start sending data", flush=True)
compressed_payload = sys.stdin.buffer.read(num_bytes)
while len(compressed_payload) < num_bytes:
    compressed_payload += sys.stdin.buffer.read(0, num_bytes - len(compressed_payload))

print(f"Read {len(compressed_payload)} bytes")
calc_crc = zlib.crc32(compressed_payload)
if crc == calc_crc:
    print("[+] CRC Checks out, all good.", flush=True)
else:
    print(f"CRC mismatch. Calculated CRC: {calc_crc:x}, expected: {crc:x}")
    exit(0)

payload = decompress(compressed_payload)
if len(payload) > DECOMPRESSED_LIMIT:
    print(f"Payload too long. Got: {len(payload)} bytes. Limit: {DECOMPRESSED_LIMIT}")
    exit(0)

print("[+] Decompressed payload", flush=True)


for seed in range(1 << 5):
    print(f"Trying seed: 0x{seed:x}", flush=True)
    for i in range(1, NUM_TESTS + 1):
        print(f"Try #{i}", flush=True)
        try:
            p = subprocess.Popen(["./right_spot", str(seed)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            stdout_output, stderr_output = p.communicate(input=payload, timeout=5)
            if stdout_output != EXPECTED_STRING:
                print("[-] Mh, not the correct output.")
                print(f"Output was: {stdout_output}")
                exit(0)
            if p.returncode != 0:
                print(f"[-] Did not return success status code. Status was: {p.returncode}")
                exit(0)
        except subprocess.TimeoutExpired as e:
            print("[-] Process timed out")
            p.kill()
            exit(0)
        except Exception as e:
            print("Something unforeseen went wrong...")
            print(e)
            p.kill()
            exit(0)

print(f"Congrats, here is your flag: {flag}", flush=True)
