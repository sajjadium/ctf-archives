#!/usr/bin/env python3

import requests
import json
import pprint
import sys

if len(sys.argv) != 2:
    print("Usage: %s [script.js]" % sys.argv[0])
    sys.exit(1)

script_path = sys.argv[1]

url = 'https://mujs.chal.uiuc.tf/go'
myobj = {'script': open(script_path).read()}

results = json.loads(requests.post(url, data = myobj).text)

if not isinstance(results, list):
    print("Invalid response from server.")
    sys.exit(1)

for i in range(0, len(results)):
    result = results[i]

    stderr_output = result["stderr"]
    stdout_output = result["stdout"]

    print("Result from run against mujs-%d binary:" % i)
    print("stdout:")
    print(stdout_output)
    print("stderr:")
    print(stderr_output)
    print()

flag = ""
for result in results:
    flag += result["stdout"].replace("\n", "")
print("Maybe flag: " + flag)
