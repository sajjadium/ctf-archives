import binascii
import os
import subprocess
import tempfile
import json
import requests

import eth_sandbox
from Crypto.Util import number

FLAG = os.getenv("FLAG", "PCTF{placeholder}")


def new_factorize_action():
    def action() -> int:
        ticket = eth_sandbox.check_ticket(input("ticket please: "))
        if not ticket:
            print("invalid ticket!")
            return 1

        if ticket.challenge_id != eth_sandbox.CHALLENGE_ID:
            print("invalid ticket!")
            return 1

        runtime_code = input("runtime bytecode: ")

        try:
            binascii.unhexlify(runtime_code)
        except:
            print("runtime code is not hex!")
            return 1

        with tempfile.TemporaryDirectory() as tempdir:
            with open("./Script.sol", "r") as f:
                script = f.read()

            a = number.getPrime(128)
            b = number.getPrime(128)
            script = script.replace("NUMBER", str(a * b)).replace("CODE", runtime_code)

            with open(f"{tempdir}/Script.sol", "w") as f:
                f.write(script)

            p = subprocess.run(
                args=[
                    "/root/.foundry/bin/forge",
                    "script",
                    "Script.sol",
                    "--tc",
                    "Script",
                ],
                cwd=tempdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            
            print()

            if p.returncode != 0:
                print("failed to run script")
                return 1

            result = p.stdout.decode("utf8").strip().split("\n")[-1].strip()

            print(result)
            if result.startswith("you factored the number!"):
                print(FLAG)

    return eth_sandbox.Action(name="factorize", handler=action)


eth_sandbox.run_launcher([
    new_factorize_action(),
])
