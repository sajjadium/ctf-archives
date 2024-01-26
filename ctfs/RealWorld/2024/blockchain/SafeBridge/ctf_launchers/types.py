from typing import Dict, NotRequired, Optional, TypedDict

from eth_account import Account
from eth_account.account import LocalAccount
from eth_account.hdaccount import key_from_seed, seed_from_mnemonic
from web3 import Web3

DEFAULT_DERIVATION_PATH = "m/44'/60'/0'/0/"


class LaunchAnvilInstanceArgs(TypedDict):
    image: NotRequired[Optional[str]]
    accounts: NotRequired[Optional[int]]
    balance: NotRequired[Optional[float]]
    derivation_path: NotRequired[Optional[str]]
    mnemonic: NotRequired[Optional[str]]
    fork_url: NotRequired[Optional[str]]
    fork_block_num: NotRequired[Optional[int]]
    fork_chain_id: NotRequired[Optional[int]]
    no_rate_limit: NotRequired[Optional[bool]]
    chain_id: NotRequired[Optional[int]]
    code_size_limit: NotRequired[Optional[int]]


class DaemonInstanceArgs(TypedDict):
    image: str


class CreateInstanceRequest(TypedDict):
    instance_id: str
    timeout: int
    anvil_instances: NotRequired[Dict[str, LaunchAnvilInstanceArgs]]
    daemon_instances: NotRequired[Dict[str, DaemonInstanceArgs]]


class InstanceInfo(TypedDict):
    id: str
    ip: str
    port: int


class UserData(TypedDict):
    instance_id: str
    external_id: str
    created_at: float
    expires_at: float
    anvil_instances: Dict[str, InstanceInfo]
    daemon_instances: Dict[str, InstanceInfo]
    metadata: Dict


def get_account(mnemonic: str, offset: int) -> LocalAccount:
    seed = seed_from_mnemonic(mnemonic, "")
    private_key = key_from_seed(seed, f"{DEFAULT_DERIVATION_PATH}{offset}")

    return Account.from_key(private_key)


def get_player_account(mnemonic: str) -> LocalAccount:
    return get_account(mnemonic, 0)


def get_additional_account(mnemonic: str, offset: int) -> LocalAccount:
    return get_account(mnemonic, offset + 2)


def get_privileged_web3(user_data: UserData, anvil_id: str) -> Web3:
    anvil_instance = user_data["anvil_instances"][anvil_id]
    return Web3(
        Web3.HTTPProvider(f"http://{anvil_instance['ip']}:{anvil_instance['port']}")
    )


def get_unprivileged_web3(user_data: UserData, anvil_id: str) -> Web3:
    return Web3(
        Web3.HTTPProvider(
            f"http://anvil-proxy:8545/{user_data['external_id']}/{anvil_id}"
        )
    )
