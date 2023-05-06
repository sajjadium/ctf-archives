import json
from pathlib import Path

import eth_sandbox
from web3 import Web3


def deploy(web3: Web3, deployer_address: str, player_address: str) -> str:
    rcpt = eth_sandbox.sendTransaction(web3, {
        "from": deployer_address,
        "value": Web3.toWei(10, 'ether'),
        "data": json.loads(Path("compiled/Setup.sol/Setup.json").read_text())["bytecode"]["object"],
    })

    return rcpt.contractAddress

eth_sandbox.run_launcher([
    eth_sandbox.new_launch_instance_action(deploy),
    eth_sandbox.new_kill_instance_action(),
    eth_sandbox.new_get_flag_action()
])
