#!/usr/bin/env python3

import datetime
import os
import requests
import signal
from yaml import *

signal.alarm(20)


def verify_records(s):
    return "[+] I'm done, let me go home\n"+s


pw = os.environ["ACCOUNTANT_PASSWORD"]

auth_data = {"username": "MisterX", "password": pw}


print("[+] Let me get into my office")

sess = requests.Session()
resp = sess.post(
    "http://bank:3000/login",
    data={"username": "MisterX", "password": pw},
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    allow_redirects=False,
)

sess.cookies.set("session_id", resp.cookies.get("session_id"))


print("[+] Verifying old records, I am shocking with dust, Damn there are rats too !")
resp = sess.get("http://bank:3000/transactions/report/info/all")
print(resp.text)

if len(resp.text)!=0:
    print("[-] I am not happy, I am not going to work today")

    reports = resp.text.split("|")


    for report in reports:
        try:
            report_id = report.split(":")[0]
            user_id = report.split(":")[1]

            print("[+] Interesting record here, ")
            res=sess.get(
                "http://bank:3000/transactions/report/gen/" + report_id + "?user_id=" + user_id
            )
            if res.status_code == 200:
                loaded_yaml = load(res.text, Loader=Loader)
                print(verify_records(loaded_yaml))
        except:
            print("[-] ~#! !!!! Oo $h/t the rats are eating the old records")



resp = sess.get("http://bank:3000/users")
print("[+] Got new reports for today hope not, let me do my work you shorty!")

for user in resp.json():
    try:
        resp = sess.get(
            "http://bank:3000/transactions/report/gen/1?user_id=" + str(user["ID"])
        )
    except:
        print("[+] a bit more ...")

print(f"[{datetime.datetime.now()}] Accountant will be back soon.")
