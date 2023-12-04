import signal
import subprocess
import sys

from ctf_server.types import UserData, get_privileged_web3, get_additional_account
from ctf_launchers.daemon import Daemon

def exit_handler(signal, frame):
    print("Terminating the process")
    exit(-1)

class BotDaemon(Daemon):
    def __init__(self):
        super().__init__(required_properties=["mnemonic", "challenge_address"])

    def _run(self, user_data: UserData):
        challenge_addr = user_data["metadata"]["challenge_address"]
        mev_guy = get_additional_account(user_data["metadata"]["mnemonic"], 0)
        web3 = get_privileged_web3(user_data, "main")

        anvil_instance = user_data["anvil_instances"]["main"]
        weth_addr = web3.eth.call({ "to": challenge_addr,  "data": "0x3fc8cef3" })[-20:].hex()   # weth()
        bot_addr = web3.eth.call({ "to": challenge_addr,  "data": "0x10814c37" })[-20:].hex()    # bot()

        print(f"bot owner: {mev_guy.address}")
        print(f"bot address: {bot_addr}")
        print(f"weth address: {weth_addr}")
        print(f"starting bot")

        signal.signal(signal.SIGINT, exit_handler)
        signal.signal(signal.SIGTERM, exit_handler)

        proc = subprocess.Popen(
            args=[
                "/home/user/frontrun-bot",
                f"ws://{anvil_instance['ip']}:{anvil_instance['port']}",
                mev_guy.key.hex(),
                bot_addr,
                weth_addr,
            ],
            text=True,
            encoding="utf8",
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        pass # allow signal handlers to catch signals
        proc.wait()

        if proc.poll() is not None:
            print("bot terminated")



signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
BotDaemon().start()