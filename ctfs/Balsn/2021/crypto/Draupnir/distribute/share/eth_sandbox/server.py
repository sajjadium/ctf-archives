from web3 import Web3
from dataclasses import dataclass
from threading import Thread, Lock
from typing import Tuple, Dict, Any
from uuid import uuid4
import sys
import os

from eth_account.hdaccount import generate_mnemonic

import socket

import random
import time

from flask import Flask, request, redirect, Response
from flask_cors import CORS, cross_origin

import requests
import subprocess

from eth_sandbox import *

app = Flask(__name__)
CORS(app)

RPC_URL = os.getenv("RPC_URL")

@dataclass
class NodeInfo:
    port: int
    mnemonic: str
    proc: subprocess.Popen
    uuid: str


instances: Dict[str, NodeInfo] = {}


def kill_ganache(node_info: NodeInfo):
    time.sleep(60 * 5)
    print(f"killing node {node_info.uuid}")
    del instances[node_info.uuid]
    node_info.proc.kill()


def launch_ganache() -> NodeInfo:
    port = random.randrange(30000, 60000)
    mnemonic = generate_mnemonic(12, "english")
    uuid = str(uuid4())

    proc = subprocess.Popen(
        args=[
            "ganache-cli",
            "--port",
            str(port),
            "--accounts",
            "1",
            "--defaultBalanceEther",
            "5000",
            "--hardfork",
            "muirGlacier",
            "--fork",
            RPC_URL,
            "--mnemonic",
            mnemonic,
            "--noVMErrorsOnRPCResponse",
            "--gasLimit",
            "12500000",
            "--allowUnlimitedContractSize",
        ],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    web3 = Web3(Web3.HTTPProvider(f"http://127.0.0.1:{port}"))
    while True:
        if proc.poll() is not None:
            return None
        if web3.isConnected():
            break
        time.sleep(0.1)

    node_info = NodeInfo(port=port, mnemonic=mnemonic, proc=proc, uuid=uuid)
    instances[uuid] = node_info

    reaper = Thread(target=kill_ganache, args=(node_info,))
    reaper.start()
    return node_info


auth_key = generate_auth_key()


@app.route("/")
def index():
    return "hello world"


@app.route("/new", methods=["POST"])
@cross_origin()
def create():
    key = request.headers.get("X-Auth-Key")
    if key != auth_key:
        return {
            "ok": False,
            "error": "nice try",
        }

    node_info = launch_ganache()

    if node_info is None:
        print("failed to launch node!")
        return {
            "ok": False,
            "error": "failed to launch node",
        }

    return {
        "ok": True,
        "uuid": node_info.uuid,
        "mnemonic": node_info.mnemonic,
    }


ALLOWED_NAMESPACES = ["web3", "eth", "net"]

@app.route("/<string:uuid>", methods=["POST"])
@cross_origin()
def proxy(uuid):
    body = request.get_json()
    if not body:
        return "invalid content type, only application/json is supported"

    if "id" not in body:
        return ""

    if uuid not in instances:
        return {
            "jsonrpc": "2.0",
            "id": body["id"],
            "error": {
                "code": -32602,
                "message": "invalid uuid specified",
            },
        }

    if "method" not in body or not isinstance(body["method"], str):
        return {
            "jsonrpc": "2.0",
            "id": body["id"],
            "error": {
                "code": -32600,
                "message": "invalid request",
            },
        }
    
    ok = any(body["method"].startswith(namespace) for namespace in ALLOWED_NAMESPACES)
    key = request.headers.get("X-Auth-Key")
    if not ok and key != auth_key:
        return {
            "jsonrpc": "2.0",
            "id": body["id"],
            "error": {
                "code": -32600,
                "message": "invalid request",
            },
        }

    instance = instances[uuid]
    resp = requests.post(f"http://127.0.0.1:{instance.port}", json=body)
    response = Response(resp.content, resp.status_code, resp.raw.headers.items())
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8545)
