import requests
import time

url = "http://localhost:5555/action/backdoor"

flag_path = "/mnt/flag.txt"

def get_flag(path: str):
    with open(path, 'r') as fp:
        return fp.read().strip()


def check_backdoor():
    r = requests.get(url)
    if r.status_code == 200:
        resp = r.json()
        if "status" in resp and resp['status'] == "success":
            r.close()
            return True
    r.close()
    return False


def post_flag(flag: str):
    params = {"flag": flag}
    r = requests.get(url, params=params)
    r.close()

try:
    if check_backdoor():
        f = get_flag(flag_path)
        post_flag(f)
except Exception:
    exit(1)
