by Hidden Investigations
Blockchain
A regional settlement node runs its ledger logic behind an upgradeable proxy. The upgrade path was added in a later release and was never checked against the proxy's existing storage layout.

Each team gets a private chain. You're given an RPC URL, a funded private key, and the address of the Setup contract. The Solidity sources for everything deployed on your instance are in contracts/ — use your own tooling (cast/forge, ethers, web3.py).

Win condition: the settlement node's treasury ends holding less than 1% of its starting reserve. Submit through the checker once Setup.isSolved() returns true.
