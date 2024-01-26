import json
import os
import time
import traceback
from threading import Thread

import requests
from eth_abi import abi
from web3 import Web3
from web3.contract.contract import Contract
from web3.middleware.signing import construct_sign_and_send_raw_middleware

from ctf_launchers.types import (UserData, get_additional_account,
                                 get_unprivileged_web3)

ORCHESTRATOR = os.getenv("ORCHESTRATOR_HOST", "http://orchestrator:7283")
INSTANCE_ID = os.getenv("INSTANCE_ID")


class Relayer:
    def __init__(self):
        self.__required_properties = ["mnemonic", "challenge_address"]

    def start(self):
        while True:
            instance_body = requests.get(
                f"{ORCHESTRATOR}/instances/{INSTANCE_ID}"
            ).json()
            if instance_body["ok"] == False:
                raise Exception("oops")

            user_data = instance_body["data"]
            if any(
                [v not in user_data["metadata"] for v in self.__required_properties]
            ):
                time.sleep(1)
                continue

            break

        self._run(user_data)

    def _run(self, user_data: UserData):
        challenge_addr = user_data["metadata"]["challenge_address"]
        relayer = get_additional_account(user_data["metadata"]["mnemonic"], 0)

        l1 = get_unprivileged_web3(user_data, "l1")
        l1.middleware_onion.add(construct_sign_and_send_raw_middleware(relayer))
        l1.eth.default_account = relayer.address

        l2 = get_unprivileged_web3(user_data, "l2")
        l2.middleware_onion.add(construct_sign_and_send_raw_middleware(relayer))
        l2.eth.default_account = relayer.address

        (l1_messenger_addr,) = abi.decode(
            ["address"],
            l1.eth.call(
                {
                    "to": l1.to_checksum_address(challenge_addr),
                    "data": l1.keccak(text="MESSENGER()")[:4].hex(),
                }
            ),
        )
        l2_messenger_addr = "0x420000000000000000000000000000000000CAFe"

        with open(
            "/artifacts/out/CrossDomainMessenger.sol/CrossDomainMessenger.json", "r"
        ) as f:
            cache = json.load(f)
            messenger_abi = cache["metadata"]["output"]["abi"]

        l1_messenger = l1.eth.contract(
            address=l1.to_checksum_address(l1_messenger_addr), abi=messenger_abi
        )
        l2_messenger = l2.eth.contract(
            address=l2.to_checksum_address(l2_messenger_addr), abi=messenger_abi
        )

        Thread(
            target=self._relayer_worker, args=(l1, l1_messenger, l2_messenger)
        ).start()
        Thread(
            target=self._relayer_worker, args=(l2, l2_messenger, l1_messenger)
        ).start()

    def _relayer_worker(
        self, src_web3: Web3, src_messenger: Contract, dst_messenger: Contract
    ):
        _src_chain_id = src_web3.eth.chain_id
        _last_processed_block_number = 0

        while True:
            try:
                latest_block_number = src_web3.eth.block_number
                if _last_processed_block_number > latest_block_number:
                    _last_processed_block_number = latest_block_number

                print(
                    f"chain {_src_chain_id} syncing {_last_processed_block_number + 1} {latest_block_number}"
                )
                for i in range(
                    _last_processed_block_number + 1, latest_block_number + 1
                ):
                    _last_processed_block_number = i
                    logs = src_messenger.events.SentMessage().get_logs(
                        fromBlock=i, toBlock=i
                    )
                    for log in logs:
                        print(f"chain {_src_chain_id} got log {src_web3.to_json(log)}")
                        try:
                            tx_hash = dst_messenger.functions.relayMessage(
                                log.args["target"],
                                log.args["sender"],
                                log.args["message"],
                                log.args["messageNonce"],
                            ).transact()

                            dst_messenger.w3.eth.wait_for_transaction_receipt(tx_hash)
                            print(
                                f"chain {_src_chain_id} relay message hash: {tx_hash.hex()} src block number: {i}"
                            )
                            time.sleep(1)
                        except Exception as e:
                            print(e)
            except:
                traceback.print_exc()
                pass
            finally:
                time.sleep(1)


Relayer().start()
