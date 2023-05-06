import cairo_sandbox

from pathlib import Path

from starknet_py.net import AccountClient
from starknet_py.contract import Contract
from starkware.python.utils import from_bytes

async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying erc20")
    erc20_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/erc20.cairo").read_text(),
        constructor_args=[
            from_bytes(b"Test Token"),
            from_bytes(b"TTK"),
            6,
            int(1000000e6),
            client.address,
        ],
    )
    await erc20_deployment.wait_for_acceptance()

    print("[+] deploying auction")
    auction_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/auction.cairo").read_text(),
        constructor_args=[
            erc20_deployment.deployed_contract.address,
            client.address,
        ],
    )
    await auction_deployment.wait_for_acceptance()

    print("[+] creating bidders")
    bidder_1 = await AccountClient.create_account(client.client)
    bidder_2 = await AccountClient.create_account(client.client)

    print("[+] initializing contracts")
    response = await client.execute(
        calls=[
            erc20_deployment.deployed_contract.functions["transfer"].prepare(bidder_1.address, int(100000e6)),
            erc20_deployment.deployed_contract.functions["transfer"].prepare(bidder_2.address, int(100000e6)),
            erc20_deployment.deployed_contract.functions["transfer"].prepare(player_address, int(50000e6)),
            auction_deployment.deployed_contract.functions["start_auction"].prepare(),
        ],
        max_fee=int(1e16)
    )
    await client.wait_for_tx(response.transaction_hash)
    
    response = await client.execute(
        calls=[
            erc20_deployment.deployed_contract.functions["approve"].prepare(auction_deployment.deployed_contract.address, int(100000e6)),
            auction_deployment.deployed_contract.functions["increase_credit"].prepare(int(100000e6)),
            auction_deployment.deployed_contract.functions["raise_bid"].prepare(1, int(100000e6)),
        ],
        max_fee=int(1e16)
    )
    await bidder_1.wait_for_tx(response.transaction_hash)
    
    response = await client.execute(
        calls=[
            erc20_deployment.deployed_contract.functions["approve"].prepare(auction_deployment.deployed_contract.address, int(100000e6)),
            auction_deployment.deployed_contract.functions["increase_credit"].prepare(int(100000e6)),
            auction_deployment.deployed_contract.functions["raise_bid"].prepare(1, int(100000e6)),
        ],
        max_fee=int(1e16)
    )
    await bidder_2.wait_for_tx(response.transaction_hash)

    return auction_deployment.deployed_contract.address


async def checker(client: AccountClient, auction_contract: Contract, player_address: int) -> bool:
    winner = (await auction_contract.functions["current_winner"].call(1)).current_winner

    return winner == player_address

cairo_sandbox.run_launcher([
    cairo_sandbox.new_launch_instance_action(deploy),
    cairo_sandbox.new_kill_instance_action(),
    cairo_sandbox.new_get_flag_action(checker),
])
