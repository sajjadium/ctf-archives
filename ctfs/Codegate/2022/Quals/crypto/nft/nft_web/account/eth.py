
from typing import Any, Dict, List, Optional, Union

import rlp
from brownie.exceptions import VirtualMachineError
from eth_typing import ChecksumAddress
from eth_utils import keccak, to_checksum_address
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import ContractFunctions


class Account:
    def __init__(self, private_key: Union[int, bytes, str] = None) -> None:
        if private_key is None:
            w3account = web3.eth.account.create()
        else:
            w3account = web3.eth.account.from_key(private_key)

        self._account = w3account
        self.address = self._account.address
        self.private_key = HexBytes(self._account.key).hex()

    def balance(self) -> int:
        balance = web3.eth.get_balance(self.address)
        return balance

    @property
    def nonce(self) -> int:
        return web3.eth.get_transaction_count(self.address)

    def get_deployment_address(self, nonce: Optional[int] = None) -> ChecksumAddress:
        if nonce is None:
            nonce = self.nonce

        address = HexBytes(self.address)
        raw = rlp.encode([address, nonce])
        deployment_address = HexBytes(keccak(raw)[12:]).hex()

        return to_checksum_address(deployment_address)

    def transact(self, tx: Dict) -> str:
        tx["chainId"] = web3.eth.chain_id
        tx["from"] = self.address
        try:
            signed_tx = self._account.sign_transaction(tx).rawTransaction  # type: ignore
            txid = web3.eth.send_raw_transaction(signed_tx)
        except ValueError as e:
            exc = VirtualMachineError(e)
            if not hasattr(exc, "txid"):
                raise exc from None
        else:
            return txid.hex()


class Contract:
    def __init__(self, build: Dict) -> None:
        self._build = build.copy()
        self.bytecode = build["bytecode"]
        self.deploy = ContractConstructor(self)

    @property
    def abi(self) -> List:
        return self._build["abi"]

    def at(self, address: ChecksumAddress) -> ContractFunctions:
        return web3.eth.contract(address=address, abi=self.abi).functions


class ContractConstructor:
    def __init__(self, parent: "Contract") -> None:
        self._instance = web3.eth.contract(abi=parent.abi, bytecode=parent.bytecode)

    def __call__(
        self,
        sender: Account,
        value: int = 0,
        args: Optional[Any] = None,
        gas_limit: Optional[int] = None,
        gas_price: Optional[int] = None,
        nonce: Optional[int] = None,
    ) -> str:
        tx: Dict = self._instance.constructor(*args).buildTransaction()
        return sender.transact(
            {
                "value": value,
                "nonce": nonce if nonce is not None else sender.nonce,
                "gas": gas_limit or tx["gas"],
                "gasPrice": gas_price or tx["gasPrice"],
                "data": tx["data"],
            },
        )

    def estimate_gas(self, args: Optional[Any] = None) -> int:
        return self._instance.constructor(*args).estimateGas()


web3 = Web3()
