#!/usr/bin/env python3
import sys
import subprocess
sys.stdout.write("Payload(hex) :")
sys.stdout.flush()
payload = sys.stdin.readline().strip()
payload_bytes = bytes.fromhex(payload)
p = subprocess.Popen("/home/SimpleLanguage/SimpleLanguage", stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.PIPE)
p.stdin.write(payload_bytes)
p.stdin.close()
p.stdout.close()
p.stderr.close()
print( p.wait(timeout=60))

