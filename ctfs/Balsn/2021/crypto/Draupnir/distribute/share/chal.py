import eth_sandbox
from web3 import Web3

eth_sandbox.run_launcher([
    eth_sandbox.new_launch_instance_action(deploy_value=Web3.toWei(100, 'ether')),
    eth_sandbox.new_get_flag_action()
])
