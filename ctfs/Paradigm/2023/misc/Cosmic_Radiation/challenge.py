from typing import List
from web3 import Web3
from anvil_server.database import UserData
from anvil_server.socket import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    UnixClient,
    UpdateMetadataRequest,
)
from eth_launchers.koth_launcher import KothChallengeLauncher
from eth_launchers.launcher import ETH_RPC_URL
from eth_launchers.score_submitter import ScoreSubmitter, get_score_submitter
from eth_launchers.team_provider import TeamProvider, get_team_provider
from eth_launchers.utils import anvil_setBalance, anvil_setCode
from foundry.anvil import LaunchAnvilInstanceArgs


class Challenge(KothChallengeLauncher):
    def __init__(
        self, project_location: str, provider: TeamProvider, submitter: ScoreSubmitter
    ):
        super().__init__(
            project_location, provider, submitter, want_metadata=["bitflips"]
        )

    def create_instance(self, client: UnixClient) -> CreateInstanceResponse:
        return client.create_instance(
            CreateInstanceRequest(
                id=self.team,
                instances={
                    "main": LaunchAnvilInstanceArgs(
                        balance=1000,
                        fork_url=ETH_RPC_URL,
                        fork_block_num=18_437_825,
                    ),
                },
            )
        )

    def deploy(self, user_data: UserData) -> str:
        web3 = user_data.get_privileged_web3("main")

        bitflips = input("bitflips? ")

        corrupted_addrs = {}

        for bitflip in bitflips.split(","):
            (addr, *bits) = bitflip.split(":")
            addr = Web3.to_checksum_address(addr)
            bits = [int(v) for v in bits]

            if addr in corrupted_addrs:
                raise Exception("already corrupted this address")

            corrupted_addrs[addr] = True

            balance = web3.eth.get_balance(addr)
            if balance == 0:
                raise Exception("invalid target")

            code = bytearray(web3.eth.get_code(addr))
            for bit in bits:
                byte_offset = bit // 8
                bit_offset = 7 - bit % 8
                if byte_offset < len(code):
                    code[byte_offset] ^= 1 << bit_offset

            total_bits = len(code) * 8
            corrupted_balance = int(balance * (total_bits - len(bits)) / total_bits)

            anvil_setBalance(web3, addr, hex(corrupted_balance))
            anvil_setCode(web3, addr, "0x" + code.hex())

        resp = UnixClient().update_metadata(
            UpdateMetadataRequest(
                id=self.team,
                metadata={
                    "bitflips": bitflips,
                },
            )
        )
        if not resp.ok:
            raise Exception(resp.message)

        return super().deploy(user_data)


Challenge(
    project_location="project",
    provider=get_team_provider(),
    submitter=get_score_submitter(),
).run()
