import json
import os
import subprocess
from typing import Dict

from web3 import Web3
from web3.types import RPCResponse


def deploy(
    web3: Web3,
    project_location: str,
    mnemonic: str,
    deploy_script: str = "script/Deploy.s.sol:Deploy",
    env: Dict = {},
) -> str:
    anvil_autoImpersonateAccount(web3, True)

    rfd, wfd = os.pipe2(os.O_NONBLOCK)

    proc = subprocess.Popen(
        args=[
            "/opt/foundry/bin/forge",
            "script",
            "--rpc-url",
            web3.provider.endpoint_uri,
            "--out",
            "/artifacts/out",
            "--cache-path",
            "/artifacts/cache",
            "--broadcast",
            "--unlocked",
            "--sender",
            "0x0000000000000000000000000000000000000000",
            deploy_script,
        ],
        env={
            "PATH": "/opt/foundry/bin:/usr/bin:" + os.getenv("PATH", "/fake"),
            "MNEMONIC": mnemonic,
            "OUTPUT_FILE": f"/proc/self/fd/{wfd}",
        }
        | env,
        pass_fds=[wfd],
        cwd=project_location,
        text=True,
        encoding="utf8",
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    anvil_autoImpersonateAccount(web3, False)

    if proc.returncode != 0:
        print(stdout)
        print(stderr)
        raise Exception("forge failed to run")

    result = os.read(rfd, 256).decode("utf8")

    os.close(rfd)
    os.close(wfd)

    return result


def anvil_setCodeFromFile(
    web3: Web3,
    addr: str,
    target: str,  # "ContractFile.sol:ContractName",
):
    file, contract = target.split(":")

    with open(f"/artifacts/out/{file}/{contract}.json", "r") as f:
        cache = json.load(f)

        bytecode = cache["deployedBytecode"]["object"]

    anvil_setCode(web3, addr, bytecode)


def check_error(resp: RPCResponse):
    if "error" in resp:
        raise Exception("rpc exception", resp["error"])


def anvil_autoImpersonateAccount(web3: Web3, enabled: bool):
    check_error(web3.provider.make_request("anvil_autoImpersonateAccount", [enabled]))


def anvil_setCode(web3: Web3, addr: str, bytecode: str):
    check_error(web3.provider.make_request("anvil_setCode", [addr, bytecode]))


def anvil_setStorageAt(
    web3: Web3,
    addr: str,
    slot: str,
    value: str,
):
    check_error(web3.provider.make_request("anvil_setStorageAt", [addr, slot, value]))
