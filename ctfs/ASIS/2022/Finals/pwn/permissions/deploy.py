#!/usr/bin/env python3
# socat TCP-LISTEN:2323,reuseaddr,fork EXEC:"./deploy.py"
import os
import re
import json
import time
import subprocess


if not os.path.exists('/tmp/ips.json'):
        f = open('/tmp/ips.json','w')
        f.write('{}')
        f.close()

ipFile = open('/tmp/ips.json','r+')
peerIp = os.environ['SOCAT_PEERADDR']
ips = {}

ips = json.loads(ipFile.read())
if(peerIp in ips):
        if(time.time() > ips[peerIp]):
                ips[peerIp] = int(time.time())+30
        else:
                print('one try each 30 seconds')
                exit(0)
else:
        ips[peerIp] = int(time.time())+30

ipFile.seek(0)
ipFile.write(json.dumps(ips))
ipFile.close()

s = input('input: ')
assert(
        re.match('^[A-Za-z0-9=+/]+$',s) and
        len(s) < 3000
)

subprocess.call(('docker run --privileged --rm permissions timeout 10 xvfb-run --auto-servernum node /app/index.js '+s).split(' '))

