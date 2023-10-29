import ast
import asyncio
import pickle
import sys
import time
import traceback
import typing

from anvil_server.database import UserData
from anvil_server.socket import GetInstanceRequest, UnixClient, UpdateMetadataRequest
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.contract import AsyncContract
from web3.middleware.signing import async_construct_sign_and_send_raw_middleware

Account.enable_unaudited_hdwallet_features()


class Watcher:
    def __init__(self, external_id: str, rpc_url: str, challenge_contract: str) -> None:
        self.__external_id = external_id
        self.__rpc_url = rpc_url
        self.__challenge_contract = challenge_contract
        self.__router_address = ""
        self.__price_cache = {}
        self.__pair_cache = {}

    async def _init(self):
        self.__router_address = (
            await self.call(
                await self.get_block_number(), self.__challenge_contract, "ROUTER()(address)"
            )
        ).strip()
        print("router address = ", self.__router_address)

    async def run(self):
        await self._init()

        while True:
            try:
                block_number = await self.get_block_number()

                flag_charity = await self.call(
                    block_number,
                    self.__router_address,
                    "flagCharity()(address)",
                )

                listing_tokens = await self.list_array(
                    block_number,
                    self.__router_address,
                    "listingTokensCount()(uint256)",
                    "listingTokens(uint256)(address)",
                )
                lp_tokens = await self.list_array(
                    block_number,
                    self.__router_address,
                    "lpTokensCount()(uint256)",
                    "lpTokensInfo(uint256)(string,address)",
                )
                lp_tokens = [info.rsplit("\n", 1) for info in lp_tokens]

                async def calculate_token_price(addr):
                    price = await self.get_token_price(block_number, addr)
                    amount = await self.get_balance(block_number, addr, flag_charity)
                    return price * amount

                async def calculate_lp_token_price(i, res):
                    pool, addr = res
                    amount = await self.get_balance(block_number, addr, flag_charity)
                    (
                        token_amount_a,
                        token_amount_b,
                        total_supply,
                    ) = await self.get_pair_status(block_number, addr)

                    if total_supply == 0:
                        return 0

                    (price_a, price_b) = await self.get_pair_prices(
                        block_number, i, pool
                    )
                    return (
                        ((price_a * token_amount_a) + (price_b * token_amount_b))
                        * amount
                        // total_supply
                    )

                acc = 0

                # Normal tokens
                acc += sum(
                    await asyncio.gather(
                        *[calculate_token_price(addr) for addr in listing_tokens]
                    )
                )

                # LP tokens
                acc += sum(
                    await asyncio.gather(
                        *[
                            calculate_lp_token_price(i, res)
                            for i, res in enumerate(lp_tokens)
                        ]
                    )
                )

                print("user has donated", acc // 10**18)

                UnixClient().update_metadata(UpdateMetadataRequest(
                    id=self.__external_id,
                    metadata={
                        'donated': acc,
                    },
                ))
            except:
                traceback.print_exc()
                pass
            finally:
                await asyncio.sleep(1)

    async def get_token_price(self, block_number, addr: str) -> int:
        key = "token_%s" % addr
        if key not in self.__price_cache:
            self.__price_cache[key] = int(
                await self.call(
                    block_number,
                    self.__router_address,
                    "priceOf(address)(uint256)",
                    addr,
                )
            )

        return self.__price_cache[key]

    async def get_pair_prices(
        self, block_number: int, index: str, pool_id: str
    ) -> typing.Tuple[int, int]:
        pool_name = "pool_%s" % pool_id
        if pool_name not in self.__pair_cache:
            token_a, token_b = (
                await self.call(
                    block_number,
                    self.__router_address,
                    "lpTokenPair(uint256)(address,address)",
                    str(index),
                )
            ).split()
            self.__pair_cache[pool_name] = (token_a, token_b)

        token_a, token_b = self.__pair_cache[pool_name]

        return (
            await self.get_token_price(block_number, token_a),
            await self.get_token_price(block_number, token_b),
        )

    async def get_pair_status(
        self, block_number: int, pair: str
    ) -> typing.Tuple[int, int, int]:
        result = await self.call(
            block_number,
            self.__router_address,
            "lpTokensStatus(address)(uint256,uint256,uint256)",
            pair,
        )
        return [int(x, 0) for x in result.strip().split("\n")]

    async def get_balance(self, block_number: int, token: str, who: str) -> int:
        result = await self.call(block_number, token, "balanceOf(address)", who)
        return int(result.strip(), 0)

    async def list_array(
        self, block_number, address, count_sig, element_sig
    ) -> typing.List[str]:
        res = await self.call(
                    block_number,
                    address,
                    count_sig,
                )
        print("list array res", res)
        count = int(res)

        result = await asyncio.gather(
            *[
                self.call(
                    block_number,
                    address,
                    element_sig,
                    str(i),
                )
                for i in range(count)
            ]
        )
        return result

    async def call(self, block_number: int, address: str, sig: str, *call_args) -> str:
        proc = await asyncio.create_subprocess_exec(
            "/opt/foundry/bin/cast", "call", "--rpc-url", self.__rpc_url, "-b", str(block_number), address, sig, *call_args,
            stdout=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        return stdout.decode()[:-1]

    async def get_block_number(self) -> int:
        proc = await asyncio.create_subprocess_exec(
            "/opt/foundry/bin/cast", "block-number", "--rpc-url", self.__rpc_url,
            stdout=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        return int(stdout)


async def main(user_data: UserData):
    r1 = Watcher(
        user_data.external_id,
        f"http://127.0.0.1:8545/{user_data.internal_id}/main",
        user_data.metadata["challenge_address"],
    )
    t1 = asyncio.create_task(r1.run())
    await t1


if __name__ == "__main__":
    internal_id = sys.argv[1]
    while True:
        time.sleep(1)
        resp = UnixClient().get_instance(GetInstanceRequest(id=internal_id))
        print("got instance", internal_id, resp)
        if not resp.ok or "challenge_address" not in resp.user_data.metadata:
            print("instance not ready")
            continue

        break

    asyncio.run(main(resp.user_data))
