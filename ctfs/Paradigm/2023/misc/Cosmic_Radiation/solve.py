import yaml
from eth_launchers.koth_solver import KothChallengeSolver
from eth_launchers.solver import TicketedRemote
from eth_launchers.utils import solve
from web3 import Web3


class Solver(KothChallengeSolver):
    def launch_instance(self):
        with TicketedRemote() as r:
            r.recvuntil(b"?")
            r.send(b"1\n")
            r.recvuntil(b"?")
            r.send(
                b"0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84:0:1:2:3:4:5:6:7,0x00000000219ab540356cbb839cbe05303d7705fa:0:1:2:3:4:5:6:7\n"
            )
            try:
                r.recvuntil(b"---\n")
            except:
                log = r.recvall().decode("utf8")
                print(log)
                raise Exception("failed to create instance")

            data_raw = r.recvall().decode("utf8")

        return yaml.safe_load(data_raw)

    def _submit(self, rpcs, player, challenge):
        web3 = Web3(Web3.HTTPProvider(rpcs[0]))
        solve(web3, "project", player, challenge, "script/Solve.s.sol:Solve")


Solver().start()
