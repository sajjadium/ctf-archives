import validators
import subprocess
import time
import os

WGET_TIMEOUT = 10

exploit_url = input("URL: ")
if not validators.url(exploit_url):
    print("Invalid URL!")
    exit(0)

try:
    fn = os.urandom(16).hex()
    fpath = f"attempts/{fn}"
    is_reachable = subprocess.call(["wget", "-p", "-k", "-P", fpath, exploit_url],
                                    stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, timeout=WGET_TIMEOUT) == 0

    if not is_reachable:
        print("Can't seem to reach that URL!")
        exit(0)

except subprocess.TimeoutExpired:
    print("Can't seem to reach that URL!")
    exit(0)


print(f"Visiting URL...")

subprocess.call(["./chrome/chrome", "--no-sandbox", "--disable-gpu", "--headless", "--virtual-time-budget=60000", exploit_url],
                 stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
