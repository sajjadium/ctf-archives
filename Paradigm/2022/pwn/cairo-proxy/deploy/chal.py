import cairo_sandbox

from pathlib import Path

from starknet_py.net import AccountClient
from starknet_py.contract import Contract

from starkware.starknet.public.abi import get_storage_var_address
from starkware.starknet.core.os.contract_address.contract_address import calculate_contract_address_from_hash

async def deploy(client: AccountClient, player_address: int) -> int:
    print("[+] deploying erc20")
    erc20_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/almost_erc20.cairo").read_text(),
        salt=111111,
    )
    await erc20_deployment.wait_for_acceptance()

    print("[+] deploying proxy")
    proxy_deployment = await Contract.deploy(
        client=client,
        compiled_contract=Path("compiled/proxy.cairo").read_text(),
        constructor_args=[await client.get_class_hash_at(erc20_deployment.deployed_contract.address)],
    )
    await proxy_deployment.wait_for_acceptance()

    wrapper_contract = Contract(
        proxy_deployment.deployed_contract.address,
        erc20_deployment.deployed_contract.data.abi,
        client,
    )

    print("[+] initializing contracts")
    response = await client.execute(
        calls=[
            wrapper_contract.functions["initialize"].prepare(client.address, int(50000e18)),
            wrapper_contract.functions["transfer"].prepare(1337, int(25000e18)),
            wrapper_contract.functions["transfer"].prepare(7331, int(25000e18)),
        ],
        max_fee=int(1e16)
    )
    await client.wait_for_tx(response.transaction_hash)

    return proxy_deployment.deployed_contract.address


async def checker(client: AccountClient, proxy_contract: Contract, player_address: int) -> bool:
    erc20_address = calculate_contract_address_from_hash(
        salt=111111,
        class_hash=await client.get_storage_at(proxy_contract.address, get_storage_var_address("implementation"), "latest"),
        constructor_calldata=[],
        deployer_address=0,
    )

    erc20_contract = await Contract.from_address(erc20_address, client)

    wrapper_contract = Contract(
        proxy_contract.address,
        erc20_contract.data.abi,
        client,
    )
    
    player_balance = (await wrapper_contract.functions["balanceOf"].call(player_address)).balance

    return player_balance == int(50000e18)

cairo_sandbox.run_launcher([
    cairo_sandbox.new_launch_instance_action(deploy),
    cairo_sandbox.new_kill_instance_action(),
    cairo_sandbox.new_get_flag_action(checker),
])
