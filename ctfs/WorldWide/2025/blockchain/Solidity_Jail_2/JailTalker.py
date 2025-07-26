#!/usr/local/bin/python
import signal
from solcx import compile_standard
import os
from web3 import Web3
import string
import re
import requests
import sys

contr_add = os.environ.get("CONTRACT_ADDDR")
rpc_url = os.environ.get("RPC_URL")

print("Enter the body of main() (end with three blank lines):")
lines = []
empty_count = 0
while True:
    try:
        line = input()
    except EOFError:
        break
    if line.strip() == "":
        empty_count += 1
    else:
        empty_count = 0
    if empty_count >= 3:
        lines = lines[:-2]
        break
    lines.append(line)

body = "\n".join(f"        {l}" for l in lines)

if not all(ch in string.printable for ch in body):
    raise ValueError("Non-printable characters detected in contract.")

if len(body) > 25000:
    raise ValueError("Maximum 25000 characters allowed.")

blacklist = [
    "call",
    "store",
    "load",
    "revert",
    "flag",
    "wwf",
    "transfer",
    "address",
    "this",
    "ext",
    "push",
    "bytes4",
    "keccak",
    "block",
    "tx",
    "origin",
    "gas",
    "fallback",
    "receive",
    "selfdestruct",
    "suicide"
]
if any(banned in body for banned in blacklist):
    raise ValueError(f"Blacklisted string found in contract.")

if re.search(r"(\d)\1", body):
    raise ValueError("Regex check failed.")


source = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Solution {{
    function main() external returns (string memory) {{
{body}
    }}
}}
"""

print("Final contract with inserted main() body:")
print(source)

compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Solution.sol": {"content": source}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["evm.bytecode.object"]
                }
            }
        },
    },
    solc_version="0.8.20",
)


bytecode_hex = "0x" + compiled["contracts"]["Solution.sol"]["Solution"]["evm"]["bytecode"]["object"]
salt_hex = "0x" + os.urandom(32).hex()

web3 = Web3(Web3.HTTPProvider(rpc_url))

contr_abi = [{"inputs":[],"name":"flag","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"_bytecode","type":"bytes"},{"internalType":"bytes32","name":"_salt","type":"bytes32"}],"name":"run","outputs":[{"internalType":"bool","name":"success","type":"bool"},{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"nonpayable","type":"function"}]
contr = web3.eth.contract(address=contr_add, abi=contr_abi)

bytecode_bytes = Web3.to_bytes(hexstr=bytecode_hex)
salt_bytes = Web3.to_bytes(hexstr=salt_hex)
print(contr.functions.run(bytecode_bytes, salt_bytes).call())