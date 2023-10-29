import asyncio
import json
import random
import sys
import time
from typing import List

from anvil_server.database import UserData
from anvil_server.socket import GetInstanceRequest, UnixClient, UpdateMetadataRequest
from eth_abi import abi
from eth_account.signers.local import LocalAccount
from eth_launchers.daemon import Daemon
from web3 import Web3
from web3.middleware.signing import construct_sign_and_send_raw_middleware


class Watcher(Daemon):
    def __init__(self):
        super().__init__(required_properties=["challenge_address"])

    def update_claimed(self, external_id: str, claimed: List[str]):
        client = UnixClient()
        data = client.get_instance(
            GetInstanceRequest(
                id=external_id,
            )
        )
        if not data.ok:
            raise Exception("failed to get instance", data.message)

        resp = client.update_metadata(
            UpdateMetadataRequest(
                id=external_id,
                metadata={
                    "claimed": data.user_data.metadata.get("claimed", []) + claimed,
                },
            )
        )
        if not resp.ok:
            raise Exception("failed to update metadata", data.message)

    def _run(self, user_data: UserData):
        randomness_provider = user_data.get_additional_account(0)

        web3 = user_data.get_unprivileged_web3("main")
        web3.middleware_onion.add(
            construct_sign_and_send_raw_middleware(randomness_provider)
        )

        (distributor,) = abi.decode(
            ["address"],
            web3.eth.call(
                {
                    "to": user_data.metadata["challenge_address"],
                    "data": web3.keccak(text="MERKLE_DISTRIBUTOR()")[:4].hex(),
                }
            ),
        )

        from_number = web3.eth.block_number - 1

        while True:
            latest_number = web3.eth.block_number

            print(f"from_number={from_number} latest={latest_number}")

            if from_number > latest_number:
                time.sleep(1)
                continue

            logs = web3.eth.get_logs(
                {
                    "address": web3.to_checksum_address(distributor),
                    "topics": [
                        web3.keccak(text="Claimed(uint256,address,uint256)").hex(),
                    ],
                    "fromBlock": from_number,
                    "toBlock": latest_number,
                }
            )

            claimed = []
            for log in logs:
                print(f"fetched log={web3.to_json(log)}")

                claimed.append(Web3.to_checksum_address(log["data"][44:64].hex()))

            if len(claimed) > 0:
                try:
                    self.update_claimed(user_data.external_id, claimed)
                except Exception as e:
                    print("failed to update claimed", e)

            from_number = latest_number + 1


Watcher().start()
